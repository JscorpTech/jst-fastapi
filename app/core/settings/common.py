from pathlib import Path
from typing import List

from app.core.config import *  # noqa
from app.core.env import env

BASE_DIR: Path = Path(__file__).parent.parent.parent.parent

PROJECT_NAME: str = env.str("PROJECT_NAME", "My Big Project")
VERSION: str = env.str("VERSION", "1.0.0")
BASE_URL: str = env.str("BASE_URL")

LANGUAGE: str = "uz"
LANGUAGES: List[str] = ["uz", "en", "ru"]


STORAGE_DIR: Path = BASE_DIR / "storage"
STORAGE_URL: str = env.str("STORAGE_URL", "storage")
DEFAULT_STORAGE: str = "fastx.storage.file.FileStorage"
