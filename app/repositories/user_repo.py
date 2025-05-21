from sqlalchemy.orm import Session
from app.models.users import Users
from exceptions.http_exceptions import NOT_FOUND_EXCEPTION


class UserRepo:
    @staticmethod
    def insert(db: Session, user: Users):
        db.add(user)
        db.commit()
        db.refresh(user)

    @staticmethod
    def find_by_username(db: Session, username: str):
        return db.query(Users).filter(Users.username == username).first()

    @staticmethod
    def find_by_email(db: Session, email: str):
        return db.query(Users).filter(Users.email == email).first()

    @staticmethod
    def find_by_id(db: Session, user_id: int):
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise NOT_FOUND_EXCEPTION
        return user

    @staticmethod
    def promote(db: Session, user: Users):
        user.role = "admin"
        db.commit()
        db.refresh(user)
        return user


