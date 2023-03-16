from pydantic import BaseModel

from db.crud.base import CRUDBase
import schemas
from sqlalchemy.orm import Session

from db.models.like import Like


class CRUDLike(CRUDBase[Like, schemas.Like, BaseModel]):
    def get_like(self, db: Session, item_id: int, user_id: int) -> Like | None:
        return db.query(self.model).filter(
            self.model.item_id == item_id and self.model.user_id == user_id).first()


crud_like = CRUDLike(Like)

