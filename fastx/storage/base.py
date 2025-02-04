from abc import ABC, abstractmethod
from pathlib import Path
from typing import IO, Any, Literal, Optional, TypeAlias, Union

from fastapi import Request
from sqlalchemy import Column

from fastx.conf import settings

OpenTextModeUpdating: TypeAlias = Literal[
    "r+",
    "+r",
    "rt+",
    "r+t",
    "+rt",
    "tr+",
    "t+r",
    "+tr",
    "w+",
    "+w",
    "wt+",
    "w+t",
    "+wt",
    "tw+",
    "t+w",
    "+tw",
    "a+",
    "+a",
    "at+",
    "a+t",
    "+at",
    "ta+",
    "t+a",
    "+ta",
    "x+",
    "+x",
    "xt+",
    "x+t",
    "+xt",
    "tx+",
    "t+x",
    "+tx",
    "rb+",
    "r+b",
    "+rb",
    "br+",
    "b+r",
    "+br",
    "wb+",
    "w+b",
    "+wb",
    "bw+",
    "b+w",
    "+bw",
    "ab+",
    "a+b",
    "+ab",
    "ba+",
    "b+a",
    "+ba",
    "xb+",
    "x+b",
    "+xb",
    "bx+",
    "b+x",
    "+bx",
]
OpenTextModeWriting: TypeAlias = Literal[
    "w",
    "wt",
    "tw",
    "a",
    "at",
    "ta",
    "x",
    "xt",
    "tx",
    "wb",
    "bw",
    "ab",
    "ba",
    "xb",
    "bx",
]
OpenTextModeReading: TypeAlias = Literal[
    "r",
    "rt",
    "tr",
    "U",
    "rU",
    "Ur",
    "rtU",
    "rUt",
    "Urt",
    "trU",
    "tUr",
    "Utr",
    "rb",
    "br",
    "rbU",
    "rUb",
    "Urb",
    "brU",
    "bUr",
    "Ubr",
]
OpenTextMode: TypeAlias = OpenTextModeUpdating | OpenTextModeWriting | OpenTextModeReading
_PATH: TypeAlias = Union[str, Path, Column[str]]


class BaseStorage(ABC):
    _basedir: Path

    def __init__(self) -> None:
        self._basedir: Path = settings.STORAGE_DIR
        super().__init__()

    @abstractmethod
    def download_url(self, path: _PATH, request: Optional[Request] = None) -> str:
        """
        Generate file download url
        """
        pass

    @abstractmethod
    def delete(self, path: _PATH, raise_exception: bool = False) -> None:
        pass

    @abstractmethod
    def path(self, path: _PATH) -> Union[str, Path]:
        pass

    @abstractmethod
    def open(self, path: _PATH, mode: OpenTextMode = "r") -> Optional[Union[IO[Any]]]:
        """
        Fayilni ochish
        """
        pass

    @abstractmethod
    def write(self, content: Any, path: _PATH, mode: OpenTextModeWriting = "w") -> Union[str, Path]:
        """
        Yozish
        """
        pass

    @abstractmethod
    def read(self, path: _PATH, mode: OpenTextModeReading = "r") -> Union[str]:
        """
        O'qish
        """
        pass
