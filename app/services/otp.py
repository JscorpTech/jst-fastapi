import string
from random import choices
from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy import Column
from sqlalchemy.orm import Session

from app.db.database import _DB
from app.db.models import OtpModel
from fastx.conf import settings
from fastx.exceptions import APIException
from app import tasks

_OTP = Optional[Union[str, Column[int]]]


class OtpService:
    otp: _OTP = None
    db: Session
    phone: str | None = None

    def __init__(self, db: _DB):
        self.db = db

    def _generate_otp(self) -> Union[str, Column[int]]:
        """Generate OTP"""
        if query := self.db.query(OtpModel).filter(OtpModel.phone == self.phone).first():
            return query.otp
        if settings.OTP_DEBUG:
            return "1" * int(settings.OTP_COUNT)
        return "".join(choices(string.digits, k=settings.OTP_COUNT))

    def _generate_message(self) -> str:
        """Generate OTP message"""
        self.otp = self._generate_otp()
        return settings.OTP_MESSAGE % {"otp": self.otp}

    def send_otp(self, phone: str) -> _OTP:
        """Send OTP"""
        try:
            self.phone = phone
            message = self._generate_message()
            otp = OtpModel(phone=phone, otp=self.otp)
            self.db.add(otp)
            self.db.commit()  # Commit is sync, no need for await here
            if settings.OTP_CONSOLE:
                print(message)
            else:
                tasks.send_message.delay(phone=phone, message=message)
            return self.otp
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to send OTP: {e}")

    def verify_otp(self, phone: str, otp: Union[str, int]) -> bool:
        """Verify OTP"""
        otp_entry = self.db.query(OtpModel).filter(OtpModel.phone == phone, OtpModel.otp == otp).first()

        if not otp_entry:
            raise APIException(APIException.VALIDATION_ERROR, data={"code": APIException.INVALID_CODE})

        self.db.delete(otp_entry)
        self.db.commit()
        return True
