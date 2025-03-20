from typing import Optional

from pydantic import EmailStr

from app.db.mongo_utils import MongoCrud
from app.schema import user as user_schema



class UserModel(MongoCrud[user_schema.UserDocument]):
    """
    This class implements the methods that handle basic operations with the mongodb database,
    while also setting the return type.
    """

    model = user_schema.UserDocument

    async def create_user(self, new_user_data: user_schema.UserCreate) -> user_schema.UserDocument:
        return await self.create(new_user_data.model_dump())

    async def update_user(self, user_id: str, update_data: user_schema.UserUpdate) -> Optional[user_schema.UserDocument]:
        return await self.update(user_id, update_data.model_dump(exclude_none=True))

    async def get_user_by_email(self, email: EmailStr):
        result = await self.get_by_fields({"email": email})
        return result[0] if len(result) > 0 else None
