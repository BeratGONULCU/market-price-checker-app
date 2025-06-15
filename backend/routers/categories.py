from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Category
from schemas import CategoryCreate, Category as CategorySchema

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

@router.post("/", response_model=CategorySchema)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(
        name=category.name,
        description=category.description,
        parent_id=category.parent_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/{category_id}", response_model=CategorySchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Prevent circular references
    if category.parent_id == category_id:
        raise HTTPException(
            status_code=400,
            detail="A category cannot be its own parent"
        )

    # Check if the new parent exists
    if category.parent_id:
        parent = db.query(Category).filter(Category.id == category.parent_id).first()
        if not parent:
            raise HTTPException(
                status_code=400,
                detail="Parent category not found"
            )

    db_category.name = category.name
    db_category.description = category.description
    db_category.parent_id = category.parent_id

    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if category has children
    has_children = db.query(Category).filter(Category.parent_id == category_id).first()
    if has_children:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with subcategories"
        )

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"} 