import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime

from config import Base


class GenderEnum(enum.Enum):
    male = "M"
    female = "F"
    other = "O"
    not_specified = "N"


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)

    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    gender = Column(Enum(GenderEnum, name="gender_enum"), nullable=False)

    create_date = Column(DateTime, default=datetime.now)
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
