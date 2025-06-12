from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

def create_review(
    db: Session,
    *,
    obj_in: ReviewCreate,
    user_id: int
) -> Review:
    """
    Yeni bir yorum oluştur.
    """
    db_obj = Review(
        user_id=user_id,
        product_id=obj_in.product_id,
        rating=obj_in.rating,
        content=obj_in.content
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_review(
    db: Session,
    review_id: int
) -> Optional[Review]:
    """
    Belirli bir yorumu getir.
    """
    return db.query(Review).filter(Review.id == review_id).first()

def get_product_reviews(
    db: Session,
    product_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Review]:
    """
    Bir ürüne ait yorumları getir.
    """
    reviews = db.query(Review).filter(
        Review.product_id == product_id
    ).offset(skip).limit(limit).all()
    
    # Her yorum için kullanıcı adını ekle
    for review in reviews:
        review.user_name = review.user.username
    
    return reviews

def update_review(
    db: Session,
    *,
    db_obj: Review,
    obj_in: ReviewUpdate
) -> Review:
    """
    Bir yorumu güncelle.
    """
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_review(
    db: Session,
    *,
    review_id: int
) -> None:
    """
    Bir yorumu sil.
    """
    db_obj = get_review(db, review_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()

def get_user_reviews(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Review]:
    """
    Bir kullanıcının yorumlarını getir.
    """
    return db.query(Review).filter(
        Review.user_id == user_id
    ).offset(skip).limit(limit).all() 