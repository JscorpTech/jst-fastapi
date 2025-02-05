from typing import Generator

from redis import Redis

from fastx.services import redis


def get_redis() -> Generator[Redis, None, None]:
    r = redis.get_redis()
    try:
        yield r
    finally:
        r.close()
