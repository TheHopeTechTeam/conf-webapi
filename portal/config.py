"""
Configuration
"""
import json
import os
from distutils.util import strtobool
from pathlib import Path, PosixPath
from typing import List, Optional, Any, Type, Tuple

from dotenv import load_dotenv
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, EnvSettingsSource, PydanticBaseSettingsSource

load_dotenv()


class MyCustomSource(EnvSettingsSource):

    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool
    ) -> Any:
        if not value:
            return None
        if field.annotation is List[str]:
            return [v for v in value.split(',')]
        return value


class Configuration(BaseSettings):
    """
    Configuration
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (MyCustomSource(settings_cls),)

    # [App Base]
    APP_NAME: str = "conf-webapi"
    ENV: str = os.getenv(key="ENV", default="dev").lower()
    DEBUG: bool = os.getenv(key="DEBUG", default=False)
    IS_PROD: bool = ENV == "prod"
    IS_DEV: bool = ENV not in ["prod", "stg"]

    # [FastAPI]
    HOST: str = os.getenv(key="HOST", default="127.0.0.1")
    PORT: int = os.getenv(key="PORT", default=8000)

    # [CORS]
    CORS_ALLOWED_ORIGINS: List[str] = os.getenv(key="CORS_ALLOWED_ORIGINS", default="*").split(",")
    CORS_ALLOW_ORIGINS_REGEX: Optional[str] = os.getenv(key="CORS_ALLOW_ORIGINS_REGEX")

    # [Redis]
    REDIS_URL: str = os.getenv(key="REDIS_URL", default="redis://localhost:6379")

    # [PostgreSQL]
    DATABASE_HOST: str = os.getenv(key="DATABASE_HOST", default="localhost")
    DATABASE_USER: str = os.getenv(key="DATABASE_USER", default="postgres")
    DATABASE_PASSWORD: str = os.getenv(key="DATABASE_PASSWORD", default="")
    DATABASE_PORT: str = os.getenv(key="DATABASE_PORT", default="5432")
    DATABASE_NAME: str = os.getenv(key="DATABASE_NAME", default="postgres")
    DATABASE_SCHEMA: Optional[str] = os.getenv(key="DATABASE_SCHEMA")
    DATABASE_APPLICATION_NAME: str = APP_NAME

    # [Database]
    DATABASE_POOL: bool = strtobool(os.getenv("DATABASE_POOL", "true"))
    SQL_ECHO: bool = strtobool(os.getenv("SQL_ECHO", "false"))
    SQLALCHEMY_DATABASE_URI: str = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@' \
                                   f'{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
    ASYNC_DATABASE_URL: str = f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@' \
                              f'{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

    # [Google Cloud]
    google_certificate_path: PosixPath = Path("env/google_certificate.json") if IS_DEV else Path("/etc/secrets/google_certificate.json")
    GOOGLE_FIREBASE_CERTIFICATE: dict = json.loads(google_certificate_path.read_text())


configs: Configuration = Configuration()
