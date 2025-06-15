from typing import List, Optional
import logging
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.shopping_list import ShoppingList, ShoppingListItem
from app.schemas.shopping_list import ShoppingListCreate, ShoppingListUpdate, ShoppingListItemCreate, ShoppingListItemUpdate
import secrets

logger = logging.getLogger(__name__)

class CRUDShoppingList(CRUDBase[ShoppingList, ShoppingListCreate, ShoppingListUpdate]):
    def create_with_items(
        self, db: Session, *, obj_in: ShoppingListCreate, user_id: int
    ) -> ShoppingList:
        try:
            logger.info(f"Creating shopping list with items for user {user_id}")
            logger.info(f"Shopping list data: {obj_in}")
            
            # Create shopping list
            db_obj = ShoppingList(
                name=obj_in.name,
                user_id=user_id
            )
            db.add(db_obj)
            db.flush()  # Get the ID without committing
            
            # Create shopping list items
            if obj_in.items:
                for item in obj_in.items:
                    db_item = ShoppingListItem(
                        shopping_list_id=db_obj.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        notes=item.notes
                    )
                    db.add(db_item)
            
            db.commit()
            db.refresh(db_obj)
            
            logger.info(f"Created shopping list with items: {db_obj}")
            return db_obj
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating shopping list with items: {str(e)}", exc_info=True)
            raise

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[ShoppingList]:
        return (
            db.query(self.model)
            .filter(ShoppingList.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self, db: Session, *, db_obj: ShoppingList, obj_in: ShoppingListUpdate
    ) -> ShoppingList:
        try:
            logger.info(f"Updating shopping list {db_obj.id}")
            logger.info(f"Update data: {obj_in}")
            
            # Update shopping list
            update_data = obj_in.dict(exclude_unset=True)
            if "items" in update_data:
                del update_data["items"]
            
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            
            # Update items if provided
            if obj_in.items is not None:
                # Delete existing items
                db.query(ShoppingListItem).filter(
                    ShoppingListItem.shopping_list_id == db_obj.id
                ).delete()
                
                # Create new items
                for item in obj_in.items:
                    db_item = ShoppingListItem(
                        shopping_list_id=db_obj.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        notes=item.notes
                    )
                    db.add(db_item)
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            
            logger.info(f"Updated shopping list: {db_obj}")
            return db_obj
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating shopping list: {str(e)}", exc_info=True)
            raise

shopping_list = CRUDShoppingList(ShoppingList)

def create_shopping_list(
    db: Session,
    shopping_list: ShoppingListCreate,
    user_id: int
) -> ShoppingList:
    """
    Yeni bir alışveriş listesi oluştur.
    """
    db_shopping_list = ShoppingList(
        name=shopping_list.name,
        user_id=user_id
    )
    db.add(db_shopping_list)
    db.commit()
    db.refresh(db_shopping_list)
    return db_shopping_list

def get_shopping_list(
    db: Session,
    shopping_list_id: int
) -> Optional[ShoppingList]:
    """
    Belirli bir alışveriş listesini getir.
    """
    return db.query(ShoppingList).filter(ShoppingList.id == shopping_list_id).first()

def get_shopping_lists_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[ShoppingList]:
    """
    Kullanıcının alışveriş listelerini getir.
    """
    return db.query(ShoppingList).filter(
        ShoppingList.user_id == user_id
    ).offset(skip).limit(limit).all()

def update_shopping_list(
    db: Session,
    shopping_list_id: int,
    shopping_list: ShoppingListUpdate
) -> Optional[ShoppingList]:
    """
    Alışveriş listesini güncelle.
    """
    db_shopping_list = get_shopping_list(db, shopping_list_id)
    if db_shopping_list:
        for key, value in shopping_list.dict(exclude_unset=True).items():
            setattr(db_shopping_list, key, value)
        db.commit()
        db.refresh(db_shopping_list)
    return db_shopping_list

def delete_shopping_list(
    db: Session,
    shopping_list_id: int
) -> bool:
    """
    Alışveriş listesini sil.
    """
    db_shopping_list = get_shopping_list(db, shopping_list_id)
    if db_shopping_list:
        db.delete(db_shopping_list)
        db.commit()
        return True
    return False

def get_shopping_list_item(
    db: Session,
    item_id: int
) -> Optional[ShoppingListItem]:
    """
    Belirli bir alışveriş listesi ürününü getir.
    """
    return db.query(ShoppingListItem).filter(ShoppingListItem.id == item_id).first()

def create_shopping_list_item(
    db: Session,
    item: ShoppingListItemCreate,
    shopping_list_id: int
) -> ShoppingListItem:
    """
    Alışveriş listesine yeni ürün ekle.
    """
    db_item = ShoppingListItem(
        **item.dict(),
        shopping_list_id=shopping_list_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

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
    Alışveriş listesi için paylaşım token'ı oluştur.
    """
    token = secrets.token_urlsafe(32)
    # Token'ı veritabanında sakla veya cache'le
    return token 