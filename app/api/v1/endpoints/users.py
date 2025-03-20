from flask import Blueprint, jsonify, abort, request

from app.models.user import UserModel
from app.schema import user as user_schema

router = Blueprint("users", __name__, url_prefix="/users")
user_model = UserModel()


@router.route("/<string:user_id>", methods=["GET"])
async def get_user(user_id: str):
    user = await user_model.get(user_id)
    if not user:
        abort(400, description="User not found")
    return jsonify(user.to_response()), 200

@router.route("/", methods=["POST"])
async def create_user():
    try:
        user_data = request.get_json()
        new_user = await user_model.create_user(user_schema.UserCreate(**user_data))
        return jsonify(new_user.to_response()), 201
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:user_id>", methods=["PUT"])
async def update_user(user_id: str):
    try:
        update_data = request.get_json()
        updated_user = await user_model.update_user(user_id, user_schema.UserUpdate(**update_data))
        if not updated_user:
            abort(400, description="User not found or update failed")
        return jsonify(updated_user.to_response()), 200
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:user_id>", methods=["DELETE"])
async def delete_user(user_id: str):
    deleted = await user_model.delete(user_id)
    if not deleted:
        abort(400, description="User not found or deletion failed")
    return jsonify({"message": "User deleted successfully"}), 200

@router.route("/", methods=["GET"])
async def get_all_users():
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 10))
        cursor = request.args.get("cursor", None)
        users_data = await user_model.get_all(skip=skip, limit=limit, cursor=cursor)
        users_data["items"] = [user.to_response() for user in users_data["items"]]
        return jsonify(users_data), 200
    except Exception as e:
        abort(400, description=str(e))

@router.route("/email/<string:email>", methods=["GET"])
async def get_user_by_email(email: str):
    user = await user_model.get_user_by_email(email)
    if not user:
        abort(400, description="User not found")
    return jsonify(user.to_response()), 200