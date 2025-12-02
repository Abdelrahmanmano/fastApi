from typing import List
from fastapi import APIRouter, FastAPI, Depends, status, Response
from .. import schemas, models, hashing, oauth2
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import blog
router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)



@router.post("/create_blog", tags=["Blogs"], status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create_blog(request, db)

@router.get("/get_blogs", status_code=status.HTTP_201_CREATED, response_model=List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/get_blog/{id}", response_model=schemas.ShowBlog)
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    return blog.get_blog(id, response, db)

@router.delete("/delete_blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return blog.delete_blog(id, db)

@router.put("/update_blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update_blog(id, request, db)

