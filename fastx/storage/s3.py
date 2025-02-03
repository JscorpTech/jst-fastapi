from fastx.storage.base import BaseStorage
from fastx.services.s3 import S3Service
from pathlib import Path
from fastx.conf import settings
from io import BytesIO


class S3Storage(BaseStorage):
    _service: S3Service

    def __init__(self):
        super().__init__()
        self._service = S3Service()

    def download(self, path, request=None):
        if not str(path).startswith("/"):
            path = "/%s" % path
        return "%s%s" % (settings.S3_URL, path)

    def path(self, path):
        return path

    def open(self, path, mode="r"):
        response = self._service.get_connection().get_object(Bucket=self._service.bucket, Key=path)["Body"]
        return response.read().decode("utf-8") if "b" not in mode else response.read()

    def read(self, path, mode="r"):
        return self.open(path, mode)

    def write(self, content, path, mode="w"):
        if isinstance(content, (str, Path)):
            content = open(content, "rb")
        elif not isinstance(content, (BytesIO,)):
            content = BytesIO(content)
        self._service.get_connection().upload_fileobj(content, self._service.bucket, path)
        return path
