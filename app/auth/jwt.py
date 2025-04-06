from fastapi import Cookie, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.core.dependencies import get_settings
from app.models.user import UserModel
from app.auth.utils import verify_password


settings = get_settings()
user_model = UserModel()

SECRET_KEY = settings.ACCESS_TOKEN_SECRET
REFRESH_SECRET_KEY = settings.REFRESH_TOKEN_SECRET
ALGORITHM = settings.ENCRYPT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRATION_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRATION_DAYS



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(email: str, password: str):
    user = await user_model.get_user_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# THIS FUNCTION IS NOT BEING USED ATM. THERE IS ANOTHER VERSION AT app/core/dependencies.py
async def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")