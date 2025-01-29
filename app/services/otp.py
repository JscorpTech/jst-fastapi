from random import choices
import string
from fastapi_core.conf import settings
from app.services import EskizService
from app.exceptions import APIException


class OtpService:
    def __init__(self):
        pass

    async def _generate_otp(self) -> str:
        if settings.OTP_DEBUG:
            return "1" * int(settings.OTP_COUNT)
        return "".join(choices(string.digits, k=settings.OTP_COUNT))

    async def _generate_message(self) -> str:
        otp: str = await self._generate_otp()
        return settings.OTP_MESSAGE % {"otp": otp}

    async def send_otp(self, phone: str):
        try:
            if settings.OTP_CONSOLE:
                return print(await self._generate_message())
            return await EskizService().send_sms(phone, await self._generate_message())
        except Exception:
            raise APIException(status_code=400, detail="Failed to send OTP")

    async def verify_otp(self, phone: str, otp: str):
        pass

    async def delete_otp(self, phone: str):
        pass
