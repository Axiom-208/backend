from fastapi import APIRouter

from app.models.courses import CourseModel
from app.schema import course as course_schema

router = APIRouter()
course_model = CourseModel()


# @router.route("/<string:course_id>", methods=["GET"])
# async def get_user(course_id: str):
#     course = await course_model.get(course_id)
#     if not course:
#         abort(400, description="Course not found")
#     return jsonify(course.to_response()), 200

# @router.route("/", methods=["POST"])
# async def create_course():
#     try:
#         course_data = request.get_json()
#         new_course = await course_model.create_course(course_schema.CourseCreate(**course_data))
#         return jsonify(new_course.to_response()), 201
#     except Exception as e:
#         abort(400, description=str(e))

# @router.route("/<string:course_id>", methods=["PUT"])
# async def update_course(course_id: str):
#     try:
#         update_data = request.get_json()
#         updated_course = await course_model.update_course(course_id, course_schema.CourseUpdate(**update_data))
#         if not updated_course:
#             abort(400, description="Course not found or update failed")
#         return jsonify(updated_course.to_response()), 200
#     except Exception as e:
#         abort(400, description=str(e))

# @router.route("/<string:course_id>", methods=["DELETE"])
# async def delete_course(course_id: str):
#     deleted = await course_model.delete(course_id)
#     if not deleted:
#         abort(400, description="Course not found or deletion failed")
#     return jsonify({"message": "Course deleted successfully"}), 200

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




