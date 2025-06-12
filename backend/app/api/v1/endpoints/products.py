from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.product import PriceHistory
from backend.crud.product import get_price_history
from backend.api.deps import get_db

router = APIRouter()

@router.get("/{product_id}/price-history", response_model=List[PriceHistory])
def get_product_price_history(
    product_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> List[PriceHistory]:
    """
    Bir ürünün fiyat geçmişini getir.
    """
    price_history = get_price_history(
        db=db, product_id=product_id, skip=skip, limit=limit
    )
    return price_history 