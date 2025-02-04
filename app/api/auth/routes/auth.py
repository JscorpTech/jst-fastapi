from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, UploadFile

from app import services as _services
from app.db.models import UserModel
from app.schemas import UserSchema
from fastx.schema.response import _R
from fastx.storage.base import BaseStorage
from fastx.utils import default_storage, upload_file
from fastx.utils.validation import validate_mine

from ..schemas import auth as _schema
from ..services.auth import create_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", summary="Register new user")
async def register(
    user: Annotated[_schema.RegisterSchema, Body()],
    service: Annotated[_services.AuthService, Depends()],
    otp_service: Annotated[_services.OtpService, Depends()],
) -> _R[_schema.RegisterSchema]:
    await service.is_already_user(user.phone, raise_exception=True)
    await service.save_user_redis(user)
    otp_service.send_otp(user.phone)
    return _R(data=user)


@router.post("/confirm", summary="confirm verification code")
async def confirm(
    confirm: _schema.ConfirmSchema,
    service: Annotated[_services.AuthService, Depends()],
    otp_service: Annotated[_services.OtpService, Depends()],
) -> _R[_schema.TokenSchema]:
    otp_service.verify_otp(confirm.phone, confirm.code)
    user = await service.create_user_redis(confirm.phone)
    return _R(status=True, data=_schema.TokenSchema(**await create_token(user)))


@router.post("/login", summary="Login already user")
async def login(
    user: Annotated[_schema.LoginSchema, Body()],
    service: Annotated[_services.AuthService, Depends()],
) -> _R[_schema.TokenSchema]:
    user = await service.validate_user(user.phone, user.password)
    return _R(status=True, data=_schema.TokenSchema(**await create_token(user)))


@router.patch("/update", summary="Update user information")
async def update(
    update_user: _schema.UpdateSchema,
    service: Annotated[_services.AuthService, Depends()],
    user: UserModel = Depends(_services.get_user),
) -> _R:
    user_data = update_user.model_dump(exclude_unset=True)
    await service.update_user(user.phone, user_data)
    return _R(data=user_data)


@router.patch("/update/avatar", summary="Update user avatar")
async def update_avatar(
    file: Annotated[UploadFile, File()],
    service: Annotated[_services.AuthService, Depends()],
    user: Annotated[UserModel, Depends(_services.get_user)],
) -> _R[_schema.UpdateAvatarResponse]:
    await validate_mine(file, ["image/jpeg", "image/png", "image/jpg"])
    storage: BaseStorage = default_storage()
    path = await upload_file("avatar/", file)
    avatar = user.avatar
    await service.update_user(user.phone, {"avatar": path})
    if avatar is not None:
        storage.delete(avatar)
    return _R(data=_schema.UpdateAvatarResponse(avatar=path))


@router.get("/me", summary="Get user information")
async def me(user: UserModel = Depends(_services.get_user)) -> _R[UserSchema]:
    return _R(data=UserSchema.model_validate(user))
