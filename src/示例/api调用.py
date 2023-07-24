import httpx
from model import Patient
from pydantic import parse_raw_as

url = "http://127.0.0.1:8000/api/v1/patients"

get = httpx.get(f"{url}/123002")

response = parse_raw_as(list[Patient], get.content)
print(response) 