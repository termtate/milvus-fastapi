from pydantic.dataclasses import dataclass
from abc import ABC
from pymilvus import CollectionSchema, DataType, FieldSchema


@dataclass
class Table:
    collection_name: str
    fields: list[FieldSchema]
    vector_fields: list[str]
    index_params: dict[str, str]
    
    

