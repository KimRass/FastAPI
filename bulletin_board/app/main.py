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
    CommentCreate,
    CommentUpdate,
)
from .models import BASE, DBUser, DBPost, DBComment
from .db import ENGINE, get_db
from logger import Logger

BASE.metadata.create_all(bind=ENGINE)

app = FastAPI()

logger = Logger(out_dir="./").get_logger()


@app.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_dict = jsonable_encoder(user)
        db_user = DBUser(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        msg = f"User created; {user}"
        logger.info(msg)
        return db_user
    except IntegrityError:
        db.rollback()
        msg = f"Duplicate attribute found; `{user}`"
        logger.warning(msg)
        raise HTTPException(status_code=400, detail=msg)
    except Exception:
        db.rollback()
        msg = f"Failed to create user; `{user}`"
        logger.warning(msg)
        raise HTTPException(status_code=500, detail=msg)


@app.get("/users")
async def read_users(user: UserRead, db: Session = Depends(get_db)):
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
        msg = f"User not found; `{user}`"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)
    msg = f"Retrieved users; {user}"
    logger.info(msg)
    return db_post


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        msg = f"User not found; `user_id={user_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    if user.name:
        db_user.name = user.name
    if user.email_addr:
        db_user.email_addr = user.email_addr

    try:
        db.commit()
        db.refresh(db_user)
        msg = f"User updated; `{user}`"
        logger.info(msg)
        return db_user
    except IntegrityError:
        db.rollback()
        msg = f"Duplicate attribute found; `{user}`"
        logger.warning(msg)
        raise HTTPException(status_code=400, detail=msg)
    except Exception:
        db.rollback()
        msg = f"Failed to update user; `{user}`"
        logger.warning(msg)
        raise HTTPException(status_code=500, detail=msg)


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        msg = f"User not found; `user_id={user_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    db.delete(db_user)
    try:
        db.commit()
        msg = f"User deleted; `user_id={user_id}`"
        logger.info(msg)
        return {"message": msg}
    except Exception:
        db.rollback()
        msg = f"Failed to update user; `user_id={user_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=500, detail=msg)


@app.post("/posts")
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == post.user_id).first()
    if db_user is None:
        msg = f"User not found; `user_id={post.user_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    post_dict = jsonable_encoder(post)
    db_post = DBPost(**post_dict)
    db.add(db_post)
    try:
        db.commit()
        db.refresh(db_post)
        msg = f"Post created; {post}"
        logger.info(msg)
        return db_post
    except Exception:
        db.rollback()
        msg = f"Failed to update post; `{post}`"
        logger.warning(msg)
        raise HTTPException(status_code=500, detail=msg)


@app.get("/posts")
async def read_posts(post: PostRead, db: Session = Depends(get_db)):
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
    if not db_post:
        msg = f"Post not found; {post}"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)
    return db_post


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post is None:
        msg = f"Post not found; `post_id={post_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    if post.title:
        db_post.title = post.title
    if post.content:
        db_post.content = post.content
    if post.title or post.content:
        db_post.updated_at = datetime.now()

    try:
        db.commit()
        db.refresh(db_post)
    except Exception:
        db.rollback()
        msg = f"Failed to update post; `{post}`"
        logger.warning(msg)
        raise HTTPException(status_code=500, detail=msg)
    return db_post


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post is None:
        msg = f"Post not found; `post_id={post_id}"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    db.delete(db_post)
    db.commit()
    msg = f"Post deleted; `post_id={post_id}`"
    logger.warning(msg)
    return {"message": msg}


@app.post("/comments/")
async def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == comment.user_id).first()
    if db_user is None:
        msg = f"User not found; `user_id={comment.user_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    db_post = db.query(DBPost).filter(DBPost.id == comment.post_id).first()
    if db_post is None:
        msg = f"Post not found; `post_id={comment.post_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    comment_dict = jsonable_encoder(comment)
    db_comment = DBComment(**comment_dict)
    db.add(db_comment)
    try:
        db.commit()
        db.refresh(db_comment)
        msg = f"Comment created; {comment}"
        logger.info(msg)
        return db_comment
    except Exception:
        db.rollback()
        msg = f"Failed to update comment; `{comment}`"
        logger.warning(msg)
        raise HTTPException(status_code=500, detail=msg)


@app.put("/comments/{comment_id}")
async def update_comment(
    comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db),
):
    db_comment = db.query(DBComment).filter(DBComment.id == comment_id).first()
    if db_comment is None:
        msg = f"Comment not found; `comment_id={comment_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)
    
    db_comment.content = comment.content

    try:
        db.commit()
        db.refresh(db_comment)
        msg = f"Comment updated; {comment}"
        logger.info(msg)
        return db_comment
    except Exception:
        db.rollback()
        msg = f"Failed to update comment; `{comment}`"
        logger.warning(msg)
        raise HTTPException(status_code=500, detail=msg)


@app.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(DBComment).filter(DBComment.id == comment_id).first()
    if db_comment is None:
        msg = f"Comment not found; `comment_id={comment_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    db.delete(db_comment)
    try:
        db.commit()
        msg = f"Comment deleted; `comment_id={comment_id}`"
        logger.info(msg)
        return {"message": msg}
    except Exception:
        db.rollback()
        msg = f"Failed to update comment; `comment_id={comment_id}`"
        logger.warning(msg)
        raise HTTPException(status_code=500, detail=msg)
