from pydantic import Field, field_validator
from fastapi_core.schemas import BaseModel
from app.db.database import SessionLocal
from app.db.models import UserModel


class LoginSchema(BaseModel):
    phone: str = Field(max_length=100)
    password: str = Field(min_length=8)


class RegisterSchema(BaseModel):
    phone: str = Field(max_length=12, min_length=12)
    password: str = Field(min_length=8)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: str | None = None

    @field_validator("phone")
    def validate_phone(cls, v):
        with SessionLocal() as db:
            if db.query(UserModel).filter(UserModel.phone == v).first():
                raise ValueError("User already exists")
            return v


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ConfirmSchema(BaseModel):
    phone: str = Field(max_length=100)
    code: str
