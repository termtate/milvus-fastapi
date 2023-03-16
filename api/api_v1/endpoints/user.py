import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

import schemas
from api.deps import get_db, get_current_user
from core.config import settings
from db import models
from db.crud.crud_user import crud_user

router = APIRouter()


@router.post("/", response_model=schemas.User)
async def create_user(
        user_name: str = Form(),
        user_password: str = Form(),
        user_phone_number: str = Form(),
        icon: UploadFile = File(),
        db: Session = Depends(get_db)
):
    if crud_user.get_by_name(db, name=user_name) is not None:
        raise HTTPException(status_code=400, detail="Name already registered")

    icon_name = f"{user_name}&{icon.filename}"
    contents = await icon.read()

    async with aiofiles.open(settings.ICONS_PATH.joinpath(icon_name), "wb") as f:
        await f.write(contents)

    return crud_user.create(
        db,
        obj_in=schemas.UserCreate(
            name=user_name,
            icon=settings.ICONS_PATH.joinpath(icon_name),
            phone_number=user_phone_number,
            password=user_password
        )
    )


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud_user.get(db, obj_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @router.post("/test")
# async def test(
#     icon: UploadFile = File(),
# ):
#     return {
#         f"{icon.filename=} {icon.content_type=}"
#     }
