from functools import lru_cache

from app.core.config import Settings
from app.db.database import MongoDBClient
from app.schema.flashcard_deck import FlashcardDeckDocument
from app.schema.quiz import QuizDocument
from app.schema.user import UserDocument


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
            QuizDocument
        ]
    )
