from app.core.env import env

OTP_MESSAGE: str = env.str("OTP_MESSAGE", "Your OTP is %(otp)s")
SMS_API_URL: str = env.str("SMS_API_URL", "https://notify.eskiz.uz/api")
SMS_LOGIN: str = env.str("SMS_LOGIN", "admin@gmail.com")
SMS_PASSWORD: str = env.str("SMS_PASSWORD", "password")
OTP_CONSOLE: bool = env.bool("OTP_CONSOLE", False)
OTP_DEBUG: bool = env.bool("OTP_DEBUG", False)
OTP_COUNT: int = env.int("OTP_COUNT", 4)
