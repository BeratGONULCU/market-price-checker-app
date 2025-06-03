from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.price_history import PriceHistory
from app.schemas.price_history import PriceHistory as PriceHistorySchema, PriceHistoryCreate

router = APIRouter()

@router.post("/", response_model=PriceHistorySchema)
def create_price_history(price_history: PriceHistoryCreate, db: Session = Depends(get_db)):
    db_price_history = PriceHistory(**price_history.dict())
    db.add(db_price_history)
    db.commit()
    db.refresh(db_price_history)
    return db_price_history

@router.get("/product/{product_id}", response_model=List[PriceHistorySchema])
def read_product_price_history(
    product_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    start_date = datetime.utcnow() - timedelta(days=days)
    price_history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.created_at >= start_date
    ).order_by(PriceHistory.created_at.desc()).all()
    return price_history

@router.get("/market/{market_id}", response_model=List[PriceHistorySchema])
def get_market_price_history(market_id: int, db: Session = Depends(get_db)):
    price_history = db.query(PriceHistory).filter(PriceHistory.market_id == market_id).all()
    return price_history

@router.get("/{price_history_id}", response_model=PriceHistorySchema)
def read_price_history(price_history_id: int, db: Session = Depends(get_db)):
    db_price_history = db.query(PriceHistory).filter(PriceHistory.id == price_history_id).first()
    if db_price_history is None:
        raise HTTPException(status_code=404, detail="Price history not found")
    return db_price_history

@router.delete("/{price_history_id}", response_model=PriceHistorySchema)
def delete_price_history(price_history_id: int, db: Session = Depends(get_db)):
    db_price_history = db.query(PriceHistory).filter(PriceHistory.id == price_history_id).first()
    if db_price_history is None:
        raise HTTPException(status_code=404, detail="Price history not found")
    
    db.delete(db_price_history)
    db.commit()
    return db_price_history 