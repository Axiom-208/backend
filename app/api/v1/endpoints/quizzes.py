from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any, List

from app.service.revision.quiz import QuizHandler
from app.schema import quiz as quiz_schema
from app.schema.notes import NoteDocument
from app.core.dependencies import get_current_user
from app.schema.user import UserDocument

router = APIRouter()
quiz_model = QuizHandler()

@router.get("/{quiz_id}")
async def get_quiz(quiz_id: str):
    quiz = await quiz_model.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=400, detail="Quiz not found")
    return quiz.to_response()

@router.get("/user", response_model=List[quiz_schema.Quiz], response_model_by_alias=True)
async def get_quizzes_by_user(current_user: UserDocument = Depends(get_current_user)):
    try:
        quizzes_ids = current_user.quizzes
        if quizzes_ids is None:
            return []
        quizzes = await quiz_model.get_many(quizzes_ids)
        return list(map(lambda doc: doc.to_response(), quizzes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
async def create_quiz(quiz_data: quiz_schema.QuizCreate):
    try:
        current_user = await get_current_user()
        if not current_user:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        new_quiz = await quiz_model.create(quiz_data.model_dump())

        await current_user.update(
            current_user.id,
            {"$push": {"quizzes": new_quiz.id}}
        )

        return new_quiz.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/ai")
async def create_quiz_from_note(note: NoteDocument):
    try:
        current_user = await get_current_user()
        if not current_user:
            raise HTTPException(status_code=401, detail="User not authenticated")

        quiz = await quiz_model.create_quiz(note)
        if not quiz:
            raise HTTPException(status_code=400, detail="Quiz not found or creation failed")
        
        await current_user.update(
            current_user.id,
            {"$push": {"quizzes": quiz.id}}
        )
        return quiz.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{quiz_id}")
async def update_quiz(quiz_id: str, update_data: quiz_schema.QuizUpdate):
    try:
        updated_quiz = await quiz_model.update(quiz_id, update_data.model_dump(exclude_none=True))
        if not updated_quiz:
            raise HTTPException(status_code=400, detail="Quiz not found or update failed")
        return updated_quiz.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{quiz_id}")
async def delete_quiz(quiz_id: str):
    current_user = await get_current_user()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    deleted = await quiz_model.delete(quiz_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Quiz not found or deletion failed")
    
    await current_user.update(
        current_user.id,
        {"$pull": {"quizzes": quiz_id}}
    )
    return {"message": "Quiz deleted successfully"}

@router.get("/all")
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
