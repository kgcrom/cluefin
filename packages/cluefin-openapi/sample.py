from loguru import logger
import os
from pydantic import SecretStr
import dotenv
from cluefin_openapi.krx._client import Client as KRXClient

# 인증 설정
dotenv.load_dotenv(dotenv_path=".env")

krx_client = KRXClient(auth_key=os.getenv("KRX_AUTH_KEY"), timeout=30)
logger.info(f"krx_client => ${krx_client}")