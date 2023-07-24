from typing import Literal
from fastapi import APIRouter, Depends, Query
from api.deps import get_collection
from milvus.client import Collection
from db.crud import crud_patient
from schemas import Patient, PatientQuery, PatientANNResp

router = APIRouter()

@router.get("/ann_search", response_model=list[PatientANNResp])
def ann_search_patient(
    query: str,
    limit: int = 10,
    collection: Collection = Depends(get_collection)
): # TODO: 优化调用速度
    '''
    进行文本的相似搜索。第一次调用，或者修改`limit`参数以后会等待较长一段时间
    '''
    return crud_patient.ann_search_patient(collection, query=query, limit=limit)

@router.get("/{patient_id}", response_model=list[Patient])
def read_patient(patient_id: int, collection: Collection = Depends(get_collection)):
    return crud_patient.get_patient_by_id(collection, id=patient_id)

@router.get("/", response_model=list[Patient])
def read_patient_by_fields(
    id_card_number: str | None = None,
    name: str | None = None,
    hospitalize_num: str | None = None,
    case_number: int | None = None,
    sex: Literal["男", "女"] | None = None,
    age: str | None = None,
    phone_number: str | None = None,
    collection: Collection = Depends(get_collection)
):
    return crud_patient.get_patient_by_fields(collection, patient=PatientQuery(
        id_card_number=id_card_number,
        name=name,
        hospitalize_num=hospitalize_num,
        case_number=case_number,
        sex=sex,
        age=age,
        phone_number=phone_number
    ))

@router.post("/")
def create_patients(
    patients: list[Patient],
    collection: Collection = Depends(get_collection)
): # TODO: 优化调用速度
    return crud_patient.create(collection, *patients)

