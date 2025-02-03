from fastapi import Request
import importlib


def build_absolute_uri(request: Request, path: str) -> str:
    return f"{request.base_url}{path}"


def build_uri(request: Request, path: str) -> str:
    return f"{request.url.components._replace(query="").geturl()}{path}"


def import_module(module: str):
    module_list = module.split(".")
    object_name = module_list[-1]
    module_path = ".".join(module_list[:-1])
    return getattr(importlib.import_module(module_path), object_name)()
