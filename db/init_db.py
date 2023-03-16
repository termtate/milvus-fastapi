from sqlalchemy.orm import Session

import schemas
from core.config import settings
from db.crud.crud_user import crud_user
from db.session import engine, Base

from db import base  # noqa: F401


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
    if crud_user.get_by_phone(db, phone_num=settings.FIRST_SUPERUSER_PHONE) is None:
        user_in = schemas.UserCreate(
            name=settings.FIRST_SUPERUSER_NAME,
            phone_number=settings.FIRST_SUPERUSER_PHONE,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            icon=settings.ICONS_PATH
        )
        crud_user.create(db, obj_in=user_in)

