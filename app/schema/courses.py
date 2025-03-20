from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import IndexModel

from app.schema.collection_id.document_id import DocumentId
from app.utils.helpers import make_optional_model
from beanie import Document, Indexed


class CourseBase(BaseModel):
    user_id: ObjectId
    title: str
    description: str
    modules: List[str] = Field(default=[])


class CourseCreate(BaseModel):
    title: str
    description: str
    modules: List[str] = Field(default=[])


CourseUpdate = make_optional_model(CourseBase)


class Course(CourseBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class CourseDocument(Course, Document):
    title: Indexed(str, unique=False, name="idx_title")

    def to_response(self) -> Course:
        return Course(**self.model_dump())

    class Settings:
        name = "courses"
        bson_encoders = {ObjectId: str}

        indexes = [
            IndexModel("title", name="idx_title"),
        ]
