from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud import crud_favorite
from app.schemas.favorite import FavoriteCreate, Favorite

router = APIRouter()

@router.post("/toggle/{detail_id}", response_model=Favorite)
def toggle_favorite(
    detail_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    Toggle favorite status for a product detail.
    """
    favorite = crud_favorite.toggle_favorite(db=db, detail_id=detail_id, user_id=current_user.id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Product detail not found")
    return favorite

@router.get("/", response_model=List[Favorite])
def get_favorites(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    Get all favorites for current user.
    """
    return crud_favorite.get_favorites_by_user(db=db, user_id=current_user.id) 