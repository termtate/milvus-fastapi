from core.config import settings
from milvus.client import MilvusConnection, Collection
from pymilvus.exceptions import ConnectionNotExistException
from db.proxy import CollectionProxy
from db.models.patients import patients
from db.models.patient_2 import patients2

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
                patients.table_name,
                patients.vector_fields
            ),
            collection2=self.connection.get_collection(
                patients2.table_name,
                patients2.vector_fields
            )
        )

    @property
    def collection(self) -> CollectionProxy:
        if self._proxy is None:
            raise ConnectionNotExistException()
        return self._proxy


session = Session()
