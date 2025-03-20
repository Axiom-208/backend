from app.db.mongo_utils import MongoCrud
from app.schema import courses as courses_schema

class CourseModel(MongoCrud[courses_schema.CourseDocument]):


    model = courses_schema.CourseDocument