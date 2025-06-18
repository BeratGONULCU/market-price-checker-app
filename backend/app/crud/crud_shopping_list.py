from typing import List, Optional
import logging
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.shopping_list import ShoppingList, ShoppingListItem
from app.schemas.shopping_list import ShoppingListCreate, ShoppingListUpdate, ShoppingListItemCreate, ShoppingListItemUpdate
import secrets

logger = logging.getLogger(__name__)

def create_shopping_list(
    db: Session,
    shopping_list: ShoppingListCreate,
    user_id: int = 1
) -> ShoppingList:
    """
    Create new shopping list.
    """
    try:
        logger.info(f"Creating shopping list for user {user_id}")
        logger.info(f"Shopping list data: {shopping_list}")
        
        # Create shopping list
        db_obj = ShoppingList(
            name=shopping_list.name,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        logger.info(f"Created shopping list with ID: {db_obj.id}")
        return db_obj
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating shopping list: {str(e)}", exc_info=True)
        raise

def get_shopping_list(
    db: Session,
    shopping_list_id: int
) -> Optional[ShoppingList]:
    """
    Get shopping list by ID.
    """
    return db.query(ShoppingList).filter(ShoppingList.id == shopping_list_id).first()

def get_shopping_lists_by_user(
    db: Session,
    user_id: int = 1,
    skip: int = 0,
    limit: int = 100
) -> List[ShoppingList]:
    """
    Get all shopping lists for a user.
    """
    return (
        db.query(ShoppingList)
        .filter(ShoppingList.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_shopping_list(
    db: Session,
    shopping_list_id: int,
    shopping_list_update: ShoppingListUpdate
) -> Optional[ShoppingList]:
    """
    Update shopping list.
    """
    try:
        logger.info(f"Updating shopping list {shopping_list_id}")
        logger.info(f"Update data: {shopping_list_update}")
        
        db_obj = get_shopping_list(db, shopping_list_id)
        if not db_obj:
            return None
            
        # Update shopping list
        update_data = shopping_list_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        logger.info(f"Updated shopping list: {db_obj}")
        return db_obj
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating shopping list: {str(e)}", exc_info=True)
        raise

def delete_shopping_list(
    db: Session,
    shopping_list_id: int
) -> bool:
    """
    Delete shopping list.
    """
    try:
        db_obj = get_shopping_list(db, shopping_list_id)
        if not db_obj:
            return False
            
        db.delete(db_obj)
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting shopping list: {str(e)}", exc_info=True)
        raise

def create_shopping_list_item(
    db: Session,
    shopping_list_id: int,
    product_id: int,
    quantity: int,
    notes: Optional[str] = None
) -> ShoppingListItem:
    """
    Create new shopping list item.
    """
    try:
        logger.info(f"Creating shopping list item for list {shopping_list_id}")
        logger.info(f"Item data: product_id={product_id}, quantity={quantity}, notes={notes}")
        
        # Create shopping list item
        db_obj = ShoppingListItem(
            shopping_list_id=shopping_list_id,
            product_id=product_id,
            quantity=quantity,
            notes=notes,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Load the product information
        from sqlalchemy.orm import joinedload
        db_obj = db.query(ShoppingListItem).options(
            joinedload(ShoppingListItem.product)
        ).filter(ShoppingListItem.id == db_obj.id).first()
        
        logger.info(f"Created shopping list item with ID: {db_obj.id}")
        return db_obj
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating shopping list item: {str(e)}", exc_info=True)
        raise

def get_shopping_list_item(
    db: Session,
    item_id: int
) -> Optional[ShoppingListItem]:
    """
    Belirli bir alışveriş listesi ürününü getir.
    """
    return db.query(ShoppingListItem).filter(ShoppingListItem.id == item_id).first()

def update_shopping_list_item(
    db: Session,
    item_id: int,
    item: ShoppingListItemUpdate
) -> Optional[ShoppingListItem]:
    """
    Alışveriş listesindeki bir ürünü güncelle.
    """
    db_item = get_shopping_list_item(db, item_id)
    if db_item:
        for key, value in item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_shopping_list_item(
    db: Session,
    item_id: int
) -> bool:
    """
    Alışveriş listesinden bir ürünü sil.
    """
    db_item = get_shopping_list_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

def generate_share_token(
    db: Session,
    shopping_list_id: int
) -> str:
    """
    Generate share token for shopping list.
    """
    token = secrets.token_urlsafe(32)
    return token 