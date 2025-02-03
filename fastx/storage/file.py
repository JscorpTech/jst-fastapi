from fastx.storage.base import BaseStorage
from typing import Union
from pathlib import Path


class FileStorage(BaseStorage):
    def __init__(self):
        super().__init__()

    def _get_path(self, path: Union[str, Path]):
        return self._basedir.joinpath(path)

    def open(self, path, mode="r"):
        with open(self._get_path(path), mode) as file:
            return file

    def write(self, content, path, mode="w"):
        path = self._get_path(path)
        with open(path, mode) as file:
            file.write(content)
        return path

    def read(self, path, mode="r"):
        with open(self._get_path(path), mode) as file:
            return file.read()
