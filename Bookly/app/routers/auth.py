from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, database, schemas, oauth2


router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentail: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentail.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_password(user_credentail.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    # return oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": oauth2.create_access_token(data={"user_id": user.id}), "token_type": "bearer"}

@router.post("/")
def auth(user_credentail: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentail.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_password(user_credentail.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    return {"token": oauth2.create_access_token(data={"user_id": user.id}), "token_type": "bearer"}
    
    