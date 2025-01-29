import jwt
import datetime
from fastapi_core.conf import settings
from app.db.models import UserModel


async def create_token(user: UserModel) -> dict:
    return {
        "access_token": await jwt_encode(user.id, "access"),
        "refresh_token": await jwt_encode(
            user.id,
            "refresh",
            exp=datetime.timedelta(
                days=settings.JWT_CONFIG["REFRESH_TOKEN_EXPIRE_MINUTES"]
            ),
        ),
    }


async def jwt_encode(
    sub: str, token_type: str = "access", exp: datetime.timedelta = None, **kwargs
) -> str:
    if not exp:
        exp = datetime.timedelta(
            minutes=settings.JWT_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"]
        )
    to_encode = {
        "exp": datetime.datetime.now(datetime.UTC) + exp,
        "sub": sub,
        "token_type": token_type,
        **kwargs,
    }
    return jwt.encode(
        to_encode,
        settings.JWT_CONFIG["SECRET"],
        algorithm=settings.JWT_CONFIG["ALGORITHM"],
    )


async def jwt_decode(token: str) -> dict:
    pass
