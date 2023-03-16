from collections.abc import Sequence, Callable
from typing import Any, TypeVar, Type

from sqlalchemy.orm import Session

from db.crud.crud_item import crud_item
from db.models.published_item import PublishItem
from schemas.publish import Publish, Post


T = TypeVar("T", bound=Publish)


def init_items(
        item_type: Type[T],
        items: Sequence[PublishItem],
        **kwargs: Callable[[PublishItem], Any]
) -> list[T]:
    return list(map(
        lambda item: item_type.from_orm(item).copy(
            update={
                key: func(item) for key, func in kwargs.items()
            }
        ),
        items
    ))


def get_likes_num(item: PublishItem) -> int:
    return len(item.likes)


def get_comments_num(
        item: PublishItem,
        db: Session
) -> int:
    return len(crud_item.get_post_comments(db, post_id=item.id))


def is_liked(item: PublishItem, user_id: int) -> int:
    return user_id in map(
        lambda like: like.user_id,
        item.likes
    )


# def init_comments(
#         items: Sequence[PublishItem],
#         user_id: int
# ) -> list[Publish]:
#     return list(map(
#         lambda item: Publish.from_orm(item).copy(
#             update={
#                 "is_liked": user_id in map(
#                     lambda like: like.user_id,
#                     item.likes
#                 ),
#                 "likes_num": len(item.likes)
#             }
#         ),
#         items
#     ))
#
#
# def init_posts(
#         posts: Sequence[PublishItem],
#         belongs_comments: Sequence[PublishItem],
#         user_id: int
# ) -> list[Post]:
#     return list(map(
#         lambda post: Post.from_orm(post).copy(
#             update={
#                 "is_liked": user_id in map(
#                     lambda like: like.user_id,
#                     post.likes
#                 ),
#                 "likes_num": len(post.likes),
#                 "comments_num": len(belongs_comments)
#             }
#         ),
#         posts
#     ))
