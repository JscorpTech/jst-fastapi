from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator

from fastx.utils import generate_link
from fastx.utils.translation import translate

FileField = Annotated[str, BeforeValidator(generate_link)]
AutoTranslatedField = Annotated[str, BeforeValidator(translate)]


class TranslatedField(BaseModel):
    uz: Optional[str]
    en: Optional[str] = None
    ru: Optional[str] = None
