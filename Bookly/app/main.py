from typing import List
from fastapi import FastAPI, HTTPException, status, Depends
from . import models
from .database import engine, get_db
from .schemas import Post, ResponsePost, CreatePost, UpdatePost, User, UserCreate
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hashing:
    @staticmethod
    def bcrypt(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str):
        return pwd_context.verify(plain_password, hashed_password)
    
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


  
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

@app.get("/")
def read_root():
    return {"Hello": "welcome to FastAPI Posts"}

@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[ResponsePost])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/latest", status_code=status.HTTP_200_OK)
def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return post

@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=ResponsePost)
def get_post(id: int, db: Session = Depends(get_db)):
    post = find_post(db=db, id=id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to get")

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=CreatePost)
def create_post(post: Post, db: Session = Depends(get_db)):
    post = models.Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return {"message": "post deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to delete")

@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=UpdatePost)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    stored_post = query.first()
    if stored_post:
        query.update(post.model_dump(exclude_unset=True), synchronize_session=False)
        db.commit()
        return query.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to update")

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserCreate)
def create_user(user: User, db: Session = Depends(get_db)):
    hashed_password = Hashing.bcrypt(user.password[:70])
    print(hashed_password, 'heree')
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user