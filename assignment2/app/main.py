from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from assignment2.app.schemas import PostCreate, PostRead, PostUpdate
from assignment2.app.models import BASE, DBPost, User
from assignment2.app.db import ENGINE, get_db

BASE.metadata.create_all(bind=ENGINE)

app = FastAPI()


@app.post("/posts/create_post")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post_dict = jsonable_encoder(post)
    db_post = DBPost(**post_dict)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/posts/read_posts")
def read_posts(post: PostRead, db: Session = Depends(get_db)):
    query = db.query(DBPost)
    filters = list()
    if post.post_id is not None:
        filters.append(DBPost.id == post.post_id)
    if post.writer is not None:
        filters.append(DBPost.writer == post.writer)
    if post.title is not None:
        filters.append(DBPost.title == post.title)
    if post.content is not None:
        filters.append(DBPost.content == post.content)
    if filters:
        query = query.filter(and_(*filters))

    db_post = query.all()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="404 Not Found: No post found.")

    if post.title:
        db_post.title = post.title
    if post.content:
        db_post.content = post.content
    if post.title or post.content:
        db_post.updated_at = datetime.now()

    try:
        db.commit()
        db.refresh(db_post)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update post:\n{e}")
    return db_post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="404 Not Found: No post found.")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}
