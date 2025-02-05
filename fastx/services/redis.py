import logging
from typing import Optional

import redis as rs

from fastx.conf import settings

logger = logging.getLogger(__name__)


class RedisService:
    _pool: Optional[rs.ConnectionPool] = None

    @classmethod
    def get_redis(cls):
        if not cls._pool:
            cls._pool = rs.ConnectionPool.from_url(str(settings.REDIS_URL), decode_responses=True, max_connections=20)
        return rs.Redis(connection_pool=cls._pool)

    @classmethod
    def close_pool(cls):
        if cls._pool:
            cls._pool.disconnect()
            logger.info("Redis connection pool closed")

    @classmethod
    def ping(cls):
        try:
            return cls.get_redis().ping()
        except Exception as e:
            logger.error(f"Redis connection error: {str(e)}")
            raise

    @classmethod
    def set_key(cls, key: str, value: str, ex: Optional[int] = None):
        with cls.get_redis() as conn:
            conn.set(key, value, ex=ex)

    @classmethod
    def get_key(cls, key: str):
        with cls.get_redis() as conn:
            return conn.get(key)

    @classmethod
    def delete_key(cls, key: str):
        with cls.get_redis() as conn:
            return conn.delete(key)

    @classmethod
    def key_exists(cls, key: str):
        with cls.get_redis() as conn:
            return conn.exists(key)


redis = RedisService
