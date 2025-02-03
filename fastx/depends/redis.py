from typing import Generator

from redis import Redis

from fastx.services import RedisService


def get_redis() -> Generator[Redis, None, None]:
    r = RedisService.get_redis()
    try:
        yield r
    finally:
        r.close()
