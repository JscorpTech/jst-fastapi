from fastx.storage.base import BaseStorage, OpenTextModeWriting, OpenTextModeReading, OpenTextMode
from typing import Optional, Any, Union, IO


class FileStorage(BaseStorage):
    _basedir: str

    def __init__(self):
        super().__init__()

    def open(self, path: str, mode: OpenTextMode = "r") -> Optional[Union[IO[Any]]]:
        with open(path, mode) as file:
            return file

    def write(self, content: Any, path: str, mode: OpenTextModeWriting = "w") -> Union[str]:
        with open(path, mode) as file:
            file.write(content)
        return path

    def read(self, path: str, mode: OpenTextModeReading = "r") -> Union[str]:
        with open(path, mode) as file:
            return file.read()


obj = FileStorage()
obj.open("salom", "+at")
