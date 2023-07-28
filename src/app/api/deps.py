from typing import Any, Generator


from milvus.client import Collection
from db import session


def get_collection() -> Generator[Collection, Any, None]:
    yield session.collection
    


