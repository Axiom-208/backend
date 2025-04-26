
from beanie import Document, Indexed
from datetime import datetime

from pydantic import Field
from pymongo import IndexModel
from pymongo.common import alias

from app.schema.collection_id.document_id import DocumentId


class Session(DocumentId, Document):
    user_id: str
    refresh_token: str

    expire_at: datetime = Indexed(expire_after_seconds=60 * 60 * 24 * 7, name="ttl_expires_at")

    model_config = {
        "populate_by_name": False,
    }

    class Settings:
        name = "sessions"

        indexes = [
            IndexModel("expires_at", expireAfterSeconds=60 * 60 * 24 * 7, name="ttl_expires_at")
        ]
