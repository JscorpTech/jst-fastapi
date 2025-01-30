from fastapi import security as _security, Depends, HTTPException
from app.api.auth.services import auth as _services
from app.db.models import UserModel
from app.db.database import _DB

oauth2_scheme = _security.OAuth2PasswordBearer(tokenUrl="auth/login/")


async def get_user(db: _DB, token: str = Depends(oauth2_scheme)):
    user = await _services.jwt_decode(token)
    user = db.query(UserModel).filter(UserModel.id == user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
