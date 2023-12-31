import logging

from db.init_db import init_db
from milvus.client import MilvusConnection
from core.config import settings
from db.models.patients import patients

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with MilvusConnection(settings.milvus.HOST, settings.milvus.PORT) as conn:
        init_db(conn=conn)  
        
        collection = conn.get_collection(
            patients.table_name,
            patients.vector_fields
        )
        with collection.load_data():
            logger.info(f"entities number: {collection.collection.num_entities}")


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
