from sqlalchemy.orm import Query
from typing import List, Annotated
from fastapi import Query as Q
from sqlalchemy import or_

_SEARCH = Annotated[str | None, Q()]


class BaseFilter:
    _queryset: Query

    def __init__(self, queryset: Query, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._queryset = queryset


class DefaultFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def search(self, fields: List[str], value: str) -> Query:
        if value is None:
            return self._queryset
        self._queryset = self._queryset.where(
            or_(
                getattr(self._queryset._entity_from_pre_ent_zero().class_, field).ilike(f"%{value}%")
                for field in fields
            )
        )
        return self._queryset
