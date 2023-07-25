from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings
from contextlib import asynccontextmanager
from app.db.session import session



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
