from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Product, ProductDetail
from ..schemas import ProductResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/favorites", response_model=List[ProductResponse])
def get_favorite_products(db: Session = Depends(get_db)):
    """
    Get all products that are marked as favorite in product_details table
    """
    try:
        # Get all product details that are marked as favorite
        favorite_details = db.query(ProductDetail).filter(ProductDetail.is_favorite == True).all()
        logger.info(f"Found {len(favorite_details)} favorite product details")
        
        # Get the corresponding products
        favorite_products = []
        for detail in favorite_details:
            product = db.query(Product).filter(Product.id == detail.product_id).first()
            if product:
                logger.info(f"Found product: {product.name} (ID: {product.id})")
                # Convert to response model
                product_response = ProductResponse(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    brand=product.brand,
                    image_url=product.image_url,
                    barcode=product.barcode,
                    created_at=product.created_at,
                    updated_at=product.updated_at
                )
                favorite_products.append(product_response)
            else:
                logger.warning(f"Product not found for detail ID: {detail.id}")
        
        logger.info(f"Returning {len(favorite_products)} favorite products")
        return favorite_products
    except Exception as e:
        logger.error(f"Error in get_favorite_products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 