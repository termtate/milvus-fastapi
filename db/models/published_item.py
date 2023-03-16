from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, RelationshipProperty, Mapped

from db.models.like import Like
from db.session import Base
import enum

if TYPE_CHECKING:
    from db.models.user import User


class Item(str, enum.Enum):
    post = "post"
    comment = "comment"


class PublishItem(Base):
    __tablename__ = "publish_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String, index=True, nullable=False)
    publish_date = Column(DateTime, nullable=False, default=datetime.now)
    type = Column(Enum(Item), nullable=False)
    belongs = Column(Integer, nullable=False, default=-1)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner: Mapped["User"] = relationship("User")

    likes: Mapped[list["Like"]] = relationship("Like")







