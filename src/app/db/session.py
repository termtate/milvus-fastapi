from core.config import settings
from milvus.client import MilvusConnection, Collection
from pymilvus.exceptions import ConnectionNotExistException
from db.proxy import CollectionProxy

class Session:
    def __init__(self) -> None:
        self.connection = MilvusConnection(
            host=settings.milvus.HOST,
            port=settings.milvus.PORT
        )
        self._proxy: CollectionProxy | None = None
    
    def get_collection(self):
        self._proxy = CollectionProxy(
            collection1=self.connection.get_collection(
                settings.milvus.COLLECTION_NAME_1,
                settings.milvus.VECTOR_FIELDS_1
            ),
            collection2=self.connection.get_collection(
                settings.milvus.COLLECTION_NAME_2,
                settings.milvus.VECTOR_FIELDS_2
            )
        )

    @property
    def collection(self) -> CollectionProxy:
        if self._proxy is None:
            raise ConnectionNotExistException()
        return self._proxy


session = Session()
