from app.db.mongo_utils import MongoCrud
from app.schema import notes as note_schema


class NoteModel(MongoCrud[note_schema.NoteDocument]):
    model = note_schema.NoteDocument