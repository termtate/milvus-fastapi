import logging
from core.config import settings
from milvus.client import Collection, MilvusConnection
from pymilvus import CollectionSchema
import pandas as pd
from db.models.patients import schema as s1
from db.models.patient_2 import schema as s2
from db.proxy import CollectionProxy


logger = logging.getLogger(__name__)

def init_db(conn: MilvusConnection) -> None:
    collection1, collection2 = create_collection(conn)
    delegation = CollectionProxy(collection1, collection2)
    logging.info("create collection1, collection2")
    
    df = pd.read_excel("output.xlsx", dtype={
            "病案号": str,
            "电话": str,
            "症状性癫痫": str
        }).rename(columns=settings.columns_name_map).fillna(value="")
    
    del df["id"]
    
    delegation.ann_insert(df.to_dict(orient="records"))
    
    

def create_collection(conn: MilvusConnection) -> tuple[Collection, Collection]:
    return (conn.create_collection(
        settings.milvus.COLLECTION_NAME_1,
        schema=s1,
        vector_fields=settings.milvus.VECTOR_FIELDS_1,
        index_params=settings.milvus.VECTOR_FIELD_INDEX_PARAMS
    ), conn.create_collection(
        settings.milvus.COLLECTION_NAME_2,
        schema=s2,
        vector_fields=settings.milvus.VECTOR_FIELDS_2,
        index_params=settings.milvus.VECTOR_FIELD_INDEX_PARAMS
    ))