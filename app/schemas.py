from datetime import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    writer: str
    title: str
    content: str


class Post(PostCreate):
    id: int
    # writer: str
    # title: str
    # content: str
    created_at: datetime
    
    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    title: str
    content: str
