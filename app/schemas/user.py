from typing import Optional, Union

from pydantic import BaseModel, Field

from fastx.schema.fields import _FILE


class UserSchema(BaseModel):
    id: int
    phone: str | int
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    avatar: Optional[Union[_FILE, str]] = None
    email: str | None = None

    class Config:
        from_attributes = True
