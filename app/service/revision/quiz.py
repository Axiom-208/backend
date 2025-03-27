from app.schema.quiz import QuizDocument, QuestionAnswer, Question
from app.models.quiz import QuizModel
from app.schema.notes import NoteDocument
from app.service.revision.ai_content_gen import AIContentGenerator
from typing import List

class QuizHandler:
    def __init__(self):
        self.quiz_model = QuizModel()
        self.ai_content_gen = AIContentGenerator()

    async def create_quiz(self, note: NoteDocument):
        # Generate quiz content
        questions = self.ai_content_gen.generate_quiz(note)
        
        quiz = {
            "topic": note.topic,
            "questions": questions[1],
            "note_id": str(note.id)
        }

        return await self.quiz_model.create(quiz)
    
    async def grade_quiz(self, quiz:QuizDocument, answers: List[int]) -> int:
        score = 0
        wrong_answers = []
        for i in range(len(answers)):
            if answers[i] == quiz.questions[i].correct_answer:
                score += 1
            else:
                wrong_answers.append(quiz.questions[i])
            
        score = (score / len(answers)) * 100

        await self.quiz_model.update(_id=str(quiz.id), data={"score": score})

        return score, wrong_answers
    
    async def explain_question(self, question: Question, marked_answer: int=None) -> str:
        explanation = self.ai_content_gen.generate_explanation(question, marked_answer=marked_answer)
        return explanation
        
    


    