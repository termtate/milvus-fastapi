from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from db.crud.base import CRUDBase
from db.models.user import User
from schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> User | None:
        return db.query(self.model).filter_by(name=name).first()

    def get_by_phone(self, db: Session, *, phone_num: str):
        return db.query(self.model).filter(self.model.phone_number == phone_num).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            name=obj_in.name,
            phone_number=obj_in.phone_number,
            hashed_password=get_password_hash(obj_in.password),
            icon=obj_in.icon,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, name: str, password: str) -> Optional[User]:
        if user := self.get_by_name(db, name=name):
            return user if verify_password(password, user.hashed_password) else None
        else:
            return None


crud_user = CRUDUser(User)
