from fastapi import FastAPI

from api.api_v1.api import api_router
from core.config import settings
from contextlib import asynccontextmanager
from db.session import session
from pymilvus import utility
from initial_data import main

if not utility.has_collection(settings.milvus.COLLECTION_NAME_1) or not utility.has_collection(settings.milvus.COLLECTION_NAME_2):
    main()



@asynccontextmanager
async def lifespan(app: FastAPI):
    session.connection.connect()
    session.get_collection()
    session.collection.load()
    
    yield
    
    session.collection.release()
    session.connection.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8000)
