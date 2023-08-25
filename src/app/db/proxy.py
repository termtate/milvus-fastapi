from typing import Any

import pandas as pd
from milvus.types import SearchConfig
from milvus.client import Collection

class CollectionProxy:
    def __init__(self, collection1: Collection, collection2: Collection):
        self.collection1 = collection1
        self.collection2 = collection2
    
    def load(self):
        self.collection1.load()
        self.collection2.load()
    
    def flush(self):
        self.collection1.flush()
        self.collection2.flush()
    
    def release(self):
        self.collection1.release()
        self.collection2.release()
    
    def dispatch(self, patients: list[dict]):
        p1_fields = self.collection1.fields()
        # p2_fields = self.collection2.fields()
        
        p1s: list[dict] = []
        p2s: list[dict] = []
        
        for p in patients:
            p1 = {}
            p2 = {}
            for name in p:
                if name in p1_fields:
                    p1[name] = p[name]
                else:
                    p2[name] = p[name]
            p1s.append(p1)
            p2s.append(p2)
        
        return p1s, p2s
    
    def concat(self, p1: list[dict], p2: list[dict]) -> list[dict]:
        p1.sort(key=lambda i: i[self.collection1.primary_field])
        p2.sort(key=lambda i: i[self.collection2.primary_field])
        
        res = []
        for a, b in zip(p1, p2):
            a.update(b)
            res.append(a)
        
        return res
        
    def from_p1(self, field) -> bool:
        return field in self.collection1.fields()
    
    def fill(self, data: list[dict], from_p1: bool):
        ids = [_[self.collection1.primary_field] for _ in data]

        if from_p1:
            other = self.collection2.query(f"{self.collection2.primary_field} in {ids}")
        else:
            other = self.collection1.query(f"{self.collection1.primary_field} in {ids}")

        return self.concat(data, other)
                
    
    def query(self, field: str, value: Any):
        if field == self.collection1.primary_field:
            a = self.collection1.query(f"{field} == {value}")
            b = self.collection2.query(f"{self.collection2.primary_field} == {value}")
            return self.concat(a, b)
        
        if self.from_p1(field):
            data = self.collection1.query(f"{field} == {value!r}")
        else:
            data = self.collection2.query(f"{field} == {value!r}")
        
        return self.fill(data, self.from_p1(field))
    
    def ann_insert(self, data: list[dict]):
        p1s, p2s = self.dispatch(data)

        res = self.collection1.ann_insert(pd.DataFrame(p1s))

        df = pd.DataFrame(p2s)
        df.insert(0, self.collection2.primary_field, list(res.primary_keys))
        self.collection2.ann_insert(df)
        return res
    
    def ann_search(self, query: str, search_config: SearchConfig):
        field = search_config["anns_field"]
        if self.from_p1(field):
            res = self.collection1.ann_search(query, search_config)
        else:
            res = self.collection2.ann_search(query, search_config)
        
        return self.fill(res, self.from_p1(field))
        
        
    
    def delete(self, *ids: int):
        res = self.collection1.delete(*ids)
        self.collection2.delete(*ids)
        return res
    
    def update(self, id: int, field: str, value):
        if self.from_p1(field):
            return self.collection1.update(id, field, value)
        return self.collection2.update(id, field, value)