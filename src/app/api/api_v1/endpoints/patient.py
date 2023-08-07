from pprint import pprint
from typing import Any, Literal
from fastapi import APIRouter, Depends
from api.deps import get_collection
from db.proxy import CollectionProxy
from db.crud import crud_patient
from schemas import Patient, PatientModifyResult, SearchResponse
from enum import Enum
from core.config import settings

router = APIRouter()

class VectorFields(str, Enum):
    seizure_evolution = "seizure_evolution"
    precipitating_factor = "precipitating_factor"  
    emotion_or_feeling = "emotion_or_feeling"
# vector_fields = Enum("VectorField", {_: _ for _ in settings.milvus.VECTOR_FIELDS}, type=str)

@router.get("/ann_search", response_model=SearchResponse)
def ann_search_patients(
    query: str,
    field: VectorFields,
    limit: int = 10,
    offset: int = 0,
    collection: CollectionProxy = Depends(get_collection)
): 
    return crud_patient.ann_search_patient(
        collection, query=query, field=field.name, limit=limit, offset=offset
    )

@router.get("/{patient_id}", response_model=list[Patient])
def read_patients(patient_id: int, collection: CollectionProxy = Depends(get_collection)):
    return crud_patient.get_patient_by_id(collection, id=patient_id)

@router.get("/", response_model=list[Patient])
def read_patients_by_fields(
    field: str,
    value: Any,
    collection: CollectionProxy = Depends(get_collection)
):
    return crud_patient.get_patient_by_fields(collection, field=field, value=value)


@router.post("/batch", response_model=PatientModifyResult)
def delete_patients(
    patients_id: list[int],
    collection: CollectionProxy = Depends(get_collection)
):
    '''
    按照id批量删除病人
    '''
    return crud_patient.delete_patients(collection, *patients_id)

@router.post("/", response_model=PatientModifyResult)
def create_patients(
    patients: list[Patient],
    collection: CollectionProxy = Depends(get_collection)
):
    
    return crud_patient.create(collection, *patients)

@router.delete("/{patient_id}", response_model=PatientModifyResult)
def delete_patient(
    patient_id: int,
    collection: CollectionProxy = Depends(get_collection)
):
    return crud_patient.delete_patients(collection, patient_id)

# @router.delete("/", response_model=PatientModifyResult)
# def delete_all_patients(
#     collection: CollectionProxy = Depends(get_collection)
# ):
#     patients = collection.query("id >= 0")
#     ids = [_["id"] for _ in patients]
    
#     return collection.delete(*ids)


@router.put("/{patient_id}", response_model=PatientModifyResult)
def update_patient(
    patient_id: int,
    field_name: str,
    value: str,
    collection: CollectionProxy = Depends(get_collection)
):
    return crud_patient.update_patient_field(
        collection, 
        patient_id=patient_id, 
        field_name=field_name, 
        value=value
    )

