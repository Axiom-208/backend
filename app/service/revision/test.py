from app.service.revision.quiz import QuizHandler
from app.models.quiz import QuizModel
from app.service.revision.ai_content_gen import AIContentGenerator
from app.service.revision.flashcard_deck import FlashcardDeckHandler
from app.service.revision.notes import NoteHandler
from app.schema.quiz import QuizDocument
from app.schema.notes import NoteDocument, NoteCreate
from app.schema.flashcard_deck import FlashcardDeckDocument

import tracemalloc
import asyncio
from app.db.database import MongoDBClient

mongo_uri = "mongodb+srv://lcfaria:200805Lf.@cluster0.5imi7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = MongoDBClient(mongo_uri=mongo_uri, database_name="axiom_db", document_models=[NoteDocument, QuizDocument, FlashcardDeckDocument])


async def test_quiz_handler():
    # Example test for QuizHandler
    quiz_model = QuizModel()
    quiz = await quiz_model.get("67e5ddbddb7239c7f0fa67af")
    quiz_handler = QuizHandler()
    score, wrong = await quiz_handler.grade_quiz(quiz, [1, 2, 3, 4, 5])
    print(score, wrong)

def test_ai_content_generator():
    # Example test for AIContentGenerator
    ai_generator = AIContentGenerator()
    result = ai_generator.some_method() 
    assert result == "expected_result"  

async def test_flashcard_deck_handler(note):
    # Example test for FlashcardDeckHandler
    flashcard_handler = FlashcardDeckHandler()
    result = await flashcard_handler.create_flashcard_deck_ai(note = note)
    print(result)

async def test_note_handler():
    # Example test for NoteHandler
    note_handler = NoteHandler()
    path = "app\\service\\revision\\cyber.pdf"
    title = "Cyber Security"
    topic = "Security"
    result = await note_handler.create_from_file(path, title, topic)
    print(result)
    return result

async def main():
    await mongo.init_db()
    await test_quiz_handler()
    
asyncio.run(main())
