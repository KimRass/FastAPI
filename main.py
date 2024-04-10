# https://wikidocs.net/176224
# https://datamoney.tistory.com/359
# https://mopil.tistory.com/m/62

from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from datetime import datetime
from typing import List

from app.schemas import PostCreate, Post
from app.models import BASE, DBPost, User
from app.db import ENGINE, get_db

BASE.metadata.create_all(bind=ENGINE)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/post/create_post")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post_data = jsonable_encoder(post)
    db_post = DBPost(**post_data)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# @app.get("/posts/{post_id}", response_model=PostResponse)
# def read_post(post_id: int):
#     db = sess_loc()
#     db_post = db.query(Post).filter(Post.id == post_id).first()
#     if db_post is None:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return db_post


@app.get("/post/get_all_posts", response_model=List[Post])
def get_all_posts(db: Session = Depends(get_db)):
    return db.query(DBPost).all()


# @app.put("/posts/{post_id}", response_model=PostResponse)
# def update_post(post_id: int, post: PostUpdate):
#     db = sess_loc()
#     db_post = db.query(Post).filter(Post.id == post_id).first()
#     if db_post is None:
#         raise HTTPException(status_code=404, detail="Post not found")
#     for key, value in post.dict().items():
#         setattr(db_post, key, value)
#     db.commit()
#     db.refresh(db_post)
#     return db_post


# @app.delete("/posts/{post_id}")
# def delete_post(post_id: int):
#     db = sess_loc()
#     db_post = db.query(Post).filter(Post.id == post_id).first()
#     if db_post is None:
#         raise HTTPException(status_code=404, detail="Post not found")
#     db.delete(db_post)
#     db.commit()
#     return {"message": "Post deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
