from typing import Optional, Union

from pydantic import BaseModel, Field

from fastx.schema.fields import _FILE, _PHONE, _PASSWORD


class LoginSchema(BaseModel):
    phone: _PHONE
    password: _PASSWORD


class RegisterSchema(BaseModel):
    phone: _PHONE
    password: _PASSWORD
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: Optional[str] = None


class UpdateSchema(BaseModel):
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    email: Optional[str] = None

    class Config:
        from_attributes = True


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str


class ResetPasswordSchema(BaseModel):
    phone: _PHONE
    code: Union[str, int]


class ResetPasswordTokenSchema(BaseModel):
    token: str


class ResetPasswordConfirmSchema(BaseModel):
    token: str
    password: _PASSWORD


class ResendCodeSchema(BaseModel):
    phone: _PHONE


class UpdateAvatarResponse(BaseModel):
    avatar: _FILE


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ConfirmSchema(BaseModel):
    phone: _PHONE
    code: str
