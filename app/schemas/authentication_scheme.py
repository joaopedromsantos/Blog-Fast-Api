from pydantic import BaseModel

from app.models.users import GenderEnum


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str

    first_name: str
    last_name: str
    gender: GenderEnum


class ResponseLoginSchema(BaseModel):
    access_token: str
    token_type: str

