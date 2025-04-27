from fastapi import APIRouter, HTTPException, Depends

from app.models.flashcard_decks import FlashcardDeckModel
from app.schema import flashcard_deck as flashcard_deck_schema
from app.schema.notes import NoteDocument
from app.core.dependencies import get_current_user
from app.schema.user import UserDocument


router = APIRouter()
flashcard_deck_model = FlashcardDeckModel()

@router.get("/{flashcard_deck_id}")
async def get_flashcard_deck(flashcard_deck_id: str):
    flashcard_deck = await flashcard_deck_model.get(flashcard_deck_id)
    if not flashcard_deck:
        raise HTTPException(status_code=400, detail="Flashcard deck not found")
    return flashcard_deck

@router.get("/user")
async def get_flashcard_decks_by_user(current_user: UserDocument = Depends(get_current_user)):
    try:
        flashcard_decks_ids = current_user.flashcards
        if flashcard_decks_ids is None:
            return []
        flashcard_decks = await flashcard_deck_model.get_many(flashcard_decks_ids)
        return list(map(lambda doc: doc.to_response(), flashcard_decks))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", status_code=201)
async def create_flashcard_deck(flash_card_deck_data: flashcard_deck_schema.FlashcardDeckCreate):
    try:
        current_user = await get_current_user()
        if not current_user:
            raise HTTPException(status_code=401, detail="User not authenticated")

        new_flashcard_deck = await flashcard_deck_model.create(flash_card_deck_data.model_dump())

        await current_user.update(  
            current_user.id,
            {"$push": {"flashcards": new_flashcard_deck.id}}
        )
        return new_flashcard_deck
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/ai")
async def create_flashcard_from_note(note: NoteDocument):
    try:
        current_user = await get_current_user()
        if not current_user:
            raise HTTPException(status_code=401, detail="User not authenticated")

        flashcard_deck = await flashcard_deck_model.create_flashcard_deck_ai(note)
        if not flashcard_deck:
            raise HTTPException(status_code=400, detail="Flashcard deck not found or creation failed")
        
        await current_user.update(
            current_user.id,
            {"$push": {"flashcards": flashcard_deck.id}}
        )
        return flashcard_deck
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.put("/{flashcard_deck_id}")
async def update_flashcard_deck(
    flashcard_deck_id: str, 
    flashcard_deck: flashcard_deck_schema.FlashcardDeckUpdate
):
    try:
        updated_flashcard_deck = await flashcard_deck_model.update(
            flashcard_deck_id, 
            flashcard_deck.model_dump(exclude_none=True)
        )
        if not updated_flashcard_deck:
            raise HTTPException(status_code=400, detail="Flashcard deck not found or update failed")
        return updated_flashcard_deck
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{flashcard_deck_id}")
async def delete_flashcard_deck(flashcard_deck_id: str):
    current_user = await get_current_user()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    deleted = await flashcard_deck_model.delete(flashcard_deck_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Flashcard deck not found or deletion failed")
    
    await current_user.update(
        current_user.id,
        {"$pull": {"flashcards": flashcard_deck_id}}
    )
    return {"message": "Flashcard deck deleted successfully"}

# @router.get("/")
# async def get_all_flashcard_decks(
#     skip: int = 0,
#     limit: int = 10,
#     cursor: Optional[str] = None
# ):
#     try:
#         flashcard_decks_data = await flashcard_deck_model.get_all(skip=skip, limit=limit, cursor=cursor)
#         flashcard_decks_data["items"] = [flashcard_deck.to_response() for flashcard_deck in flashcard_decks_data["items"]]
#         return flashcard_decks_data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))