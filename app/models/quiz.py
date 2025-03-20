from app.db.mongo_utils import MongoCrud
from app.schema import quiz as quiz_schema


class QuizModel(MongoCrud[quiz_schema.QuizDocument]):
    model = quiz_schema.QuizDocument

    def create_quiz(self, new_quiz_data: quiz_schema.QuizCreate) -> quiz_schema.QuizDocument:
        return self.create(**new_quiz_data.model_dump())
