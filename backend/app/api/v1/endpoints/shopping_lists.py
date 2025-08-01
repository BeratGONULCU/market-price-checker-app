from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Body, status, Response
from sqlalchemy.orm import Session, joinedload
from app import models, schemas, crud
from app.api import deps
from app.models.shopping_list import ShoppingList, ShoppingListItem
from app.models.product import Product
from app.models.market import Market
from app.schemas.shopping_list import (
    ShoppingList,
    ShoppingListCreate,
    ShoppingListUpdate,
    ShoppingListItem,
    ShoppingListItemCreate,
    ShoppingListItemUpdate,
    ShoppingListItemInDB,
    MarketComparisonResponse
)
from app.crud.crud_shopping_list import (
    create_shopping_list,
    get_shopping_lists_by_user,
    get_shopping_list,
    update_shopping_list,
    delete_shopping_list,
    generate_share_token,
    create_shopping_list_item
)
from app.utils.pdf_generator import generate_shopping_list_pdf
import json
from app.models.user import User
import logging
from app.models.product_detail import ProductDetail
from pydantic import BaseModel
from sqlalchemy import text

logger = logging.getLogger(__name__)
router = APIRouter()

class MarketComparisonResponse(BaseModel):
    market_id: int
    market_name: str
    total_price: float
    items: List[dict]
    found_products: int
    total_products: int
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ShoppingList)
def create_shopping_list_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_in: ShoppingListCreate,
) -> Any:
    """
    Create new shopping list.
    """
    try:
        logger.info("=== Shopping List Creation Request ===")
        logger.info(f"Raw request data: {shopping_list_in.dict()}")
        
        # Create shopping list with default user_id=1
        result = create_shopping_list(
            db=db,
            shopping_list=shopping_list_in
        )
        
        logger.info(f"Successfully created shopping list with ID: {result.id}")
        return result
        
    except Exception as e:
        logger.error("=== Error Creating Shopping List ===")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error(f"Request data: {shopping_list_in.dict() if hasattr(shopping_list_in, 'dict') else shopping_list_in}")
        logger.error("===================================")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating shopping list: {str(e)}"
        )

