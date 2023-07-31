from typing import Any
from milvus.client import Collection
from schemas import Patient, PatientQuery, PatientANNResp, PatientWithVector
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
        patient: PatientQuery,
    ) -> list[dict[str, Any]]:
        res = []
        for k, v in patient.dict().items():
            if v is not None:
                if isinstance(v, str):
                    v = f'"{v}"'
                res.append(f"{k} == {v}")
        

        return collection.query(
            expr=" and ".join(res)
        )
    
    def create(self, collection: Collection, *patients: Patient):
        df = pd.DataFrame([_.dict() for _ in patients])
        
        r = collection.ann_insert(df)

        collection.flush()

        return [
            _["res"] for _ in r.to_list(kv_format=True) # type: ignore
        ]
    
    def ann_search_patient(self, collection: Collection, query: str, field: str, limit: int):
        res = collection.ann_search(
            query=query,
            search_config= {
                "anns_field": f"vector_{field}",
                "param": settings.milvus.VECTOR_FIELD_INDEX_PARAMS,
                "limit": limit
            }
        )
        
        col = DataCollection(res).to_dict()
        return [
            PatientANNResp(**_) for _ in [
                dict(zip(col["schema"], row)) for row in col["iterable"]
            ]
        ]
    
    def delete_patients(
        self, 
        collection: Collection,
        *id: int
    ):
        return collection.delete(*id)
    
    def update_patient_field(
        self, 
        collection: Collection, 
        patient_id: int, 
        field_name: str, 
        value: Any
    ):
        patients = collection.query(
            f"id == {patient_id}",
            output_fields=collection.fields(include_vector_fields=True)
        )
        if len(patients) == 0:
            raise PrimaryKeyException(message="id not exist")
        
        
        patient = PatientWithVector.parse_obj(patients[0])
        assert field_name in patient.__fields__
        
        collection.delete(patient.id)
        
        patient = patient.copy(
            update={
                field_name: value
            }
        )
        return collection.insert(list(patient.dict().values()))
        
        
        
        
        
        
crud_patient = CRUDPatient()