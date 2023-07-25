from typing import Any, Sequence, TypedDict
from typing_extensions import Required


class IndexParams(TypedDict):
    field_name: str
    index_params: dict[str, Any] # https://milvus.io/docs/v2.0.x/search.md#Prepare-search-parameters


class SearchConfig(TypedDict, total=False):
    output_fields: Sequence[str]
    anns_field: str
    limit: int
    param: dict[str, Any] # https://milvus.io/docs/v2.0.x/search.md#Prepare-search-parameters