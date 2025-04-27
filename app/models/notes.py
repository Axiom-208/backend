from app.db.mongo_utils import MongoCrud
from app.schema import notes as note_schema
from app.service.revision.ai_content_gen import get_ai_content_generator


class NoteModel(MongoCrud[note_schema.NoteDocument]):
    model = note_schema.NoteDocument

    async def create_from_file(self, file_path: str, title: str, topic: str):
        ai_content_gen = get_ai_content_generator()
        content = ai_content_gen.parse_pdf(file_path)

        note = {
            "topic": topic,
            "content": content,
            "title": title
        }
        return await self.create(note)