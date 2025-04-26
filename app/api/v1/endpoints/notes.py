from fastapi import APIRouter, HTTPException, Depends
from app.models.notes import NoteModel
from app.schema import notes as note_schema
from app.core.dependencies import get_current_user
from app.schema.user import UserDocument

from app.service.revision.notes import NoteHandler

router = APIRouter(prefix="/notes", tags=["notes"])
note_handler = NoteHandler()

@router.get("/{note_id}")
async def get_note(note_id: str):
    note = await note_handler.get(note_id)
    if not note:
        raise HTTPException(status_code=400, detail="Note not found")
    return note.to_response()

@router.get("/user")
async def get_note_by_user(current_user: UserDocument =  Depends(get_current_user)):
    try:
        notes = current_user.notes
        return [note.to_response() for note in notes]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/file", status_code=201)
async def create_note(file_path: str, title: str, topic: str):
    try:
        current_user = await get_current_user()
        if not current_user:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        new_note = await note_handler.create_from_file(file_path, title, topic)

        await current_user.update(
            current_user.id,
            {"$push": {"notes": new_note.id}}
        )

        return new_note.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/", status_code=201)
async def create_note(note: note_schema.NoteCreate):
    try:    
        current_user = await get_current_user()
        if not current_user:
            raise HTTPException(status_code=401, detail="User not authenticated")

        new_note = await note_handler.create(note.model_dump())
        await current_user.update(
            current_user.id,
            {"$push": {"notes": new_note.id}}
        )
        return new_note.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{note_id}")
async def update_note(note_id: str, note: note_schema.NoteUpdate):
    try:
        updated_note = await note_handler.update(note_id, note.model_dump(exclude_none=True))
        if not updated_note:
            raise HTTPException(status_code=400, detail="Note not found or update failed")
        return updated_note.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{note_id}")
async def delete_note(note_id: str):
    current_user = await get_current_user()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    deleted = await note_handler.delete(note_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Note not found or deletion failed")
    
    await current_user.update(
        current_user.id,
        {"$pull": {"notes": note_id}}
    )
    return {"message": "Note deleted successfully"}

# @router.get("/", methods=["GET"])
# async def get_all_notes():
#     try:
#         skip = int(request.args.get("skip", 0))
#         limit = int(request.args.get("limit", 10))
#         cursor = request.args.get("cursor", None)
#         notes_data = await note_handler.get_all(skip=skip, limit=limit, cursor=cursor)
#         notes_data["items"] = [note.to_response() for note in notes_data["items"]]
#         return jsonify(notes_data), 200
#     except Exception as e:
#         abort(400, description=str(e))