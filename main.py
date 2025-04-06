from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.dependencies import get_mongo_client, get_settings
from app.api.base_router import router as base_router
from app.middleware.response_middleware import ResponseFormatterMiddleware


settings = get_settings()

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:

    print(f"App started in {settings.ENVIRONMENT} mode")

    mongo_client = get_mongo_client()

    try:
        await mongo_client.init_db()
        print("Initialized Mongo DB client")

        # db = mongo_client.get_db()
        # indexes = await db.get_collection("sessions").list_indexes().to_list()
        # for index in indexes:
        #     print(index)


    except Exception as error:
        print(f"ERROR: {error}")
    yield

    print("Closing Mongo DB client connection")
    await mongo_client.close_connection()

    print("Shutting down")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

app.include_router(base_router, prefix="/api")



app.add_middleware(ResponseFormatterMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)