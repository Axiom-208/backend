from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any

from app.models.quiz import QuizModel
from app.schema import quiz as quiz_schema

router = APIRouter(prefix="/quizzes", tags=["quizzes"])
quiz_model = QuizModel()

@router.get("/{quiz_id}")
async def get_quiz(quiz_id: str):
    quiz = await quiz_model.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=400, detail="Quiz not found")
    return quiz.to_response()

@router.post("/", status_code=201)
async def create_quiz(quiz_data: quiz_schema.QuizCreate):
    try:
        new_quiz = await quiz_model.create_quiz(quiz_data)
        return new_quiz.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{quiz_id}")
async def update_quiz(quiz_id: str, update_data: quiz_schema.QuizUpdate):
    try:
        updated_quiz = await quiz_model.update_quiz(quiz_id, update_data)
        if not updated_quiz:
            raise HTTPException(status_code=400, detail="Quiz not found or update failed")
        return updated_quiz.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{quiz_id}")
async def delete_quiz(quiz_id: str):
    deleted = await quiz_model.delete(quiz_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Quiz not found or deletion failed")
    return {"message": "Quiz deleted successfully"}

@router.get("/")
async def get_all_quizzes(
    skip: int = 0,
    limit: int = 10,
    cursor: Optional[str] = None
):
    try:
        quizzes_data = await quiz_model.get_all(skip=skip, limit=limit, cursor=cursor)
        quizzes_data["items"] = [quiz.to_response() for quiz in quizzes_data["items"]]
        return quizzes_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
