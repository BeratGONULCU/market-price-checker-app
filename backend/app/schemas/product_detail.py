from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseSchema

class ProductDetailBase(BaseModel):
    product_id: int
    market_id: int
    price: float
    recorded_at: datetime
    last_updated: datetime
    expiration_date: Optional[datetime] = None
    calories: Optional[float] = None

class ProductDetailCreate(ProductDetailBase):
    pass

class ProductDetailUpdate(BaseModel):
    price: Optional[float] = None
    last_updated: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    calories: Optional[float] = None

class ProductDetailInDB(ProductDetailBase, BaseSchema):
    pass

class ProductDetail(ProductDetailInDB):
    pass 