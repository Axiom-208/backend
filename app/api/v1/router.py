from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.courses import router as courses_router
from app.api.v1.endpoints.flashcard_decks import router as flashcard_decks_router
from app.api.v1.endpoints.modules import router as modules_router
from app.api.v1.endpoints.quizzes import router as quizzes_router
from app.api.v1.endpoints.video_chapter import router as video_chapters_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(courses_router, prefix="/courses", tags=["Course"])
router.include_router(flashcard_decks_router, prefix="/decks", tags=["Flashcard Deck"])
router.include_router(modules_router, prefix="/modules", tags=["Module"])
router.include_router(quizzes_router, prefix="/quizzes", tags=["Quiz"])
router.include_router(video_chapters_router, prefix="/chapters", tags=["Video Chapter"])