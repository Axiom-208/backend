from fastapi import APIRouter, Depends, Response, HTTPException, Cookie
from jose import jwt, JWTError

from app.auth.jwt import create_access_token, authenticate_user, create_refresh_token
from app.core.dependencies import get_settings, get_current_user
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

    # Delete any existing sessions for this user
    try:
        existing_sessions = await Session.find(Session.user_id == str(user.id)).to_list()
        for session in existing_sessions:
            await session_model.delete(str(session.id))
    except Exception as error:
        print(f"Error while deleting existing sessions: {error}")

    # Create new session
    await session_model.create_session(user_id=str(user.id), refresh_token=refresh_token)

    # Set cookies with environment-aware settings
    is_production = settings.ENVIRONMENT == "production"
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none" if is_production else "lax",
        secure=is_production,
        max_age=settings.ACCESS_TOKEN_EXPIRATION_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none" if is_production else "lax",
        secure=is_production,
        max_age=settings.REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60
    )
    return {"message": "Logged in", "data": {"username": user.username}}

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
        is_production = settings.ENVIRONMENT == "production"
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="none" if is_production else "lax",
            secure=is_production,
            max_age = settings.ACCESS_TOKEN_EXPIRATION_MINUTES * 60
        )
        return {"message": "Token refreshed"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/logout")
async def logout(response: Response, refresh_token: str = Cookie(None)):
    await Session.find_one(Session.refresh_token == refresh_token).delete()
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out", "data": True}


@router.post("/register")
async def register(user: user_schema.UserCreate, response: Response = None):
    try:
        created_user = await user_model.create_user(user)
        
        # Create tokens
        access_token = create_access_token({"sub": created_user.username})
        refresh_token = create_refresh_token({"sub": created_user.username})

        # Create session
        await session_model.create_session(user_id=str(created_user.id), refresh_token=refresh_token)

        # Set cookies with environment-aware settings
        is_production = settings.ENVIRONMENT == "production"
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="none" if is_production else "lax",
            secure=is_production,
            max_age=settings.ACCESS_TOKEN_EXPIRATION_MINUTES * 60
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="none" if is_production else "lax",
            secure=is_production,
            max_age=settings.REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60
        )

        return {"message": "User created and logged in", "data": created_user.to_response()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=user_schema.User)
async def read_current_user(current_user: user_schema.UserDocument = Depends(get_current_user)):
    return current_user.to_response()