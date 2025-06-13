from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.shopping_list import ShoppingList, ShoppingListItem
from app.schemas.shopping_list import ShoppingListCreate, ShoppingListUpdate, ShoppingListItemCreate, ShoppingListItemUpdate
import secrets

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