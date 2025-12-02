from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"data": "blog list", "Hi": "There"}

# @app.get("/blog")
# def read_blogs(page: Optional[int] = 1, page_size: Optional[int] = 10):
#     return {"page": page, "page_size": page_size, "blogs": "List of blogs."}

@app.get("/blog")
def index(limit: Optional[int]=10, published: Optional[bool]=False, sort: Optional[str]=None):
    if published:
        return {"data": f"{limit} published blogs from the db is sorted in {sort} order"}
    else:
        return {"data": f"{limit} blogs from the db is sorted in {sort} order"}

@app.get("/blog/unpublished")
def read_unpublished_blogs():
    return {"Unpublished Blogs": "List of unpublished blogs."}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/about")
def read_about():
    return {"About": "This is a sample FastAPI application."}

@app.get("/blog/{blog_id}")
def read_blog_data(blog_id: int):
    return {"Blog": f"This is blog data for blog ID {blog_id}."}

@app.get("/blog/{blog_id}/comments/{comment_id}")
def read_blog_comment(blog_id: int, comment_id: int):
    return {"blog_id": blog_id, "comment_id": comment_id}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = False
