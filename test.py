from pydantic import BaseModel, BeforeValidator
from typing import Annotated, Generic, TypeVar, Literal
from pyinstrument import Profiler
import time

p = Profiler()
p.start()

T = TypeVar("T")


class Unique(Generic[T]):

    def __class_getitem__(cls, params):
        def validate(v):
            return v

        print(params[1].__args__[0])
        return Annotated[str, BeforeValidator(validate)]


class User(BaseModel):
    phone: Unique[int, Literal["name"]]


def test():
    user = User(phone="salom")
    print(user)
    time.sleep(2)


test()
p.stop()
p.print()
