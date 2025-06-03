from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.shopping_list_item import ShoppingListItem
from app.schemas.shopping_list_item import ShoppingListItem as ShoppingListItemSchema, ShoppingListItemCreate, ShoppingListItemUpdate

router = APIRouter()

@router.post("/", response_model=ShoppingListItemSchema)
def create_shopping_list_item(shopping_list_item: ShoppingListItemCreate, db: Session = Depends(get_db)):
    # Check if item already exists in user's shopping list
    existing_item = db.query(ShoppingListItem).filter(
        ShoppingListItem.user_id == shopping_list_item.user_id,
        ShoppingListItem.product_id == shopping_list_item.product_id
    ).first()
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already in shopping list"
        )
    
    db_shopping_list_item = ShoppingListItem(**shopping_list_item.dict())
    db.add(db_shopping_list_item)
    db.commit()
    db.refresh(db_shopping_list_item)
    return db_shopping_list_item

@router.get("/user/{user_id}", response_model=List[ShoppingListItemSchema])
def read_user_shopping_list_items(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shopping_list_items = db.query(ShoppingListItem).filter(
        ShoppingListItem.user_id == user_id
    ).offset(skip).limit(limit).all()
    return shopping_list_items

@router.get("/{shopping_list_item_id}", response_model=ShoppingListItemSchema)
def read_shopping_list_item(shopping_list_item_id: int, db: Session = Depends(get_db)):
    db_shopping_list_item = db.query(ShoppingListItem).filter(ShoppingListItem.id == shopping_list_item_id).first()
    if db_shopping_list_item is None:
        raise HTTPException(status_code=404, detail="Shopping list item not found")
    return db_shopping_list_item

@router.put("/{shopping_list_item_id}", response_model=ShoppingListItemSchema)
def update_shopping_list_item(shopping_list_item_id: int, shopping_list_item: ShoppingListItemUpdate, db: Session = Depends(get_db)):
    db_shopping_list_item = db.query(ShoppingListItem).filter(ShoppingListItem.id == shopping_list_item_id).first()
    if db_shopping_list_item is None:
        raise HTTPException(status_code=404, detail="Shopping list item not found")
    
    for key, value in shopping_list_item.dict(exclude_unset=True).items():
        setattr(db_shopping_list_item, key, value)
    
    db.commit()
    db.refresh(db_shopping_list_item)
    return db_shopping_list_item

@router.delete("/{shopping_list_item_id}", response_model=ShoppingListItemSchema)
def delete_shopping_list_item(shopping_list_item_id: int, db: Session = Depends(get_db)):
    db_shopping_list_item = db.query(ShoppingListItem).filter(ShoppingListItem.id == shopping_list_item_id).first()
    if db_shopping_list_item is None:
        raise HTTPException(status_code=404, detail="Shopping list item not found")
    
    db.delete(db_shopping_list_item)
    db.commit()
    return db_shopping_list_item 