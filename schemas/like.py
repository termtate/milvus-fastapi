from pydantic import BaseModel, Field


class LikeBase(BaseModel):
    item_id: int


class LikeCreate(LikeBase):
    pass


class LikeDelete(LikeBase):
    pass


class Like(LikeBase):
    user_id: int

    class Config:
        orm_mode = True
