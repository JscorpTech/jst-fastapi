from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    status: bool = True
    data: T
    message: str | None = None
