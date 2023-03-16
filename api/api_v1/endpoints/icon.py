from fastapi import APIRouter
from starlette.responses import FileResponse

from core.config import settings

router = APIRouter()


@router.get("/{icon_name}")
def get_icon(
        icon_name: str
):
    return FileResponse(
        settings.ICONS_PATH.joinpath(icon_name),
        media_type="image"
    )
