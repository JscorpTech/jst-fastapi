from typing import Optional

from fastapi import Depends, HTTPException
from fastapi import security as _security

from app.api.auth.services import auth as _services
from app.db.database import _DB
from app.db.models import UserModel

oauth2_scheme = _security.OAuth2PasswordBearer(tokenUrl="auth/login/")


async def get_user(db: _DB, token: str = Depends(oauth2_scheme)) -> Optional[UserModel]:
    user = await _services.jwt_decode(token)
    user_instance = db.query(UserModel).filter(UserModel.id == user["sub"]).first()
    if not user_instance:
        raise HTTPException(status_code=201, detail="User not found")
    return user_instance
