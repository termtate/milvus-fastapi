
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
        "precipitating_factor"                                     
    ]


class Settings(BaseSettings):
    milvus = MilvusSettings()
    
    API_V1_STR: str = "/api/v1"
    
    colnums_name_map = {
        "ID": "id",
        "身份证号": "id_card_number",
        "姓名": "name",
        "第几次住院": "hospitalize_num",
        "病案号": "case_number",
        "性别": "sex",
        "年龄": "age",
        "电话": "phone_number",
        "发作演变过程": "seizure_evolution",
        "发作持续时间": "seizure_duration",
        "发作频次": "seizure_freq",
        "母孕年龄": "maternal_pregnancy_age",
        "孕次产出": "pregnancy_num",
        "出生体重": "birth_weight",
        "头围": "head_c",
        "血、尿代谢筛查": "blood_urine_screening",
        "铜兰蛋白": "copper_cyanin",
        "脑脊液": "csf",
        "基因检查": "genetic_test",
        "头部CT": "head_ct",
        "头部MRI": "head_mri",
        "头皮脑电图": "scalp_eeg",
        "诱发因素": "precipitating_factor",
    }


settings = Settings()
