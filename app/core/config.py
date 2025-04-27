import os

from dotenv import load_dotenv, find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(usecwd=True))


class Settings(BaseSettings):

    # App settings
    PROJECT_NAME: str = "Axiom"
    PROJECT_DESCRIPTION: str = "A FastAPI backend with authentication, database integration, and more"
    PROJECT_VERSION: str ="1.0.0"

    # Environment
    ENVIRONMENT: str = Field(default="development")

    # CORS settings
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:5174",
    ]

    # MongoDB Config
    MONGO_DB_URI: str
    MONGO_DB_DATABASE_NAME: str = Field(default="axiom_db")

    MONGO_DATABASE_USER: str = Field(default="admin")
    MONGO_DATABASE_PASSWORD: str = Field(default="password")

    # Authentication Config
    ACCESS_TOKEN_SECRET: str
    REFRESH_TOKEN_SECRET: str
    ENCRYPT_ALGORITHM: str = "HS256"

    # Firebase Config
    FIREBASE_CREDENTIALS: str
    FIREBASE_STORAGE_BUCKET: str

    ACCESS_TOKEN_EXPIRATION_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 7

    # GEMINI Config
    GEMINI_API_KEY: str

    # OPENAI Config
    OPEN_AI_API_KEY: str

    model_config = SettingsConfigDict(case_sensitive=True, env_file_encoding='utf-8')
