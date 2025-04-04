from fastapi import APIRouter
from starlette.exceptions import HTTPException

from app.models.user import UserModel
from app.schema import user as user_schema

router = APIRouter()
user_model = UserModel()


@router.get("/{user_id}")
async def get_user(user_id: str):
    user = await user_model.get(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user.to_response()

@router.post("/")
async def create_user(user_data: user_schema.UserCreate):
    try:
        new_user = await user_model.create_user(user_data)
        return new_user.to_response()
    except Exception as e:
        raise HTTPException(detail=f"Error: {e}", status_code=400)

@router.put("/{user_id}")
async def update_user(user_id: str, update_data: user_schema.UserUpdate):
    updated_user = await user_model.update_user(user_id, update_data)
    if not updated_user:
        HTTPException(detail="User not found or update failed", status_code=400)
    return updated_user.to_response()


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    deleted = await user_model.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="User not found or deletion failed")
    return {"message": "User deleted successfully"}

# @router.get("/")
# async def get_all_users():
#     try:
#         skip = int(request.args.get("skip", 0))
#         limit = int(request.args.get("limit", 10))
#         cursor = request.args.get("cursor", None)
#         users_data = await user_model.get_all(skip=skip, limit=limit, cursor=cursor)
#         users_data["items"] = [user_schema.UserDocument(user).to_response() for user in users_data["items"]]
#         return users_data
#     except Exception as e:
#         raise HTTPException(detail=f"Error: {e}", status_code=400)

@router.get("/email/{email}")
async def get_user_by_email(email: str):
    user = await user_model.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user.to_response()