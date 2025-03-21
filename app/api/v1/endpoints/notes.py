from flask import Blueprint, jsonify, abort, request

from app.models.notes import NoteModel
from app.schema import note as note_schema

router = Blueprint("notes", __name__, url_prefix="/notes")
note_model = NoteModel()

@router.route("/<string:note_id>", methods=["GET"])
async def get_note(note_id: str):
    note = await note_model.get(note_id)
    if not note:
        abort(400, description="Note not found")
    return jsonify(note.to_response()), 200

@router.route("/", methods=["POST"])
async def create_note():
    try:
        note_data = request.get_json()
        new_note = await note_model.create_note(note_schema.NoteCreate(**note_data))
        return jsonify(new_note.to_response()), 201
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:note_id>", methods=["PUT"])
async def update_note(note_id: str):
    try:
        update_data = request.get_json()
        updated_note = await note_model.update_note(note_id, note_schema.NoteUpdate(**update_data))
        if not updated_note:
            abort(400, description="Note not found or update failed")
        return jsonify(updated_note.to_response()), 200
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:note_id>", methods=["DELETE"])
async def delete_note(note_id: str):
    deleted = await note_model.delete(note_id)
    if not deleted:
        abort(400, description="Note not found or deletion failed")
    return jsonify({"message": "Note deleted successfully"}), 200

@router.route("/", methods=["GET"])
async def get_all_notes():
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 10))
        cursor = request.args.get("cursor", None)
        notes_data = await note_model.get_all(skip=skip, limit=limit, cursor=cursor)
        notes_data["items"] = [note.to_response() for note in notes_data["items"]]
        return jsonify(notes_data), 200
    except Exception as e:
        abort(400, description=str(e))