from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    kiwoom_app_key: Optional[str] = None
    kiwoom_secret_key: Optional[str] = None
    openai_api_key: Optional[str] = None


settings = Settings()
