from fastapi import FastAPI
from app.api.base_router import router as base_router
from app.db.database import MongoDBClient
from app.schema.quiz import QuizDocument
from app.schema.notes import NoteDocument
from app.schema.flashcard_deck import FlashcardDeckDocument
import asyncio


mongo_uri = ""
mongo = MongoDBClient(mongo_uri=mongo_uri, database_name="axiom_db", document_models=[NoteDocument, QuizDocument, FlashcardDeckDocument])


async def lifespan(app: FastAPI):
    await mongo.init_db()
    yield
    await mongo.close_db()


app = FastAPI(lifespan=lifespan)


app.include_router(base_router)
