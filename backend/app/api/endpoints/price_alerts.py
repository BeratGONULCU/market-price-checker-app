from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.price_alert import PriceAlert
from app.schemas.price_alert import PriceAlert as PriceAlertSchema, PriceAlertCreate, PriceAlertUpdate

router = APIRouter()

@router.post("/", response_model=PriceAlertSchema)
def create_price_alert(price_alert: PriceAlertCreate, db: Session = Depends(get_db)):
    # Check if alert already exists for this user and product
    existing_alert = db.query(PriceAlert).filter(
        PriceAlert.user_id == price_alert.user_id,
        PriceAlert.product_id == price_alert.product_id
    ).first()
    
    if existing_alert:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price alert already exists for this product"
        )
    
    db_price_alert = PriceAlert(**price_alert.dict())
    db.add(db_price_alert)
    db.commit()
    db.refresh(db_price_alert)
    return db_price_alert

@router.get("/user/{user_id}", response_model=List[PriceAlertSchema])
def read_user_price_alerts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    price_alerts = db.query(PriceAlert).filter(
        PriceAlert.user_id == user_id
    ).offset(skip).limit(limit).all()
    return price_alerts

@router.get("/{price_alert_id}", response_model=PriceAlertSchema)
def read_price_alert(price_alert_id: int, db: Session = Depends(get_db)):
    db_price_alert = db.query(PriceAlert).filter(PriceAlert.id == price_alert_id).first()
    if db_price_alert is None:
        raise HTTPException(status_code=404, detail="Price alert not found")
    return db_price_alert

@router.put("/{price_alert_id}", response_model=PriceAlertSchema)
def update_price_alert(price_alert_id: int, price_alert: PriceAlertUpdate, db: Session = Depends(get_db)):
    db_price_alert = db.query(PriceAlert).filter(PriceAlert.id == price_alert_id).first()
    if db_price_alert is None:
        raise HTTPException(status_code=404, detail="Price alert not found")
    
    for key, value in price_alert.dict(exclude_unset=True).items():
        setattr(db_price_alert, key, value)
    
    db.commit()
    db.refresh(db_price_alert)
    return db_price_alert

@router.delete("/{price_alert_id}", response_model=PriceAlertSchema)
def delete_price_alert(price_alert_id: int, db: Session = Depends(get_db)):
    db_price_alert = db.query(PriceAlert).filter(PriceAlert.id == price_alert_id).first()
    if db_price_alert is None:
        raise HTTPException(status_code=404, detail="Price alert not found")
    
    db.delete(db_price_alert)
    db.commit()
    return db_price_alert 