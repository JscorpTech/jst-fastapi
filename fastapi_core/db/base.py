from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from app.db.database import _DB, Base
from fastapi_core.manager import DBManager


class Model(Base):
    __abstract__: bool = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def manager(self, db: _DB):
        return DBManager(self, db)

    class NotFound(Exception):

        def __init__(self, *args):
            super().__init__(*args)

    def __str__(self) -> str:
        return "Object with id: {}".format(self.id)
