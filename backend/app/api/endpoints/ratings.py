from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, Rating as RatingSchema

router = APIRouter()

@router.post("/", response_model=RatingSchema)
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    db_rating = Rating(**rating.model_dump())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/product/{product_id}", response_model=List[RatingSchema])
def get_product_ratings(product_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.product_id == product_id).all()
    return ratings

@router.get("/user/{user_id}", response_model=List[RatingSchema])
def get_user_ratings(user_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    return ratings

@router.get("/{rating_id}", response_model=RatingSchema)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@router.put("/{rating_id}", response_model=RatingSchema)
def update_rating(rating_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    for key, value in rating.model_dump().items():
        setattr(db_rating, key, value)
    
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.delete("/{rating_id}")
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(rating)
    db.commit()
    return {"message": "Rating deleted successfully"} 