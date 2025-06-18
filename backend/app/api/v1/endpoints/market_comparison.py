from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api import deps
from app.models.shopping_list import ShoppingListItem
from pydantic import BaseModel

router = APIRouter()

class MarketComparisonResponse(BaseModel):
    market_id: int
    market_name: str
    total_price: float
    items: List[dict]
    found_products: int
    total_products: int
    
    class Config:
        from_attributes = True

@router.get("/test")
def test_endpoint():
    """
    Test endpoint to check if router is working.
    """
    return {"message": "Market comparison router is working!"}

@router.get("/{shopping_list_id}/markets", response_model=List[MarketComparisonResponse])
def get_markets_for_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_id: int,
):
    """
    Alışveriş listesindeki ürünleri satan marketleri getir.
    """
    # 1. Alışveriş listesindeki ürünleri al
    items = db.query(ShoppingListItem).filter(
        ShoppingListItem.shopping_list_id == shopping_list_id
    ).all()
    
    if not items:
        return []
    
    # 2. Bu ürünleri satan marketleri bul
    product_ids = [item.product_id for item in items]
    
    # 3. SQL ile marketleri çek
    query = text("""
        SELECT DISTINCT m.id, m.name
        FROM shopping_list_items sli
        JOIN product_details pd ON sli.product_id = pd.product_id
        JOIN markets m ON pd.market_id = m.id
        WHERE sli.shopping_list_id = :list_id
    """)
    
    result = db.execute(query, {"list_id": shopping_list_id})
    markets = result.fetchall()
    
    comparisons = []
    
    for market in markets:
        # 4. Her market için fiyat hesapla
        price_query = text("""
            SELECT p.name, sli.quantity, pd.price
            FROM shopping_list_items sli
            JOIN product_details pd ON sli.product_id = pd.product_id
            JOIN products p ON sli.product_id = p.id
            WHERE sli.shopping_list_id = :list_id AND pd.market_id = :market_id
        """)
        
        price_result = db.execute(price_query, {
            "list_id": shopping_list_id,
            "market_id": market.id
        })
        
        items_list = []
        total_price = 0
        
        for row in price_result:
            item_price = float(row.price) * row.quantity
            total_price += item_price
            
            items_list.append({
                "product_id": 0,
                "product_name": row.name,
                "price": float(row.price),
                "quantity": row.quantity
            })
        
        comparisons.append({
            "market_id": market.id,
            "market_name": market.name,
            "total_price": total_price,
            "items": items_list,
            "found_products": len(items_list),
            "total_products": len(items)
        })
    
    # 5. Fiyata göre sırala
    comparisons.sort(key=lambda x: x["total_price"])
    
    return comparisons 