from fastapi import APIRouter, HTTPException

from app.models.flashcard_decks import FlashcardDeckModel
from app.schema import flashcard_deck as flashcard_deck_schema


router = APIRouter()
flashcard_deck_handler = FlashcardDeckModel()

@router.get("/{flashcard_deck_id}")
async def get_flashcard_deck(flashcard_deck_id: str):
    flashcard_deck = await flashcard_deck_handler.get(flashcard_deck_id)
    if not flashcard_deck:
        raise HTTPException(status_code=400, detail="Flashcard deck not found")
    return flashcard_deck.to_response()

@router.post("/", status_code=201)
async def create_flashcard_deck(flash_card_deck_data: flashcard_deck_schema.FlashcardDeckCreate):
    try:
        new_flashcard_deck = await flashcard_deck_handler.create(flash_card_deck_data.model_dump())
        return new_flashcard_deck.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{flashcard_deck_id}")
async def update_flashcard_deck(
    flashcard_deck_id: str, 
    flashcard_deck: flashcard_deck_schema.FlashcardDeckUpdate
):
    try:
        updated_flashcard_deck = await flashcard_deck_handler.update(
            flashcard_deck_id, 
            flashcard_deck
        )
        if not updated_flashcard_deck:
            raise HTTPException(status_code=400, detail="Flashcard deck not found or update failed")
        return updated_flashcard_deck.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{flashcard_deck_id}")
async def delete_flashcard_deck(flashcard_deck_id: str):
    deleted = await flashcard_deck_handler.delete(flashcard_deck_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Flashcard deck not found or deletion failed")
    return {"message": "Flashcard deck deleted successfully"}

# @router.get("/")
# async def get_all_flashcard_decks(
#     skip: int = 0,
#     limit: int = 10,
#     cursor: Optional[str] = None
# ):
#     try:
#         flashcard_decks_data = await flashcard_deck_handler.get_all(skip=skip, limit=limit, cursor=cursor)
#         flashcard_decks_data["items"] = [flashcard_deck.to_response() for flashcard_deck in flashcard_decks_data["items"]]
#         return flashcard_decks_data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))