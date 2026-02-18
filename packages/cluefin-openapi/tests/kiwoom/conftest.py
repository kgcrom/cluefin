"""Shared fixtures for Kiwoom integration tests."""

import os
import time

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client


@pytest.fixture(scope="module")
def auth():
    """Fixture to create Auth instance."""
    dotenv.load_dotenv(dotenv_path=".env.test")
    app_key = os.getenv("KIWOOM_APP_KEY")
    secret_key = os.getenv("KIWOOM_SECRET_KEY")
    env = os.getenv("KIWOOM_ENV", "dev").lower()

    if not app_key or not secret_key:
        pytest.skip("Kiwoom API credentials not available in environment variables")

    return Auth(
        app_key=app_key,
        secret_key=SecretStr(secret_key),
        env=env,
    )


@pytest.fixture(scope="module")
def client(auth) -> Client:
    """Fixture to create Kiwoom Client with valid token."""
    token = auth.generate_token()
    return Client(token=token.get_token(), env=os.getenv("KIWOOM_ENV", "dev").lower())


@pytest.fixture(autouse=True)
def _kiwoom_api_rate_limit():
    """Rate-limit guard: wait 1 second before each test."""
    time.sleep(1)
