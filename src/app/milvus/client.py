from pprint import pprint
from sre_constants import ANY
from types import TracebackType
from pymilvus import SearchResult, connections, CollectionSchema, DataType, utility, FieldSchema
from pymilvus import Collection as _Collection
from typing import Any, Union, Optional, overload, List, Sequence, Callable
from contextlib import contextmanager, AbstractContextManager
from pymilvus.orm.schema import CollectionSchema
import pandas as pd
from towhee.runtime.data_queue import DataQueue
from milvus.types import SearchConfig
from functools import cache, cached_property
from milvus.embedding import text_embedding
from logging import getLogger
from pymilvus.exceptions import PrimaryKeyException


logger = getLogger(__name__)


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
        
    def get_collection(self, name: str, embedding_fields: Sequence[str]):
        return Collection(
            self, 
            _Collection(name=name),
            [_Collection(name=field) for field in embedding_fields]
        ) 
    

    def create_collection(
        self, 
        collection_name: str, 
        schema: CollectionSchema,
        # embedding_field: Sequence[str],
        vector_fields: Optional[list[str]] = None,
        index_params: Optional[dict[str, str]] = None
    ):
        # assert schema.fields[-1].dtype == DataType.FLOAT_VECTOR, "向量字段需要放在最后"
        
        # 如果数据库有同名collection就丢弃
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
        
        vector_collections: list[_Collection] = []
        
        
        if vector_fields is not None:
            for name in vector_fields:
                vector_schema = [
                    FieldSchema(
                        name="id",
                        dtype=DataType.INT64,
                        is_primary=True,
                        auto_id=True
                    ),
                    FieldSchema(
                        name="pid",
                        dtype=DataType.INT64,
                    ),
                    FieldSchema(
                        name="vector",
                        dtype=DataType.FLOAT_VECTOR,
                        dim=768
                    )
                ]
                collection_schema = CollectionSchema(
                    fields=vector_schema,
                    description=""
                )
                if utility.has_collection(name):
                    utility.drop_collection(name)
                coll = _Collection(name, collection_schema)
                coll.create_index(field_name="vector", index_params=index_params)
                vector_collections.append(coll)
            
            # collection = _Collection(name=collection_name, schema=schema)
            
            # return Collection(self, collection, vector_fields)
        schema.add_field(
            field_name="unused",
            datatype=DataType.FLOAT_VECTOR,
            dim=1
        )

        collection = _Collection(name=collection_name, schema=schema)
        
        collection.create_index(field_name="unused")

        return Collection(self, collection, vector_collections)
    
    
