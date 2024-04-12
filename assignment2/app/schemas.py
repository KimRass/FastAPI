from datetime import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    writer: str
    title: str
    content: str


class Post(PostCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: str
    content: str
