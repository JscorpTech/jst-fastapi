from fastapi_core.db import Model
from sqlalchemy import Column, String, Integer


class OtpModel(Model):
    __tablename__ = "otps"

    phone = Column(String(100))
    otp = Column(Integer)
