from fastapi.exceptions import HTTPException, RequestValidationError

from app import load  # noqa
from app.api.auth.routes import auth
from app.api.v1 import routes as v1_routes
from fastx.asgi import application
from fastx.exceptions import APIException
from fastx.handlers import api_exception_handler, http_exception_handler, request_validation_exception_handler
from fastx.middlewares import translation_middleware  # profiler_middleware

app = application()

app.include_router(v1_routes.news.router, prefix="/v1/news")
app.include_router(v1_routes.root.router)
app.include_router(auth.router)
app.exception_handler(APIException)(api_exception_handler)
app.exception_handler(HTTPException)(http_exception_handler)
app.exception_handler(RequestValidationError)(request_validation_exception_handler)


app.middleware("http")(translation_middleware)
# app.middleware("http")(profiler_middleware)
