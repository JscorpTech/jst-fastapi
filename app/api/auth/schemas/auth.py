from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    phone: str = Field(max_length=100)
    password: str = Field(min_length=8)


class RegisterSchema(BaseModel):
    phone: str = Field(max_length=100)
    password: str = Field(min_length=8)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: str | None = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ConfirmSchema(BaseModel):
    phone: str = Field(max_length=100)
    code: str
