
from pydantic import BaseSettings
from pymilvus import FieldSchema, DataType
from milvus.types import VectorField


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
    ]
    
    EMBEDDING_FIELD_NAME = "seizure_evolution"
    
    VECTOR_FIELD_INDEX_PARAMS = {
        'metric_type': "L2", 
        'index_type': "FLAT",
    }
    
    VECTOR_FIELDS: list[VectorField] = [
        {
            "field_name": "seizure_evolution",
            
            # https://milvus.io/docs/v2.0.x/build_index.md#Prepare-index-parameter
            "index_params": VECTOR_FIELD_INDEX_PARAMS
        },                                           
    ]


class Settings(BaseSettings):
    milvus = MilvusSettings()
    
    API_V1_STR: str = "/api/v1"


settings = Settings()
