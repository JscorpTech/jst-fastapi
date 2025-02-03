from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from app.db.models import Base


class BaseModel(Base):
    __abstract__: bool = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    class NotFound(Exception):

        def __init__(self, *args):
            super().__init__(*args)