@router.get("/", response_model=List[ShoppingList])
def read_shopping_lists(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve shopping lists.
    """
    try:
        # Get all lists for user_id 1 with items
        lists = db.query(ShoppingList).options(
            joinedload(ShoppingList.items)
        ).filter(
            ShoppingList.user_id == 1
        ).offset(skip).limit(limit).all()
        
        return lists
    except Exception as e:
        logger.error(f"Error retrieving shopping lists: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{shopping_list_id}/markets", response_model=List[MarketComparisonResponse])
def get_markets_for_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
):
    """
    Alışveriş listesindeki ürünleri satan marketleri getir.
    """
    # 1. Alışveriş listesindeki ürünleri al
    items = db.query(ShoppingListItem).filter(
        ShoppingListItem.shopping_list_id == shopping_list_id
    ).all()
    
    if not items:
        return []
    
    # 2. Bu ürünleri satan marketleri bul
    product_ids = [item.product_id for item in items]
    
    # 3. SQL ile marketleri çek
    query = text("""
        SELECT DISTINCT m.id, m.name
        FROM shopping_list_items sli
        JOIN product_details pd ON sli.product_id = pd.product_id
        JOIN markets m ON pd.market_id = m.id
        WHERE sli.shopping_list_id = :list_id
    """)
    
    result = db.execute(query, {"list_id": shopping_list_id})
    markets = result.fetchall()
    
    comparisons = []
    
    for market in markets:
        # 4. Her market için fiyat hesapla
        price_query = text("""
            SELECT p.name, sli.quantity, pd.price
            FROM shopping_list_items sli
            JOIN product_details pd ON sli.product_id = pd.product_id
            JOIN products p ON sli.product_id = p.id
            WHERE sli.shopping_list_id = :list_id AND pd.market_id = :market_id
        """)
        
        price_result = db.execute(price_query, {
            "list_id": shopping_list_id,
            "market_id": market.id
        })
        
        items_list = []
        total_price = 0
        
        for row in price_result:
            item_price = float(row.price) * row.quantity
            total_price += item_price
            
            items_list.append({
                "product_id": 0,  # Gerekirse eklenebilir
                "product_name": row.name,
                "price": float(row.price),
                "quantity": row.quantity
            })
        
        comparisons.append({
            "market_id": market.id,
            "market_name": market.name,
            "total_price": total_price,
            "items": items_list,
            "found_products": len(items_list),
            "total_products": len(items)
        })
    
    # 5. Fiyata göre sırala
    comparisons.sort(key=lambda x: x["total_price"])
    
    return comparisons

@router.get("/{id}", response_model=ShoppingList)
def read_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get shopping list by ID.
    """
    result = db.query(ShoppingList).options(
        joinedload(ShoppingList.items)
    ).filter(ShoppingList.id == id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return result

@router.put("/{id}", response_model=ShoppingList)
def update_shopping_list_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    shopping_list_in: ShoppingListUpdate,
) -> Any:
    """
    Update shopping list.
    """
    result = get_shopping_list(db=db, shopping_list_id=id)
    if not result:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return update_shopping_list(
        db=db,
        shopping_list_id=id,
        shopping_list_update=shopping_list_in
    )

@router.delete("/{id}", response_model=ShoppingList)
def delete_shopping_list_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete shopping list.
    """
    result = get_shopping_list(db=db, shopping_list_id=id)
    if not result:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return delete_shopping_list(db=db, shopping_list_id=id)

@router.get("/{shopping_list_id}/items", response_model=List[ShoppingListItemInDB])
def get_shopping_list_items(
    shopping_list_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    db_shopping_list = get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    items = db.query(ShoppingListItem).options(
        joinedload(ShoppingListItem.product)
    ).filter(
        ShoppingListItem.shopping_list_id == shopping_list_id
    ).all()
    
    return items

@router.post("/{shopping_list_id}/items", response_model=ShoppingListItemInDB)
def create_shopping_list_item_endpoint(
    shopping_list_id: int,
    item: ShoppingListItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    db_shopping_list = get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return create_shopping_list_item(
        db=db,
        shopping_list_id=shopping_list_id,
        product_id=item.product_id,
        quantity=item.quantity,
        notes=item.notes
    )

@router.delete("/{shopping_list_id}/items/{item_id}")
def delete_shopping_list_item(
    shopping_list_id: int,
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    db_shopping_list = get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_item = crud.get_shopping_list_item(db, item_id)
    if not db_item or db_item.shopping_list_id != shopping_list_id:
        raise HTTPException(status_code=404, detail="Item not found")
    if crud.delete_shopping_list_item(db, item_id):
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=500, detail="Error deleting item")

@router.post("/{shopping_list_id}/items/bulk", response_model=List[ShoppingListItemInDB])
def create_shopping_list_items_bulk(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
    items: List[ShoppingListItemCreate],
) -> Any:
    """
    Add multiple items to shopping list.
    """
    try:
        # Check if shopping list exists
        shopping_list = get_shopping_list(db=db, shopping_list_id=shopping_list_id)
        if not shopping_list:
            raise HTTPException(status_code=404, detail="Shopping list not found")

        # Create shopping list items
        db_items = []
        for item in items:
            db_item = create_shopping_list_item(
                db=db,
                shopping_list_id=shopping_list_id,
                product_id=item.product_id,
                quantity=item.quantity,
                notes=item.notes
            )
            db_items.append(db_item)
        
        return db_items
        
    except Exception as e:
        logger.error(f"Error creating shopping list items: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{shopping_list_id}/export")
def export_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
):
    """
    Alışveriş listesini PDF olarak dışa aktar.
    """
    shopping_list = get_shopping_list(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    
    # Market karşılaştırmasını al
    market_comparisons = get_markets_for_shopping_list(
        db=db,
        shopping_list_id=shopping_list_id,
    )
    
    # PDF oluştur
    pdf_content = generate_shopping_list_pdf(
        shopping_list=shopping_list,
        market_comparisons=market_comparisons
    )
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{shopping_list.name}.pdf"'
        }
    )

@router.post("/{shopping_list_id}/share")
def share_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
):
    """
    Alışveriş listesini paylaş.
    """
    shopping_list = get_shopping_list(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    
    # Paylaşım linki oluştur
    share_token = generate_share_token(
        db=db,
        shopping_list_id=shopping_list_id
    )
    
    share_url = f"http://localhost:3000/shopping-lists/shared/{share_token}"
    return {"share_url": share_url}