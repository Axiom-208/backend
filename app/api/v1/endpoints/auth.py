from fastapi import APIRouter, Depends, Response, HTTPException, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app.auth.jwt import create_access_token, authenticate_user, create_refresh_token
from app.core.dependencies import get_settings
from app.models.session import SessionModel
from app.schema import user as user_schema
from app.models.user import UserModel
from app.schema.auth import LoginRequest
from app.schema.session import Session



router = APIRouter()
user_model = UserModel()
session_model = SessionModel()
settings = get_settings()


@router.post("/login")
async def login(payload: LoginRequest, response: Response = None):
    user = await authenticate_user(email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    try:
        existing_session = await Session.find_one(Session.user_id == user.id)
        if existing_session:
            await session_model.delete(str(existing_session.id))
    except Exception as error:
        print(f"Error while deleting existing session: {error}")

    await session_model.create_session(user_id=str(user.id), refresh_token=refresh_token)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=False
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="Lax",
        secure=False
    )
    return {"message": "Logged in"}

@router.post("/refresh")
async def refresh(response: Response, refresh_token: str = Cookie(None)):
    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        session = await Session.find_one(Session.refresh_token == refresh_token)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")

        # Issue new access token
        new_access_token = create_access_token({"sub": username})
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="Lax",
            secure=False
        )
        return {"message": "Token refreshed"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/logout")
async def logout(response: Response, refresh_token: str = Cookie(None)):
    await Session.find_one(Session.refresh_token == refresh_token).delete()
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}


@router.post("/register")
async def register(user: user_schema.UserCreate):
    try:
        created_user = await user_model.create_user(user)
        return {"message": "User created", "data": created_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))