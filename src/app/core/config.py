
from pydantic import BaseSettings
from pymilvus import FieldSchema, DataType


class MilvusSettings(BaseSettings):
    HOST = "localhost"
    PORT = 19530
    
    COLLECTION_NAME_1 = "test1"
    COLLECTION_NAME_2 = "test2"
    
    # https://milvus.io/docs/v2.0.x/build_index.md#Prepare-index-parameter
    VECTOR_FIELD_INDEX_PARAMS = {
        'metric_type': "L2", 
        'index_type': "FLAT",
    }
    
    VECTOR_FIELDS_1: list[str] = [
        "seizure_evolution",   
        "precipitating_factor"                                     
    ]
    
    VECTOR_FIELDS_2: list[str] = [
        "emotion_or_feeling"
    ]


class Settings(BaseSettings):
    milvus = MilvusSettings()
    
    API_V1_STR: str = "/api/v1"
    
    columns_name_map = {
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
        "儿童期起病": "childhood_onset",
        "抗癫痫药物": "aed",
        "癫痫外科": "epilepsy_surgery",
        "简单感觉发作": "simple_sensory_seizure",
        "父母是否有过热性惊厥": "is_parent_febrile_convulsion",
        "孕期疾病": "pregnancy_diseases",
        "婴儿期起病": "infancy_onset",
        "运动型": "motor_seizure",
        "遗传代谢疾病": "metabolic_disorders",
        "发作后表现": "postictal_manifestation",
        "症状性癫痫": "symptomatic_epilepsy",
        "有手术史": "have_surgery_history",
        "自动症": "automatism",
        "全面性运动性发作": "generalized_motor_seizures",
        "色素沉积": "pigmentation",
        "局灶运动性发作": "local_motor_seizures",
        "自主神经": "autonomic_nerves",
        "认知": "cognition",
        "其他癫痫综合征": "other_epilepsy_syndrome",
        "电解质": "electrolyte",
        "新生儿期起病": "neonatal_onset",
        "预防接种史": "vaccination_history",
        "亲属是否有癫痫病人": "is_relatives_have_epilepsy",
        "血乳酸": "lactate",
        "生长发育里程碑": "growth_milestone",
        "生长发育史迟缓": "growth_retardation",
        "青少年_成年期起病": "adolescent_adult_onset",
        "发育迟缓": "stunting",
        "血氨": "blood_ammonia",
        "全面性非运动性发作": "generalized_non_motor_seizures",
        "求学困难": "learning_difficulties",
        "局灶非运动发作": "focal_non_motor_seizures",
        "被过度保护": "overprotected",
        "有无热性惊厥史": "has_febrile_seizures_history",
        "有无新生儿惊厥": "has_neonatal_convulsion",
        "注意缺陷多动障碍": "adhd",
        "是否有重度黄疸": "has_severe_jaundice",
        "喂养困难": "feeding_difficulties",
        "情绪或情感": "emotion_or_feeling",
        "与年龄无特殊关系的癫痫综合征": "epilepsy_syndromes_no_specifically_related_to_age",
        "生酮饮食": "ketogenic_diet",
        "羊水污染": "stained_amniotic_fluid",
        "输血史": "blood_transfusion_history",
        "外伤史": "trauma_history",
        "局灶性继发双侧强直_阵挛发作": "focal_secondary_bilateral_tonic_clonic_seizures",
        "父母是否近亲结婚": "is_parents_consanguineous_married",
        "跌倒": "fall",
        "是否有出生窒息": "has_birth_asphyxia",
        "惊厥史": "convulsion_history",
        "生长发育倒退": "growth_regression",
        "心理压力大": "high_psychological_pressure",
        "呕吐": "vomit",
        "伴发热": "accompanying_fever",
        "分娩方式": "delivery_mode",
        "腹泻": "diarrhea",
        "抽动症": "tic",
        "自闭症": "autism"
    }


settings = Settings()
