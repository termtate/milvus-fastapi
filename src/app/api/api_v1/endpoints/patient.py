from typing import Literal
from fastapi import APIRouter, Depends
from api.deps import get_collection
from milvus.client import Collection
from db.crud import crud_patient
from schemas import Patient, PatientQuery, PatientANNResp, PatientModifyResult
from enum import Enum
from core.config import settings

router = APIRouter()

class VectorFields(str, Enum):
    seizure_evolution = "seizure_evolution"
# vector_fields = Enum("VectorField", {_: _ for _ in settings.milvus.VECTOR_FIELDS}, type=str)

@router.get("/ann_search", response_model=list[PatientANNResp])
def ann_search_patients(
    query: str,
    field: VectorFields,
    limit: int = 10,
    collection: Collection = Depends(get_collection)
): 
    return crud_patient.ann_search_patient(collection, query=query, field=field.name, limit=limit)

@router.get("/{patient_id}", response_model=list[Patient])
def read_patients(patient_id: int, collection: Collection = Depends(get_collection)):
    return crud_patient.get_patient_by_id(collection, id=patient_id)

@router.get("/", response_model=list[Patient])
def read_patients_by_fields(
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


@router.post("/batch", response_model=PatientModifyResult)
def delete_patients(
    patients_id: list[int],
    collection: Collection = Depends(get_collection)
):
    '''
    按照id批量删除病人
    '''
    return crud_patient.delete_patients(collection, *patients_id)

@router.post("/", response_model=list[PatientModifyResult])
def create_patients(
    patients: list[Patient],
    collection: Collection = Depends(get_collection)
):
    return crud_patient.create(collection, *patients)

@router.delete("/{patient_id}", response_model=PatientModifyResult)
def delete_patient(
    patient_id: int,
    collection: Collection = Depends(get_collection)
):
    return crud_patient.delete_patients(collection, patient_id)
