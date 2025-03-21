from flask import Blueprint, jsonify, abort, request

from app.models.video_chapters import VideoChapterModel
from app.schema import video_chapter as video_chapter_schema

router = Blueprint("video_chapters", __name__, url_prefix="/video_chapters")
video_chapter_model = VideoChapterModel()


@router.route("/<string:video_chapter_id>", methods=["GET"])
async def get_video_chapter(video_chapter_id: str):
    video_chapter = await video_chapter_model.get(video_chapter_id)
    if not video_chapter:
        abort(400, description="Video chapter not found")
    return jsonify(video_chapter.to_response()), 200

@router.route("/", methods=["POST"])
async def create_video_chapter():
    try:
        video_chapter_data = request.get_json()
        new_video_chapter = await video_chapter_model.create_video_chapter(video_chapter_schema.VideoChapterCreate(**video_chapter_data))
        return jsonify(new_video_chapter.to_response()), 201
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:video_chapter_id>", methods=["PUT"])
async def update_video_chapter(video_chapter_id: str):
    try:
        update_data = request.get_json()
        updated_video_chapter = await video_chapter_model.update_video_chapter(video_chapter_id, video_chapter_schema.VideoChapterUpdate(**update_data))
        if not updated_video_chapter:
            abort(400, description="Video chapter not found or update failed")
        return jsonify(updated_video_chapter.to_response()), 200
    except Exception as e:
        abort(400, description=str(e))

@router.route("/<string:video_chapter_id>", methods=["DELETE"])
async def delete_video_chapter(video_chapter_id: str):
    deleted = await video_chapter_model.delete(video_chapter_id)
    if not deleted:
        abort(400, description="Video chapter not found or deletion failed")
    return jsonify({"message": "Video chapter deleted successfully"}), 200

@router.route("/", methods=["GET"])
async def get_all_video_chapters():
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 10))
        cursor = request.args.get("cursor", None)
        video_chapters_data = await video_chapter_model.get_all(skip=skip, limit=limit, cursor=cursor)
        video_chapters_data["items"] = [video_chapter.to_response() for video_chapter in video_chapters_data["items"]]
        return jsonify(video_chapters_data), 200
    except Exception as e:
        abort(400, description=str(e))