from pydantic import BaseModel, validator


class UserBase(BaseModel):
    name: str
    icon: str


class UserCreate(UserBase):
    phone_number: str
    password: str

    @validator("phone_number")
    def check_phone_number(cls, v: str) -> str:
        assert v.isdecimal(), "must be decimal"
        if len(v) != 11:
            raise ValueError("length is not 11")
        return v


class UserUpdate(UserBase):
    password: str
    phone_number: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

