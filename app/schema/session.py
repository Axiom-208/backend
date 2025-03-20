from datetime import datetime

from beanie import Document

from app.schema.collection_id.document_id import DocumentId


class Session(DocumentId, Document):
    user_id: str
    refresh_token: str

    class Settings:
        name = "sessions"
        indexes = [
            ("created_at", {"expireAfterSeconds": 120})
        ]