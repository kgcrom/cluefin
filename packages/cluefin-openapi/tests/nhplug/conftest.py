"""Shared fixtures for NH PLUG integration tests."""

import os
import time
from typing import Literal, cast

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.nhplug._auth import Auth
from cluefin_openapi.nhplug._http_client import HttpClient


@pytest.fixture(scope="module")
def auth():
    """Auth instance backed by real credentials.

    토큰 발급은 운영 도메인 전용이므로 env 구분이 없다. generate() 는 파일 캐시를
    우선 사용하므로, 테스트를 반복 실행해도 실제 발급은 토큰 만료 전까지 1회다.
    """
    dotenv.load_dotenv(dotenv_path=".env.test")
    app_key = os.getenv("NHPLUG_APP_KEY")
    secret_key = os.getenv("NHPLUG_SECRET_KEY")

    if not app_key or not secret_key:
        pytest.skip("NH PLUG API credentials not available in environment variables")

    return Auth(app_key=app_key, secret_key=SecretStr(secret_key))


@pytest.fixture(scope="module")
def client(auth) -> HttpClient:
    """HttpClient with a valid token, targeting the env from NHPLUG_ENV."""
    env = cast(Literal["prod", "dev"], os.getenv("NHPLUG_ENV", "dev"))
    token_response = auth.generate()
    return HttpClient(
        token=token_response.access_token,
        app_key=auth.app_key,
        secret_key=auth.secret_key,
        env=env,
    )


@pytest.fixture(autouse=True)
def _nhplug_api_rate_limit(request):
    """Rate-limit guard: wait 1 second before each integration test."""
    if request.node.get_closest_marker("integration"):
        time.sleep(1)
