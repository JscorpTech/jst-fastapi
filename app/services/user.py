from passlib.hash import bcrypt
from app.db.models import UserModel
from fastapi_core.services import RedisService
import json
from app.api.auth.schemas.auth import RegisterSchema


class UserService:
    def __init__(self):
        pass

    async def save_user_redis(self, user: RegisterSchema):
        return await RedisService.set_key(
            self._redis_key(user.phone), user.model_dump_json(), ex=60 * 60
        )

    async def create_user_redis(self, phone: str | int) -> UserModel:
        user = await RedisService.get_key(self._redis_key(phone))
        if not user:
            raise Exception("User not found")
        user: RegisterSchema = json.loads(user)
        return await self.create_user(**user)

    async def create_user(self, phone: str, password: str, *args, **kwargs):
        return await UserModel.create(
            phone=phone, password=await self.make_hash(password), **kwargs
        )

    async def make_hash(self, password: str) -> str:
        return bcrypt.hash(password)

    async def check_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)

    def _redis_key(self, phone: str) -> str:
        return "user_%s" % phone
