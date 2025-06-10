from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseSchema

class PriceAlertBase(BaseModel):
    user_id: int
    product_id: int
    target_price: float
    is_active: bool = True
    notified: bool = False

class PriceAlertCreate(PriceAlertBase):
    pass

class PriceAlertUpdate(PriceAlertBase):
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    target_price: Optional[float] = None
    is_active: Optional[bool] = None
    notified: Optional[bool] = None

class PriceAlertInDB(PriceAlertBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_checked: Optional[datetime] = None

    class Config:
        from_attributes = True

class PriceAlert(PriceAlertInDB):
    pass 