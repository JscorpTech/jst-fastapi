from abc import ABC
from abc import abstractmethod
from typing import Optional, IO, Any, Union, TypeAlias, Literal

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
]
OpenTextModeWriting: TypeAlias = Literal["w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx"]
OpenTextModeReading: TypeAlias = Literal["r", "rt", "tr", "U", "rU", "Ur", "rtU", "rUt", "Urt", "trU", "tUr", "Utr"]
OpenTextMode: TypeAlias = OpenTextModeUpdating | OpenTextModeWriting | OpenTextModeReading


class BaseStorage(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def open(self, path: str, mode: OpenTextMode) -> Optional[Union[IO[Any]]]:
        pass

    @abstractmethod
    def write(self, content: Any, path: str, mode: OpenTextModeWriting):
        pass

    @abstractmethod
    def read(self, path: str, mode: OpenTextModeReading) -> Union[str]:
        pass
