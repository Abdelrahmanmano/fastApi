from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, hashing
from ..database import get_db
from ..repository import user
router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/create_user", status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)

@router.get("/users", response_model=List[schemas.ShowUser], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    return user.get_users(db)

@router.get("/user/{id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db)

@router.delete("/delete_user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    return user.delete_user(id, db)