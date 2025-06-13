from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.api import deps
from app.crud import crud_review
from app.schemas.review import Comment, CommentCreate, CommentUpdate
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_in: CommentCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Comment:
    """
    Yeni bir yorum oluştur.
    """
    try:
        logger.info(f"Creating comment: {comment_in.dict()}")
        comment = crud_review.create_review(db=db, obj_in=comment_in, user_id=current_user.id)
        logger.info(f"Comment created successfully: {comment.id}")
        return comment
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating comment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Veritabanı işlemi sırasında bir hata oluştu"
        )
    except Exception as e:
        logger.error(f"Unexpected error while creating comment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/product/{product_id}", response_model=List[Comment])
def get_product_comments(
    product_id: int,
    db: Session = Depends(deps.get_db)
) -> List[Comment]:
    """
    Bir ürüne ait yorumları getir.
    """
    try:
        logger.info(f"Getting comments for product: {product_id}")
        comments = crud_review.get_product_reviews(db=db, product_id=product_id)
        logger.info(f"Found {len(comments)} comments")
        return comments
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting comments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Veritabanı işlemi sırasında bir hata oluştu"
        )

@router.put("/{comment_id}", response_model=Comment)
def update_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    comment_in: CommentUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Comment:
    """
    Bir yorumu güncelle.
    """
    try:
        comment = crud_review.get_review(db=db, review_id=comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Yorum bulunamadı"
            )
        if comment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bu yorumu düzenleme yetkiniz yok"
            )
        comment = crud_review.update_review(db=db, db_obj=comment, obj_in=comment_in)
        return comment
    except SQLAlchemyError as e:
        logger.error(f"Database error while updating comment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Veritabanı işlemi sırasında bir hata oluştu"
        )

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Bir yorumu sil.
    """
    try:
        comment = crud_review.get_review(db=db, review_id=comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Yorum bulunamadı"
            )
        if comment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bu yorumu silme yetkiniz yok"
            )
        crud_review.delete_review(db=db, review_id=comment_id)
    except SQLAlchemyError as e:
        logger.error(f"Database error while deleting comment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Veritabanı işlemi sırasında bir hata oluştu"
        )

@router.get("/user", response_model=List[Comment])
def get_user_comments(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[Comment]:
    """
    Kullanıcının yorumlarını getir.
    """
    try:
        comments = crud_review.get_user_reviews(db=db, user_id=current_user.id, skip=skip, limit=limit)
        return comments
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting user comments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Veritabanı işlemi sırasında bir hata oluştu"
        ) 