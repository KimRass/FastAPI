from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PostCreate(BaseModel):
    writer: str
    title: str
    content: str


class PostRead(BaseModel):
    post_id: Optional[int] = None
    writer: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
