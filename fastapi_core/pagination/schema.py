from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")


class Link(BaseModel):
    first: Optional[str] = None
    last: Optional[str] = None
    next: Optional[str] = None
    prev: Optional[str] = None


class PaginationSchema(BaseModel, Generic[T]):
    page: int = 1
    link: Link
    page_size: int = 10
    total: int = 1
    total_pages: Optional[int] = None
    result: T
