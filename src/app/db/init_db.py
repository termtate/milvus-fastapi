import logging
from core.config import settings
from milvus.client import Collection, MilvusConnection
from pymilvus import CollectionSchema
import pandas as pd
from db.models.patients import patients
from db.models.patient_2 import patients2
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
        collection_name=patients.table_name,
        schema=CollectionSchema(patients.fields),
        vector_fields=patients.vector_fields,
        index_params=patients.index_params
    ), conn.create_collection(
        collection_name=patients2.table_name,
        schema=CollectionSchema(patients2.fields),
        vector_fields=patients2.vector_fields,
        index_params=patients2.index_params
    ))