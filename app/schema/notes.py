from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import IndexModel

from app.schema.collection_id.document_id import DocumentId
from app.utils.helpers import make_optional_model
from beanie import Document, Indexed


class NoteBase(BaseModel):
    module_id: ObjectId
    title: str
    topic: str
    content: str


class NoteCreate(BaseModel):
    title: str
    topic: str
    content: str


NoteUpdate = make_optional_model(NoteBase)


class Note(NoteBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class NoteDocument(Note, Document):
    title: Indexed(str, unique=False, name="idx_title")

    def to_response(self) -> Note:
        return Note(**self.model_dump())

    class Settings:
        name = "notes"
        bson_encoders = {ObjectId: str}

        indexes = [
            IndexModel("title", name="idx_title"),
        ]
