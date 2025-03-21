from flask import Blueprint, jsonify, abort, request

from app.models.quiz import QuizModel
from app.schema import quiz as quiz_schema

router = Blueprint("quizzes", __name__, url_prefix="/quizzes")
quiz_model = QuizModel()


@router.route("/<string:quiz_id>", methods=["GET"])
async def get_quiz(quiz_id: str):
    quiz = await quiz_model.get(quiz_id)
    if not quiz:
        abort(400, description="Quiz not found")
    return jsonify(quiz.to_response()), 200

@router.route("/", methods=["POST"])
async def create_quiz():
    try:
        quiz_data = request.get_json()
        new_quiz = await quiz_model.create_quiz(quiz_schema.QuizCreate(**quiz_data))
        return jsonify(new_quiz.to_response()), 201
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:quiz_id>", methods=["PUT"])
async def update_quiz(quiz_id: str):
    try:
        update_data = request.get_json()
        updated_quiz = await quiz_model.update_quiz(quiz_id, quiz_schema.QuizUpdate(**update_data))
        if not updated_quiz:
            abort(400, description="Quiz not found or update failed")
        return jsonify(updated_quiz.to_response()), 200
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:quiz_id>", methods=["DELETE"])
async def delete_quiz(quiz_id: str):
    deleted = await quiz_model.delete(quiz_id)
    if not deleted:
        abort(400, description="Quiz not found or deletion failed")
    return jsonify({"message": "Quiz deleted successfully"}), 200

@router.route("/", methods=["GET"])
async def get_all_quizzes():
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 10))
        cursor = request.args.get("cursor", None)
        quizzes_data = await quiz_model.get_all(skip=skip, limit=limit, cursor=cursor)
        quizzes_data["items"] = [quiz.to_response() for quiz in quizzes_data["items"]]
        return jsonify(quizzes_data), 200
    except Exception as e:
        abort(400, description=str(e))