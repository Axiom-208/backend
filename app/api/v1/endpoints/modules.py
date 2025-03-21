from flask import Blueprint, jsonify, abort, request

from app.models.modules import ModuleModel
from app.schema import module as module_schema

router = Blueprint("modules", __name__, url_prefix="/modules")
module_model = ModuleModel()


@router.route("/<string:module_id>", methods=["GET"])
async def get_module(module_id: str):
    module = await module_model.get(module_id)
    if not module:
        abort(400, description="Module not found")
    return jsonify(module.to_response()), 200

@router.route("/", methods=["POST"])
async def create_module():
    try:
        module_data = request.get_json()
        new_module = await module_model.create_module(module_schema.ModuleCreate(**module_data))
        return jsonify(new_module.to_response()), 201
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:module_id>", methods=["PUT"])
async def update_module(module_id: str):
    try:
        update_data = request.get_json()
        updated_module = await module_model.update_module(module_id, module_schema.ModuleUpdate(**update_data))
        if not updated_module:
            abort(400, description="Module not found or update failed")
        return jsonify(updated_module.to_response()), 200
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:module_id>", methods=["DELETE"])
async def delete_module(module_id: str):
    deleted = await module_model.delete(module_id)
    if not deleted:
        abort(400, description="Module not found or deletion failed")
    return jsonify({"message": "Module deleted successfully"}), 200

@router.route("/", methods=["GET"])
async def get_all_modules():
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 10))
        cursor = request.args.get("cursor", None)
        modules_data = await module_model.get_all(skip=skip, limit=limit, cursor=cursor)
        modules_data["items"] = [module.to_response() for module in modules_data["items"]]
        return jsonify(modules_data), 200
    except Exception as e:
        abort(400, description=str(e))