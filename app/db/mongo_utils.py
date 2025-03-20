from beanie import Document
from bson import ObjectId
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic, Union
from datetime import datetime

from app.schema.collection_id.object_id import PyObjectId


T = TypeVar("T", bound=Document)

def to_object_id(_id: str) -> PyObjectId:
    try:
        _id = PyObjectId(
            ObjectId(_id)
        )
        return _id
    except:
        raise ValueError("Invalid ObjectId")

class ComparingMethods:
    equals="$eq"
    not_equals="$ne"
    greater_than="$gt"
    greater_or_equal="$gte"
    less_than="$lt"
    less_or_equal="$lte"
    in_="$in"
    not_in="$nin"

class MongoCrud(Generic[T]):
    """
    pagination is not finished
    """

    model: Type[Document]

    def __init__(self):
        if not hasattr(self, "model") or not issubclass(self.model, Document):
            raise ValueError("A Beanie Document model must be set in the child class.")

    async def create(self, data: Dict[str, Any]) -> T:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()

        document = self.model(**data)
        return await document.insert()

    async def get_all(self, skip: int = 0, limit: int = 10, cursor: Optional[Union[str, datetime]] = None) -> Dict[str, Any]:
        return await self.paginate({}, skip, limit, cursor)

    async def get(self, _id: str) -> Optional[T]:
        return await self.model.get(_id)

    async def get_by_fields(
            self, filters: Dict[str, Any], skip: int = 0, limit: int = 10
    ) -> List[T]:
        return await self.model.find(filters).skip(skip).limit(limit).to_list()

    async def update(self, _id: str, data: Dict[str, Any]) -> Optional[T]:
        document = await self.model.get(_id)
        if not document:
            return None

        for key, value in data.items():
            setattr(document, key, value)

        document.updated_at = datetime.now()
        await document.save()
        return document

    async def delete(self, _id: str) -> bool:
        document = await self.model.get(_id)
        if document:
            await document.delete()
            return True
        return False

    async def paginate(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, cursor: Optional[Union[str, datetime]] = None) -> Dict[str, Any]:
        query = filters.copy()

        if cursor:
            if isinstance(cursor, str):  # If using `_id` for pagination
                query["_id"] = {"$gt": cursor}
            elif isinstance(cursor, datetime):  # If using `created_at` for pagination
                query["created_at"] = {"$gt": cursor}

        documents = await self.model.find(query).sort("created_at").skip(skip).limit(limit).to_list()

        next_cursor = None
        if documents:
            next_cursor = documents[-1].created_at  # Use `created_at` as the cursor

        total_count = await self.model.find(filters).count()

        return {
            "items": documents,
            "next_cursor": next_cursor,
            "total_count": total_count,
        }

