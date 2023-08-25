from pydantic_settings import BaseSettings
from core.config import settings as _settings


class Settings(BaseSettings):
    VECTOR_DIM: int = _settings.milvus.VECTER_DIM
    MODEL_NAME_OR_PATH: str = _settings.milvus.MODEL_NAME_OR_PATH


settings = Settings()