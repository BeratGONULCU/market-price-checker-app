from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.comment import Comment
from app.schemas.comment import Comment as CommentSchema, CommentCreate, CommentUpdate

router = APIRouter()

@router.post("/", response_model=CommentSchema)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/", response_model=List[CommentSchema])
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = db.query(Comment).offset(skip).limit(limit).all()
    return comments

@router.get("/{comment_id}", response_model=CommentSchema)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    for key, value in comment.dict(exclude_unset=True).items():
        setattr(db_comment, key, value)
    
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/{comment_id}", response_model=CommentSchema)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    db.delete(db_comment)
    db.commit()
    return db_comment 