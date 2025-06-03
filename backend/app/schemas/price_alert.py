from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseSchema

class PriceAlertBase(BaseModel):
    user_id: int
    product_id: int
    target_price: float
    is_active: bool
    created_at: datetime
    last_checked: Optional[datetime] = None
    notified: bool

class PriceAlertCreate(BaseModel):
    product_id: int
    target_price: float

class PriceAlertUpdate(BaseModel):
    target_price: Optional[float] = None
    is_active: Optional[bool] = None
    last_checked: Optional[datetime] = None
    notified: Optional[bool] = None

class PriceAlertInDB(PriceAlertBase, BaseSchema):
    pass

class PriceAlert(PriceAlertInDB):
    pass 