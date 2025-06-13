from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas
from app.models.favorite import Favorite
from app.models.product_detail import ProductDetail

def toggle_favorite(db: Session, detail_id: int, user_id: int) -> Favorite:
    """
    Toggle favorite status for a product detail.
    If favorite exists, remove it. If not, create it.
    """
    # Önce ürün detayının var olup olmadığını kontrol et
    detail = db.query(ProductDetail).filter(ProductDetail.id == detail_id).first()
    if not detail:
        return None

    # Mevcut favoriyi kontrol et
    favorite = db.query(Favorite).filter(
        Favorite.product_detail_id == detail_id,
        Favorite.user_id == user_id
    ).first()

    if favorite:
        # Favoriyi kaldır
        db.delete(favorite)
        db.commit()
        # Ürün detayının is_favorite durumunu güncelle
        detail.is_favorite = False
        db.commit()
        return None
    else:
        # Yeni favori oluştur
        favorite = Favorite(
            product_detail_id=detail_id,
            user_id=user_id
        )
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        # Ürün detayının is_favorite durumunu güncelle
        detail.is_favorite = True
        db.commit()
        return favorite

def get_favorites_by_user(db: Session, user_id: int) -> list[Favorite]:
    """
    Get all favorites for a user.
    """
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()

def get_product_detail_by_product_and_market(db: Session, product_id: int, market_id: int) -> Optional[models.ProductDetail]:
    return db.query(models.ProductDetail).filter(
        models.ProductDetail.product_id == product_id,
        models.ProductDetail.market_id == market_id
    ).first()

def update_product_detail_favorite(db: Session, product_detail_id: int, is_favorite: bool) -> models.ProductDetail:
    product_detail = db.query(models.ProductDetail).filter(models.ProductDetail.id == product_detail_id).first()
    if product_detail:
        product_detail.is_favorite = is_favorite
        db.commit()
        db.refresh(product_detail)
    return product_detail

def get_favorite_product_details(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[models.ProductDetail]:
    return db.query(models.ProductDetail).filter(
        models.ProductDetail.is_favorite == True
    ).offset(skip).limit(limit).all() 