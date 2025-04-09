from datetime import datetime, timedelta

from app.db.mongo_utils import MongoCrud
from app.schema import session as session_schema


class SessionModel(MongoCrud[session_schema.Session]):
    model = session_schema.Session

    async def create_session(self, user_id: str, refresh_token: str):
        session = session_schema.Session(
            user_id=user_id,
            refresh_token=refresh_token,
            expire_at=datetime.now() + timedelta(days=7)

        )
        await session.insert()

