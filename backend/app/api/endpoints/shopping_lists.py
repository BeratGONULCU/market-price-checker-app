from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=schemas.ShoppingListInDB)
def create_shopping_list(
    shopping_list: schemas.ShoppingListCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Yeni bir alışveriş listesi oluştur.
    """
    return crud.create_shopping_list(db, shopping_list, current_user.id)

@router.get("/", response_model=List[schemas.ShoppingListInDB])
def read_shopping_lists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Kullanıcının alışveriş listelerini getir.
    """
    return crud.get_shopping_lists_by_user(db, current_user.id, skip, limit)

@router.get("/{shopping_list_id}", response_model=schemas.ShoppingListInDB)
def read_shopping_list(
    shopping_list_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Belirli bir alışveriş listesini getir.
    """
    shopping_list = crud.get_shopping_list(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return shopping_list

@router.put("/{shopping_list_id}", response_model=schemas.ShoppingListInDB)
def update_shopping_list(
    shopping_list_id: int,
    shopping_list: schemas.ShoppingListUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Alışveriş listesini güncelle.
    """
    db_shopping_list = crud.get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.update_shopping_list(db, shopping_list_id, shopping_list)

@router.delete("/{shopping_list_id}")
def delete_shopping_list(
    shopping_list_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Alışveriş listesini sil.
    """
    db_shopping_list = crud.get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if crud.delete_shopping_list(db, shopping_list_id):
        return {"message": "Shopping list deleted successfully"}
    raise HTTPException(status_code=500, detail="Error deleting shopping list")

@router.post("/{shopping_list_id}/items", response_model=schemas.ShoppingListItemInDB)
def create_shopping_list_item(
    shopping_list_id: int,
    item: schemas.ShoppingListItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Alışveriş listesine yeni ürün ekle.
    """
    db_shopping_list = crud.get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.create_shopping_list_item(db, item, shopping_list_id)

@router.put("/items/{item_id}", response_model=schemas.ShoppingListItemInDB)
def update_shopping_list_item(
    item_id: int,
    item: schemas.ShoppingListItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Alışveriş listesindeki bir ürünü güncelle.
    """
    db_item = crud.get_shopping_list_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_shopping_list = crud.get_shopping_list(db, db_item.shopping_list_id)
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.update_shopping_list_item(db, item_id, item)

@router.delete("/items/{item_id}")
def delete_shopping_list_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Alışveriş listesinden bir ürünü sil.
    """
    db_item = crud.get_shopping_list_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_shopping_list = crud.get_shopping_list(db, db_item.shopping_list_id)
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if crud.delete_shopping_list_item(db, item_id):
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=500, detail="Error deleting item") 