import secrets
from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, Field, HttpUrl, tools
from pymilvus import FieldSchema, DataType
from app.milvus.types import IndexParams


class MilvusSettings(BaseSettings):
    HOST = "localhost"
    PORT = 19530
    
    COLLECTION_NAME = "test1"
    
    COLLECTION_FIELDS: list[FieldSchema] = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="id_card_number", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="hospitalize_num", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="case_number", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="sex", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="age", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="phone_number", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="seizure_evolution", dtype=DataType.VARCHAR, max_length=600),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768),
    ]
    
    EMBEDDING_FIELD_NAME = "seizure_evolution"
    
    FIELD_INDEX_PARAMS: IndexParams = {
        "field_name": "vector",
        
        # https://milvus.io/docs/v2.0.x/build_index.md#Prepare-index-parameter
        "index_params": {
            'metric_type': "L2", 
            'index_type': "FLAT",
        }
    }


class Settings(BaseSettings):
    milvus = MilvusSettings()
    
    API_V1_STR: str = "/api/v1"


settings = Settings()
