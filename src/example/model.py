from pydantic.dataclasses import dataclass
from typing import Literal

@dataclass
class Patient:
    id: int
    id_card_number: str
    name: str
    hospitalize_num: str
    case_number: str
    sex: Literal["男", "女"]
    age: str
    phone_number: str
    seizure_evolution: str

