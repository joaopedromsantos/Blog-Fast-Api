from sqlalchemy.orm import Session

from app.schemas.posts_schema import UpdatePostsSchema
from exceptions.http_exceptions import NOT_FOUND_EXCEPTION
from app.models.posts import Posts


class PostsRepo:

    @staticmethod
    def insert(db: Session, post: Posts):
        db.add(post)
        db.commit()
        db.refresh(post)

    @staticmethod
    def delete(db: Session, post: Posts):
        db.delete(post)
        db.commit()

    @staticmethod
    def find_all(db: Session):
        return db.query(Posts).all()

    @staticmethod
    def find_all_paginated(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Posts).offset(skip).limit(limit).all()

    @staticmethod
    def find_by_id(db: Session, post_id: int):
        post = db.query(Posts).filter(Posts.id == post_id).first()
        if not post:
            raise NOT_FOUND_EXCEPTION
        return post

    @staticmethod
    def update(db: Session, post: Posts, request: UpdatePostsSchema):
        post.title = request.title
        post.content = request.content
        post.cover_image_url = request.cover_image_url
        post.author_id = request.author_id

        db.commit()
        db.refresh(post)
        return post

