import pandas as pd
from towhee import ops, pipe
from towhee.runtime.data_queue import DataQueue
from typing import Callable, Sequence, Union, Optional
from functools import lru_cache, partial
from milvus.types import SearchConfig
from numpy.typing import NDArray


# 文本嵌入模型
text_embedding_model = ops.sentence_embedding.transformers(model_name='distiluse-base-multilingual-cased-v2') # type: ignore


def text_embedding(text: str) -> NDArray:
    return text_embedding_model(text)

# def embedding_df(fields: Sequence[str], df):
#     # return {
#     #     f"vector_{field}": df.apply(lambda x: text_embedding_model(x[field]), axis=1)
#     #     for field in fields
#     # }
#     for field in fields:
#         df[f"vector_{field}"] = df.apply(lambda x: text_embedding(x[field]), axis=1)
    
#     # print(df.head())
#     return df

# @lru_cache(maxsize=20)