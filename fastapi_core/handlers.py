from fastapi import responses

from fastapi_core.response import ResponseSchema


def api_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(status=False, message=exc.detail, data=exc.data).model_dump(),
    )


def http_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(status=False, message=exc.detail, data=[]).model_dump(),
    )
