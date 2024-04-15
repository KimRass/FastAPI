from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email_addr: str


class UserRead(BaseModel):
    user_id: Optional[int] = None
    name: Optional[str] = None
    email_addr: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email_addr: Optional[str] = None


class PostCreate(BaseModel):
    user_id: int
    title: str
    content: str


class PostRead(BaseModel):
    post_id: Optional[int] = None
    user_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
