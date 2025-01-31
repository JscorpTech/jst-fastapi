from pydantic import BaseModel
from typing import Optional


class TranslationSchema(BaseModel):
    uz: Optional[str]
    en: Optional[str] = None
    ru: Optional[str] = None
