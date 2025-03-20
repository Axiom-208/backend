from typing import Optional, List

from beanie import Document
from pydantic import BaseModel, Field

from app.schema.collection_id.document_id import DocumentId
from app.utils.helpers import make_optional_model


class QuestionOption(BaseModel):
    text: str
    is_correct: bool

class Question(BaseModel):
    options: List[QuestionOption]

class QuizBase(BaseModel):
    topic: str
    questions: Optional[List[str]] = Field(default=[])
    score: Optional[float] = Field(default=0.0)


class QuizCreate(QuizBase):
    pass


QuizUpdate = make_optional_model(QuizBase)


class Quiz(QuizBase, DocumentId):

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class QuizDocument(Quiz, Document):

    class Settings:
        name = "quiz"