class Collection:
    def __init__(
        self, 
        connection: "MilvusConnection",
        collection: _Collection,
        vector_collections: Sequence[_Collection]
    ) -> None:
        self.conn = connection
        self.collection = collection
        
        self.vector_collections = {
            coll.name: coll for coll in vector_collections 
        }
        
    def load(self):
        self.collection.load()
        
        for vc in self.vector_collections.values():
            vc.load()
        
    def flush(self):
        self.collection.flush()
        
        for vc in self.vector_collections.values():
            vc.flush()
    
    def release(self):
        self.collection.release()
        
        for vc in self.vector_collections.values():
            vc.release()
    
    @contextmanager
    def load_data(self):
        self.flush()
        self.load()
        
        try:
            yield
        finally:
            self.release()
    
    
    # @cache
    def fields(self, include_auto_id: bool = False) -> list[str]:
        fields: list[FieldSchema] = self.collection.schema.fields 

        return [
            _.name for _ in filter(
                lambda field: not(
                    # (field.name in self.vector_fields and not include_vector_fields) or
                    (field.is_primary and (field.auto_id and include_auto_id))
                    or field.name == "unused"
                ),
                fields
            )
        ]
    
    @cached_property
    def vector_fields(self):
        return list(self.vector_collections.keys())

    
    @cached_property
    def primary_field(self) -> str:
        primary_field = self.collection.schema.primary_field
        if primary_field is None:
            raise PrimaryKeyException()
        return primary_field.name
        
    
    def query(self, expr: str, output_fields: Sequence[str] | None = None) -> list[dict]: # TODO: 防止注入
        '''
        进行标量查询
        args:
            expr: 查询表达式，具体参见 https://milvus.io/docs/boolean.md
        '''
        if output_fields is None:
            output_fields = self.fields()
        
        return self.collection.query(
            expr=expr,
            output_fields=output_fields
        )
    
    def delete(self, *id: int):
        res = self.collection.delete(f"id in {list(id)}")
        for coll in self.vector_collections.values():
            ids = [_["id"] for _ in coll.query(f"id in {list(id)}")]
            coll.delete(f"id in {ids}")

        return res
    
    # def drop_collection(self):
    #     self.release()
    #     self.collection.drop()
    #     return 
    
    
    def ann_insert(self, data: pd.DataFrame): # TODO: 其他输入类型
        '''
        向数据库中插入数据,同时自动为指定字段生成向量
        args:
            data: dataframe. 表头名必须与collection字段名匹配
            
        '''
        return self._insert_df(data)
    
    
    def update(self, id: int, field: str, value: Any):
        items = self.query(f"{self.primary_field} == {id}")
        assert len(items) != 0
        
        item = items[0]
        assert field in item
        
        item[field] = value
        
        self.delete(id)
        a = [
            _[1] for _ in sorted(
                list(item.items()),
                key=lambda i: self.fields().index(i[0])
            )
        ]
        a.append([0])
        # pprint(a)
        return self.collection.insert([[_] for _ in a])

    
    def _insert_df(self, df):
        fields = tuple(df.columns)
        # print(self.fields())
        assert tuple(self.fields()) == fields, \
            "dataframe的字段名需要与milvus的collection的字段名的名称、数量、顺序一致"
        
        for name, collection in self.vector_collections.items():
            vector_column = df.apply(lambda x: text_embedding(x[name]), axis=1)
            insert_data = [
                df[self.primary_field],
                vector_column,
            ]
            
            collection.insert(
                [_.to_list() for _ in insert_data],
            )
        df["unused"] = df.apply(lambda _: [0], axis=1)
        return self.collection.insert(
            data=df
        )
    
    
    def insert(self, *data: list):
        return self.collection.insert(list(zip(*data)))
    
    def ann_search(
        self, 
        query: str,
        search_config: SearchConfig
    ) -> list:
        '''
        执行query的向量相似度查询
        args:
            query: 输入的查询，如果为多个，会返回多个对应的结果
            
            search_config: 查询设置，具体参见 https://milvus.io/docs/v2.0.x/search.md#Conduct-a-vector-search
        '''        
        # if "output_fields" in search_config and tuple(search_config["output_fields"]) != self.fields(include_auto_id=True):
        #     return search_pipe(
        #         host=self.conn.host,
        #         port=self.conn.port,
        #         collection_name=self.collection.name,
        #         primary_field=self.primary_field,
        #         output_fields=tuple(search_config["output_fields"])
        #     )(search_config, query)
        data = text_embedding(query)
        vector_field = search_config["anns_field"]

        assert vector_field in self.vector_collections

        search_config["anns_field"] = "vector"
        output_fields = search_config["output_fields"] \
            if "output_fields" in search_config else self.fields(include_auto_id=True)
        search_config["output_fields"] = ["pid"]

        if "param" not in search_config:
            search_config["param"] = {}

        if "limit" not in search_config:
            search_config["limit"] = 10

        if "offset" not in search_config:
            search_config["offset"] = 0

        res: SearchResult = self.vector_collections[vector_field].search(
            data=[data.tolist()],
            **search_config
        ) # type: ignore

        pids: dict[int, float] = {
            e.entity.get("pid"): e.distance
            for e in res[0]
        }
        # print(pids)

        return sorted(
            self.collection.query(
                expr=f"{self.primary_field} in {list(pids.keys())}",
                limit=search_config["limit"],
                offset=search_config["offset"],
                output_fields=output_fields
            ),
            key=lambda i: pids[i[self.primary_field]]
        )
        
        
        # self.collection.search(
        #     data=[data.tolist()],
        #     **search_config
        # )
        
        # return self._search_pipe(search_config, query)




