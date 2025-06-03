from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.favorite import Favorite
from app.schemas.favorite import Favorite as FavoriteSchema, FavoriteCreate

router = APIRouter()

@router.post("/", response_model=FavoriteSchema)
def create_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db)):
    # Check if favorite already exists
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == favorite.user_id,
        Favorite.product_id == favorite.product_id
    ).first()
    
    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already in favorites"
        )
    
    db_favorite = Favorite(**favorite.dict())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

@router.get("/user/{user_id}", response_model=List[FavoriteSchema])
def read_user_favorites(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    favorites = db.query(Favorite).filter(
        Favorite.user_id == user_id
    ).offset(skip).limit(limit).all()
    return favorites

@router.get("/{favorite_id}", response_model=FavoriteSchema)
def read_favorite(favorite_id: int, db: Session = Depends(get_db)):
    db_favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return db_favorite

@router.delete("/{favorite_id}", response_model=FavoriteSchema)
def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    db_favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(db_favorite)
    db.commit()
    return db_favorite 