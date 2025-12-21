from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """dartex 설정"""

    dart_api_key: str = ""
    data_dir: str = "./data"

    model_config = {"env_prefix": "DARTEX_", "env_file": ".env"}


def get_settings() -> Settings:
    return Settings()
