
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from db.models.published_item import PublishItem
from db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    icon = Column(String, nullable=False)

    posts: Mapped[list["PublishItem"]] = relationship(
        "PublishItem",
        order_by="desc(PublishItem.publish_date)",
        primaryjoin="and_(User.id==PublishItem.user_id, PublishItem.type=='post')",
        viewonly=True
    )

    comments: Mapped[list["PublishItem"]] = relationship(
        "PublishItem",
        order_by="desc(PublishItem.publish_date)",
        primaryjoin="and_(User.id==PublishItem.user_id, PublishItem.type=='comment')",
        viewonly=True
    )

    liked_posts: Mapped[list["PublishItem"]] = relationship(
        "PublishItem",
        secondary="likes",
        secondaryjoin="and_(Like.item_id==PublishItem.id, PublishItem.type=='post')",
        viewonly=True
    )
    liked_comments: Mapped[list["PublishItem"]] = relationship(
        "PublishItem",
        secondary="likes",
        secondaryjoin="and_(Like.item_id==PublishItem.id, PublishItem.type=='comment')",
        viewonly=True
    )
