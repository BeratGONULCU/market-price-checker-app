from pydantic import BaseModel
from typing import Optional
from .base import BaseSchema

class ShoppingListItemBase(BaseModel):
    user_id: int
    product_id: int
    is_checked: bool

class ShoppingListItemCreate(BaseModel):
    product_id: int

class ShoppingListItemUpdate(BaseModel):
    is_checked: Optional[bool] = None

class ShoppingListItemInDB(ShoppingListItemBase, BaseSchema):
    pass

class ShoppingListItem(ShoppingListItemInDB):
    pass 