from flask import Blueprint, jsonify, abort, request
from fastapi import APIRouter, HTTPException
from app.models.notes import NoteModel
from app.schema import notes as note_schema

from app.service.revision.notes import NoteHandler

router = APIRouter(prefix="/notes", tags=["notes"])
note_handler = NoteHandler()

@router.get("/{note_id}")
async def get_note(note_id: str):
    note = await note_handler.get(note_id)
    if not note:
        raise HTTPException(status_code=400, detail="Note not found")
    return note.to_response()

@router.post("/file", status_code=201)
async def create_note(file_path: str, title: str, topic: str):
    try:
        new_note = await note_handler.create_from_file(file_path, title, topic)
        return new_note.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{note_id}")
async def update_note(note_id: str, note: note_schema.NoteUpdate):
    try:
        updated_note = await note_handler.update(note_id, note)
        if not updated_note:
            raise HTTPException(status_code=400, detail="Note not found or update failed")
        return updated_note.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{note_id}")
async def delete_note(note_id: str):
    deleted = await note_handler.delete(note_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Note not found or deletion failed")
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