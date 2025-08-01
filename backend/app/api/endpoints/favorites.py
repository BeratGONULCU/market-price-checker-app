from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from app import crud, models, schemas
from app.api import deps
from app.models.product_detail import ProductDetail
import logging
import traceback

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/{product_id}", response_model=schemas.ProductDetail)
def create_favorite(
    product_id: int,
    market_id: int = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Add a product to favorites by updating product_details.
    """
    logger.info(f"Creating favorite for product {product_id} and market {market_id} by user {current_user.id}")
    
    # Check if product exists
    product = crud.get_product(db, product_id)
    if not product:
        logger.error(f"Product {product_id} not found")
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if market exists
    market = crud.get_market(db, market_id)
    if not market:
        logger.error(f"Market {market_id} not found")
        raise HTTPException(status_code=404, detail="Market not found")
    
    # Get product detail
    product_detail = crud.get_product_detail_by_product_and_market(db, product_id, market_id)
    if not product_detail:
        logger.error(f"Product detail not found for product {product_id} and market {market_id}")
        raise HTTPException(status_code=404, detail="Product detail not found")
    
    # Check if already favorited
    if product_detail.is_favorite:
        logger.warning(f"Product {product_id} already in favorites for user {current_user.id}")
        raise HTTPException(status_code=400, detail="Product already in favorites")
    
    # Update product detail
    try:
        updated_detail = crud.update_product_detail_favorite(db, product_detail.id, True)
        logger.info(f"Successfully created favorite: {updated_detail}")
        return updated_detail
    except Exception as e:
        logger.error(f"Error creating favorite: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}")
def delete_favorite(
    product_id: int,
    market_id: int = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Remove a product from favorites by updating product_details.
    """
    product_detail = crud.get_product_detail_by_product_and_market(db, product_id, market_id)
    if not product_detail:
        raise HTTPException(status_code=404, detail="Product detail not found")
    
    if not product_detail.is_favorite:
        raise HTTPException(status_code=400, detail="Product is not in favorites")
    
    updated_detail = crud.update_product_detail_favorite(db, product_detail.id, False)
    return updated_detail

@router.get("/", response_model=List[schemas.ProductDetail])
def read_favorites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    """
    Get all favorite products from product_details.
    """
    try:
        logger.info("Getting all favorites")
        logger.info(f"Database session: {db}")
        
        # Test database connection
        try:
            db.execute(text("SELECT 1"))
            logger.info("Database connection successful")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        favorites = crud.get_favorite_product_details(db, skip=skip, limit=limit)
        logger.info(f"Found {len(favorites)} favorites")
        logger.info(f"First favorite (if any): {favorites[0] if favorites else None}")
        
        return favorites
    except Exception as e:
        logger.error(f"Error in read_favorites: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/toggle/{detail_id}", response_model=schemas.ProductDetail)
def toggle_favorite(
    detail_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Toggle favorite status for a product detail.
    """
    try:
        logger.info(f"Toggling favorite for detail_id: {detail_id}")
        product_detail = db.query(ProductDetail).filter(ProductDetail.id == detail_id).first()
        
        if not product_detail:
            logger.error(f"Product detail not found for id: {detail_id}")
            raise HTTPException(status_code=404, detail="Product detail not found")
        
        logger.info(f"Current favorite status: {product_detail.is_favorite}")
        product_detail.is_favorite = not product_detail.is_favorite
        logger.info(f"New favorite status: {product_detail.is_favorite}")
        
        db.commit()
        db.refresh(product_detail)
        logger.info(f"Successfully toggled favorite status for detail_id: {detail_id}")
        
        return product_detail
    except Exception as e:
        logger.error(f"Error in toggle_favorite: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/check/{product_id}")
def check_favorite(
    product_id: int,
    market_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Check if a product is in user's favorites by checking product_details.
    """
    product_detail = crud.get_product_detail_by_product_and_market(db, product_id, market_id)
    return {"is_favorite": product_detail.is_favorite if product_detail else False} 