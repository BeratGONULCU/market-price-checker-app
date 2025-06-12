from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_review
from app.schemas.review import ReviewCreate, ReviewUpdate, Review
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Review)
def create_review(
    *,
    db: Session = Depends(deps.get_db),
    review_in: ReviewCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Review:
    """
    Yeni bir yorum oluştur.
    """
    review = crud_review.create_review(db=db, obj_in=review_in, user_id=current_user.id)
    return review

@router.get("/product/{product_id}", response_model=List[Review])
def get_product_reviews(
    product_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> List[Review]:
    """
    Belirli bir ürüne ait yorumları getir.
    """
    reviews = crud_review.get_product_reviews(db=db, product_id=product_id, skip=skip, limit=limit)
    return reviews

@router.put("/{review_id}", response_model=Review)
def update_review(
    *,
    db: Session = Depends(deps.get_db),
    review_id: int,
    review_in: ReviewUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Review:
    """
    Bir yorumu güncelle.
    """
    review = crud_review.get_review(db=db, review_id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu yorumu güncelleme yetkiniz yok")
    review = crud_review.update_review(db=db, db_obj=review, obj_in=review_in)
    return review

@router.delete("/{review_id}", response_model=Review)
def delete_review(
    *,
    db: Session = Depends(deps.get_db),
    review_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Review:
    """
    Bir yorumu sil.
    """
    review = crud_review.get_review(db=db, review_id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu yorumu silme yetkiniz yok")
    review = crud_review.delete_review(db=db, review_id=review_id)
    return review

@router.get("/user", response_model=List[Review])
def get_user_reviews(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[Review]:
    """
    Kullanıcının yorumlarını getir.
    """
    reviews = crud_review.get_user_reviews(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return reviews 