import json
from typing import Any, Dict, Optional, Union

from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy import Column
from sqlalchemy.orm import Session

from app.api.auth.schemas.auth import RegisterSchema
from app.db.database import _DB
from app.db.models import UserModel
from fastx.exceptions import APIException
from fastx.services import redis


async def make_password(password: str) -> str:
    return bcrypt.hash(password)


async def check_password(password: str, hashed_password: str, raise_exception: bool = False) -> bool:
    is_verify = bcrypt.verify(password, hashed_password)
    if not is_verify:
        if raise_exception:
            raise APIException(APIException.VALIDATION_ERROR, data={"password": "Invalid password"})
        return False
    return True


def redis_key(phone: Union[str, int]) -> str:
    return "user_%s" % phone


# noinspection PyTypeChecker
class AuthService:
    db: Session

    def __init__(self, db: _DB) -> None:
        self.db = db

    async def is_already_user(self, phone: Union[str, int], raise_exception: bool = False) -> bool:
        user = self.db.query(UserModel).filter(UserModel.phone == phone).first()
        if user is not None:
            if raise_exception:
                raise APIException(APIException.VALIDATION_ERROR, 400, data={"phone": "User already"})
            return True
        return False

    async def update_user(self, phone: Union[int, str, Column[str]], user_data: Dict[str, Any]) -> Dict[str, Any]:
        user_instance = self.db.query(UserModel).filter(UserModel.phone == phone).first()
        for key, value in user_data.items():
            setattr(user_instance, key, value)
        self.db.commit()
        self.db.refresh(user_instance)
        return user_data

    # noinspection PyMethodMayBeStatic
    async def save_user_redis(self, user: RegisterSchema) -> str:
        return redis.set_key(redis_key(user.phone), user.model_dump_json(), ex=60 * 60)

    async def create_user_redis(self, phone: Union[str, int]) -> UserModel:
        user = redis.get_key(redis_key(phone))
        if not user:
            raise APIException(APIException.VALIDATION_ERROR, data={"phone": APIException.TEMPORARY_USER_NOT_FOUND})
        user = json.loads(user)
        redis.delete_key(redis_key(phone))
        return await self.create_user(**user)

    async def create_user(self, phone: str, password: str, *args, **kwargs) -> UserModel:
        user = UserModel(phone=phone, password=await make_password(password), **kwargs)
        self.db.add(user)
        self.db.commit()
        return user

    async def validate_user(self, phone: str, password: str) -> UserModel:
        user: Optional[UserModel] = self.db.query(UserModel).filter(UserModel.phone == phone).first()
        if not user or not await check_password(password, str(user.password)):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return user
