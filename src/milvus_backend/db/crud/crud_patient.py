from typing import Any
from milvus.client import Collection
from schemas import Patient, PatientQuery, PatientANNResp
import pandas as pd
from core.config import settings
from towhee import DataCollection



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
        df = pd.DataFrame(patients)
        
        r = collection.ann_insert(
            df,
            embedding_field=settings.milvus.EMBEDDING_FIELD_NAME
        )

        collection.flush()

        # print(DataCollection(r).to_list())
        return [
            _["res"] for _ in r.to_list(kv_format=True) # type: ignore
        ]
    
    def ann_search_patient(self, collection: Collection, query: str, limit: int):
        res = collection.ann_search(
            query=query,
            search_config= {
                "param": settings.milvus.FIELD_INDEX_PARAMS["index_params"],
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
        id: int
    ):
        return collection.delete(id)
        
        
crud_patient = CRUDPatient()