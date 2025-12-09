from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime, func, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True')
    rating = Column(Float, nullable=True, server_default='0')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    phone_number = Column(Integer, nullable=True)
    
class Likes(Base):
    __tablename__ = "likes"
    
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    
    
class Comments(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)