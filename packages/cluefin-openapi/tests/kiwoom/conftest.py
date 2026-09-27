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
from ._spec_conformance import record_exchanges


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
    """Fixture to create Kiwoom Client with valid token.

    `record_exchanges` 로 감싸 `assert_spec_conformance` 가 마지막 요청·응답 원문을 읽을 수 있게 한다.
    """
    token = auth.generate_token()
    return record_exchanges(Client(token=token.get_token(), env=kiwoom_env()))


@pytest.fixture(autouse=True)
def _kiwoom_api_rate_limit(request):
    """Rate-limit guard: wait 1 second before each integration test."""
    if request.node.get_closest_marker("integration"):
        time.sleep(1)
