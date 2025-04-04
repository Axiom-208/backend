import os

from dotenv import load_dotenv, find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(usecwd=True))


class Settings(BaseSettings):

    # App settings
    PROJECT_NAME: str = "Axiom"
    PROJECT_DESCRIPTION: str = "A production-ready FastAPI backend with authentication, database integration, and more"
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

    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int = 900
    JWT_REFRESH_TOKEN_EXPIRES: int = 604800


    model_config = SettingsConfigDict(case_sensitive=True, env_file_encoding='utf-8')
