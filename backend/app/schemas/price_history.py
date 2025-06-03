from pydantic import BaseModel
from datetime import datetime
from .base import BaseSchema

class PriceHistoryBase(BaseModel):
    product_id: int
    market_id: int
    price: float
    recorded_at: datetime

class PriceHistoryCreate(PriceHistoryBase):
    pass

class PriceHistoryInDB(PriceHistoryBase, BaseSchema):
    pass

class PriceHistory(PriceHistoryInDB):
    pass 