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
    theme: Optional[Theme] = Field(default=Theme.light)
    notification_email: Optional[bool] = Field(default=True)
    language: Optional[Language] = Field(default=Language.en)
    study_reminder: Optional[bool] = Field(default=True)


class UserBase(BaseModel):
    first_name: str
    last_name: str
    hashed_password: str
    email: EmailStr
    username: str
    is_admin: Optional[bool] = Field(default=False)
    preferences: Optional[Preferences] = Field(default_factory=Preferences)
    courses: Optional[List[str]] = Field(default=[])
    is_verify: Optional[bool] = Field(default=False)


    # decks: List[str] = Field(default=[])
    # quizzes: List[str] = Field(default=[])
    # chapters_folders: List[str] = Field(default=[])


class UserCreate(BaseModel):
    username: str = Field(..., min_length=4)
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: str
    last_name: str


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
        return User(**self.model_dump())

    class Settings:
        name = "users"
        bson_encoders = {ObjectId: str}

        indexes = [
            IndexModel("email", unique=True, name="idx_email"),
            IndexModel("username", unique=True, name="idx_username"),
        ]
