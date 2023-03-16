from functools import partial

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.orm import Session

import schemas
from api.deps import get_db, get_current_user
from api.utils.init_items import init_items, is_liked, get_likes_num, get_comments_num
from db import models
from db.crud.crud_item import crud_item
from db.crud.crud_like import crud_like
from db.crud.crud_user import crud_user
from db.models.published_item import Item

router = APIRouter()


@router.post("/like", response_model=schemas.Like)
def like_item(
        item_id: int = Form(),
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    item_db = crud_item.get(db, obj_id=item_id)
    if item_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such item: {item_id=}"
        )

    if crud_like.get_like(db, item_id=item_id, user_id=current_user.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Item already liked: {item_id=}"
        )

    return crud_like.create(db, obj_in=schemas.Like(user_id=current_user.id, item_id=item_id))


@router.delete("/unlike/{item_id}", response_model=schemas.Like)
def unlike_item(
        item_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    item_db = crud_item.get(db, obj_id=item_id)
    if item_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such item: {item_id=}")

    like = crud_like.get_like(db, item_id=item_id, user_id=current_user.id)
    if like is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This item has not been liked ")

    return crud_like.remove(db, obj_id=like.id)


@router.post("/{item_type}", response_model=schemas.Publish)
def publish_item(
        item: schemas.PublishCreate,
        item_type: Item,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return crud_item.publish_item(db, item=item, item_type=item_type, user_id=current_user.id)


@router.get("/posts", response_model=Page[schemas.Post])
def read_posts(
        params: Params = Depends(),
        db: Session = Depends(get_db)
):
    return paginate(crud_item.get_posts(db), params)


@router.get("/posts/me", response_model=Page[schemas.Post])
def read_posts_me(
        current_user: models.User = Depends(get_current_user),
        params: Params = Depends(),
        db: Session = Depends(get_db)
):
    items_db = crud_item.get_posts(db)
    items = init_items(
        item_type=schemas.Post,
        items=items_db,
        is_liked=partial(is_liked, user_id=current_user.id),
        likes_num=get_likes_num,
        comments_num=partial(get_comments_num, db=db)
    )

    return paginate(items, params)


# @router.get("/comments", response_model=Page[schemas.Publish])
# def read_post_comments(
#         post_id: int,
#         params: Params = Depends(),
#         db: Session = Depends(get_db)
# ):
#     if crud_item.get(db, obj_id=post_id) is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"No such post: id={post_id}"
#         )
#     return paginate(crud_item.get_post_comments(db, post_id=post_id), params)


@router.get("/comments/me", response_model=Page[schemas.Comment])
def read_post_comments_me(
        post_id: int,
        current_user: models.User = Depends(get_current_user),
        params: Params = Depends(),
        db: Session = Depends(get_db)
):
    if crud_item.get(db, obj_id=post_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such post: id={post_id}"
        )
    comments_db = crud_item.get_post_comments(db, post_id=post_id)
    comments = init_items(
        item_type=schemas.Comment,
        items=comments_db,
        is_liked=partial(is_liked, user_id=current_user.id),
        likes_num=get_likes_num,
    )
    return paginate(comments, params)


@router.get("/{item_type}/{user_id}", response_model=Page[schemas.Publish])
def read_user_items(
        item_type: Item,
        user_id: int,
        params: Params = Depends(),
        db: Session = Depends(get_db)
):
    user = crud_user.get(db, obj_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such user"
        )
    if item_type.name == "post":
        return paginate(user.posts, params)
    else:
        return paginate(user.comments, params)
