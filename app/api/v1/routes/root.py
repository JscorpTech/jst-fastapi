import pathlib
from typing import Annotated

from fastapi import APIRouter, Path, Request
from fastapi.responses import FileResponse, PlainTextResponse

from fastx.storage.file import FileStorage
from fastx.utils import default_storage

router = APIRouter()


@router.get("/")
async def root(request: Request) -> dict:
    storage = default_storage()
    return {"detail": "ok", "file": storage.download_url("image.png", request)}


@router.get("/storage/{file_path:path}")
def storage(file_path: Annotated[str, Path()]):
    file = pathlib.Path(FileStorage().path(file_path))
    if not file.exists():
        return PlainTextResponse("File not found", 404)
    return FileResponse(file, media_type="application/octet-stream")
