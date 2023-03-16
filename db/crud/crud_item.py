from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.crud.base import CRUDBase
from db.models.published_item import PublishItem, Item
from schemas import PublishCreate


class CRUDPublishItem(CRUDBase[PublishItem, PublishCreate, BaseModel]):
    def publish_item(self, db: Session, item: PublishCreate, user_id: int, item_type: Item):
        db_item = self.model(**item.dict(), user_id=user_id, type=item_type)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def get_posts(self, db: Session) -> list[PublishItem]:
        return db.query(self.model)\
            .filter(self.model.type == Item.post)\
            .order_by(self.model.publish_date.desc())\
            .all()

    def get_post_comments(self, db: Session, post_id: int) -> list[PublishItem]:
        return db.query(self.model)\
            .filter(self.model.type == Item.comment)\
            .filter(self.model.belongs == post_id)\
            .order_by(self.model.publish_date.desc())\
            .all()


crud_item = CRUDPublishItem(PublishItem)
