from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Product
from schemas import ProductCreate, Product as ProductSchema

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=List[ProductSchema])
def get_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    search: str = None
):
    query = db.query(Product)
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(search)) |
            (Product.brand.ilike(search)) |
            (Product.barcode.ilike(search))
        )
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        brand=product.brand,
        barcode=product.barcode,
        image_url=product.image_url,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.brand = product.brand
    db_product.barcode = product.barcode
    db_product.image_url = product.image_url
    db_product.category_id = product.category_id

    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"} 