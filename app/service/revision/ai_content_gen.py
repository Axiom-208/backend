"""
Axiom AI Content Generator
Uses Google Generative AI client for content generation
"""
from datetime import datetime
from bson.objectid import ObjectId
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import json
import re
from google import genai
from typing import Dict, List, Tuple, Union, Optional, Any
from app.models.notes import NoteModel
from app.schema.notes import NoteDocument
from app.schema.quiz import Question


# Load environment variables
load_dotenv()

class AIContentGenerator:
    
    def __init__(self):        
        # Initialize Google Generative AI
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("Warning: No API_KEY found in environment variables. Using mock generators.")
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=api_key)
                print("Successfully initialized Google Generative AI client")
            except Exception as e:
                print(f"Failed to initialize Google Generative AI client: {str(e)}")
                self.client = None
    
    def parse_pdf(self, file_path: str) -> str:
        """Parse a PDF file and extract text content as plain text"""
        try:
            # First try using docling if available
            try:
                from docling.document_converter import DocumentConverter
                converter = DocumentConverter()
                result = converter.convert(file_path)
                return result.document.export_to_markdown()
            except ImportError:
                # Fall back to PyPDF2
                print("docling not available, using PyPDF2 as fallback")
                reader = PdfReader(file_path)
                text = ""
                
                # Extract text from each page
                for page in reader.pages:
                    text += page.extract_text() + "\n\n"
                
                return text
            
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    

    def generate_quiz(self, note: NoteDocument) -> Tuple[bool, Union[str, Dict]]:
        """Generate a quiz from notes using Google Generative AI"""
        try:
            
            # Truncate content if it's too long
            content = note.content
            if len(content) > 30000:  # Limit to 30k characters
                content = content[:30000] + "..."
            
            try:
                # Generate the quiz using Google Generative AI client - UPDATED API CALL
                prompt = f"""
                Generate a multiple-choice quiz to test the student's knowledge on the following notes:
                
                {content}
                
                The quiz should be in JSON format with the following structure:
                {{

                    {{
                      "question_number": "Number of the question",
                      "question": "Specific question about the content",
                      "options": [{"text: string, is_correct: boolean"}],
                      "correct_answer": "Number of option that is correct (index starting from 0)"
                    }},
                    ... more questions ...
                  ]
                }}
                
                Make sure that all questions and options focus on the specific subject matter in the content,
                and avoid generic questions about studying techniques or the document itself.
                Please create at least 5 questions that directly test understanding of the specific 
                information in the content.
                """
                
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                    config={'response_mime_type': 'application/json'}
                )
                
                # Get the response text
                response_text = response.text
                
                # Parse the response
                try:
                    quiz_data = json.loads(response_text)
                    
                    return True, quiz_data
                except json.JSONDecodeError:
                    print("Failed to parse AI response as JSON")
                    
            except Exception as e:
                print(f"Error generating quiz with AI: {str(e)}")
                
        except Exception as e:
            return False, f"Error generating quiz: {str(e)}"
    
    def generate_flashcards(self, note: NoteDocument) -> Tuple[bool, Union[str, Dict]]:
        """Generate flashcards from notes using Google Generative AI"""
        try:
            # Truncate content if it's too long
            content = note.content



            try:
                # Generate the flashcards using Google Generative AI client - UPDATED API CALL
                prompt = f"""
                Generate a set of flashcards based on the following content:
                
                {content}
                
                The flashcards should be in JSON format with the following structure:
                
                {{
                    "front": "Specific term or concept from the content",
                    "back": "Definition or explanation from the content"
                }},
                ... more cards ...
                
                
                Please create at least 8 flashcards that directly focus on the specific information in the
                content. The front of each card should have a specific question or key term from 
                the content, and the back should have the definition or explanation.
                
                Make sure that all cards focus on the specific subject matter in the content and avoid
                generic cards about studying techniques or the document itself.
                """
                
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents= prompt,
                    config={'response_mime_type': 'application/json'}
                )
                
                # Get the response text
                response_text = response.text
                
                # Parse the response
                try:
                    flashcard_data = json.loads(response_text)

                    
                    return True, flashcard_data
                except json.JSONDecodeError:
                    print("Failed to parse AI response as JSON, falling back to content-aware mock implementation")
                    
            except Exception as e:
                print(f"Error generating flashcards with AI: {str(e)}")
                
        except Exception as e:
            return False, f"Error generating flashcards: {str(e)}"
    
    def generate_explanation(self, question:Question, marked_answer: int=None) -> str:
        try:
            prompt = f"""
            Explain why the answer of the following question {question.question} is {question.options[question.correct_answer].text} 
            but not {question.options[marked_answer].text or ""}.
            """

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={'response_mime_type': 'text/plain'}
            )

            return response.text
        except Exception as e:
            print(f"Error generating explanation: {str(e)}")
            return "Error generating explanation"