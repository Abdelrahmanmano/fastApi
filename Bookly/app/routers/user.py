from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from .. import models, utils
from ..database import get_db
from ..schemas import User, UserCreate, UserGet, UserUpdate
from sqlalchemy.orm import Session
from typing import List
from .. import oauth2

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

  
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreate)
def create_user(user: User, db: Session = Depends(get_db)):
    # hashed_password = hash_password(user.password)
    hashed_password = utils.hash_password(user.password)
    print(hashed_password, 'heree')
    user.password = hashed_password
    try:
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserGet])
def get_users(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} not found")

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UserGet)
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user_obj = db.query(models.User).filter(models.User.id == id)
    if user_obj.first():
        user_obj.update(user.model_dump(exclude_unset=True), synchronize_session=False)
        db.commit()
        return user_obj.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} not found to update")

