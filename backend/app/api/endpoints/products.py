from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import logging

from app.db.session import get_db
from app.models.product import Product
from app.models.product_detail import ProductDetail
from app.schemas.product import Product as ProductSchema, ProductCreate, ProductUpdate
from ... import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@router.get("/", response_model=List[ProductSchema])
def read_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    try:
        # Önce ürünleri al
        query = db.query(Product)
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        products = query.offset(skip).limit(limit).all()
        
        # Her ürün için detayları ve market bilgilerini al
        for product in products:
            details = db.query(ProductDetail).join(
                ProductDetail.market,
                isouter=True
            ).filter(
                ProductDetail.product_id == product.id
            ).all()
            product.details = details
        
        # Debug logs
        logging.info(f"Found {len(products)} products")
        if products:
            first_product = products[0]
            logging.info(f"First product: ID={first_product.id}, Name={first_product.name}")
            logging.info(f"Product details count: {len(first_product.details)}")
            if first_product.details:
                first_detail = first_product.details[0]
                logging.info(f"First detail: Price={first_detail.price}, Market={first_detail.market.name if first_detail.market else 'No market'}")
        
        return products
    except Exception as e:
        logging.error(f"Error in read_products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    # Ürünü ve ilişkili tüm verileri tek sorguda al
    db_product = db.query(Product).options(
        joinedload(Product.details).joinedload(ProductDetail.market)
    ).filter(Product.id == product_id).first()
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Debug log
    logging.info(f"Product details count: {len(db_product.details)}")
    for detail in db_product.details:
        logging.info(f"Detail: Price={detail.price}, Market={detail.market.name if detail.market else 'No market'}")
    
    return db_product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", response_model=ProductSchema)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return db_product 