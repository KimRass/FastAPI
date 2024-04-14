# https://wikidocs.net/176224
# https://datamoney.tistory.com/359
# https://mopil.tistory.com/m/62
# https://fastapi.tiangolo.com/ko/tutorial/first-steps/

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from assignment2.app.schemas import PostCreate, PostUpdate
from assignment2.app.models import BASE, DBPost, User
from assignment2.app.db import ENGINE, get_db

BASE.metadata.create_all(bind=ENGINE)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/post/create_post")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post_dict = jsonable_encoder(post)
    db_post = DBPost(**post_dict)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


### 수정!!!!! 쿼리 스트링! URL에 데이터 노출!
@app.get("/post/read_posts")
def read_posts(
    post_id: int = Query(None),
    writer: str = Query(None),
    title: str = Query(None),
    content: str = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(DBPost)
    filters = list()
    if post_id is not None:
        filters.append(DBPost.id == post_id)
    if writer is not None:
        filters.append(DBPost.writer == writer)
    if title is not None:
        filters.append(DBPost.title == title)
    if content is not None:
        filters.append(DBPost.content == content)
    if filters:
        query = query.filter(and_(*filters))

    db_post = query.all()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


### 요청은 바디에 데이터를 담아서!! URL에 데이터 노출 x
@app.put("/post/{post_id}")
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="404 Not Found: No post found.")
    post_dict = jsonable_encoder(post)
    for key, value in post_dict.items():
        if key != "id" and value is not None:
            setattr(db_post, key, value)
    db_post.updated_at = datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post


@app.delete("/post/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="404 Not Found: No post found.")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
