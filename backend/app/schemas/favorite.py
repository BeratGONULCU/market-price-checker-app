from pydantic import BaseModel
from .base import BaseSchema

class FavoriteBase(BaseModel):
    user_id: int
    product_id: int

class FavoriteCreate(BaseModel):
    product_id: int

class FavoriteInDB(FavoriteBase, BaseSchema):
    pass

class Favorite(FavoriteInDB):
    pass

    class Config:
        from_attributes = True 