from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base import BaseSchema

class PriceHistoryBase(BaseModel):
    price: float
    product_id: int
    market_id: int

class PriceHistoryCreate(PriceHistoryBase):
    pass

class PriceHistoryUpdate(PriceHistoryBase):
    price: Optional[float] = None
    product_id: Optional[int] = None
    market_id: Optional[int] = None

class PriceHistoryInDB(PriceHistoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PriceHistory(PriceHistoryInDB):
    pass 