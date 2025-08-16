from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kiwoom_app_key: Optional[str] = None
    kiwoom_secret_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
