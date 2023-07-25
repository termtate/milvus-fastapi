from app.core.config import settings
from app.milvus.client import MilvusConnection, Collection
from pymilvus.exceptions import ConnectionNotExistException

class Session:
    def __init__(self) -> None:
        self.connection = MilvusConnection(
            host=settings.milvus.HOST,
            port=settings.milvus.PORT
        )
        self._collection: Collection | None = None
    
    def get_collection(self):
        self._collection = self.connection.get_collection(
            settings.milvus.COLLECTION_NAME,
            settings.milvus.EMBEDDING_FIELD_NAME
        )
        
    @property
    def collection(self) -> Collection:
        if self._collection is None:
            raise ConnectionNotExistException()
        return self._collection

session = Session()
# session = MilvusConnection(
#         host=settings.milvus.HOST,
#         port=settings.milvus.PORT
# )
# session.connect()
# collection = session.get_collection(settings.milvus.COLLECTION_NAME)
