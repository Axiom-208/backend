
from fastapi import APIRouter, HTTPException
from flask import Blueprint, jsonify, abort, request

from app.models.modules import ModuleModel
from app.schema import modules as module_schema

router = APIRouter()
module_model = ModuleModel()


@router.get("/{module_id}")
async def get_module(module_id: str):
    module = await module_model.get(module_id)
    if not module:
        abort(400, description="Module not found")
    return jsonify(module.to_response()), 200

@router.post("/")
async def create_module(module_data: module_schema.ModuleCreate):
    try:
        new_module = await module_model.create(module_data.model_dump())
        return new_module.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{module_id}")
async def update_module(module_id: str, update_data: module_schema.ModuleUpdate):
    try:
        updated_module: module_schema.ModuleDocument = await module_model.update(module_id, update_data)
        if not updated_module:
            raise HTTPException(status_code=400, detail="Module not found or update failed")
        return updated_module.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{module_id}")
async def delete_module(module_id: str):
    deleted = await module_model.delete(module_id)
    if not deleted:
        abort(400, description="Module not found or deletion failed")
    return jsonify({"message": "Module deleted successfully"}), 200

# @router.get("/all")
# async def get_all_modules():
#     try:
#         skip = int(request.args.get("skip", 0))
#         limit = int(request.args.get("limit", 10))
#         cursor = request.args.get("cursor", None)
#         modules_data = await module_model.get_all(skip=skip, limit=limit, cursor=cursor)
#         modules_data["items"] = [module.to_response() for module in modules_data["items"]]
#         return jsonify(modules_data), 200
#     except Exception as e:
#         abort(400, description=str(e))