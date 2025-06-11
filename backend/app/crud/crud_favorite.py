from sqlalchemy.orm import Session
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