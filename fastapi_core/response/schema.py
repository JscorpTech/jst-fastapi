from typing import Generic, TypeVar, List, Dict

from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    status: bool = True
    data: T | List[T] | Dict[str, T] | None = None
    message: str | None = None


_R = ResponseSchema
