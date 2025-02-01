from contextvars import ContextVar
from typing import Any

from fastapi_core.conf import settings

LANGUAGE = ContextVar("LANGUAGE", default=settings.LANGUAGE)


def get_language() -> str:
    return LANGUAGE.get()


def set_language(lang: str) -> Any:
    return LANGUAGE.set(lang)


def translate(val: dict) -> str | None:
    data = val.get(get_language())
    if data is None:
        return val.get(settings.LANGUAGE)
    return data
