from pymilvus import SearchResult, connections, CollectionSchema, DataType, utility, FieldSchema
from pymilvus import Collection as _Collection
from typing import Any, Union, Optional, Sequence
from contextlib import contextmanager, AbstractContextManager
from pymilvus.orm.schema import CollectionSchema
import pandas as pd
from milvus.types import SearchConfig
from functools import cache, cached_property
from milvus.embedding import text_embedding
from logging import getLogger
from pymilvus.exceptions import PrimaryKeyException
from milvus.config import settings


logger = getLogger(__name__)


class MilvusConnection(AbstractContextManager):
    '''
    用来建立milvus连接，获取或者创建milvus的collection
    :example:
        >>> from milvus.client import MilvusConnection
        >>> with MilvusConnection("localhost", 19530) as connection:
        >>>     collection = connection.get_collection(name="collection_name", embedding_fields=[])
    '''
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
        vector_fields: Optional[list[str]] = None,
        index_params: Optional[dict[str, str]] = None
    ):
        '''
        创建一个collection，如果有同名collection就丢弃之前的collection。\n
        由于milvus中限制一个collection中只能有一个vector字段，所以若要在collection进行多个列的向量搜索，
        就必须让每一个向量列都单独建立一个collection，这些collection以pid（外键）联系主表
        :args:
            schema: CollectionSchema，其中不需要添加vector类型的字段，向量字段会根据`vector_fields`参数自动生成 \n
            vector_fields: 需要增加向量字段的字段名 \n
            index_params: 详情参考 https://milvus.io/docs/build_index.md#Prepare-index-parameter
        :example:
            >>> name = "table"
            >>> fields = [
            ...     FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            ...     FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=100),
            ...     FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=500)
            ... ]
            >>> vector_fields = ["name", "content"]
            >>> index_params = {
            ...     'metric_type': "L2", 
            ...     'index_type': "FLAT",
            ... }
            >>> collection = connection.create_collection(
            ...     collection_name=name,
            ...     schema=CollectionSchema(fields),
            ...     vector_fields=vector_fields,
            ...     index_params=index_params
            ... )
            
        '''

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
                        name="pid",  # 原collection的一行数据对应的id
                        dtype=DataType.INT64,
                    ),
                    FieldSchema(
                        name="vector",
                        dtype=DataType.FLOAT_VECTOR,
                        dim=settings.VECTOR_DIM
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
            
        # collection必须要有一个vector字段
        schema.add_field(
            field_name="unused",
            datatype=DataType.FLOAT_VECTOR,
            dim=1
        )

        collection = _Collection(name=collection_name, schema=schema)
        
        collection.create_index(field_name="unused")

        return Collection(self, collection, vector_collections)
    
    
class Collection:
    '''
    :example:
        >>> with collection.load_data():
        >>>     res = collection.query(expr="id in [1, 2]")
        >>>     print(res)
        -   [{"id": 1, ...}, {"id": 2, ...}]
    '''
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
        '''
        collection在搜索数据前需要将数据装载进内存，即每次搜索前要先调用collection.load()
        '''
        self.collection.load()
        
        for vc in self.vector_collections.values():
            vc.load()
        
    def flush(self):
        '''
        保证在collection.flush()之前插入的数据都插入至collection，
        详情参考 https://milvus.io/api-reference/pymilvus/v2.3.x/Collection/flush().md
        '''
        self.collection.flush()
        
        for vc in self.vector_collections.values():
            vc.flush()
    
    def release(self):
        '''
        释放装载数据的内存
        '''
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
    
    
    @cache
    def fields(self, *, include_auto_id: bool = False) -> list[str]:
        fields: list[FieldSchema] = self.collection.schema.fields 

        return [
            _.name for _ in filter(
                lambda field: not(
                    # (field.name in self.vector_fields and not include_vector_fields) or
                    (field.is_primary and (field.auto_id and not include_auto_id))
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
        returns:
            包含字典的列表，每个字典的键为字段名，值为字段值
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

        # pprint(tuple(self.fields()))
        # pprint(fields)
        assert tuple(self.fields()) == fields, \
            "dataframe的字段名需要与milvus的collection的字段名的名称、数量、顺序一致"
            
        df["unused"] = df.apply(lambda _: [0], axis=1)
        
        res = self.collection.insert(
            data=df
        )
        
        
        
        for name, collection in self.vector_collections.items():
            vector_column = df.apply(lambda x: text_embedding(x[name]), axis=1)
            insert_data = [
                list(res.primary_keys),
                vector_column.to_list(),
            ]
            collection.insert(insert_data)

        return res
    
    
    def insert(self, *data: list):
        '''
        insert raw data
        '''
        return self.collection.insert(list(zip(*data)))
    
    def ann_search(
        self, 
        query: str,
        search_config: SearchConfig
    ) -> list[dict]:
        '''
        执行query的向量相似度查询
        args:            
            search_config: 查询设置，具体参见 https://milvus.io/docs/v2.0.x/search.md#Conduct-a-vector-search
        returns:
            包含字典的列表，每个字典的键为字段名，值为字段值
        '''        
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

        return sorted(
            self.collection.query(
                expr=f"{self.primary_field} in {list(pids.keys())}",
                limit=search_config["limit"],
                offset=search_config["offset"],
                output_fields=output_fields
            ),
            key=lambda i: pids[i[self.primary_field]]
        )





