from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.flashcard_decks import router as flashcard_decks_router
from app.api.v1.endpoints.notes import router as notes_router
from app.api.v1.endpoints.quizzes import router as quizzes_router

router = APIRouter(prefix="/api/v1")


router.include_router(flashcard_decks_router)
router.include_router(notes_router)
router.include_router(quizzes_router)

