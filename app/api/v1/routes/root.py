import pathlib
from typing import Annotated

from fastapi import APIRouter, Path, Request
from fastapi.responses import FileResponse, PlainTextResponse

from fastx.schema.response import _R
from fastx.storage.file import FileStorage

router = APIRouter()


@router.get("/", tags=["root"])
async def root(request: Request) -> _R:
    return _R()


@router.get("/health", include_in_schema=False)
async def health() -> _R:
    return _R()


@router.get("/storage/{file_path:path}", tags=["root"])
def storage(file_path: Annotated[str, Path()]):
    file = pathlib.Path(FileStorage().path(file_path))
    if not file.exists():
        return PlainTextResponse("File not found", 404)
    return FileResponse(file, media_type="application/octet-stream")
