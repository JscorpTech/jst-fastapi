from fastapi import HTTPException

from app import load  # noqa
from app.api.auth.routes import auth
from app.api.v1.routes import news
from fastapi_core.asgi import application
from fastapi_core.exceptions import APIException
from fastapi_core.handlers import api_exception_handler, http_exception_handler
from fastapi_core.middlewares import profiler_middleware, translation_middleware

app = application()

app.include_router(news.router, prefix="/v1/news")
app.include_router(auth.router)
app.exception_handler(APIException)(api_exception_handler)
app.exception_handler(HTTPException)(http_exception_handler)


app.middleware("http")(translation_middleware)
app.middleware("http")(profiler_middleware)
