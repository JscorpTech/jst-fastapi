import datetime
from typing import Optional

import jwt
from fastapi import HTTPException

from app.db.models import UserModel
from fastapi_core.conf import settings


async def create_token(user: UserModel) -> dict:
    return {
        "access_token": await jwt_encode(str(user.id), "access"),
        "refresh_token": await jwt_encode(
            str(user.id),
            "refresh",
            exp=datetime.timedelta(days=settings.JWT_CONFIG["REFRESH_TOKEN_EXPIRE_MINUTES"]),
        ),
    }


async def jwt_encode(sub: str, token_type: str = "access", exp: Optional[datetime.timedelta] = None, **kwargs) -> str:
    if not exp:
        exp = datetime.timedelta(minutes=settings.JWT_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"])
    to_encode = {
        "exp": datetime.datetime.now(datetime.UTC) + exp,
        "sub": str(sub),
        "token_type": token_type,
        **kwargs,
    }
    return jwt.encode(
        to_encode,
        settings.JWT_CONFIG["SECRET"],
        algorithm=settings.JWT_CONFIG["ALGORITHM"],
    )


async def jwt_decode(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_CONFIG["SECRET"],
            algorithms=[settings.JWT_CONFIG["ALGORITHM"]],
            options={"verify_exp": True},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
