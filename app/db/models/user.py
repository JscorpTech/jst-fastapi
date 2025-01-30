from fastapi_core.db import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class UserModel(Model):
    __tablename__ = "users"

    phone = Column(String(255))
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), nullable=True)
    tokens = relationship("UserTokenModel", back_populates="user")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserTokenModel(Model):
    __tablename__ = "user_tokens"
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String(500))
    user = relationship("UserModel", back_populates="tokens")
