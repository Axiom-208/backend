from app.schema.quiz import QuizDocument
from app.models.quiz import QuizModel
from app.schema.notes import NoteDocument
from app.service.revision.ai_content_gen import AIContentGenerator

class QuizHandler:
    def __init__(self):
        self.quiz_model = QuizModel()
        self.ai_content_gen = AIContentGenerator()

    async def create_quiz(self, note: NoteDocument):
        # Generate quiz content
        quiz_content = self.ai_content_gen.generate_quiz(note)
        quiz = QuizDocument(content=quiz_content, note_id=note.id)

        return self.quiz_model.create_quiz(quiz)


    