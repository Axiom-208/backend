from typing import List, Type
from beanie import Document
from motor.motor_asyncio import AsyncIOMotorClient

class CascadeManager:
    """Generic cascading manager with transaction support for Beanie."""


    def __init__(self, parent_model: Type[Document], child_relations: List[dict], client: AsyncIOMotorClient):
        """
        :param parent_model: The parent document model
        :param child_relations: List of child relations (model, field, children, is_list)
        :param client: Motor client (used for starting sessions)
        """
        self.client = client
        self.parent_model = parent_model
        self.child_relations = child_relations


    async def delete_with_cascade(self, parent_id: str):
        """Performs recursive cascade delete inside a MongoDB transaction."""

        async with await self.client.start_session() as session:
            async with session.start_transaction():
                await self._run_deletion(parent_id, session)

    async def _run_deletion(self, parent_id: str, session):
        """Recursive deletion logic that runs inside a transaction."""

        async def cascade_delete(model, field, parent_id, is_list, nested_relations):
            # Find children related to this parent ID
            if is_list:
                children = await model.find({field: {"$in": [parent_id]}}).to_list()
            else:
                children = await model.find({field: parent_id}).to_list()

            for child in children:
                child_id = str(child.id)

                # Recursively delete any nested children
                for relation in nested_relations:
                    await cascade_delete(
                        relation["model"], relation["field"], child_id,
                        relation.get("is_list", False), relation.get("children", [])
                    )

                # Delete the child
                await child.delete(session=session)

        # Start deletion from top-level children
        for relation in self.child_relations:
            await cascade_delete(
                relation["model"], relation["field"], parent_id,
                relation.get("is_list", False), relation.get("children", [])
            )

        # Delete the parent last
        await self.parent_model.get(parent_id).delete(session=session)
