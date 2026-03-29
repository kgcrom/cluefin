"""Shared fixtures for KIS integration tests."""

import os
import sys
import time
from typing import Literal, cast

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._http_client import HttpClient


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose pytest reports to fixtures so they can append debug context on failure."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="module")
def auth_dev():
    """Fixture to create Auth instance for dev environment."""
    dotenv.load_dotenv(dotenv_path=".env.test")
    app_key = os.getenv("KIS_APP_KEY")
    secret_key = os.getenv("KIS_SECRET_KEY")
    env = cast(Literal["dev", "prod"], os.getenv("KIS_ENV", "dev"))

    if not app_key or not secret_key:
        pytest.skip("KIS API credentials not available in environment variables")

    return Auth(app_key=app_key, secret_key=SecretStr(secret_key), env=env)


@pytest.fixture(scope="module")
def client(auth_dev) -> HttpClient:
    """Fixture to create KIS HttpClient with valid token."""
    token_response = auth_dev.generate()
    return HttpClient(
        app_key=auth_dev.app_key,
        secret_key=auth_dev.secret_key,
        token=token_response.access_token,
        env=auth_dev.env,
    )


@pytest.fixture(autouse=True)
def _kis_api_rate_limit(request):
    """Rate-limit guard: wait 1 second before each integration test."""
    if request.node.get_closest_marker("integration"):
        time.sleep(1)


@pytest.fixture(autouse=True)
def _attach_last_kis_response_debug(request):
    """Attach the last raw KIS response to failed test reports."""
    yield

    if not request.node.get_closest_marker("integration"):
        return

    report = getattr(request.node, "rep_call", None)
    if report is None or not report.failed or "client" not in request.fixturenames:
        return

    client = request.getfixturevalue("client")
    debug_text = client.format_last_response_debug()
    debug_enabled = os.getenv("KIS_DEBUG_ON_FAILURE", "").lower() in {"1", "true", "yes", "on"}
    if debug_text and debug_enabled:
        print(f"\n[KIS LAST RESPONSE]\n{debug_text}\n", file=sys.stderr)
        request.node.add_report_section("call", "kis-last-response", debug_text)
