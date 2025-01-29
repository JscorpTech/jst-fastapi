from typing import Annotated
from fastapi import APIRouter, Body, Depends, Request
from fastapi_core.response import ResponseSchema
from ..schemas.auth import ConfirmSchema, LoginSchema, RegisterSchema, TokenSchema
from app.services import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
    user: Annotated[RegisterSchema, Body()], service: UserService = Depends(UserService)
) -> ResponseSchema[RegisterSchema]:
    await service.save_user_redis(user)
    return ResponseSchema(data=user)


@router.post("/confirm")
async def confirm(
    confirm: ConfirmSchema, service: UserService = Depends(UserService)
) -> ResponseSchema[TokenSchema]:
    await service.create_user_redis(confirm.phone)
    return ResponseSchema(
        status=True, data=TokenSchema(access_token="11212", refresh_token="11212")
    )


@router.post("/login")
async def login(
    user: Annotated[LoginSchema, Body()], request: Request
) -> ResponseSchema[TokenSchema]:
    return ResponseSchema(
        status=True, data=TokenSchema(access_token="11212", refresh_token="11212")
    )
