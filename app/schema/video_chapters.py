from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl
from pymongo import IndexModel

from app.schema.collection_id.document_id import DocumentId
from app.utils.helpers import make_optional_model
from beanie import Document, Indexed


class VideoChapterBase(BaseModel):
    module_id: str
    title: str
    video_url: HttpUrl
    start_time: int
    end_time: int
    transcript: Optional[str] = None


class VideoChapterCreate(BaseModel):
    title: str
    video_url: HttpUrl
    start_time: int
    end_time: int
    transcript: Optional[str] = None


VideoChapterUpdate = make_optional_model(VideoChapterBase)


class VideoChapter(VideoChapterBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class VideoChapterDocument(VideoChapter, Document):
    title: Indexed(str, unique=False, name="idx_title")

    def to_response(self) -> VideoChapter:
        return VideoChapter(**self.model_dump())

    class Settings:
        name = "video_chapters"
        bson_encoders = {ObjectId: str}

        indexes = [
            IndexModel("title", name="idx_title"),
        ]
