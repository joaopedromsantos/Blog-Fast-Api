from sqlalchemy.orm import Session
from app.models.users import Users


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




