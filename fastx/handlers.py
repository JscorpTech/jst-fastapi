from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastx.response import ResponseSchema


def api_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(status=False, message=exc.detail, data=exc.data).model_dump(),
    )


def http_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(status=False, message=exc.detail, data=[]).model_dump(),
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        errors[error["loc"][-1]] = error["msg"]

    return JSONResponse(
        status_code=422,
        content=ResponseSchema(status=False, data=errors, message="Oops! Validation error").model_dump(),
    )
