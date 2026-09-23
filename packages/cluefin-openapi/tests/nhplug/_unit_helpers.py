"""Shared helpers for NH PLUG unit tests (network-free — no .env, no real credentials)."""

from typing import Literal

from cluefin_openapi.nhplug._http_client import HttpClient


def make_client(env: Literal["prod", "dev"] = "prod") -> HttpClient:
    """HttpClient with dummy credentials for requests_mock-based unit tests."""
    return HttpClient(token="TOKEN", app_key="test-app-key", secret_key="test-secret", env=env)
