from app.schema.notes import NoteDocument, NoteCreate
from app.models.notes import NoteModel
from app.service.revision.ai_content_gen import AIContentGenerator

class NoteHandler(NoteModel):
    def __init__(self):
        self.ai_content_gen = AIContentGenerator()

    async def create_from_file(self, file_path: str, title: str, topic: str):
        content = self.ai_content_gen.parse_pdf(file_path)
        
        note = {
            "topic": topic,
            "content": content,
            "title": title
        }

        return await self.create(note)
    

