from pydantic import Field

from fastx.schemas import BaseModel
from typing import Optional


class LoginSchema(BaseModel):
    phone: str = Field(max_length=100)
    password: str = Field(min_length=8)


class RegisterSchema(BaseModel):
    phone: str = Field(max_length=12, min_length=12)
    password: str = Field(min_length=8)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: Optional[str] = None


class UpdateSchema(BaseModel):
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    email: Optional[str] = None

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ConfirmSchema(BaseModel):
    phone: str = Field(max_length=100)
    code: str
