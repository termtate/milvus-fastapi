from fastapi import APIRouter

from api.api_v1.endpoints import user, login, publish_item, icon

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(publish_item.router, prefix="/items", tags=["items"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(icon.router, prefix="/icons", tags=["icons"])
