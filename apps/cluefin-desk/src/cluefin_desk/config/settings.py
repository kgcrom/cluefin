from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Kiwoom API settings
    kiwoom_app_key: str | None = None
    kiwoom_secret_key: str | None = None
    kiwoom_env: Literal["dev", "prod"] = "dev"

    # KIS API settings (optional — KIS-backed panels are skipped without keys)
    kis_app_key: str | None = None
    kis_secret_key: str | None = None
    kis_env: Literal["dev", "prod"] = "dev"
    # KIS HTS 로그인 ID — HTS 관심종목 조회에만 쓴다. 없으면 관심종목 화면이 안내 문구만 띄운다.
    kis_hts_user_id: str | None = None

    # DART API settings
    dart_auth_key: str | None = None


settings = Settings()
