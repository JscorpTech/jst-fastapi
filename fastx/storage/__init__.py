from fastx.conf import settings
from fastx.utils import import_module
from fastx.storage.base import BaseStorage
from typing import Any, Union


def default_storage() -> Union[Any, BaseStorage]:
    return import_module(settings.DEFAULT_STORAGE)
