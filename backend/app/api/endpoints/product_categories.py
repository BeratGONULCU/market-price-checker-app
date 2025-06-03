from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.product import Product
from app.models.category import Category
from app.schemas.category import CategoryResponse

router = APIRouter()

@router.get("/products/{product_id}/categories", response_model=List[CategoryResponse])
def get_product_categories(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.categories

@router.post("/products/{product_id}/categories/{category_id}")
def add_category_to_product(product_id: int, category_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category in product.categories:
        raise HTTPException(status_code=400, detail="Category already added to product")
    
    product.categories.append(category)
    db.commit()
    return {"message": "Category added to product successfully"}

@router.delete("/products/{product_id}/categories/{category_id}")
def remove_category_from_product(product_id: int, category_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category not in product.categories:
        raise HTTPException(status_code=400, detail="Category not associated with product")
    
    product.categories.remove(category)
    db.commit()
    return {"message": "Category removed from product successfully"} 