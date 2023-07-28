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
        }).rename(columns={
        "ID": "id",
        "身份证号": "id_card_number",
        "姓名": "name",
        "第几次住院": "hospitalize_num",
        "病案号": "case_number",
        "性别": "sex",
        "年龄": "age",
        "电话": "phone_number",
        "发作演变过程": "seizure_evolution"
    })[["id", "id_card_number", "name", "hospitalize_num", "case_number", 
        "sex", "age", "phone_number", "seizure_evolution"]]
    
    collection.ann_insert(df)
    
    

def create_collection(conn: MilvusConnection) -> Collection:
    schema = CollectionSchema(fields=settings.milvus.COLLECTION_FIELDS, description='search text')
    
    return conn.create_collection(
        settings.milvus.COLLECTION_NAME,
        schema=schema,
        vector_fields=settings.milvus.VECTOR_FIELDS,
    )