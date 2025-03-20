from app.db.mongo_utils import MongoCrud
from app.schema import flashcard_deck as flashcard_deck_schema


class FlashcardDeckModel(MongoCrud[flashcard_deck_schema.FlashcardDeckDocument]):
    model = flashcard_deck_schema.FlashcardDeckDocument