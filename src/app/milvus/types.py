from typing import Any, Sequence, TypedDict
from typing_extensions import Required


class SearchConfig(TypedDict, total=False):
    output_fields: Sequence[str]
    anns_field: Required[str]
    limit: int
    offset: int
    param: dict[str, str] # https://milvus.io/docs/v2.0.x/search.md#Prepare-search-parameters