from typing import Any, Sequence, TypedDict
from typing_extensions import Required


# class VectorField(TypedDict):
#     field_name: str
#     index_params: dict[str, str] # https://milvus.io/docs/v2.0.x/search.md#Prepare-search-parameters


class SearchConfig(TypedDict, total=False):
    output_fields: Sequence[str]
    anns_field: Required[str]
    limit: int
    offset: int
    param: dict[str, str] # https://milvus.io/docs/v2.0.x/search.md#Prepare-search-parameters