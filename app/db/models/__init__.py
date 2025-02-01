from app.db.database import Base

from .auth import OtpModel
from .news import PostModel, TagsModel
from .user import UserModel

__all__ = [
    "UserModel",
    "OtpModel",
    "PostModel",
    "TagsModel",
    "Base",
]
