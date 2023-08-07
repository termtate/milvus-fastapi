from typing import Any, Generator


from db.proxy import CollectionProxy
from db import session


def get_collection() -> Generator[CollectionProxy, Any, None]:
    yield session.collection
    


