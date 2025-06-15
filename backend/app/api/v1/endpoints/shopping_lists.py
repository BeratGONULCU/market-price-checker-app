from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Body, status
from sqlalchemy.orm import Session
from app import models, schemas
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

logger = logging.getLogger(__name__)
router = APIRouter()

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
        # Get all lists for user_id 1
        result = get_shopping_lists_by_user(
            db=db,
            skip=skip,
            limit=limit
    )
        return result
    except Exception as e:
        logger.error(f"Error retrieving shopping lists: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{id}", response_model=ShoppingList)
def read_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get shopping list by ID.
    """
    result = get_shopping_list(db=db, shopping_list_id=id)
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

@router.post("/{shopping_list_id}/items", response_model=ShoppingListItemInDB)
def create_shopping_list_item(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
    item: ShoppingListItemCreate,
) -> Any:
    """
    Add new item to shopping list.
    """
    try:
        # Check if shopping list exists
        shopping_list = get_shopping_list(db=db, shopping_list_id=shopping_list_id)
        if not shopping_list:
            raise HTTPException(status_code=404, detail="Shopping list not found")

        # Create shopping list item
        db_item = create_shopping_list_item(
            db=db,
            shopping_list_id=shopping_list_id,
            product_id=item.product_id,
            quantity=item.quantity,
            notes=item.notes
        )
        
        return db_item
        
    except Exception as e:
        logger.error(f"Error creating shopping list item: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

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

@router.get("/{shopping_list_id}/market-comparison", response_model=List[MarketComparisonResponse])
def get_market_comparison(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
):
    """
    Alışveriş listesindeki ürünlerin farklı marketlerdeki fiyat karşılaştırmasını getir.
    """
    shopping_list = get_shopping_list(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    
    # Tüm marketleri al
    markets = db.query(Market).all()
    comparisons = []
    
    for market in markets:
        total_price = 0
        items = []
        
        for list_item in shopping_list.items:
            # Ürünün bu marketteki fiyatını bul
            product_price = db.query(Product).filter(
                Product.id == list_item.product_id,
                Product.market_id == market.id
            ).first()
            
            if product_price:
                item_price = product_price.price
                total_price += item_price * list_item.quantity
                
                items.append({
                    "product_id": list_item.product_id,
                    "product_name": product_price.name,
                    "price": item_price,
                    "quantity": list_item.quantity
                })
        
        comparisons.append({
            "market_id": market.id,
            "market_name": market.name,
            "total_price": total_price,
            "items": items
        })
    
    # Toplam fiyata göre sırala
    comparisons.sort(key=lambda x: x["total_price"])
    return comparisons

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
    market_comparisons = get_market_comparison(
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