from abc import ABC
from abc import abstractmethod
from typing import Optional, IO, Any, Union, TypeAlias, Literal
from fastx.conf import settings
from pathlib import Path
from fastapi import Request

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


class BaseStorage(ABC):
    _basedir: Path

    def __init__(self) -> None:
        self._basedir: Path = settings.STORAGE_DIR
        super().__init__()

    @abstractmethod
    def download(self, path: Union[str, Path], request: Optional[Request] = None) -> str:
        pass

    @abstractmethod
    def path(self, path: Union[str, Path]) -> Union[str, Path]:
        pass

    @abstractmethod
    def open(self, path: Union[str, Path], mode: OpenTextMode = "r") -> Optional[Union[IO[Any]]]:
        """
        Fayilni ochish
        """
        pass

    @abstractmethod
    def write(self, content: Any, path: Union[str, Path], mode: OpenTextModeWriting = "w") -> Union[str, Path]:
        """
        Yozish
        """
        pass

    @abstractmethod
    def read(self, path: Union[str, Path], mode: OpenTextModeReading = "r") -> Union[str]:
        """
        O'qish
        """
        pass
