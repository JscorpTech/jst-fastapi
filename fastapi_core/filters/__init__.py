from sqlalchemy.orm import Query
from typing import List, Annotated
from fastapi import Query as Q, Request
from sqlalchemy import or_, and_

_SEARCH = Annotated[str | None, Q()]


class BaseFilter:
    _queryset: Query

    def __init__(self, queryset: Query, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._queryset = queryset

    def queryset(self):
        return self._queryset

    @property
    def model(self):
        return self._queryset._entity_from_pre_ent_zero().class_


class DefaultFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def search(self, fields: List[str], value: str):
        if value is None:
            return self
        self._queryset = self._queryset.filter(or_(getattr(self.model, field).ilike(f"%{value}%") for field in fields))
        return self

    def filter(self, fields: List[str], request: Request):
        filters = [
            getattr(self.model, field).ilike("%{}%".format(request.query_params[field]))
            for field in fields
            if request.query_params.get(field) is not None
        ]
        self._queryset = self._queryset.filter(and_(*filters)) if filters else self._queryset
        return self
