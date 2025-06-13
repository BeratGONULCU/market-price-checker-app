from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from backend.schemas.product import PriceHistory, PriceAlert
from backend.crud.product import get_price_history, get_price_alert, create_price_alert, delete_price_alert
from backend.api.deps import get_db
from backend.models.user import User
from backend.models.product import Product
from backend.models.product_detail import ProductDetail
from backend.models.market import Market
from backend.schemas.product import ProductDetail as ProductDetailSchema

router = APIRouter()

@router.get("/{product_id}", response_model=ProductDetailSchema)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Bir ürünün detaylarını getir.
    """
    product = db.query(Product).options(
        joinedload(Product.details).joinedload(ProductDetail.market)
    ).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    return product

@router.get("/{product_id}/details", response_model=List[ProductDetailSchema])
def get_product_details(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Bir ürünün tüm market detaylarını getir.
    """
    details = db.query(ProductDetail).options(
        joinedload(ProductDetail.market)
    ).filter(
        ProductDetail.product_id == product_id
    ).all()
    
    return details

@router.get("/{product_id}/price-history", response_model=List[PriceHistory])
def get_product_price_history(
    product_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> List[PriceHistory]:
    """
    Bir ürünün fiyat geçmişini getir.
    """
    price_history = get_price_history(
        db=db, product_id=product_id, skip=skip, limit=limit
    )
    return price_history

@router.get("/{product_id}/price-alert", response_model=Optional[PriceAlert])
def get_price_alert(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Optional[PriceAlert]:
    """
    Bir ürün için fiyat alarmını getir.
    """
    price_alert = get_price_alert(db=db, product_id=product_id, user_id=current_user.id)
    return price_alert

@router.post("/{product_id}/price-alert", response_model=PriceAlert)
def create_price_alert(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    target_price: float,
    current_user: User = Depends(get_current_user)
) -> PriceAlert:
    """
    Bir ürün için fiyat alarmı oluştur.
    """
    price_alert = create_price_alert(
        db=db, product_id=product_id, user_id=current_user.id, target_price=target_price
    )
    return price_alert

@router.delete("/{product_id}/price-alert")
def delete_price_alert(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Bir ürün için fiyat alarmını kaldır.
    """
    delete_price_alert(db=db, product_id=product_id, user_id=current_user.id)
    return {"message": "Fiyat alarmı kaldırıldı"} 