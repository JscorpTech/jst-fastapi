from typing import Annotated, Optional, TypeAlias

from pydantic import BaseModel, BeforeValidator, Field

from fastx.utils import generate_link
from fastx.utils.translation import translate

_FILE: TypeAlias = Annotated[str, BeforeValidator(generate_link)]
_AUTOTRANSLATE: TypeAlias = Annotated[str, BeforeValidator(translate)]

_PHONE: TypeAlias = Annotated[str, Field(max_length=12, min_length=12)]
_PASSWORD: TypeAlias = Annotated[str, Field(min_length=8, max_length=100)]


class TranslatedField(BaseModel):
    uz: Optional[str]
    en: Optional[str] = None
    ru: Optional[str] = None
