import os

from dotenv import load_dotenv, find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(usecwd=True))


class Settings(BaseSettings):

    # Environment
    ENVIRONMENT: str = Field(default="development")

    # MongoDB Config
    MONGO_DB_URI: str
    MONGO_DB_DATABASE_NAME: str = Field(default="axiom_db")

    # Authentication Config
    ACCESS_TOKEN_SECRET: str
    REFRESH_TOKEN_SECRET: str

    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int = 900
    JWT_REFRESH_TOKEN_EXPIRES: int = 604800


    model_config = SettingsConfigDict(case_sensitive=True, env_file_encoding='utf-8')
