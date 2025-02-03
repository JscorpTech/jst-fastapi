from typing import Annotated, Optional

from fastapi import Query, Request
from sqlalchemy.orm import Query as Queryset

from fastx.utils import build_uri

from .schema import Link, PaginationSchema

_PAGE = Annotated[int | None, Query()]
_PAGE_SIZE = Annotated[int | None, Query()]


class BasePagination:
    page: int = 1
    page_size: int = 10
    _total: int
    _queryset: Queryset
    _request: Request

    def __init__(self, request: Request, page: Optional[int] = None, page_size: Optional[int] = None):
        self.page = page if page else self.page
        self.page_size = page_size if page_size else self.page_size
        self._request = request

    def queryset(self, queryset: Queryset):
        self._total = queryset.count()
        self._queryset = queryset.offset((self.page - 1) * self.page_size).limit(self.page_size)
        return self

    @property
    def next_url(self) -> Optional[str]:
        return (
            build_uri(self._request, f"?page={self.page + 1}")
            if self.page < self._total // self.page_size + 1
            else None
        )

    @property
    def prev_url(self) -> Optional[str]:
        return build_uri(self._request, f"?page={self.page - 1}") if self.page > 1 else None

    @property
    def first_url(self) -> str:
        return build_uri(self._request, "?page=1")

    @property
    def last_url(self) -> str:
        return build_uri(self._request, f"?page={self._total // self.page_size + 1}")

    def pagination_links(self) -> Link:
        return Link(first=self.first_url, last=self.last_url, next=self.next_url, prev=self.prev_url)

    def response(self) -> PaginationSchema:
        return PaginationSchema(
            page=self.page,
            page_size=self.page_size,
            total=self._total,
            result=self._queryset.all(),
            link=self.pagination_links(),
            total_pages=self._total // self.page_size + 1,
        )


class DefaultPagination(BasePagination):
    page_size: int = 10
