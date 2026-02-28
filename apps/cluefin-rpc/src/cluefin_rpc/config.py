from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class RpcSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    kis_app_key: Optional[str] = None
    kis_secret_key: Optional[str] = None
    kis_env: Literal["dev", "prod"] = "dev"

    kiwoom_app_key: Optional[str] = None
    kiwoom_secret_key: Optional[str] = None
    kiwoom_env: Literal["dev", "prod"] = "dev"

    dart_auth_key: Optional[str] = None

    kis_account_no: Optional[str] = None
    kis_account_product_code: Optional[str] = None
