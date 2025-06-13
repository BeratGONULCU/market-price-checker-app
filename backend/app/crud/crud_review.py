from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.review import Comment
from app.schemas.review import ReviewCreate, ReviewUpdate

def get_review(db: Session, review_id: int) -> Optional[Comment]:
    return db.query(Comment).filter(Comment.id == review_id).first()

def get_reviews(
    db: Session,
    skip: int = 0, 
    limit: int = 100,
    product_id: Optional[int] = None,
    user_id: Optional[int] = None
) -> List[Comment]:
    query = db.query(Comment)
    
    if product_id:
        query = query.filter(Comment.product_id == product_id)
    if user_id:
        query = query.filter(Comment.user_id == user_id)
        
    return query.offset(skip).limit(limit).all()

def create_review(db: Session, review: ReviewCreate) -> Comment:
    db_review = Comment(
        user_id=review.user_id,
        product_id=review.product_id,
        content=review.content,
        rating=review.rating
        )
    db.add(db_review)
        db.commit()
    db.refresh(db_review)
    return db_review

def update_review(
    db: Session,
    review_id: int,
    review: ReviewUpdate
) -> Optional[Comment]:
    db_review = get_review(db, review_id)
    if not db_review:
        return None
        
    for field, value in review.dict(exclude_unset=True).items():
        setattr(db_review, field, value)
        
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int) -> bool:
    db_review = get_review(db, review_id)
    if not db_review:
        return False
        
    db.delete(db_review)
    db.commit()
    return True

def get_product_reviews(
    db: Session,
    product_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Comment]:
    """
    Bir ürüne ait yorumları getir.
    """
    reviews = db.query(Comment).filter(
        Comment.product_id == product_id
    ).offset(skip).limit(limit).all()
    
    # Her yorum için kullanıcı adını ekle
    for review in reviews:
        review.user_name = review.user.username
    
    return reviews

def get_user_reviews(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Comment]:
    """
    Bir kullanıcının yorumlarını getir.
    """
    reviews = db.query(Comment).filter(
        Comment.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    # Her yorum için kullanıcı adını ekle
    for review in reviews:
        review.user_name = review.user.username
    
    return reviews 