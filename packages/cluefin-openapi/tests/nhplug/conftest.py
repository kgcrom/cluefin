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


def _account_for_env(client) -> str:
    """호출 환경과 acct_type 이 맞는 계좌번호.

    모의투자(dev)는 03 계좌만, 운영(prod)은 01·02 계좌만 유효하다. 이 조건은
    krstock·gbstock 이 동일하다. 같은 계좌번호가 여러 행으로 내려올 수 있어
    첫 매칭을 쓴다.
    """
    wanted = ("03",) if client.env == "dev" else ("01", "02")
    accounts = client.common.get_account_list().body.output_0 or []
    for account in accounts:
        if account.acct_type in wanted:
            return account.acct_no
    pytest.skip(f"{client.env} 환경에 맞는 계좌(acct_type {wanted})가 없다")


@pytest.fixture(scope="module")
def krstock_account(client) -> str:
    """국내주식 조회·주문에 쓸 계좌번호."""
    return _account_for_env(client)


@pytest.fixture(scope="module")
def gbstock_account(client) -> str:
    """해외주식 조회·주문에 쓸 계좌번호."""
    return _account_for_env(client)


@pytest.fixture(autouse=True)
def _nhplug_api_rate_limit(request):
    """Rate-limit guard: wait 1 second before each integration test."""
    if request.node.get_closest_marker("integration"):
        time.sleep(1)
