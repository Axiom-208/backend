from app.db.mongo_utils import MongoCrud
from app.schema import session as session_schema


class SessionModel(MongoCrud[session_schema.Session]):
    model = session_schema.Session