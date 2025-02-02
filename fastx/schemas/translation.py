from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator

from fastx.utils.translation import translate


class TranslatedField(BaseModel):
    uz: Optional[str]
    en: Optional[str] = None
    ru: Optional[str] = None


AutoTranslatedField = Annotated[str, BeforeValidator(translate)]
