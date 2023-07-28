from enum import Enum
from pydantic import BaseModel
from typing import Literal

class Patient(BaseModel):
    id: int
    id_card_number: str
    name: str
    hospitalize_num: str
    case_number: str
    sex: Literal["男", "女"]
    age: str
    phone_number: str
    seizure_evolution: str

