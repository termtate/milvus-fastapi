import pandas as pd
from towhee import ops, pipe
from towhee.runtime.data_queue import DataQueue
from typing import Callable, Sequence, Union, Optional
from functools import lru_cache, partial
from milvus.types import SearchConfig


# 文本嵌入模型
text_embedding_model = ops.sentence_embedding.transformers(model_name='distiluse-base-multilingual-cased-v2') # type: ignore


def embedding(fields, df):
    # return {
    #     f"vector_{field}": df.apply(lambda x: text_embedding_model(x[field]), axis=1)
    #     for field in fields
    # }
    for field in fields:
        df[f"vector_{field}"] = df.apply(lambda x: text_embedding_model(x[field]), axis=1)
    
    # print(df.head())
    return df.values.tolist()

# @lru_cache(maxsize=20)
def insert_pipe(
    host: str, 
    port: Union[int, str], 
    collection_name: str, 
    # fields: tuple[str, ...],
    vector_fields: tuple[str, ...],
) -> Callable[[pd.DataFrame], DataQueue]:
    '''
    向指定milvus客户端插入数据
    '''
    # v_fields = tuple(f"v{field}" for field in vector_fields)
    return (pipe
        .input('df')
        # .map("df", "temp", lambda df: partial(embedding, df))  # TODO order
        # .flat_map(vector_fields, "v", lambda v: v)
        .flat_map("df", "data", partial(embedding, vector_fields))
        # .flat_map("df", fields, lambda df: df.values.tolist()) 
        # .flat_map(vector_fields, v_fields, lambda fields: [text_embedding_model(field) for field in fields])
        # .map("data", "ss", lambda s: print(s))
        .map(
            "data", 
            'res', 
            ops.ann_insert.milvus_client( # type: ignore
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
        .map("kwargs", "client", lambda kwargs: ops.ann_search.milvus_client( # type: ignore
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