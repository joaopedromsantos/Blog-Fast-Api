from typing import Optional, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class ResponseSchema(BaseModel):
    code: int
    status: str
    message: str
    result: Optional[T] = None
