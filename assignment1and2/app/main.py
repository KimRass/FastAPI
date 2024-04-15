from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from .schemas import (
    UserCreate,
    UserRead,
    UserUpdate,
    PostCreate,
    PostRead,
    PostUpdate,
)
from .models import BASE, DBPost, DBUser
from .db import ENGINE, get_db
from logger import Logger

BASE.metadata.create_all(bind=ENGINE)

app = FastAPI()

logger = Logger(out_dir="./").get_logger()


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_dict = jsonable_encoder(user)
        db_user = DBUser(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        msg = f"User created; {user}"
        logger.info(msg)
        return db_user
    except IntegrityError as e:
        db.rollback()
        msg = f"Email address already exists!; '{user.email_addr}'"
        logger.warning(msg)
        raise HTTPException(status_code=400, detail=e)


@app.get("/users")
def read_users(user: UserRead, db: Session = Depends(get_db)):
    query = db.query(DBUser)
    filters = list()
    if user.user_id is not None:
        filters.append(DBUser.id == user.user_id)
    if user.name is not None:
        filters.append(DBUser.name == user.name)
    if user.email_addr is not None:
        filters.append(DBUser.email_addr == user.email_addr)
    if filters:
        query = query.filter(and_(*filters))

    db_post = query.all()
    if not db_post:
        msg = f"User not found!; {user}"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)
    msg = f"Retrieved users; {user}"
    logger.info(msg)
    return db_post


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        msg = f"User not found!; {user}"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    if user.name:
        db_user.name = user.name
    if user.email_addr:
        db_user.email_addr = user.email_addr

    try:
        db.commit()
        db.refresh(db_user)
    # except Exception as e:
    #     db.rollback()
    #     msg = f"Failed to update user; {user}"
    #     logger.warning(msg)
    #     raise HTTPException(status_code=500, detail=e)
    except IntegrityError as e:
        db.rollback()
        msg = f"Email address already exists!; '{user.email_addr}'"
        logger.warning(msg)
        raise HTTPException(status_code=400, detail=f"{e}")
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == post.user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {post.user_id} not found!",
        )

    post_dict = jsonable_encoder(post)
    db_post = DBPost(**post_dict)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/posts")
def read_posts(post: PostRead, db: Session = Depends(get_db)):
    query = db.query(DBPost)
    filters = list()
    if post.post_id is not None:
        filters.append(DBPost.id == post.post_id)
    if post.user_id is not None:
        filters.append(DBPost.user_id == post.user_id)
    if post.title is not None:
        filters.append(DBPost.title == post.title)
    if post.content is not None:
        filters.append(DBPost.content == post.content)
    if filters:
        query = query.filter(and_(*filters))

    db_post = query.all()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found!")
    return db_post


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="404 Not Found: Post not found!")

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
        raise HTTPException(status_code=500, detail=f"Failed to update post!:\n{e}")
    return db_post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="404 Not Found: Post not found!")

    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully."}
