from typing import Dict, Generic, List, TypeVar, Type

from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    status: bool = True
    data: T | List[T] | Dict[str, T] | None = None
    message: str | None = "🫠 OK"


_R: Type[ResponseSchema] = ResponseSchema
