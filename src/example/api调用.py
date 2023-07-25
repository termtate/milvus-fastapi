import httpx  # 或者可以使用requests
from example.model import Patient
from pydantic import parse_raw_as
import asyncio
from pprint import pprint

url = "http://127.0.0.1:8000/api/v1/patients"

# get请求方式

def get(url: str, params: dict | None = None) -> list[Patient]:
    res = httpx.get(url, params=params, follow_redirects=True) # 需要加follow_redirects允许重定向
    response = parse_raw_as(list[Patient], res.content)  # 解析响应的json为Patient类
    return response

# 或者可以异步调用
async def async_call(url: str, params: dict | None = None):
    async with httpx.AsyncClient() as client:
        get = await client.get(url, params=params, follow_redirects=True)
        response = parse_raw_as(list[Patient], get.content)
        pprint(response) 



pprint(get(f"{url}/123002"))  # 查询id为123002的病人


asyncio.run(async_call(f"{url}/123002")) # 异步调用

pprint(get(url, params={"sex": "男"}))   # 查询男病人，具体参数参见api文档
pprint(get(f"{url}/ann_search", params={  # 向量相似查询
    "query": "闻到糊味",
    # "limit": 10  # limit参数可选，默认10
}))




# post请求方式

# 添加一个病人
httpx.post(url, json=[
  {
    "id": 0,
    "id_card_number": "string",
    "name": "test",
    "hospitalize_num": "string",
    "case_number": "string",
    "sex": "男",
    "age": "string",
    "phone_number": "string",
    "seizure_evolution": "string"
  }
], follow_redirects=True)


# 或者使用Patient类添加
# insert_patients = [
#     Patient(
#         id=0,
#         id_card_number="string",
#         name="test",
#         hospitalize_num="string",
#         case_number="string",
#         sex="男",
#         age="string",
#         phone_number="string",
#         seizure_evolution="string"
#     )
# ]
# httpx.post(url, json=[patient.dict() for patient in insert_patients], follow_redirects=True)

# 删除一个病人
httpx.delete(f"{url}/0") # 删除id为0的病人

# 删除多个病人
# httpx.post(f"{url}/batch", json=[123002, 123003, 123004, ]) # 删除id为123002, 123003, 123004的病人