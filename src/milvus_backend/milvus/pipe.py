import pandas as pd
from towhee import ops, pipe
from towhee.runtime.data_queue import DataQueue
from typing import Callable, Sequence, Union, Optional
from functools import lru_cache

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


def search_pipe(
    host: str, 
    port: Union[int, str], 
    collection_name: str, 
    output_fields: Sequence[str],
    primary_field: str,
    **kwargs,
):
    '''
    向milvus客户端中进行向量相似搜索
    '''
    fields = tuple(output_fields)

    return (pipe
        .input('query')
        .map('query', 'vec', text_embedding_model)
        .flat_map(
            'vec',
            (primary_field, 'score') + tuple(_ for _ in fields if _ != primary_field),
            ops.ann_search.milvus_client(
                host=host,
                port=port,
                collection_name=collection_name,
                output_fields=list(_ for _ in fields if _ != primary_field),
                **kwargs
            )
        )
        .output('query', 'score', *fields)
    )