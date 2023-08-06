from typing import Literal, Any, TypeAlias

from pydantic import BaseModel, create_model
from pydantic.dataclasses import dataclass
from core.config import settings
from pymilvus import DataType

class PatientQuery(BaseModel):
    id_card_number: str | None = None
    name: str | None = None
    hospitalize_num: str | None = None
    case_number: int | None = None
    sex: Literal["男", "女"] | None = None
    age: str | None = None
    phone_number: str | None = None
    # seizure_evolution: str | None = None


# @dataclass
# class Patient:
#     id: int
#     id_card_number: str
#     name: str
#     hospitalize_num: str
#     case_number: str
#     sex: Literal["男", "女"]
#     age: str
#     phone_number: str
#     seizure_evolution: str

#     class Config:
#         orm_mode = True

class Patient(BaseModel):
    id: int
    id_card_number: str
    name: str
    hospitalize_num: str
    case_number: str
    sex: str
    age: str
    phone_number: str
    seizure_evolution: str
    seizure_duration: str
    seizure_freq: str
    maternal_pregnancy_age: str
    pregnancy_num: str
    birth_weight: str
    head_c: str
    blood_urine_screening: str
    copper_cyanin: str
    csf: str
    genetic_test: str
    head_ct: str
    head_mri: str
    scalp_eeg: str
    precipitating_factor: str


class SearchResponse(BaseModel):
    data: list[Patient]
    limit: int
    offset: int
    
    

class PatientWithVector(Patient):
    vector_seizure_evolution: list[float]

class PatientANNResp(Patient):
    query: str
    score: float


class PatientModifyResult(BaseModel):
    insert_count: int
    delete_count: int
    upsert_count: int
    timestamp: int
    succ_count: int
    err_count: int
    
    class Config:
        orm_mode = True

    
    
    

