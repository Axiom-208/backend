from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import IndexModel

from app.schema.collection_id.document_id import DocumentId
from app.utils.helpers import make_optional_model
from beanie import Document, Indexed


class ModuleBase(BaseModel):
    course_id: ObjectId
    title: str
    description: str
    notes: List[str] = Field(default=[])
    flashcard_decks: List[str] = Field(default=[])
    video_chapters: List[str] = Field(default=[])
    quizzes: List[str] = Field(default=[])


class ModuleCreate(BaseModel):
    title: str
    description: str
    notes: List[str] = Field(default=[])
    flashcard_decks: List[str] = Field(default=[])
    video_chapters: List[str] = Field(default=[])
    quizzes: List[str] = Field(default=[])


ModuleUpdate = make_optional_model(ModuleBase)


class Module(ModuleBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class ModuleDocument(Module, Document):
    title: Indexed(str, unique=False, name="idx_title")

    def to_response(self) -> Module:
        return Module(**self.model_dump())

    class Settings:
        name = "modules"
        bson_encoders = {ObjectId: str}

        indexes = [
            IndexModel("title", name="idx_title"),
        ]