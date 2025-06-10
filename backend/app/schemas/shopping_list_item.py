from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base import BaseSchema

class ShoppingListItemBase(BaseModel):
    shopping_list_id: int
    product_id: int
    quantity: int
    notes: Optional[str] = None

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItemUpdate(ShoppingListItemBase):
    shopping_list_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    notes: Optional[str] = None

class ShoppingListItemInDB(ShoppingListItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShoppingListItem(ShoppingListItemInDB):
    pass 