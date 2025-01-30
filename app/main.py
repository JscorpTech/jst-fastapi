from app import load  # noqa
from app.api.auth.routes import auth
from app.api.v1.routes import news
from fastapi_core.asgi import application
from fastapi import HTTPException, responses
from fastapi_core.exceptions import APIException
from fastapi_core.response import ResponseSchema
from pyinstrument import Profiler

app = application()

app.include_router(news.router, prefix="/v1/news")
app.include_router(auth.router)


@app.middleware("http")
async def profiler_middleware(request, call_next):
    profiler = Profiler()
    profiler.start()
    response = await call_next(request)
    profiler.stop()
    with open("profiler.html", "w") as f:
        f.write(profiler.output_html())
    return response


@app.exception_handler(APIException)
def api_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(status=False, message=exc.detail, data=exc.data).model_dump(),
    )


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(status=False, message=exc.detail, data=[]).model_dump(),
    )
