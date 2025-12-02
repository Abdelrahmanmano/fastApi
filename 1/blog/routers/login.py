# blog/routers/login.py

from datetime import timedelta
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from blog.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from .. import schemas, database, models, hashing
from sqlalchemy.orm import Session

# THIS LINE IS CRITICAL
router = APIRouter(
    prefix="/login", # Optional: defines the base URL for routes in this file
    tags=["Authentication"] # Optional: used for grouping in Swagger docs
)

# Example route defined using the 'router' object
@router.post('/')
def login_user(request: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    # your login logic here
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not hashing.Hashing.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expire_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}