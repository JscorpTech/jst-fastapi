from typing import Generator
from fastapi_core.services import RedisService
from redis import Redis


def get_redis() -> Generator[Redis, None, None]:
    r = RedisService.get_redis()
    try:
        yield r
    finally:
        r.close()
