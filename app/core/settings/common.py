from typing import List

from app.core.config import *  # noqa
from app.core.env import env

PROJECT_NAME: str = env.str("PROJECT_NAME", "My Big Project")
VERSION: str = env.str("VERSION", "1.0.0")

LANGUAGE: str = "uz"
LANGUAGES: List[str] = ["uz", "en", "ru"]
