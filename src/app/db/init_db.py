import logging
from core.config import settings
from milvus.client import Collection, MilvusConnection
from pymilvus import CollectionSchema
import pandas as pd



logger = logging.getLogger(__name__)

def init_db(conn: MilvusConnection) -> None:
    collection = create_collection(conn)
    logging.info(f"创建collection: {[_.name for _ in collection.collection.schema.fields]}")
    
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
    
    df = pd.read_excel("output.xlsx", dtype={
            "病案号": str,
            "电话": str
        }).rename(columns=colnums_name_map)[list(colnums_name_map.values())]
    
    collection.ann_insert(df)
    
    

def create_collection(conn: MilvusConnection) -> Collection:
    schema = CollectionSchema(fields=settings.milvus.COLLECTION_FIELDS, description='search text')
    
    return conn.create_collection(
        settings.milvus.COLLECTION_NAME,
        schema=schema,
        vector_fields=settings.milvus.VECTOR_FIELDS,
        index_params=settings.milvus.VECTOR_FIELD_INDEX_PARAMS
    )