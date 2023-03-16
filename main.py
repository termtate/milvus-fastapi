from fastapi import FastAPI

from api.api_v1.api import api_router
from core.config import settings
from db.session import Base, engine

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8000)
