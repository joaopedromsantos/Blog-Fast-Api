from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.models.users import Users
from app.utils import s3_utils
from dependencies.db import get_session
from dependencies.auth import get_current_user_dependency, get_admin_user_dependency
from exceptions.http_exceptions import NOT_FOUND_EXCEPTION, FORBIDDEN_EXCEPTION
from app.models.posts import Posts
from app.repositories.posts_repo import PostsRepo
from app.schemas.base_schema import ResponseSchema
from app.schemas.posts_schema import GetPostsSchema

router = APIRouter(
    tags=['Posts']
)


@router.post("/posts", status_code=HTTPStatus.CREATED)
async def create_post(
    title: str = Form(...),
    author_id: int = Form(...),
    content: str = Form(...),
    cover_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user_dependency)
):
    image_url = None
    if cover_image:
        image_url = s3_utils.upload_image_to_s3(cover_image)

    new_post = Posts(
        title=title,
        author_id=author_id,
        cover_image_url=image_url,
        content=content
    )

    PostsRepo.insert(db, new_post)
    return ResponseSchema(
        code=status.HTTP_201_CREATED,
        status="Success",
        message="Post created successfully",
        result={
            "id": new_post.id,
            "title": new_post.title,
            "author_id": new_post.author_id
        }
    )


@router.delete("/posts/{post_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user_dependency)
):
    post = PostsRepo.find_by_id(db, post_id)
    if post is None:
        raise NOT_FOUND_EXCEPTION

    if current_user.role != "admin" and post.author_id != current_user.id:
        raise FORBIDDEN_EXCEPTION

    PostsRepo.delete(db, post)
    if post.cover_image_url:
        s3_utils.delete_s3_file(post.cover_image_url)

    return ResponseSchema(
        code=status.HTTP_204_NO_CONTENT,
        status="Success",
        message="Post deleted successfully"
    )


@router.get("/posts", status_code=HTTPStatus.OK)
def get_posts(
    post_id: int = None,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user_dependency),
    skip: int = 0,
    limit: int = 10,
):
    if post_id:
        post = PostsRepo.find_by_id(db, post_id)
        if not post:
            raise NOT_FOUND_EXCEPTION
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="Success",
            message="Post retrieved successfully",
            result=GetPostsSchema.model_validate(post.__dict__)
        )
    else:
        posts = PostsRepo.find_all_paginated(db, skip=skip, limit=limit)
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="Success",
            message="All posts retrieved",
            result=[GetPostsSchema.model_validate(post.__dict__) for post in posts]
        )


@router.put("/posts/{post_id}", status_code=HTTPStatus.OK)
def update_posts(
        post_id: int,
        title: Optional[str] = Form(None),
        author_id: Optional[int] = Form(None),
        content: Optional[str] = Form(None),
        cover_image: Optional[UploadFile] = File(None),
        db: Session = Depends(get_session),
        current_user=Depends(get_current_user_dependency)
):
    post = PostsRepo.find_by_id(db, post_id)

    if not post:
        raise NOT_FOUND_EXCEPTION

    old_image_url = post.cover_image_url
    image_url = None
    if cover_image:
        image_url = s3_utils.upload_image_to_s3(cover_image)

    updated_post = PostsRepo.update(
        db=db,
        post=post,
        title=title,
        content=content,
        author_id=author_id,
        cover_image_url=image_url
    )

    if cover_image and old_image_url:
        s3_utils.delete_s3_file(old_image_url)

    return ResponseSchema(
        code=status.HTTP_200_OK,
        status="Success",
        message="Post updated successfully",
        result={
            "title": updated_post.title,
            "author_id": updated_post.author_id
        }
    )

