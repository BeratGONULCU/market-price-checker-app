from pydantic import BaseModel
from datetime import datetime

class ProductPriceBase(BaseModel):
    price: float
    market_id: int
    product_id: int

class ProductPriceCreate(ProductPriceBase):
    pass

class ProductPrice(ProductPriceBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True 