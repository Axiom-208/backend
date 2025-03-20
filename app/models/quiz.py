from app.db.mongo_utils import MongoCrud
from app.schema import quiz as quiz_schema


class QuizModel(MongoCrud[quiz_schema.QuizDocument]):
    model = quiz_schema.QuizDocument