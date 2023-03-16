from datetime import datetime

from pydantic import BaseModel

from db.models.published_item import Item
from schemas import User


class PublishBase(BaseModel):
    content: str
    belongs: int = -1


class PublishCreate(PublishBase):
    pass


class Publish(PublishBase):
    id: int
    type: Item
    owner: User

    publish_date: datetime

    is_liked: bool = False
    likes_num: int = 0

    class Config:
        orm_mode = True


class Comment(Publish):
    pass


class Post(Publish):
    comments_num: int = 0
