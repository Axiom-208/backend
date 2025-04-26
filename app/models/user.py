from typing import Optional

from pydantic import EmailStr

from app.db.mongo_utils import MongoCrud
from app.schema import user as user_schema
from app.auth.utils import hash_password


class UserModel(MongoCrud[user_schema.UserDocument]):

    model = user_schema.UserDocument

    async def create_user(self, new_user_data: user_schema.UserCreate) -> user_schema.UserDocument:
        print("CREATING THE USER")
        existing = await self.get_user_by_username(username=new_user_data.username)
        if existing is not None:
            raise ValueError("User already exists")

        print("NO USER WITH THIS USERNAME")

        print(new_user_data)

        hashed = hash_password(new_user_data.password)

        new_user = user_schema.UserBase(
            first_name=new_user_data.first_name,
            last_name=new_user_data.last_name,
            email=new_user_data.email,
            username=new_user_data.username,
            hashed_password=hashed
        )

        print(new_user_data)
        print(new_user)

        return await self.create(new_user.model_dump(by_alias=False))

    async def update_user(self, user_id: str, update_data: user_schema.UserUpdate) -> Optional[user_schema.UserDocument]:
        return await self.update(user_id, update_data.model_dump(exclude_none=True))

    async def get_user_by_email(self, email: EmailStr):
        result = await self.get_by_fields({"email": email})
        return result[0] if len(result) > 0 else None

    async def get_user_by_username(self, username: str):
        result = await self.get_by_fields({"username": username})
        return result[0] if len(result) > 0 else None
