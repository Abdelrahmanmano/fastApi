from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    content: Optional[str] = 'No content provided'
    published: bool = True
    rating: Optional[int] = None

class CreatePost(Post):
    created_at: datetime

class ResponsePost(BaseModel):
    title: str
    author: str
    class Config:
        from_attributes = True
        
class UpdatePost(ResponsePost):
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class User(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True
        
class UserCreate(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True