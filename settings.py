# -*- coding: utf-8 -*-

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)

__all__ = ["Settings", "settings"]


class ServerSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    access_log: bool = True


class DatabaseSettings(BaseModel):
    url: str = "sqlite://./data/database.sqlite"


class JWTSecretSettings(BaseModel):
    secret: str = "replace_this_with_a_strong_secret"
    algorithm: str = "HS256"
    expire_minutes: int = 30


class Settings(BaseSettings):
    server: ServerSettings = ServerSettings()
    database: DatabaseSettings = DatabaseSettings()
    jwt_secret: JWTSecretSettings = JWTSecretSettings()

    model_config = SettingsConfigDict(
        nested_model_default_partial_update=True,
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        toml_file="settings.toml",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls),
        )


settings = Settings()
