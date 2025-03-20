from typing import List
from xml.dom.minidom import Document

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from beanie import init_beanie
from pymongo.errors import PyMongoError


class MongoDBClient:
    def __init__(self, mongo_uri: str, database_name: str, document_models = None):
        self.mongo_uri = mongo_uri
        self.document_models = document_models if document_models is not None else []
        self.database_name = database_name
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None

    async def init_db(self) -> None:
        try:
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client[self.database_name]

            await self.ping()

            await init_beanie(database=self.db, document_models=self.document_models)
            print("✅ MongoDB connection established and Beanie initialized.")
        except Exception as e:
            print(f"❌ Error initializing MongoDB: {e}")
            raise

    async def close_connection(self) -> None:
        if self.client:
            self.client.close()
            print("🔴 MongoDB connection closed.")

    async def ping(self) -> None:
        try:
            await self.client.admin.command('ping')
            print("✅ Pinged MongoDB deployment successfully.")
        except PyMongoError as e:
            print(f"❌ Failed to ping MongoDB: {e}")
            raise

    def get_db(self) -> AsyncIOMotorDatabase:
        if self.db is None:
            raise ValueError("❌ Database not initialized. Call `init_db()` first.")
        return self.db

    def get_client(self) -> AsyncIOMotorClient:
        if self.client is None:
            raise ValueError("❌ Client not initialized. Call `init_db()` first.")
        return self.client