from typing import List
from fastapi import HTTPException, status, Depends, APIRouter
from .. import models
from ..database import  get_db
from ..schemas import Post, ResponsePost, CreatePost, UpdatePost
from sqlalchemy.orm import Session
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

def find_post(id, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    return None

def del_post(id, db: Session=Depends(get_db)):
    post = find_post(id, db)
    if post:
        db.delete(post)
        db.commit()
        return True
    return False

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ResponsePost])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/latest", status_code=status.HTTP_200_OK)
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return post

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponsePost)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = find_post(db=db, id=id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to get")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreatePost)
def create_post(post: Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = models.Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return {"message": "post deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to delete")

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UpdatePost)
def update_post(id: int, post: Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    stored_post = query.first()
    if stored_post:
        query.update(post.model_dump(exclude_unset=True), synchronize_session=False)
        db.commit()
        return query.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to update")
