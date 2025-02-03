import os
from pathlib import Path

from fastx.conf import settings
from fastx.storage.base import BaseStorage


class FileStorage(BaseStorage):
    def __init__(self):
        super().__init__()

    def download_url(self, path, request=None):
        if request is not None:
            base_url = request.base_url
        else:
            base_url: str = settings.BASE_URL  # type: ignore
            if not base_url.endswith("/"):
                base_url = f"{base_url}/"
        if not str(path).startswith("/"):
            path = "/%s" % path
        return "%s%s%s" % (base_url, settings.STORAGE_URL, path)

    def delete(self, path, raise_exception=False):
        path = self.path(path)
        if not Path(path).exists():
            if raise_exception:
                raise ValueError("File not found")
            return
        os.remove(path)

    def path(self, path):
        return self._basedir.joinpath(path)

    def open(self, path, mode="r"):
        return open(self.path(path), mode)

    def write(self, content, path, mode="w"):
        path = self.path(path)
        with open(path, mode) as file:
            file.write(content)
        return path

    def read(self, path, mode="r"):
        with open(self.path(path), mode) as file:
            return file.read()
