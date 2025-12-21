from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """dartex 설정"""

    dart_auth_key: str = ""
    data_dir: str = "./data"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
