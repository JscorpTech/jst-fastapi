from sqlalchemy import Column, Integer, String

from fastx.db import Model


class OtpModel(Model):
    __tablename__ = "otps"

    phone = Column(String(100))
    otp = Column(Integer)
