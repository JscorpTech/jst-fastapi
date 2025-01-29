from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from fastapi_core.asgi import application

__version__ = "0.1.0"
__all__ = [
    "application",
    "setup",
]


def setup() -> FastAPI:
    from fastapi_core.conf import settings

    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    register_tortoise(
        app,
        config=settings.TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    return app
