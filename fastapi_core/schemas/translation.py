from pydantic import BaseModel, BeforeValidator
from typing import Optional, Annotated
from fastapi_core.utils.translation import translate


class TranslatedField(BaseModel):
    uz: Optional[str]
    en: Optional[str] = None
    ru: Optional[str] = None


AutoTranslatedField = Annotated[str, BeforeValidator(translate)]
