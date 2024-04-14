from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PostCreate(BaseModel):
    writer: str
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
