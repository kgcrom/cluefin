from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Kiwoom API settings
    kiwoom_app_key: Optional[str] = None
    kiwoom_secret_key: Optional[str] = None
    kiwoom_env: Literal["dev", "prod"] = "dev"

    # KIS API settings (optional — KIS-backed panels are skipped without keys)
    kis_app_key: Optional[str] = None
    kis_secret_key: Optional[str] = None
    kis_env: Literal["dev", "prod"] = "dev"

    # DART API settings
    dart_auth_key: Optional[str] = None


settings = Settings()
