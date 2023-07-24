from types import TracebackType
from pymilvus import connections, CollectionSchema, DataType, utility
from pymilvus import Collection as _Collection
from typing import Union, Optional, overload, List, Sequence, Callable
from contextlib import contextmanager, AbstractContextManager
from pymilvus.orm.schema import CollectionSchema
import pandas as pd
from towhee.runtime.data_queue import DataQueue
from milvus.types import IndexParams, SearchConfig
from functools import cached_property
from milvus.pipe import insert_pipe, search_pipe
from logging import getLogger
from pymilvus.exceptions import PrimaryKeyException

logger = getLogger(__name__)


def _cache(func: Callable):
        last_param = None
        last_result = None
        
        def wrapper(self, search_config):
            nonlocal last_param, last_result
            
            if last_result is not None and last_param == search_config:
                logger.info("search_pipe cache hits")
                return last_result

            result = func(self, search_config)
            last_param = search_config
            last_result = result
            
            return result
        
        return wrapper

class MilvusConnection(AbstractContextManager):
    def __init__(
        self, 
        host: str, 
        port: Union[str, int]
    ) -> None:
        self.host = host
        self.port = port
        
        
    def connect(self, alias: str = "default"):
        connections.connect(alias=alias, host=self.host, port=self.port)
    
    def disconnect(self, alias: str = "default"):
        connections.disconnect(alias=alias)
    
    
    def __enter__(self) -> "MilvusConnection":
        self.connect()
        return self
    
    def __exit__(self, __exc_type, __exc_value, __traceback):
        self.disconnect()
        
    def get_collection(self, name: str):
        return Collection(
            self, 
            _Collection(name=name) # type: ignore
        ) 
    

    def create_collection(
        self, 
        collection_name: str, 
        schema: CollectionSchema,
        embedding_field: str,
        index_params: Optional[IndexParams] = None
    ):
        assert schema.fields[-1].dtype == DataType.FLOAT_VECTOR, "向量字段需要放在最后"
        
        # 如果数据库有同名collection就丢弃
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)

        collection = _Collection(name=collection_name, schema=schema)
        if index_params is not None:
            collection.create_index(**index_params)
        
        return Collection(self, collection)
    
    
class Collection:
    def __init__(
        self, 
        connection: "MilvusConnection",
        collection: _Collection,
    ) -> None:
        self.conn = connection
        self.collection = collection
        
        self._search_pipe = search_pipe(
            host=self.conn.host,
            port=self.conn.port,
            collection_name=self.collection.name,
            primary_field=self.primary_field,
            output_fields=tuple(self.fields)
        )
        
    def load(self):
        self.collection.load()
        
    def flush(self):
        self.collection.flush()
    
    def release(self):
        self.collection.release()
    
    @contextmanager
    def load_data(self):
        self.flush()
        self.load()
        
        try:
            yield
        finally:
            self.release()
    
    
    @cached_property
    def fields(self) -> list[str]:
        return [
            _.name for _ in self.collection.schema.fields if _.dtype != DataType.FLOAT_VECTOR
        ]
    
    @cached_property
    def primary_field(self) -> str:
        primary_field = self.collection.schema.primary_field
        if primary_field is None:
            raise PrimaryKeyException()
        return primary_field.name
        
    
    def query(self, expr: str, output_fields: Sequence[str] | None = None): # TODO: 防止注入
        '''
        进行标量查询
        args:
            expr: 查询表达式，具体参见 https://milvus.io/docs/boolean.md
        '''
        if output_fields is None:
            output_fields = self.fields
        
        return self.collection.query(
            expr=expr,
            output_fields=output_fields
        )
    
    def delete(self, id: int):
        return self.collection.delete(f"id in [{id}]")
    
    
    def ann_insert(self, df: pd.DataFrame, embedding_field: str): # TODO: 其他输入类型
        '''
        插入dataframe中的数据
        args:
            data: dataframe. 表头名必须与collection字段名匹配
            embedding_field: 要进行词向量化的字段名，
        '''
        collection_schema = filter(
            lambda field: (not field.is_primary or not field.auto_id)
                and field.dtype != DataType.FLOAT_VECTOR,
            self.collection.schema.fields,
        )

        fields = tuple(df.columns)

        assert tuple(_.name for _ in collection_schema) == fields, \
            "dataframe的字段名需要与milvus的collection的字段名的名称、数量、顺序一致"

        assert embedding_field in fields

        return insert_pipe(
            self.conn.host, 
            self.conn.port, 
            self.collection.name,
            fields,
            embedding_field
        )(df)
    
    
    @overload
    def ann_search(self, query: str, search_config: Optional[SearchConfig]) -> DataQueue: ...
    @overload
    def ann_search(self, query: Sequence[str], search_config: Optional[SearchConfig]) -> List[DataQueue]: ...
    
    def ann_search(
        self, 
        query: Union[str, Sequence[str]],
        search_config: Optional[SearchConfig] = None
    ) -> Union[DataQueue, List[DataQueue]]:
        '''
        执行query的向量相似度查询
        args:
            query: 输入的查询，如果为多个，会返回多个对应的结果
            
            search_config: 查询设置，具体参见 https://milvus.io/docs/v2.0.x/search.md#Conduct-a-vector-search
        '''
        config: SearchConfig = search_config if search_config is not None else {}
        
        if "output_fields" in config and tuple(config["output_fields"]) != self.fields:
            return search_pipe(
                host=self.conn.host,
                port=self.conn.port,
                collection_name=self.collection.name,
                primary_field=self.primary_field,
                output_fields=tuple(config["output_fields"])
            )(config, query)
            
        return self._search_pipe(config, query)




