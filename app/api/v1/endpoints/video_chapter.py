from fastapi import APIRouter
from flask import Blueprint, jsonify, abort, request
from starlette.exceptions import HTTPException

from app.models.video_chapters import VideoChapterModel
from app.schema import video_chapters as video_chapter_schema


router = APIRouter()
video_chapter_model = VideoChapterModel()


@router.get("/{video_chapter_id}")
async def get_video_chapter(video_chapter_id: str):
    video_chapter = await video_chapter_model.get(video_chapter_id)
    if not video_chapter:
        raise HTTPException(status_code=400, detail="Video chapter not found")
    return video_chapter.to_response()

@router.post("/")
async def create_video_chapter(video_chapter_data: video_chapter_schema.VideoChapterCreate):
    try:
        new_video_chapter = await video_chapter_model.create(video_chapter_data.model_dump())
        return new_video_chapter.to_response()
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@router.put("/{video_chapter_id}")
async def update_video_chapter(video_chapter_id: str, update_data: video_chapter_schema.VideoChapterUpdate):
    try:
        updated_video_chapter: video_chapter_schema.VideoChapterDocument = await video_chapter_model.update(video_chapter_id, update_data)
        if not updated_video_chapter:
            raise HTTPException(status_code=400, detail="Video chapter not found or update failed")
        return updated_video_chapter.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{video_chapter_id}")
async def delete_video_chapter(video_chapter_id: str):
    deleted = await video_chapter_model.delete(video_chapter_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Video chapter not found or deletion failed")
    return {"message": "Video chapter deleted successfully"}

# @router.route("/", methods=["GET"])
# async def get_all_video_chapters():
#     try:
#         skip = int(request.args.get("skip", 0))
#         limit = int(request.args.get("limit", 10))
#         cursor = request.args.get("cursor", None)
#         video_chapters_data = await video_chapter_model.get_all(skip=skip, limit=limit, cursor=cursor)
#         video_chapters_data["items"] = [video_chapter.to_response() for video_chapter in video_chapters_data["items"]]
#         return jsonify(video_chapters_data), 200
#     except Exception as e:
#         abort(400, description=str(e))
#
