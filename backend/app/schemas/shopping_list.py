from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ShoppingListItemBase(BaseModel):
    product_id: int
    quantity: int
    is_checked: bool = False

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItemResponse(ShoppingListItemBase):
    id: int
    shopping_list_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ShoppingListBase(BaseModel):
    name: str

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingListResponse(ShoppingListBase):
    id: int
    user_id: int
    items: List[ShoppingListItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MarketComparisonItem(BaseModel):
    product_id: int
    product_name: str
    price: float
    quantity: int

class MarketComparisonResponse(BaseModel):
    market_id: int
    market_name: str
    total_price: float
    items: List[MarketComparisonItem]

    class Config:
        orm_mode = True 