import json
from functools import lru_cache

from fastapi import HTTPException, Cookie
from jose import jwt, JWTError
from starlette import status

from app.core.config import Settings
from app.db.database import MongoDBClient
from app.schema.flashcard_deck import FlashcardDeckDocument
from app.schema.quiz import QuizDocument
from app.schema.session import Session
from app.schema.user import UserDocument
from app.models.user import UserModel


user_model = UserModel()

@lru_cache()
def get_settings():
    return Settings()


@lru_cache()
def get_mongo_client():

    settings = Settings()

    return MongoDBClient(
        mongo_uri=settings.MONGO_DB_URI,
        database_name=settings.MONGO_DB_DATABASE_NAME,
        document_models=[
            UserDocument,
            FlashcardDeckDocument,
            QuizDocument,
            Session
        ]
    )


async def get_current_user(access_token: str = Cookie(None)) -> UserDocument:

    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")

    try:
        settings = get_settings()
        payload = jwt.decode(access_token, settings.ACCESS_TOKEN_SECRET, algorithms=[settings.ENCRYPT_ALGORITHM])

        print(payload)

        username: str = payload.get("sub")

        print(username)

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    user = await user_model.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

def get_service_account_credentials():
    settings = get_settings()
    credentials = json.loads(settings.FIREBASE_CREDENTIALS)
    credentials["private_key"] = credentials["private_key"].replace("\\n", "\n")
    return credentials