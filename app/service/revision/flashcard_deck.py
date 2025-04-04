from app.schema.flashcard_deck import FlashcardDeckDocument, Flashcard
from app.models.flashcard_decks import FlashcardDeckModel
from app.schema.notes import NoteDocument
from app.service.revision.ai_content_gen import AIContentGenerator
import json

class FlashcardDeckHandler(FlashcardDeckModel):
    def __init__(self):
        self.ai_content_gen = AIContentGenerator()

    async def create_flashcard_deck_ai(self, note: NoteDocument):
        flashcards = self.ai_content_gen.generate_flashcards(note)


        flashcard_deck_data = {
            "flashcards": flashcards[1],
            "note_id": str(note.id)
        }

        return await self.create(flashcard_deck_data)