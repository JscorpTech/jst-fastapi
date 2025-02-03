from fastx.storage.base import BaseStorage


class S3Storage(BaseStorage):

    def __init__(self):
        super().__init__()

    def open(self, path, mode="r"):
        pass

    def read(self, path, mode="r"):
        pass

    def write(self, content, path, mode="w"):
        pass
