from random import choices
import string
from fastapi_core.conf import settings
from app.services import EskizService
from app.exceptions import APIException
from app.db.models import OtpModel


class OtpService:
    otp: int | None = None

    def __init__(self):
        pass

    async def _generate_otp(self) -> str:
        """Generate OTP"""
        if settings.OTP_DEBUG:
            return "1" * int(settings.OTP_COUNT)
        return "".join(choices(string.digits, k=settings.OTP_COUNT))

    async def _generate_message(self) -> str:
        """Generate OTP message"""
        self.otp: str = await self._generate_otp()
        return settings.OTP_MESSAGE % {"otp": self.otp}

    async def send_otp(self, phone: str):
        """Send OTP"""
        try:
            message = await self._generate_message()
            await OtpModel.create(phone=phone, otp=self.otp)
            if settings.OTP_CONSOLE:
                return print(message)
            await EskizService().send_sms(phone, message)
        except Exception as e:
            raise APIException(status_code=400, detail=f"Failed to send OTP: {e}")

    async def verify_otp(self, phone: str, otp: str) -> bool:
        """Verify OTP"""
        otp_queryset = OtpModel.filter(phone=phone, otp=otp)
        if not await otp_queryset.exists():
            raise APIException(status_code=400, detail="Invalid OTP")
        await otp_queryset.delete()
        return True
