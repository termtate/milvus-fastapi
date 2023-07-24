from typing import Any, Generator

from fastapi.security import OAuth2PasswordBearer

from milvus.client import MilvusConnection, Collection
from core.config import settings
from db import session


def get_collection() -> Generator[Collection, Any, None]:
    yield session.collection
    
    # with session:
    #     collection = session.get_collection(settings.milvus.COLLECTION_NAME)
        
    #     with collection.load_data():
    #         print("collection")
    #         yield collection
