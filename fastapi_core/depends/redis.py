from typing import Generator

from redis import Redis

from fastapi_core.services import RedisService


def get_redis() -> Generator[Redis, None, None]:
    r = RedisService.get_redis()
    try:
        yield r
    finally:
        r.close()
