from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from app.schemas.settings_schema import Settings

settings = Settings()

DATABASE_URL = settings.DATABASE_URL
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
BUCKET_NAME = settings.BUCKET_NAME
REGION_NAME = settings.REGION_NAME

engine = create_engine(DATABASE_URL)
Base = declarative_base()
