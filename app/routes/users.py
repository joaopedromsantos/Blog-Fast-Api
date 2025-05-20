from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from dependencies.db import get_session
from app.models.users import Users
from app.repositories.jwt_repo import JWTRepo
from app.repositories.user_repo import UserRepo
from app.schemas.authentication_scheme import RegisterSchema, ResponseLoginSchema
from app.schemas.base_schema import ResponseSchema

router = APIRouter(
    tags=['Authentication']
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/signup', status_code=HTTPStatus.CREATED)
async def signup(
        request: RegisterSchema,
        db: Session = Depends(get_session)
):
    existing_user = UserRepo.find_by_username(db, request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    existing_email = UserRepo.find_by_email(db, request.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    user = Users(
        username=request.username,
        email=request.email,
        password=pwd_context.hash(request.password),
        phone_number=request.phone_number,
        first_name=request.first_name,
        last_name=request.last_name,
        gender=request.gender,
    )

    UserRepo.insert(db, user)
    return ResponseSchema(
        code=status.HTTP_201_CREATED,
        status="Success",
        message="User registered successfully",
        result={"username": user.username, "email": user.email}
    )


@router.post('/login', status_code=HTTPStatus.OK)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_session)
):
    user = UserRepo.find_by_username(db, form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Password"
        )

    token = JWTRepo.generate_token(user)

    return ResponseLoginSchema(access_token=token, token_type='bearer')

