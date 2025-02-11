from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, UploadFile

from app import services as _services
from app.db.models import UserModel
from app.schemas import UserSchema
from fastx.schema.response import _R
from fastx.storage.base import BaseStorage
from fastx.utils import default_storage, upload_file
from fastx.utils.validation import validate_mine
from app.services.auth import AuthService
from fastx.services import redis
from fastx.exceptions import APIException
from uuid import uuid4
from app.api.auth.services.auth import jwt_encode, jwt_decode

from ..schemas import auth as _schema
from ..services.auth import create_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", summary="Register new user", tags=["register"])
async def register(
    user: Annotated[_schema.RegisterSchema, Body()],
    service: Annotated[_services.AuthService, Depends()],
    otp_service: Annotated[_services.OtpService, Depends()],
) -> _R[_schema.RegisterSchema]:
    await service.is_already_user(user.phone, raise_exception=True)
    await service.save_user_redis(user)
    otp_service.send_otp(user.phone)
    return _R(data=user)


@router.post("/confirm", summary="confirm verification code", tags=["register"])
async def confirm(
    confirm: _schema.ConfirmSchema,
    service: Annotated[_services.AuthService, Depends()],
    otp_service: Annotated[_services.OtpService, Depends()],
) -> _R[_schema.TokenSchema]:
    otp_service.verify_otp(confirm.phone, confirm.code)
    user = await service.create_user_redis(confirm.phone)
    return _R(status=True, data=_schema.TokenSchema(**await create_token(user)))


@router.post("/resend-code", tags=["register", "reset-password"])
async def resend_code(
    data: _schema.ResendCodeSchema,
    otp_service: Annotated[_services.OtpService, Depends()],
) -> _R:
    otp_service.send_otp(data.phone)
    return _R()


@router.post("/login", summary="Login already user")
async def login(
    user: Annotated[_schema.LoginSchema, Body()],
    service: Annotated[_services.AuthService, Depends()],
) -> _R[_schema.TokenSchema]:
    user = await service.validate_user(user.phone, user.password)
    return _R(status=True, data=_schema.TokenSchema(**await create_token(user)))


@router.post("/refresh-token")
async def refresh_token(data: Annotated[_schema.RefreshTokenSchema, Body()]) -> _R[_schema.RefreshTokenResponseSchema]:
    user = await jwt_decode(data.token)
    if user["token_type"] != "refresh":
        raise APIException("Invalid token")
    return _R(data=_schema.RefreshTokenResponseSchema(access_token=await jwt_encode(user["sub"])))


@router.post("/change-password")
async def change_password(
    password: _schema.ChangePasswordSchema,
    user: Annotated[UserModel, Depends(_services.get_user)],
    service: Annotated[AuthService, Depends()],
) -> _R[_schema.ChangePasswordSchema]:
    await service.check_password(password.old_password, str(user.password), raise_exception=True)
    await service.update_user(user.phone, {"password": await service.make_password(password.new_password)})
    return _R(data=password)


@router.post("/reset-password", tags=["reset-password"])
async def reset_password(
    data: _schema.ResetPasswordSchema,
    otp_service: Annotated[_services.OtpService, Depends()],
    service: Annotated[AuthService, Depends()],
) -> _R[_schema.ResetPasswordTokenSchema]:
    if not await service.is_already_user(data.phone):
        raise APIException(data={"phone": "User not found"}, detail=APIException.VALIDATION_ERROR)
    otp_service.verify_otp(data.phone, data.code)
    token = str(uuid4())
    redis.set_key("reset-password:{}".format(token), data.phone, 60 * 60)
    return _R(data=_schema.ResetPasswordTokenSchema(token=token))


@router.post("/reset-password/confirm", tags=["reset-password"])
async def reset_password_confirm(
    data: _schema.ResetPasswordConfirmSchema, service: Annotated[_services.AuthService, Depends()]
) -> _R:
    key = "reset-password:{}".format(data.token)
    user = redis.get_key(key)
    if user is None or not await service.is_already_user(user):
        raise APIException(APIException.VALIDATION_ERROR, data={"token": APIException.INVALID_TOKEN})
    await service.update_user(user, {"password": await service.make_password(data.password)})
    redis.delete_key(key)
    return _R()


@router.patch("/update", summary="Update user information")
async def update(
    update_user: _schema.UpdateSchema,
    service: Annotated[_services.AuthService, Depends()],
    user: UserModel = Depends(_services.get_user),
) -> _R[_schema.UpdateSchema]:
    user_data = update_user.model_dump(exclude_unset=True)
    await service.update_user(user.phone, user_data)
    return _R(data=user_data)


@router.post("/update/avatar", summary="Update user avatar")
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
