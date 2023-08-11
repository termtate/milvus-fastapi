from typing import Any
from db.proxy import CollectionProxy
from schemas import Patient, SearchResponse, PatientCreate
import pandas as pd
from core.config import settings
from towhee import DataCollection
from pymilvus.exceptions import PrimaryKeyException



class CRUDPatient:
    def get_patient_by_id(self, collection: CollectionProxy, *, id: int) -> list[dict[str, Any]]:
        return collection.query("id", id)
    
    def get_patient_by_fields(
        self,
        collection: CollectionProxy, 
        *, 
        field: str,
        value: Any
    ) -> list[dict[str, Any]]:
        return collection.query(field, value)
    
    def create(self, collection: CollectionProxy, *patients: PatientCreate):        
        r = collection.ann_insert([_.dict() for _ in patients])

        collection.flush()

        return r
    
    def ann_search_patient(self, collection: CollectionProxy, query: str, field: str, limit: int, offset: int):
        return {
            "data": collection.ann_search(
                query=query,
                search_config={
                    "anns_field": field,
                    "param": settings.milvus.VECTOR_FIELD_INDEX_PARAMS,
                    "limit": limit,
                    "offset": offset
                },
            ),
            "limit": limit,
            "offset": offset
        }
    
    def delete_patients(
        self, 
        collection: CollectionProxy,
        *id: int
    ):
        return collection.delete(*id)
    
    def delete_all(self, collection: CollectionProxy):
        pass
    
    def update_patient_field(
        self, 
        collection: CollectionProxy, 
        patient_id: int, 
        field_name: str, 
        value: Any
    ):
        return collection.update(id=patient_id, field=field_name, value=value)
        
        
        
        
        
        
crud_patient = CRUDPatient()