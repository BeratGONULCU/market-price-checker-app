from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas
from app.models.favorite import Favorite
from app.models.product_detail import ProductDetail
import logging
import traceback

logger = logging.getLogger(__name__)

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

def get_product_detail_by_product_and_market(db: Session, product_id: int, market_id: int) -> Optional[ProductDetail]:
    return db.query(ProductDetail).filter(
        ProductDetail.product_id == product_id,
        ProductDetail.market_id == market_id
    ).first()

def update_product_detail_favorite(db: Session, product_detail_id: int, is_favorite: bool) -> ProductDetail:
    product_detail = db.query(ProductDetail).filter(ProductDetail.id == product_detail_id).first()
    if product_detail:
        product_detail.is_favorite = is_favorite
        db.commit()
        db.refresh(product_detail)
    return product_detail

def get_favorite_product_details(
    db: Session, skip: int = 0, limit: int = 100
) -> List[ProductDetail]:
    """
    Get all favorite products from product_details table.
    """
    try:
        logger.info("Getting favorite product details")
        logger.info(f"Skip: {skip}, Limit: {limit}")
        
        # Test query
        test_query = db.query(ProductDetail).filter(ProductDetail.is_favorite == True)
        logger.info(f"Generated SQL: {test_query.statement}")
        
        # Execute query
        favorites = test_query.offset(skip).limit(limit).all()
        logger.info(f"Found {len(favorites)} favorite products")
        
        if favorites:
            logger.info(f"First favorite product: {favorites[0]}")
            logger.info(f"First favorite product details: id={favorites[0].id}, product_id={favorites[0].product_id}, is_favorite={favorites[0].is_favorite}")
        
        return favorites
    except Exception as e:
        logger.error(f"Error in get_favorite_product_details: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise 