from pydantic import BaseModel, ConfigDict
from pymilvus import FieldSchema


class Table(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    table_name: str
    fields: list[FieldSchema]
    vector_fields: list[str]  # 会给 vector_fields 内的每一个字段都生成向量字段
    index_params: dict[str, str]
    