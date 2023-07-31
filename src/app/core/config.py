
from pydantic import BaseSettings
from pymilvus import FieldSchema, DataType


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
        FieldSchema(name="seizure_duration", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="seizure_freq", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="maternal_pregnancy_age", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="pregnancy_num", dtype=DataType.VARCHAR, max_length=10),
        FieldSchema(name="birth_weight", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="head_c", dtype=DataType.VARCHAR, max_length=15),
        FieldSchema(name="blood_urine_screening", dtype=DataType.VARCHAR, max_length=30),
        FieldSchema(name="copper_cyanin", dtype=DataType.VARCHAR, max_length=25),
        FieldSchema(name="csf", dtype=DataType.VARCHAR, max_length=25),
        FieldSchema(name="genetic_test", dtype=DataType.VARCHAR, max_length=25),
        FieldSchema(name="head_ct", dtype=DataType.VARCHAR, max_length=25),
        FieldSchema(name="head_mri", dtype=DataType.VARCHAR, max_length=25),
        FieldSchema(name="scalp_eeg", dtype=DataType.VARCHAR, max_length=25),
        FieldSchema(name="precipitating_factor", dtype=DataType.VARCHAR, max_length=300),
    ]
    
    # https://milvus.io/docs/v2.0.x/build_index.md#Prepare-index-parameter
    VECTOR_FIELD_INDEX_PARAMS = {
        'metric_type': "L2", 
        'index_type': "FLAT",
    }
    
    VECTOR_FIELDS: list[str] = [
        "seizure_evolution",   
        # "precipitating_factor"                                     
    ]


class Settings(BaseSettings):
    milvus = MilvusSettings()
    
    API_V1_STR: str = "/api/v1"


settings = Settings()
