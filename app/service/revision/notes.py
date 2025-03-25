from app.schema.notes import NoteDocument
from app.models.notes import NoteModel
from app.service.revision.ai_content_gen import AIContentGenerator

class NoteHandler:
    def __init__(self):
        self.note_model = NoteModel()
        self.ai_content_gen = AIContentGenerator()

    def create_from_file(self, file_path: str, title: str, topic: str) -> NoteDocument:
        content = self.ai_content_gen.parse_pdf(file_path)
        note = NoteDocument(content=content, title=title, topic=topic)
        return self.note_model.create(note)
    

