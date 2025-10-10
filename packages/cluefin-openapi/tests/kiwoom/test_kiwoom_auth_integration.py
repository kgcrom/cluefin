import os
from datetime import datetime

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.kiwoom._auth import Auth


@pytest.fixture
def auth():
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Auth(
        app_key=os.getenv("KIWOOM_APP_KEY", ""),
        secret_key=SecretStr(os.getenv("KIWOOM_SECRET_KEY", "")),
        env="dev",
    )


@pytest.mark.integration
def test_generate_token(auth):
    response = auth.generate_token()

    assert response.token is not None
    assert response.token_type.startswith("Bearer")
    assert isinstance(response.expires_dt, datetime)
