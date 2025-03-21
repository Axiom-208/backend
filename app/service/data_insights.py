from typing import Dict, List, Optional
from datetime import datetime

from app.models.quiz import QuizModel
from app.schema import quiz as quiz_schema


""" TODO: Need to edit the database and schema for quizzes, so that it includes an attribute with the result of each quiz"""


class DataInsightsService:
    
    def __init__(self):
        self.quiz_result_model = quiz_schema()
    
    async def get_user_quiz_averages(self, user_id: str, module_id: Optional[str] = None) -> Dict:
        
        #Calculate average quiz scores for a user
        #Returns: Dictionary containing average score and related statistics
        
        results = await self.quiz_result_model.get_user_results(user_id, module_id)
        
        if not results:
            return {
                "user_id": user_id,
                "module_id": module_id,
                "average_percentage": 0,
                "quizzes_taken": 0,
                "highest_score": 0,
                "lowest_score": 0
            }
        
        percentages = [result.percentage for result in results]
        avg_percentage = sum(percentages) / len(percentages)
        
        return {
            "user_id": user_id,
            "module_id": module_id,
            "average_percentage": round(avg_percentage, 2),
            "quizzes_taken": len(results),
            "highest_score": round(max(percentages), 2),
            "lowest_score": round(min(percentages), 2)
        }
    
    async def get_module_quiz_averages(self, user_id: str, module_id: str) -> Dict:
        
        #Calculate average quiz score for a user in a specific module
        #Returns: Dictionary containing the user's average score for a quiz, and a status (e.g. passed)
        
        # Get all quiz results for this user in this module
        results = await self.quiz_result_model.get_user_results(user_id, module_id)
        
        if not results:
            return {
                "user_id": user_id,
                "module_id": module_id,
                "average_percentage": 0,
                "quizzes_taken": 0,
                "status": "No quizzes completed"
            }
        
        percentages = [result.percentage for result in results]
        avg_percentage = sum(percentages) / len(percentages)
        
        # Determine status based on average score
        status = "Failed"
        if avg_percentage >= 40:
            status = "Passed"
        if avg_percentage >= 70:
            status = "Excellent"
            
        return {
            "user_id": user_id,
            "module_id": module_id,
            "average_percentage": round(avg_percentage, 2),
            "quizzes_taken": len(results),
            "status": status,
            "highest_score": round(max(percentages), 2),
            "completed_at": results[-1].created_at if results else None
        }
    