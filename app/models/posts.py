from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

from config import Base


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))

    cover_image_url = Column(String)
    content = Column(Text, nullable=False)

    create_date = Column(DateTime, default=datetime.now)
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
