from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, HttpUrl


class InsertPostsSchema(BaseModel):
    title: str
    author_id: int
    cover_image_url: str = None
    content: str


class UpdatePostsSchema(BaseModel):
    id: int
    title: str = None
    author_id: int = None
    cover_image_url: str = None
    content: str = None


class DeletePostsSchema(BaseModel):
    id: int


class GetPostsSchema(BaseModel):
    id: int
    title: str
    author_id: int
    cover_image_url: str
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
