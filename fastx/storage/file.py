from fastx.storage.base import BaseStorage


class FileStorage(BaseStorage):
    def __init__(self):
        super().__init__()

    def download(self, path, request=None):
        if request is None:
            raise Exception("request is required")
        if not str(path).startswith("/"):
            path = "/%s" % path
        return "%s%s%s" % (request.base_url, "storage", path)

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
