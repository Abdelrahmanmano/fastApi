from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    content: Optional[str] = 'No content provided'
    published: bool = True
    rating: Optional[int] = None
    
while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print(f"Database connection was successful connected to {connection.get_dsn_parameters()['dbname']}")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(3)
  
def find_post(id):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if post:
        return post
    return None

def del_post(id):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    connection.commit()
    if post:
        return True
    return False

@app.get("/")
def read_root():
    return {"Hello": "welcome to FastAPI Posts"}

@app.get("/posts", status_code=status.HTTP_200_OK)
def get_post():
    cursor.execute("SELECT * FROM posts")
    my_post = cursor.fetchall()
    return {"date": my_post}

@app.get("/posts/latest", status_code=status.HTTP_200_OK)
def get_latest_post():
    cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    my_post = cursor.fetchone()
    return {"latest_post": my_post}

@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    post = find_post(id)
    if post:
        return {"post": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to get")

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, author, content, published, rating) VALUES (%s, %s, %s, %s, %s) RETURNING *",
                   (post.title, post.author, post.content, post.published, post.rating))
    my_post = cursor.fetchone()
    connection.commit()
    return my_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    if del_post(id):
        return {"message": "post deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to delete")

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    stored_post = find_post(id)
    if stored_post:
        cursor.execute("UPDATE posts SET title = %s, author = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *",
                       (post.title, post.author, post.content, post.published, post.rating, str(id)))
        connection.commit()
        return {"message": "post updated successfully", "post": stored_post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to update")

@app.post("/posts/db", status_code=status.HTTP_201_CREATED)
def create_post_db(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, author=post.author, content=post.content, published=post.published, rating=post.rating)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/get/db", status_code=status.HTTP_200_OK)
def get_posts_db(db: Session = Depends(get_db)):
    print("here in all")
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts/db/{id}", status_code=status.HTTP_200_OK)
def get_post_db(id: int, db: Session = Depends(get_db)):
    print("here in one")
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return {"post": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to get from db")

@app.delete("/posts/db/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_db(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to delete from db")
    db.delete(post)
    db.commit()
    return {"message": "post deleted successfully from db"}

@app.put("/posts/db/{id}", status_code=status.HTTP_200_OK)
def update_post_db(id: int, post: Post, db: Session = Depends(get_db)):
    stored_post = db.query(models.Post).filter(models.Post.id == id).first()
    if stored_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found to update in db")
    stored_post.title = post.title
    stored_post.author = post.author
    stored_post.content = post.content
    stored_post.published = post.published
    stored_post.rating = post.rating
    db.commit()
    db.refresh(stored_post)
    return {"message": "post updated successfully in db", "post": stored_post}