from pydantic.dataclasses import dataclass
from pydantic import BaseModel, validate_model
from typing import Literal, TypedDict
from pydantic import Field


class PatientQuery(BaseModel):
    id_card_number: str | None = None
    name: str | None = None
    hospitalize_num: str | None = None
    case_number: int | None = None
    sex: Literal["男", "女"] | None = None
    age: str | None = None
    phone_number: str | None = None
    # seizure_evolution: str | None = None


@dataclass
class Patient:
    id: int
    id_card_number: str
    name: str
    hospitalize_num: str
    case_number: int
    sex: Literal["男", "女"]
    age: str
    phone_number: str
    seizure_evolution: str

    class Config:
        orm_mode = True


@dataclass
class PatientANNResp(Patient):
    query: str
    score: float
    
