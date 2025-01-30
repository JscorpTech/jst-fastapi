from passlib.hash import bcrypt
from app.db.models import UserModel
from fastapi_core.services import RedisService
import json
from app.api.auth.schemas.auth import RegisterSchema
from sqlalchemy.orm import Session
from app.db.database import _DB
from fastapi import HTTPException


class AuthService:
    db: Session

    def __init__(self, db: _DB) -> None:
        self.db = db

    async def save_user_redis(self, user: RegisterSchema):
        return await RedisService.set_key(self._redis_key(user.phone), user.model_dump_json(), ex=60 * 60)

    async def create_user_redis(self, phone: str | int) -> UserModel:
        user = await RedisService.get_key(self._redis_key(phone))
        if not user:
            raise Exception("User not found")
        user: RegisterSchema = json.loads(user)
        return await self.create_user(**user)

    async def create_user(self, phone: str, password: str, *args, **kwargs) -> UserModel:
        user = UserModel(phone=phone, password=await self.make_hash(password), **kwargs)
        self.db.add(user)
        self.db.commit()
        return user

    async def validate_user(self, phone: str, password: str) -> UserModel:
        user: UserModel = self.db.query(UserModel).filter(UserModel.phone == phone).first()
        if not user or not await self.check_password(password, user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return user

    async def make_hash(self, password: str) -> str:
        return bcrypt.hash(password)

    async def check_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)

    def _redis_key(self, phone: str) -> str:
        return "user_%s" % phone
