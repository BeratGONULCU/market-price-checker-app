from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ShoppingListItemBase(BaseModel):
    product_id: int
    quantity: int = 1
    notes: Optional[str] = None

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItemUpdate(ShoppingListItemBase):
    pass

class ShoppingListItemInDB(ShoppingListItemBase):
    id: int
    shopping_list_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ShoppingListBase(BaseModel):
    name: str

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingListUpdate(ShoppingListBase):
    pass

class ShoppingListInDB(ShoppingListBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    items: List[ShoppingListItemInDB] = []

    class Config:
        from_attributes = True

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