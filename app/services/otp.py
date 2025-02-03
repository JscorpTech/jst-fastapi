import string
from random import choices
from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy import Column
from sqlalchemy.orm import Session

from app.db.database import _DB
from app.db.models import OtpModel
from app.services.sms import EskizService
from fastx.conf import settings


class OtpService:
    otp: Optional[Union[str, Column[int]]] = None
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

    def send_otp(self, phone: str):
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
                EskizService().send_sms(phone, message)  # Make sure this method is sync
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to send OTP: {e}")

    def verify_otp(self, phone: str, otp: str) -> bool:
        """Verify OTP"""
        otp_entry = self.db.query(OtpModel).filter(OtpModel.phone == phone, OtpModel.otp == otp).first()

        if not otp_entry:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        self.db.delete(otp_entry)
        self.db.commit()
        return True
