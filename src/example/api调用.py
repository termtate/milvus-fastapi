import httpx
from example.model import Patient
from pydantic import parse_raw_as
import asyncio

url = "http://127.0.0.1:8000/api/v1/patients"

# get请求方式

get = httpx.get(f"{url}/123002")  # 查询id为123002的病人
# get = httpx.get(f"{url}/123002")

response = parse_raw_as(list[Patient], get.content)  # 解析响应的json为Patient类
print(response) 

# 或者可以异步调用
async def async_call():
    async with httpx.AsyncClient() as client:
        get = await client.get(f"{url}/123002")
        response = parse_raw_as(list[Patient], get.content)
        print(response) 
        

httpx.get(url, params={"sex": "男"})   # 查询男病人


asyncio.run(async_call())


# post请求方式

post = httpx.post(url, )
