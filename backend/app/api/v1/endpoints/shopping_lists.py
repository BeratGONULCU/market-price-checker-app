from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
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

router = APIRouter()

@router.post("/", response_model=ShoppingList)
def create_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_in: ShoppingListCreate,
    current_user: User = Depends(deps.get_current_user)
) -> ShoppingList:
    """
    Yeni bir alışveriş listesi oluştur.
    """
    shopping_list = crud_shopping_list.create_shopping_list(
        db=db, obj_in=shopping_list_in, user_id=current_user.id
    )
    return shopping_list

@router.get("/", response_model=List[ShoppingList])
def get_shopping_lists(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[ShoppingList]:
    """
    Kullanıcının alışveriş listelerini getir.
    """
    shopping_lists = crud_shopping_list.get_user_shopping_lists(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return shopping_lists

@router.get("/{shopping_list_id}", response_model=ShoppingList)
def get_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> ShoppingList:
    """
    Belirli bir alışveriş listesini getir.
    """
    shopping_list = crud_shopping_list.get_shopping_list(db=db, shopping_list_id=shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    if shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu alışveriş listesine erişim yetkiniz yok")
    return shopping_list

@router.post("/{shopping_list_id}/items", response_model=ShoppingListItem)
def add_shopping_list_item(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
    item_in: ShoppingListItemCreate,
    current_user: User = Depends(deps.get_current_user)
) -> ShoppingListItem:
    """
    Alışveriş listesine ürün ekle.
    """
    shopping_list = crud_shopping_list.get_shopping_list(db=db, shopping_list_id=shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    if shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu alışveriş listesine ürün ekleme yetkiniz yok")
    item = crud_shopping_list.add_shopping_list_item(
        db=db, shopping_list_id=shopping_list_id, obj_in=item_in
    )
    return item

@router.put("/items/{item_id}", response_model=ShoppingListItemResponse)
def update_shopping_list_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: ShoppingListItemCreate,
    current_user = Depends(deps.get_current_user)
):
    """
    Alışveriş listesindeki bir ürünü güncelle.
    """
    item = crud_shopping_list.get_shopping_list_item(
        db=db,
        item_id=item_id
    )
    if not item:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    # Kullanıcının bu listeye erişim yetkisi var mı kontrol et
    shopping_list = crud_shopping_list.get_shopping_list(
        db=db,
        shopping_list_id=item.shopping_list_id,
        user_id=current_user.id
    )
    if not shopping_list:
        raise HTTPException(status_code=403, detail="Bu işlem için yetkiniz yok")
    
    item = crud_shopping_list.update_shopping_list_item(
        db=db,
        item_id=item_id,
        item_in=item_in
    )
    return item

@router.delete("/{shopping_list_id}/items/{item_id}")
def remove_shopping_list_item(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
    item_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Alışveriş listesinden ürün kaldır.
    """
    shopping_list = crud_shopping_list.get_shopping_list(db=db, shopping_list_id=shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    if shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu alışveriş listesinden ürün kaldırma yetkiniz yok")
    crud_shopping_list.remove_shopping_list_item(db=db, item_id=item_id)
    return {"message": "Ürün alışveriş listesinden kaldırıldı"}

@router.get("/{shopping_list_id}/market-comparison", response_model=List[MarketComparisonResponse])
def get_market_comparison(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
    current_user = Depends(deps.get_current_user)
):
    """
    Alışveriş listesindeki ürünlerin farklı marketlerdeki fiyat karşılaştırmasını getir.
    """
    shopping_list = crud_shopping_list.get_shopping_list(
        db=db,
        shopping_list_id=shopping_list_id,
        user_id=current_user.id
    )
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
    current_user = Depends(deps.get_current_user)
):
    """
    Alışveriş listesini PDF olarak dışa aktar.
    """
    shopping_list = crud_shopping_list.get_shopping_list(
        db=db,
        shopping_list_id=shopping_list_id,
        user_id=current_user.id
    )
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    
    # Market karşılaştırmasını al
    market_comparisons = get_market_comparison(
        db=db,
        shopping_list_id=shopping_list_id,
        current_user=current_user
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
    current_user = Depends(deps.get_current_user)
):
    """
    Alışveriş listesini paylaş.
    """
    shopping_list = crud_shopping_list.get_shopping_list(
        db=db,
        shopping_list_id=shopping_list_id,
        user_id=current_user.id
    )
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    
    # Paylaşım linki oluştur
    share_token = crud_shopping_list.generate_share_token(
        db=db,
        shopping_list_id=shopping_list_id
    )
    
    share_url = f"http://localhost:3000/shopping-lists/shared/{share_token}"
    return {"share_url": share_url}

@router.put("/{shopping_list_id}", response_model=ShoppingList)
def update_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
    shopping_list_in: ShoppingListUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> ShoppingList:
    """
    Bir alışveriş listesini güncelle.
    """
    shopping_list = crud_shopping_list.get_shopping_list(db=db, shopping_list_id=shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    if shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu alışveriş listesini düzenleme yetkiniz yok")
    shopping_list = crud_shopping_list.update_shopping_list(
        db=db, db_obj=shopping_list, obj_in=shopping_list_in
    )
    return shopping_list

@router.delete("/{shopping_list_id}")
def delete_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Bir alışveriş listesini sil.
    """
    shopping_list = crud_shopping_list.get_shopping_list(db=db, shopping_list_id=shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Alışveriş listesi bulunamadı")
    if shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu alışveriş listesini silme yetkiniz yok")
    crud_shopping_list.delete_shopping_list(db=db, shopping_list_id=shopping_list_id)
    return {"message": "Alışveriş listesi silindi"} 