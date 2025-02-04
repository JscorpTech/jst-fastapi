from typing import Generic, List, Optional, TypeVar

from fastapi import Request
from sqlalchemy.orm import Query, Session

from fastx.db.base import BaseModel
from fastx.filters import DefaultFilter
from fastx.pagination import DefaultPagination

T = TypeVar("T", bound=BaseModel)


class DBManager(Generic[T]):
    _model: T
    _db: Session

    def __init__(self, model: T, db: Session) -> None:
        self._model = model
        self._db = db

    def all(self) -> List[T]:
        return self._db.query(self._model).all()

    def queryset(self) -> Query:
        return self._db.query(self._model)

    def get(self, id: int) -> Optional[T]:
        return self._db.query(self._model).filter(self._model.id == id).first()

    def create(self, **kwargs) -> T:
        model = self._model(**kwargs)
        self._db.add(model)
        self._db.commit()
        return model

    def update(self, id: int, **kwargs) -> Optional[T]:
        model = self._db.query(self._model).filter(self._model.id == id).first()
        if not model:
            raise BaseModel("object not found")
        for key, value in kwargs.items():
            setattr(model, key, value)
        self._db.commit()
        return model

    def delete(self, id: int) -> bool:
        model = self._db.query(self._model).filter(self._model.id == id).first()
        self._db.delete(model)
        self._db.commit()
        return True

    def get_filter(self) -> DefaultFilter:
        return DefaultFilter(self.queryset())

    def pagination(self, queryset: Query, request: Request, *args, **kwargs) -> DefaultPagination:
        return DefaultPagination(request, *args, **kwargs).queryset(queryset)
