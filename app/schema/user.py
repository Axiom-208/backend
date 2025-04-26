from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from pymongo import IndexModel

from app.schema.collection_id.document_id import DocumentId
from app.utils.helpers import make_optional_model
from beanie import Document, Indexed


class Theme(str, Enum):
    light = "light"
    dark = "dark"
    system = "system"

class Language(str, Enum):
    en = "en"


class Preferences(BaseModel):
    theme: Optional[Theme] = Field(default=Theme.light, alias="theme")
    notification_email: Optional[bool] = Field(default=True, alias="notificationEmail")
    language: Optional[Language] = Field(default=Language.en, alias="language")
    study_reminder: Optional[bool] = Field(default=True, alias="studyReminder")



class UserBase(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    hashed_password: str = Field(..., alias="hashedPassword")
    email: EmailStr = Field(..., alias="email")
    username: str = Field(..., alias="username")
    is_admin: Optional[bool] = Field(default=False, alias="isAdmin")
    preferences: Optional[Preferences] = Field(default_factory=Preferences, alias="preferences")
    notes: Optional[List[str]] = Field(default=[], alias="notes")
    quizzes: Optional[List[str]] = Field(default=[], alias="quizzes")
    flashcards: Optional[List[str]] = Field(default=[], alias="flashcards")
    chapters: Optional[List[str]] = Field(default=[], alias="chapters")
    is_verify: Optional[bool] = Field(default=False, alias="isVerify")

    model_config = {
        "populate_by_name": True
    }

    # decks: List[str] = Field(default=[])
    # quizzes: List[str] = Field(default=[])
    # chapters_folders: List[str] = Field(default=[])


class UserCreate(BaseModel):
    username: str = Field(..., min_length=4, alias="username")
    email: EmailStr = Field(..., alias="email")
    password: str = Field(..., min_length=6, alias="password")
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")



UserUpdate = make_optional_model(UserBase)


class User(UserBase, DocumentId):

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class UserDocument(User, Document):
    email: Indexed(EmailStr, unique=True, name="idx_email")
    username: Indexed(str, unique=True, name="idx_username")

    def to_response(self) -> User:
        return User(**self.model_dump(by_alias=True))


    class Settings:
        name = "users"
        bson_encoders = {ObjectId: str}

        indexes = [
            IndexModel("email", unique=True, name="idx_email"),
            IndexModel("username", unique=True, name="idx_username"),
        ]
