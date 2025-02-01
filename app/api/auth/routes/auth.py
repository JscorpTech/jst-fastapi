from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app import services as _services
from app.schemas import UserSchema
from fastapi_core.response import _R

from ..schemas import auth as _schema
from ..services.auth import create_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
    user: Annotated[_schema.RegisterSchema, Body()],
    service: Annotated[_services.AuthService, Depends()],
    otp_service: Annotated[_services.OtpService, Depends()],
) -> _R[_schema.RegisterSchema]:
    await service.save_user_redis(user)
    otp_service.send_otp(user.phone)
    return _R(data=user)


@router.post("/confirm")
async def confirm(
    confirm: _schema.ConfirmSchema,
    service: Annotated[_services.AuthService, Depends()],
    otp_service: Annotated[_services.OtpService, Depends()],
) -> _R[_schema.TokenSchema]:
    otp_service.verify_otp(confirm.phone, confirm.code)
    user = await service.create_user_redis(confirm.phone)
    return _R(status=True, data=_schema.TokenSchema(**await create_token(user)))


@router.post("/login")
async def login(
    user: Annotated[_schema.LoginSchema, Body()],
    service: Annotated[_services.AuthService, Depends()],
) -> _R[_schema.TokenSchema]:
    user = await service.validate_user(user.phone, user.password)
    return _R(status=True, data=_schema.TokenSchema(**await create_token(user)))


@router.get("/me")
async def me(user: int = Depends(_services.get_user)) -> _R[UserSchema]:
    return _R(data=UserSchema.model_validate(user))
