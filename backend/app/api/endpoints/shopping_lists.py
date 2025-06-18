from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, crud
from app.api import deps
from app.schemas.shopping_list import (
    ShoppingList,
    ShoppingListCreate,
    ShoppingListUpdate,
    ShoppingListItemInDB,
    ShoppingListItemCreate,
    ShoppingListItemUpdate
)
from app.crud.crud_shopping_list import (
    create_shopping_list,
    get_shopping_lists_by_user,
    get_shopping_list,
    update_shopping_list,
    delete_shopping_list,
    create_shopping_list_item
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=ShoppingList)
def create_shopping_list_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_in: ShoppingListCreate,
) -> Any:
    """
    Create new shopping list.
    """
    try:
        logger.info("=== Shopping List Creation Request ===")
        logger.info(f"Raw request data: {shopping_list_in.dict()}")
        
        # Create shopping list with default user_id=1
        result = create_shopping_list(
            db=db,
            shopping_list=shopping_list_in
        )
        
        logger.info(f"Successfully created shopping list with ID: {result.id}")
        return result
        
    except Exception as e:
        logger.error("=== Error Creating Shopping List ===")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error(f"Request data: {shopping_list_in.dict() if hasattr(shopping_list_in, 'dict') else shopping_list_in}")
        logger.error("===================================")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating shopping list: {str(e)}"
        )

@router.get("/", response_model=List[ShoppingList])
def read_shopping_lists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Kullanıcının alışveriş listelerini getir.
    """
    return get_shopping_lists_by_user(db, current_user.id, skip, limit)

@router.get("/{shopping_list_id}", response_model=ShoppingList)
def read_shopping_list(
    shopping_list_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Belirli bir alışveriş listesini getir.
    """
    shopping_list = get_shopping_list(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return shopping_list

@router.put("/{shopping_list_id}", response_model=ShoppingList)
def update_shopping_list_endpoint(
    shopping_list_id: int,
    shopping_list: ShoppingListUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Alışveriş listesini güncelle.
    """
    db_shopping_list = get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return update_shopping_list(db, shopping_list_id, shopping_list)

@router.delete("/{shopping_list_id}")
def delete_shopping_list_endpoint(
    shopping_list_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Alışveriş listesini sil.
    """
    db_shopping_list = get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if delete_shopping_list(db, shopping_list_id):
        return {"message": "Shopping list deleted successfully"}
    raise HTTPException(status_code=500, detail="Error deleting shopping list")

@router.post("/{shopping_list_id}/items", response_model=ShoppingListItemInDB)
def create_shopping_list_item_endpoint(
    shopping_list_id: int,
    item: ShoppingListItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Alışveriş listesine yeni ürün ekle.
    """
    db_shopping_list = get_shopping_list(db, shopping_list_id)
    if not db_shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    if db_shopping_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return create_shopping_list_item(
        db=db,
        shopping_list_id=shopping_list_id,
        product_id=item.product_id,
        quantity=item.quantity,
        notes=item.notes
    )

@router.put("/items/{item_id}", response_model=ShoppingListItemInDB)
def update_shopping_list_item(
    item_id: int,
    item: ShoppingListItemUpdate,
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