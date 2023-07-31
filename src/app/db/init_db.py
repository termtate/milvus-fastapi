import logging
from core.config import settings
from milvus.client import Collection, MilvusConnection
from pymilvus import CollectionSchema
import pandas as pd



logger = logging.getLogger(__name__)

def init_db(conn: MilvusConnection) -> None:
    collection = create_collection(conn)
    logging.info(f"创建collection: {[_.name for _ in collection.collection.schema.fields]}")
    
    df = pd.read_excel("output.xlsx", dtype={
            "病案号": str,
            "电话": str
        }).rename(columns=settings.colnums_name_map)[list(settings.colnums_name_map.values())]
    
    collection.ann_insert(df)
    
    

def create_collection(conn: MilvusConnection) -> Collection:
    schema = CollectionSchema(fields=settings.milvus.COLLECTION_FIELDS, description='search text')
    
    return conn.create_collection(
        settings.milvus.COLLECTION_NAME,
        schema=schema,
        vector_fields=settings.milvus.VECTOR_FIELDS,
        index_params=settings.milvus.VECTOR_FIELD_INDEX_PARAMS
    )