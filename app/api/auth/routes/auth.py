from typing import Annotated
from fastapi import APIRouter, Body, Depends, Request
from fastapi_core.response import ResponseSchema
from ..schemas.auth import ConfirmSchema, LoginSchema, RegisterSchema, TokenSchema
from app.services import UserService, OtpService
from ..services.auth import create_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
    user: Annotated[RegisterSchema, Body()],
    service: UserService = Depends(UserService),
    otp_service: OtpService = Depends(OtpService),
) -> ResponseSchema[RegisterSchema]:
    await user.is_valid(raise_exception=True)
    await service.save_user_redis(user)
    await otp_service.send_otp(user.phone)
    return ResponseSchema(data=user)


@router.post("/confirm")
async def confirm(
    confirm: ConfirmSchema, service: UserService = Depends(UserService),
    otp_service: OtpService = Depends(OtpService),
) -> ResponseSchema[TokenSchema]:
    await otp_service.verify_otp(confirm.phone, confirm.code)
    user = await service.create_user_redis(confirm.phone)
    return ResponseSchema(status=True, data=TokenSchema(**await create_token(user)))


@router.post("/login")
async def login(
    user: Annotated[LoginSchema, Body()], request: Request
) -> ResponseSchema[TokenSchema]:
    return ResponseSchema(
        status=True, data=TokenSchema(access_token="11212", refresh_token="11212")
    )
