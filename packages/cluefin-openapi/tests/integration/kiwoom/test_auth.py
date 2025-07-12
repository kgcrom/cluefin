import os
from datetime import datetime

import dotenv
import pytest

from cluefin_openapi.kiwoom._auth import Auth


@pytest.fixture
def auth():
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Auth(
        app_key=os.getenv("APP_KEY"),
        secret_key=os.getenv("SECRET_KEY"),
        env="dev",
    )


def test_generate_token(auth):
    response = auth.generate_token()

    assert response.token is not None
    assert response.token_type.startswith("Bearer")
    assert isinstance(response.expires_dt, datetime)
