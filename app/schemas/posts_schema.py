from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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

