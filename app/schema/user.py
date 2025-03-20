from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from pymongo import IndexModel

from app.schema.collection_id.document_id import DocumentId
from app.utils.helpers import make_optional_model
from beanie import Document, Indexed


class Preferences(BaseModel):
    pass

class UserBase(BaseModel):
    first_name: str
    last_name: str
    hashed_password: str
    email: EmailStr
    username: str
    preferences: Optional[Preferences] = None
    decks: List[str] = Field(default=[])
    quizzes: List[str] = Field(default=[])
    chapters_folders: List[str] = Field(default=[])


class UserCreate(UserBase):
    pass


UserUpdate = make_optional_model(UserBase)


class User(UserBase, DocumentId):

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class UserDocument(User, Document):
    email: Indexed(EmailStr, unique=True, name="idx_email")


    class Settings:
        name = "users"
        bson_encoders = {ObjectId: str}

        indexes = [
            IndexModel("email", unique=True, name="idx_email"),
        ]
