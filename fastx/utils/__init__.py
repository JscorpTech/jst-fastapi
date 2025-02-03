from fastapi import Request
import importlib
from uuid import uuid4
from fastapi import UploadFile
from typing import Union, Optional, Literal, TypeAlias
from pathlib import Path
from mimetypes import guess_extension
from fastx.conf import settings
from fastx.storage.base import BaseStorage
from fastx.storage.s3 import S3Storage
from fastx.storage.file import FileStorage

_STORAGES: TypeAlias = Literal["s3", "file"]


def build_absolute_uri(request: Request, path: str) -> str:
    return f"{request.base_url}{path}"


def build_uri(request: Request, path: str) -> str:
    return f"{request.url.components._replace(query="").geturl()}{path}"


def import_module(module: str):
    module_list = module.split(".")
    object_name = module_list[-1]
    module_path = ".".join(module_list[:-1])
    return getattr(importlib.import_module(module_path), object_name)()


def generate_filename(extension: str) -> str:
    return "%s%s" % (uuid4(), extension)


async def upload_file(upload_dir: Union[str, Path], file: UploadFile, storage: Optional[_STORAGES] = None):
    extension = None
    if file.content_type is not None:
        extension = guess_extension(file.content_type)
    if extension is None:
        extension = ".bin"
    file_name = generate_filename(extension)
    path = f"{upload_dir}{file_name}"
    default_storage(storage).write(await file.read(), path, "wb")
    return path


def default_storage(storage: Optional[_STORAGES] = None) -> BaseStorage:
    if storage is None:
        return import_module(settings.DEFAULT_STORAGE)
    elif "s3":
        return S3Storage()
    elif "file":
        return FileStorage()
    raise Exception("Invalid storage")
