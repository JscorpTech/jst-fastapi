from sqlalchemy import Column, Integer, String

from fastapi_core.db import Model


class OtpModel(Model):
    __tablename__ = "otps"

    phone = Column(String(100))
    otp = Column(Integer)
