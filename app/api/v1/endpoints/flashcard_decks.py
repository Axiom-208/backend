from flask import Blueprint, jsonify, abort, request

from app.models.flashcard_decks import FlashcardDeckModel
from app.schema import flashcard_deck as flashcard_deck_schema

router = Blueprint("flashcard_decks", __name__, url_prefix="/flashcard_decks")
flashcard_deck_model = FlashcardDeckModel()


@router.route("/<string:flashcard_deck_id>", methods=["GET"])
async def get_flashcard_deck(flashcard_deck_id: str):
    flashcard_deck = await flashcard_deck_model.get(flashcard_deck_id)
    if not flashcard_deck:
        abort(400, description="Flashcard deck not found")
    return jsonify(flashcard_deck.to_response()), 200

@router.route("/", methods=["POST"])
async def create_flashcard_deck():
    try:
        flashcard_deck_data = request.get_json()
        new_flashcard_deck = await flashcard_deck_model.create_flashcard_deck(flashcard_deck_schema.FlashcardDeckCreate(**flashcard_deck_data))
        return jsonify(new_flashcard_deck.to_response()), 201
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:flashcard_deck_id>", methods=["PUT"])
async def update_flashcard_deck(flashcard_deck_id: str):
    try:
        update_data = request.get_json()
        updated_flashcard_deck = await flashcard_deck_model.update_flashcard_deck(flashcard_deck_id, flashcard_deck_schema.FlashcardDeckUpdate(**update_data))
        if not updated_flashcard_deck:
            abort(400, description="Flashcard deck not found or update failed")
        return jsonify(updated_flashcard_deck.to_response()), 200
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:flashcard_deck_id>", methods=["DELETE"])
async def delete_flashcard_deck(flashcard_deck_id: str):
    deleted = await flashcard_deck_model.delete(flashcard_deck_id)
    if not deleted:
        abort(400, description="Flashcard deck not found or deletion failed")
    return jsonify({"message": "Flashcard deck deleted successfully"}), 200

@router.route("/", methods=["GET"])
async def get_all_flashcard_decks():
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 10))
        cursor = request.args.get("cursor", None)
        flashcard_decks_data = await flashcard_deck_model.get_all(skip=skip, limit=limit, cursor=cursor)
        flashcard_decks_data["items"] = [flashcard_deck.to_response() for flashcard_deck in flashcard_decks_data["items"]]
        return jsonify(flashcard_decks_data), 200
    except Exception as e:
        abort(400, description=str(e))