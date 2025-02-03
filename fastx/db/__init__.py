from app.db.database import _DB
from fastx.db.base import BaseModel
from fastx.manager import DBManager


class Model(BaseModel):
    __abstract__ = True

    @classmethod
    def manager(self, db: _DB):
        return DBManager(self, db)

    def __str__(self) -> str:
        return "Object with id: {}".format(self.id)
