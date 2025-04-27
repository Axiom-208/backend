from app.db.mongo_utils import MongoCrud
from app.schema import flashcard_deck as flashcard_deck_schema
from app.schema.notes import NoteDocument
from app.service.revision.ai_content_gen import get_ai_content_generator


class FlashcardDeckModel(MongoCrud[flashcard_deck_schema.FlashcardDeckDocument]):
    model = flashcard_deck_schema.FlashcardDeckDocument

    async def create_flashcard_deck_ai(self, note: NoteDocument):
        ai_content_gen = get_ai_content_generator()
        flashcards = ai_content_gen.generate_flashcards(note)

        flashcard_deck_data = {
            "flashcards": flashcards[1],
            "note_id": str(note.id)
        }

        return await self.create(flashcard_deck_data)

