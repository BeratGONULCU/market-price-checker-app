from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import logging

from app.db.session import get_db
from app.models.product import Product
from app.models.product_detail import ProductDetail
from app.schemas.product import Product as ProductSchema, ProductCreate, ProductUpdate
from app import crud, schemas, models
from app.api import deps

router = APIRouter()

@router.post("", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@router.get("/test-details")
def test_product_details(db: Session = Depends(get_db)):
    """
    Test endpoint to check product details data.
    """
    try:
        logging.info("Starting test_product_details function")
        
        # Tüm ürün detaylarını çek
        details = db.query(ProductDetail).all()
        
        logging.info(f"Found {len(details)} product details")
        
        # İlk birkaç detayı logla
        for i, detail in enumerate(details):
            logging.info(f"Detail {i+1}:")
            logging.info(f"  ID: {detail.id}")
            logging.info(f"  Product ID: {detail.product_id}")
            logging.info(f"  Market ID: {detail.market_id}")
            logging.info(f"  Price: {detail.price}")
            logging.info(f"  Calories: {detail.calories}")
            logging.info(f"  Expiration Date: {detail.expiration_date}")
            logging.info(f"  Is Favorite: {detail.is_favorite}")
            logging.info(f"  Created At: {detail.created_at}")
            logging.info(f"  Updated At: {detail.updated_at}")
        
        
        return {
            "total_details": len(details),
            "sample_details": [
                {
                    "id": detail.id,
                    "product_id": detail.product_id,
                    "market_id": detail.market_id,
                    "price": detail.price,
                    "calories": detail.calories,
                    "expiration_date": detail.expiration_date,
                    "is_favorite": detail.is_favorite,
                    "created_at": detail.created_at,
                    "updated_at": detail.updated_at
                }
                for detail in details
            ]
        }
    except Exception as e:
        logging.error(f"Error in test_product_details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/product-details")
def get_product_details(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get all product details with their market information.
    """
    try:
        logging.info("Starting get_product_details function")
        
        # Tüm ürün detaylarını çek
        details = db.query(ProductDetail).all()
        
        logging.info(f"Found {len(details)} product details")
        
        # İlk birkaç detayı logla
        for i, detail in enumerate(details[:5]):
            logging.info(f"Detail {i+1}:")
            logging.info(f"  ID: {detail.id}")
            logging.info(f"  Product ID: {detail.product_id}")
            logging.info(f"  Market ID: {detail.market_id}")
            logging.info(f"  Price: {detail.price}")
            logging.info(f"  Calories: {detail.calories}")
            logging.info(f"  Expiration Date: {detail.expiration_date}")
            logging.info(f"  Is Favorite: {detail.is_favorite}")
            logging.info(f"  Created At: {detail.created_at}")
            logging.info(f"  Updated At: {detail.updated_at}")
        
        return {
            "total_details": len(details),
            "sample_details": [
                {
                    "id": detail.id,
                    "product_id": detail.product_id,
                    "market_id": detail.market_id,
                    "price": detail.price,
                    "calories": detail.calories,
                    "expiration_date": detail.expiration_date,
                    "is_favorite": detail.is_favorite,
                    "created_at": detail.created_at,
                    "updated_at": detail.updated_at
                }
                for detail in details
            ]
        }
    except Exception as e:
        logging.error(f"Error in get_product_details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/favorites", response_model=List[schemas.Product])
def get_favorite_products(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get all products that are marked as favorite.
    """
    try:
        logging.info("Starting get_favorite_products function")
        
        # Favori olan ürün detaylarını bul
        favorite_details = db.query(ProductDetail).filter(
            ProductDetail.is_favorite == True
        ).all()
        
        logging.info(f"Found {len(favorite_details)} favorite details")
        
        # Favori detayların ürün ID'lerini al
        product_ids = [detail.product_id for detail in favorite_details]
        logging.info(f"Product IDs: {product_ids}")
        
        if not product_ids:
            logging.info("No favorite products found")
            return []
        
        # Bu ürünleri ve detaylarını çek
        products = db.query(Product).filter(
            Product.id.in_(product_ids)
        ).options(
            joinedload(Product.details).joinedload(ProductDetail.market)
        ).all()
        
        logging.info(f"Found {len(products)} products")
        
        # Her ürün için sadece favori olan detayları göster
        for product in products:
            product.details = [detail for detail in product.details if detail.is_favorite]
            logging.info(f"Product {product.id} has {len(product.details)} favorite details")
            for detail in product.details:
                logging.info(f"Detail: product_id={detail.product_id}, market_id={detail.market_id}, is_favorite={detail.is_favorite}")
        
        return products
    except Exception as e:
        logging.error(f"Error in get_favorite_products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[ProductSchema])
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
        logging.info("Starting read_products function")
        
        # Önce ürünleri al
        query = db.query(Product).options(
            joinedload(Product.details).joinedload(ProductDetail.market)
        )
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        products = query.offset(skip).limit(limit).all()
        
        # Debug logs
        logging.info(f"Found {len(products)} products")
        if products:
            first_product = products[0]
            logging.info(f"First product: ID={first_product.id}, Name={first_product.name}")
            logging.info(f"Product details count: {len(first_product.details)}")
            if first_product.details:
                first_detail = first_product.details[0]
                logging.info(f"First detail: Price={first_detail.price}, Market={first_detail.market.name if first_detail.market else 'No market'}")
                logging.info(f"First detail is_favorite: {first_detail.is_favorite}")
        else:
            logging.warning("No products found in database")
            
            # Check if there are any products in the database
            total_products = db.query(Product).count()
            logging.info(f"Total products in database: {total_products}")
        
        return products
    except Exception as e:
        logging.error(f"Error in read_products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", response_model=ProductSchema)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return db_product

@router.patch("/{product_id}/details/{market_id}/favorite", response_model=schemas.ProductDetail)
def toggle_favorite(
    product_id: int,
    market_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Toggle favorite status of a product detail.
    """
    try:
        # Ürün detayını bul
        product_detail = db.query(ProductDetail).filter(
            ProductDetail.product_id == product_id,
            ProductDetail.market_id == market_id
        ).first()
        
        if not product_detail:
            raise HTTPException(status_code=404, detail="Product detail not found")
        
        # Favori durumunu tersine çevir
        product_detail.is_favorite = not product_detail.is_favorite
        
        db.commit()
        db.refresh(product_detail)
        
        logging.info(f"Toggled favorite status for product {product_id} at market {market_id} to {product_detail.is_favorite}")
        
        return product_detail
    except Exception as e:
        logging.error(f"Error in toggle_favorite: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 