from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from dependencies.db import get_db
from dependencies.auth import get_current_user_dependency
from exceptions.http_exceptions import NOT_FOUND_EXCEPTION
from app.models.posts import Posts
from app.repositories.posts_repo import PostsRepo
from app.schemas.base_schema import ResponseSchema
from app.schemas.posts_schema import InsertPostsSchema, DeletePostsSchema, GetPostsSchema, UpdatePostsSchema

router = APIRouter(
    tags=['Posts']
)


@router.post("/posts", status_code=HTTPStatus.CREATED)
def create_post(
        request: InsertPostsSchema,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user_dependency)
):
    new_post = Posts(
        title=request.title,
        author_id=request.author_id,
        cover_image_url=request.cover_image_url,
        content=request.content
    )

    PostsRepo.insert(db, new_post)
    return ResponseSchema(
        code=status.HTTP_201_CREATED,
        status="Success",
        message="Post created successfully",
        result={
            "title": new_post.title,
            "author_id": new_post.author_id,
            "user": current_user
        }
    )


@router.delete("/posts", status_code=HTTPStatus.NO_CONTENT)
def delete_post(
    request: DeletePostsSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dependency)
):
    post = PostsRepo.find_by_id(db, request.id)
    if post is None:
        raise NOT_FOUND_EXCEPTION

    PostsRepo.delete(db, post)

    return ResponseSchema(
        code=status.HTTP_204_NO_CONTENT,
        status="Success",
        message="Post deleted successfully"
    )


@router.get("/posts", status_code=HTTPStatus.OK)
def get_posts(
    post_id: int = None,
    db: Session = Depends(get_db),
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


@router.put("/posts", status_code=HTTPStatus.OK)
def update_posts(
        request: UpdatePostsSchema,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user_dependency)
):
    post = PostsRepo.find_by_id(db, request.id)
    if not post:
        raise NOT_FOUND_EXCEPTION

    updated_post = PostsRepo.update(db, post, request)

    return ResponseSchema(
        code=status.HTTP_200_OK,
        status="Success",
        message="Post updated successfully",
        result={
            "title": updated_post.title,
            "author_id": updated_post.author_id,
            "user": current_user
        }
    )

