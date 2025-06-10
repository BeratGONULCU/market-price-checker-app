from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/{product_id}", response_model=schemas.Favorite)
def create_favorite(
    product_id: int,
    market_id: int = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Add a product to favorites.
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
    
    # Check if already favorited
    favorite = crud.get_favorite_by_user_and_product(db, current_user.id, product_id)
    if favorite:
        logger.warning(f"Product {product_id} already in favorites for user {current_user.id}")
        raise HTTPException(status_code=400, detail="Product already in favorites")
    
    # Create favorite
    favorite_in = schemas.FavoriteCreate(
        user_id=current_user.id,
        product_id=product_id,
        market_id=market_id
    )
    try:
        result = crud.create_favorite(db, favorite_in)
        logger.info(f"Successfully created favorite: {result}")
        return result
    except Exception as e:
        logger.error(f"Error creating favorite: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}")
def delete_favorite(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Remove a product from favorites.
    """
    favorite = crud.get_favorite_by_user_and_product(db, current_user.id, product_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return crud.delete_favorite(db, favorite.id)

@router.get("/", response_model=List[schemas.Favorite])
def read_favorites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get user's favorite products.
    """
    logger.info(f"Getting favorites for user {current_user.id}")
    favorites = crud.get_favorites_by_user(db, current_user.id, skip, limit)
    logger.info(f"Found {len(favorites)} favorites")
    return favorites

@router.get("/check/{product_id}")
def check_favorite(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Check if a product is in user's favorites.
    """
    favorite = crud.get_favorite_by_user_and_product(db, current_user.id, product_id)
    return {"is_favorite": favorite is not None} 