import os

from dotenv import load_dotenv  # noqa

load_dotenv()  # noqa

from app.core.config import *  # noqa

PROJECT_NAME: str = os.getenv("PROJECT_NAME", "My Big Project")
VERSION: str = os.getenv("VERSION", "1.0.0")
JWT_SECRET: str = os.getenv("JWT_SECRET", "secret")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
