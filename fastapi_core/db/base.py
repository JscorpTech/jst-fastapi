from sqlalchemy import Column, DateTime, Integer
from app.db.database import Base
from sqlalchemy.sql import func


class Model(Base):
    __abstract__: bool = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __str__(self) -> str:
        return "Object with id: {}".format(self.id)
