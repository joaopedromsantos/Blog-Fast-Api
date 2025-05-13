from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, HttpUrl


class InsertPostsSchema(BaseModel):
    title: str
    author_id: int
    cover_image_url: Optional[str] = None
    content: str


class UpdatePostsSchema(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    cover_image_url: Optional[str] = None
    content: Optional[str] = None


class GetPostsSchema(BaseModel):
    id: int
    title: str
    author_id: int
    cover_image_url: Optional[str] = None
    content: str
    create_date: datetime
    update_date: datetime

    class Config:
        model_config = {'from_attributes': True}


class PostsResponseSchema(BaseModel):
    code: int
    status: str
    message: str
    result: List[GetPostsSchema] = []
