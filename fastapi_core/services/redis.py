import logging
from typing import Optional

import redis.asyncio as redis

from fastapi_core.conf import settings

logger = logging.getLogger(__name__)


class RedisService:
    _pool: Optional[redis.ConnectionPool] = None

    @classmethod
    def get_redis(cls):
        if not cls._pool:
            cls._pool = redis.ConnectionPool.from_url(
                str(settings.REDIS_URL), decode_responses=True, max_connections=20
            )
        return redis.Redis(connection_pool=cls._pool)

    @classmethod
    async def close_pool(cls):
        if cls._pool:
            await cls._pool.disconnect()
            logger.info("Redis connection pool closed")

    @classmethod
    async def ping(cls):
        try:
            return await cls.get_redis().ping()
        except Exception as e:
            logger.error(f"Redis connection error: {str(e)}")
            raise

    @classmethod
    async def set_key(cls, key: str, value: str, ex: Optional[int] = None):
        async with cls.get_redis() as conn:
            await conn.set(key, value, ex=ex)

    @classmethod
    async def get_key(cls, key: str):
        async with cls.get_redis() as conn:
            return await conn.get(key)

    @classmethod
    async def delete_key(cls, key: str):
        async with cls.get_redis() as conn:
            return await conn.delete(key)

    @classmethod
    async def key_exists(cls, key: str):
        async with cls.get_redis() as conn:
            return await conn.exists(key)
