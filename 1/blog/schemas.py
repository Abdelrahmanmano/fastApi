from pydantic import BaseModel
from typing import Optional, List


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = False
    user_id: Optional[int]
    
    class Config:
        orm_mode = True
        
class User(BaseModel):
    name: str
    email: str
    password: str
    
class ShowBlog(BaseModel):
    title: str
    body: str
    creator: Optional['ShowUser']

    class Config:
        orm_mode = True 
    
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[ShowBlog] = []

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None