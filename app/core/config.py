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
    MONGO_DB_DATABASE_NAME: str



    model_config = SettingsConfigDict(case_sensitive=True, env_file_encoding='utf-8')


    # class Config:
    #     case_sensitive = True
    #     env_file = ".env"


settings = Settings()

