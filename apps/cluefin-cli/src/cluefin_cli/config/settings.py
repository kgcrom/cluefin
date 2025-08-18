from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    kiwoom_app_key: Optional[str] = None
    kiwoom_secret_key: Optional[str] = None
    krx_auth_key: Optional[str] = None
    openai_api_key: Optional[str] = None


settings = Settings()
