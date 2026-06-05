"""
Configuración central de la aplicación.
Lee variables de entorno desde .env
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "PrácticasPro"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./local.db"
    SECRET_KEY: str = "changeme"

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
