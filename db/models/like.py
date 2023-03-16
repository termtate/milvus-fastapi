from sqlalchemy import Column, Integer, ForeignKey

from db.session import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("publish_items.id"))



