from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.shopping_list import ShoppingList, ShoppingListItem
from app.schemas.shopping_list import ShoppingListCreate, ShoppingListItemCreate
import secrets

def create_shopping_list(
    db: Session,
    obj_in: ShoppingListCreate,
    user_id: int
) -> ShoppingList:
    """
    Yeni bir alışveriş listesi oluştur.
    """
    db_obj = ShoppingList(
        name=obj_in.name,
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_shopping_list(
    db: Session,
    shopping_list_id: int,
    user_id: int
) -> Optional[ShoppingList]:
    """
    Belirli bir alışveriş listesini getir.
    """
    return db.query(ShoppingList).filter(
        ShoppingList.id == shopping_list_id,
        ShoppingList.user_id == user_id
    ).first()

def get_user_shopping_lists(
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

def add_item_to_shopping_list(
    db: Session,
    shopping_list_id: int,
    item_in: ShoppingListItemCreate
) -> ShoppingListItem:
    """
    Alışveriş listesine yeni ürün ekle.
    """
    db_obj = ShoppingListItem(
        shopping_list_id=shopping_list_id,
        product_id=item_in.product_id,
        quantity=item_in.quantity,
        is_checked=item_in.is_checked
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_shopping_list_item(
    db: Session,
    item_id: int
) -> Optional[ShoppingListItem]:
    """
    Belirli bir alışveriş listesi ürününü getir.
    """
    return db.query(ShoppingListItem).filter(
        ShoppingListItem.id == item_id
    ).first()

def update_shopping_list_item(
    db: Session,
    item_id: int,
    item_in: ShoppingListItemCreate
) -> Optional[ShoppingListItem]:
    """
    Alışveriş listesindeki bir ürünü güncelle.
    """
    db_obj = get_shopping_list_item(db, item_id)
    if db_obj:
        for field, value in item_in.dict().items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    return db_obj

def delete_shopping_list_item(
    db: Session,
    item_id: int
) -> None:
    """
    Alışveriş listesinden bir ürünü sil.
    """
    db_obj = get_shopping_list_item(db, item_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()

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