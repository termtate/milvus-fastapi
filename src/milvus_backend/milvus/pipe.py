import pandas as pd
from towhee import ops, pipe
from towhee.runtime.data_queue import DataQueue
from typing import Callable, Sequence, Union, Optional
from functools import lru_cache
from milvus.types import SearchConfig

# 文本嵌入模型
text_embedding_model = ops.sentence_embedding.transformers(model_name='distiluse-base-multilingual-cased-v2')


@lru_cache(maxsize=20)
def insert_pipe(
    host: str, 
    port: Union[int, str], 
    collection_name: str, 
    fields: tuple[str, ...],
    vector_field: str,
) -> Callable[[pd.DataFrame], DataQueue]:
    '''
    向指定milvus客户端插入数据
    '''
    return (pipe
        .input('df')
        .flat_map("df", fields, lambda df: df.values.tolist()) 
        .map(vector_field, "vector", text_embedding_model)
        .map(
            fields + ("vector", ), 
            'res', 
            ops.ann_insert.milvus_client(
                host=host,
                port=port,
                collection_name=collection_name
            )
        )
        .output('res')
    )


# @lru_cache(maxsize=20)
def search_pipe(
    host: str, 
    port: Union[int, str], 
    collection_name: str, 
    output_fields: tuple[str],
    primary_field: str,
    
) -> Callable[[SearchConfig, str | Sequence[str]], DataQueue]:
    '''
    向milvus客户端中进行向量相似搜索
    '''
    return (pipe
        .input('kwargs', 'query')
        .map('query', 'vec', text_embedding_model)
        .map("kwargs", "fields", lambda kwargs: kwargs["output_fields"])
        .map("kwargs", "client", lambda kwargs: ops.ann_search.milvus_client(
                host=host,
                port=port,
                collection_name=collection_name,
                output_fields=list(_ for _ in output_fields if _ != primary_field),
                **kwargs
            )
        )
        .flat_map(
            ('vec', 'client'),  
            (primary_field, 'score') + tuple(_ for _ in output_fields if _ != primary_field),
            lambda vec, client: client(vec)
        )
        .output('query', 'score', *output_fields)
    )