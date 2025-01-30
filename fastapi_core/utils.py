from fastapi import Request


def build_absolute_uri(request: Request, path: str) -> str:
    return f"{request.base_url}{path}"


def build_uri(request: Request, path: str) -> str:
    return f"{request.url.components._replace(query="").geturl()}{path}"
