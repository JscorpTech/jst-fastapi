from app import load  # noqa
from app.api.auth.routes import auth
from app.api.v1.routes import root
from fastapi_core.asgi import application
from fastapi import HTTPException, responses
from fastapi.exceptions import RequestValidationError
from app.exceptions import APIException
from fastapi_core.response import ResponseSchema

app = application()

app.include_router(root.router)
app.include_router(auth.router)


@app.exception_handler(APIException)
def api_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(status=False, message=exc.detail, data=exc.data).model_dump(),
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=400,
        content=ResponseSchema(status=False, data=[{_['loc'][1]: _['msg']} for _ in exc.errors()]).model_dump(),
    )


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(status=False, message=exc.detail, data=[]).model_dump(),
    )
