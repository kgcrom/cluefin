"""Shared fixtures for Kiwoom integration tests."""

import os
import time

import pytest
from pydantic import SecretStr

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client

# `.env.test` 로딩은 여기 임포트만으로 끝난다 — 모듈 레벨 skipif가 KIWOOM_ENV를 보려면
# 픽스처 실행이 아니라 수집 시점에 로드돼 있어야 한다.
from ._integration_helpers import kiwoom_env


@pytest.fixture(scope="module")
def auth():
    """Fixture to create Auth instance."""
    app_key = os.getenv("KIWOOM_APP_KEY")
    secret_key = os.getenv("KIWOOM_SECRET_KEY")

    if not app_key or not secret_key:
        pytest.skip("Kiwoom API credentials not available in environment variables")

    return Auth(
        app_key=app_key,
        secret_key=SecretStr(secret_key),
        env=kiwoom_env(),
    )


@pytest.fixture(scope="module")
def client(auth) -> Client:
    """Fixture to create Kiwoom Client with valid token."""
    token = auth.generate_token()
    return Client(token=token.get_token(), env=kiwoom_env())


@pytest.fixture(autouse=True)
def _kiwoom_api_rate_limit(request):
    """Rate-limit guard: wait 1 second before each integration test."""
    if request.node.get_closest_marker("integration"):
        time.sleep(1)
