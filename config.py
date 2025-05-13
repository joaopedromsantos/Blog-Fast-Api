from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from app.schemas.settings_schema import Settings

settings = Settings()

DATABASE_URL = settings.DATABASE_URL
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

engine = create_engine(DATABASE_URL)
Base = declarative_base()
