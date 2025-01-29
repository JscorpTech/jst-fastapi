from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationSchema(BaseModel, Generic[T]):
    page: int = 1
    page_size: int = 10
    total: int = 1
    result: T
