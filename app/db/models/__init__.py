from .user import UserModel
from .auth import OtpModel
from .news import PostModel, TagsModel
from app.db.database import Base

__all__ = [
    "UserModel",
    "OtpModel",
    "PostModel",
    "TagsModel",
    "Base",
]
