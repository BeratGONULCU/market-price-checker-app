from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Body, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.models.shopping_list import ShoppingList, ShoppingListItem
from app.models.product import Product
from app.models.market import Market
from app.schemas.shopping_list import (
    ShoppingListCreate,
    ShoppingListResponse,
    ShoppingListItemCreate,
    ShoppingListItemResponse,
    MarketComparisonResponse,
    ShoppingListUpdate
)
from app.crud import crud_shopping_list
from app.utils.pdf_generator import generate_shopping_list_pdf
import json
from app.models.user import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=schemas.ShoppingList)
def create_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_in: schemas.ShoppingListCreate,
    # current_user: models.User = Depends(deps.get_current_user)  # Commented out auth check
) -> Any:
    """
    Create new shopping list.
    """
    try:
        # Set user_id to 1 by default
        shopping_list = crud_shopping_list.shopping_list.create_with_items(
            db=db,
            obj_in=shopping_list_in,
            user_id=1
        )
        return shopping_list
    except Exception as e:
        logger.error(f"Error creating shopping list: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[schemas.ShoppingList])
def read_shopping_lists(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_user)  # Commented out auth check
) -> Any:
    """
    Retrieve shopping lists.
    """
    try:
        # Get all lists for user_id 1
        shopping_lists = crud_shopping_list.shopping_list.get_multi_by_user(
            db=db,
            user_id=1,
            skip=skip,
            limit=limit
        )
        return shopping_lists
    except Exception as e:
        logger.error(f"Error retrieving shopping lists: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{id}", response_model=schemas.ShoppingListInDB)
def read_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_user)  # Commented out auth check
) -> Any:
    """
    Get shopping list by ID.
    """
    shopping_list = crud.shopping_list.get(db=db, id=id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return shopping_list

@router.put("/{id}", response_model=schemas.ShoppingListInDB)
def update_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    shopping_list_in: schemas.ShoppingListUpdate,
    # current_user: models.User = Depends(deps.get_current_user)  # Commented out auth check
) -> Any:
    """
    Update shopping list.
    """
    shopping_list = crud.shopping_list.get(db=db, id=id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return crud.shopping_list.update(db=db, db_obj=shopping_list, obj_in=shopping_list_in)

@router.delete("/{id}", response_model=schemas.ShoppingListInDB)
def delete_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_user)  # Commented out auth check
) -> Any:
    """
    Delete shopping list.
    """
    shopping_list = crud.shopping_list.get(db=db, id=id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return crud.shopping_list.remove(db=db, id=id)

@router.post("/{shopping_list_id}/items", response_model=schemas.ShoppingListItemInDB)
def create_shopping_list_item(
    shopping_list_id: int,
    item: schemas.ShoppingListItemCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Alışveriş listesine yeni ürün ekle.
    """
    db_shopping_list = crud.get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return crud.create_shopping_list_item(db, item, shopping_list_id)

@router.get("/{shopping_list_id}/market-comparison", response_model=List[MarketComparisonResponse])
def get_market_comparison(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
):
    """
    Alışveriş listesindeki ürünlerin farklı marketlerdeki fiyat karşılaştırmasını getir.
    """
    shopping_list = crud.get_shopping_list(db, shopping_list_id)
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
    shopping_list = crud.get_shopping_list(db, shopping_list_id)
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
    shopping_list = crud.get_shopping_list(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    
    # Paylaşım linki oluştur
    share_token = crud.generate_share_token(
        db=db,
        shopping_list_id=shopping_list_id
    )
    
    share_url = f"http://localhost:3000/shopping-lists/shared/{share_token}"
    return {"share_url": share_url} 