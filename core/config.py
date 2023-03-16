import secrets
from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, Field, HttpUrl, tools


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    ALGORITHM = "HS256"

    FIRST_SUPERUSER_NAME: str = "admin"
    FIRST_SUPERUSER_PHONE: str = "12345678901"
    FIRST_SUPERUSER_PASSWORD: str = "123456"

    ICONS_PATH: Path = Path(r"F:\fastapi_test - 副本\icons")

    DEFAULT_AVATAR: Path = ICONS_PATH.joinpath("admin.png")


settings = Settings()
