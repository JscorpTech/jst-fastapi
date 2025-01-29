from app.core.env import env
from app.core.config import *  # noqa

PROJECT_NAME: str = env.str("PROJECT_NAME", "My Big Project")
VERSION: str = env.str("VERSION", "1.0.0")
JWT_SECRET: str = env.str("JWT_SECRET", "secret")
JWT_ALGORITHM: str = env.str("JWT_ALGORITHM", "HS256")
