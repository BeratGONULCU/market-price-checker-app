from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.product_detail import ProductDetail
from app.schemas.product_detail import ProductDetail as ProductDetailSchema, ProductDetailCreate, ProductDetailUpdate

router = APIRouter()

@router.post("/", response_model=ProductDetailSchema)
def create_product_detail(product_detail: ProductDetailCreate, db: Session = Depends(get_db)):
    db_product_detail = ProductDetail(**product_detail.dict())
    db.add(db_product_detail)
    db.commit()
    db.refresh(db_product_detail)
    return db_product_detail

@router.get("/", response_model=List[ProductDetailSchema])
def read_product_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product_details = db.query(ProductDetail).offset(skip).limit(limit).all()
    return product_details

@router.get("/{product_detail_id}", response_model=ProductDetailSchema)
def read_product_detail(product_detail_id: int, db: Session = Depends(get_db)):
    db_product_detail = db.query(ProductDetail).filter(ProductDetail.id == product_detail_id).first()
    if db_product_detail is None:
        raise HTTPException(status_code=404, detail="Product detail not found")
    return db_product_detail

@router.put("/{product_detail_id}", response_model=ProductDetailSchema)
def update_product_detail(product_detail_id: int, product_detail: ProductDetailUpdate, db: Session = Depends(get_db)):
    db_product_detail = db.query(ProductDetail).filter(ProductDetail.id == product_detail_id).first()
    if db_product_detail is None:
        raise HTTPException(status_code=404, detail="Product detail not found")
    
    for key, value in product_detail.dict(exclude_unset=True).items():
        setattr(db_product_detail, key, value)
    
    db.commit()
    db.refresh(db_product_detail)
    return db_product_detail

@router.delete("/{product_detail_id}", response_model=ProductDetailSchema)
def delete_product_detail(product_detail_id: int, db: Session = Depends(get_db)):
    db_product_detail = db.query(ProductDetail).filter(ProductDetail.id == product_detail_id).first()
    if db_product_detail is None:
        raise HTTPException(status_code=404, detail="Product detail not found")
    
    db.delete(db_product_detail)
    db.commit()
    return db_product_detail 