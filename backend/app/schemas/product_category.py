from pydantic import BaseModel

class ProductCategoryCreate(BaseModel):
    product_id: int
    category_id: int
 
class ProductCategoryResponse(ProductCategoryCreate):
    id: int
    class Config:
        orm_mode = True 