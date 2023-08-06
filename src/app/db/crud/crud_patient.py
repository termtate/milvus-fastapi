from typing import Any
from milvus.client import Collection
from schemas import Patient, PatientQuery, PatientANNResp, SearchResponse
import pandas as pd
from core.config import settings
from towhee import DataCollection
from pymilvus.exceptions import PrimaryKeyException



class CRUDPatient:
    def get_patient_by_id(self, collection: Collection, *, id: int) -> list[dict[str, Any]]:
        return collection.query(
            f"id == {id}" # TODO: 防止注入
        )
    
    def get_patient_by_fields(
        self,
        collection: Collection, 
        *, 
        field: str,
        value: Any
    ) -> list[dict[str, Any]]:
        return collection.query(
            expr=f"{field} == {value!r}"
        )
    
    def create(self, collection: Collection, *patients: Patient):
        df = pd.DataFrame([_.dict() for _ in patients])
        
        r = collection.ann_insert(df)

        collection.flush()

        return r
    
    def ann_search_patient(self, collection: Collection, query: str, field: str, limit: int, offset: int):
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
        collection: Collection,
        *id: int
    ):
        return collection.delete(*id)
    
    def delete_all(self, collection: Collection):
        pass
    
    def update_patient_field(
        self, 
        collection: Collection, 
        patient_id: int, 
        field_name: str, 
        value: Any
    ):
        return collection.update(id=patient_id, field=field_name, value=value)
        
        
        
        
        
        
crud_patient = CRUDPatient()