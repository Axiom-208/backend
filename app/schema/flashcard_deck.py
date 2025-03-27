from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field

from app.schema.collection_id.document_id import DocumentId
from app.utils.helpers import make_optional_model


class Flashcard(BaseModel):
    front: str
    back: str


class FlashcardDeckBase(BaseModel):
    flashcards: Optional[List[Flashcard]] = Field(default=[])
    note_id: str


class FlashcardDeckCreate(FlashcardDeckBase):
    pass


FlashcardDeckUpdate = make_optional_model(FlashcardDeckBase)

class FlashcardDeck(FlashcardDeckBase, DocumentId):

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class FlashcardDeckDocument(FlashcardDeck, Document):

    class Settings:
        name = "decks"