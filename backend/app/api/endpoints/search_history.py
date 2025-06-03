from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.search_history import SearchHistory
from app.schemas.search_history import SearchHistoryCreate, SearchHistory as SearchHistorySchema

router = APIRouter()

@router.post("/", response_model=SearchHistorySchema)
def create_search_history(search_history: SearchHistoryCreate, db: Session = Depends(get_db)):
    db_search_history = SearchHistory(**search_history.model_dump())
    db.add(db_search_history)
    db.commit()
    db.refresh(db_search_history)
    return db_search_history

@router.get("/user/{user_id}", response_model=List[SearchHistorySchema])
def get_user_search_history(user_id: int, db: Session = Depends(get_db)):
    search_history = db.query(SearchHistory).filter(SearchHistory.user_id == user_id).all()
    return search_history

@router.get("/{search_history_id}", response_model=SearchHistorySchema)
def get_search_history(search_history_id: int, db: Session = Depends(get_db)):
    search_history = db.query(SearchHistory).filter(SearchHistory.id == search_history_id).first()
    if not search_history:
        raise HTTPException(status_code=404, detail="Search history not found")
    return search_history

@router.delete("/{search_history_id}")
def delete_search_history(search_history_id: int, db: Session = Depends(get_db)):
    search_history = db.query(SearchHistory).filter(SearchHistory.id == search_history_id).first()
    if not search_history:
        raise HTTPException(status_code=404, detail="Search history not found")
    
    db.delete(search_history)
    db.commit()
    return {"message": "Search history deleted successfully"} 