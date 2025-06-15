from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import ShoppingList, ShoppingListItem, User
from schemas import ShoppingListCreate, ShoppingList as ShoppingListSchema, ShoppingListItemCreate, ShoppingListItem as ShoppingListItemSchema
from auth import get_current_user

router = APIRouter(
    prefix="/shopping-lists",
    tags=["shopping-lists"]
)

@router.get("/", response_model=List[ShoppingListSchema])
def get_shopping_lists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lists = db.query(ShoppingList).filter(ShoppingList.user_id == current_user.id).all()
    return lists

@router.post("/", response_model=ShoppingListSchema)
def create_shopping_list(
    list_data: ShoppingListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_list = ShoppingList(
        name=list_data.name,
        user_id=current_user.id
    )
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.get("/{list_id}", response_model=ShoppingListSchema)
def get_shopping_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.user_id == current_user.id
    ).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return db_list

@router.delete("/{list_id}")
def delete_shopping_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.user_id == current_user.id
    ).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    db.delete(db_list)
    db.commit()
    return {"message": "Shopping list deleted successfully"}

@router.post("/{list_id}/items", response_model=ShoppingListItemSchema)
def add_item_to_list(
    list_id: int,
    item_data: ShoppingListItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.user_id == current_user.id
    ).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")

    db_item = ShoppingListItem(
        shopping_list_id=list_id,
        product_id=item_data.product_id,
        quantity=item_data.quantity,
        notes=item_data.notes
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{list_id}/items/{item_id}")
def delete_item_from_list(
    list_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.user_id == current_user.id
    ).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")

    db_item = db.query(ShoppingListItem).filter(
        ShoppingListItem.id == item_id,
        ShoppingListItem.shopping_list_id == list_id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"} 