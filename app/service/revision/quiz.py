from app.schema.quiz import QuizDocument, QuestionAnswer, Question
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
    
    async def grade_quiz(self, quiz:QuizDocument, answers: List(QuestionAnswer)) -> int:
        score = 0
        wrong_answers = []
        for i in range(len(answers)):
            if answers[i].answer == quiz.questions[i].correct_answer:
                score += 1
                wrong_answers.append(quiz.questions[i])

        quiz.score = score
        return score, wrong_answers
    
    async def explain_question(self, question: Question, marked_answer: int=None) -> str:
        explanation = self.ai_content_gen.generate_explanation(question, marked_answer=marked_answer)
        return explanation
        
    


    