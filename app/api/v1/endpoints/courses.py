from fastapi import APIRouter
from starlette.exceptions import HTTPException

from app.models.courses import CourseModel
from app.schema import courses as course_schema

router = APIRouter()
course_model = CourseModel()


@router.get("/{course_id}")
async def get_user(course_id: str):
    course = await course_model.get(course_id)
    if not course:
        raise HTTPException(status_code=400, detail="Course not found")
    return course.to_response()

@router.post("/")
async def create_course(course_data: course_schema.CourseCreate):
    try:
        new_course = await course_model.create(course_data.model_dump())
        return new_course.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{course_id}")
async def update_course(course_id: str, update_data: course_schema.CourseUpdate):
    try:
        updated_course: course_schema.CourseDocument = await course_model.update(course_id, update_data)
        if not updated_course:
            raise HTTPException(status_code=400, detail="Course not found or update failed")
        return updated_course.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{course_id}")
async def delete_course(course_id: str):
    deleted = await course_model.delete(course_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Course not found or deletion failed")
    return {"message": "Course deleted successfully"}


# @router.route("/", methods=["GET"])
# async def get_all_courses():
#     try:
#         skip = int(request.args.get("skip", 0))
#         limit = int(request.args.get("limit", 10))
#         cursor = request.args.get("cursor", None)
#         courses_data = await course_model.get_all(skip=skip, limit=limit, cursor=cursor)
#         courses_data["items"] = [course.to_response() for course in courses_data["items"]]
#         return jsonify(courses_data), 200
#     except Exception as e:
#         abort(400, description=str(e))
#
#
#

