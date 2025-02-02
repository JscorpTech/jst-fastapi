from fastapi import FastAPI

from fastx.asgi import application

__version__ = "0.1.0"
__all__ = [
    "application",
    "setup",
]


def setup() -> FastAPI:
    from app.db.database import engine
    from app.db.models import Base
    from fastx.conf import settings

    Base.metadata.create_all(bind=engine)

    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    return app
