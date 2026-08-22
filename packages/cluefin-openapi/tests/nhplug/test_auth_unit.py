"""Unit tests for NH PLUG auth (token issue/revoke) and token caching."""

import pytest
import requests
import requests_mock
from pydantic import SecretStr

from cluefin_openapi.nhplug._auth import AUTH_BASE_URL, Auth
from cluefin_openapi.nhplug._auth_types import TokenResponse
from cluefin_openapi.nhplug._token_manager import TokenManager

TOKEN_URL = f"{AUTH_BASE_URL}/oauth2/token"
REVOKE_URL = f"{AUTH_BASE_URL}/oauth2/revoke"

TOKEN_BODY = {
    "access_token": "TOKEN",
    "scope": "oob",
    "token_type": "Bearer",
    "expires_in": 86400,
}


@pytest.fixture
def auth(tmp_path) -> Auth:
    return Auth(app_key="test-app-key", secret_key=SecretStr("test-secret"), cache_dir=str(tmp_path))


class TestGenerate:
    def test_generate_issues_token(self, auth):
        with requests_mock.Mocker() as m:
            m.post(TOKEN_URL, json=TOKEN_BODY)
            token = auth.generate()

        assert token.access_token == "TOKEN"
        assert token.expires_in == 86400
        assert token.get_token() == "TOKEN"

        request = m.request_history[0]
        assert request.headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert "grant_type=client_credentials" in request.text
        assert "scope=oob" in request.text
        assert "appkey=test-app-key" in request.text

    def test_generate_reuses_cached_token(self, auth):
        with requests_mock.Mocker() as m:
            m.post(TOKEN_URL, json=TOKEN_BODY)
            auth.generate()
            auth.generate()

        # Second call must come from cache — one network request only.
        assert m.call_count == 1

    def test_cache_is_shared_across_instances(self, auth, tmp_path):
        with requests_mock.Mocker() as m:
            m.post(TOKEN_URL, json=TOKEN_BODY)
            auth.generate()

            other = Auth(app_key="test-app-key", secret_key=SecretStr("test-secret"), cache_dir=str(tmp_path))
            other.generate()

        assert m.call_count == 1

    def test_expired_cache_triggers_reissue(self, auth):
        with requests_mock.Mocker() as m:
            m.post(TOKEN_URL, json={**TOKEN_BODY, "expires_in": 0})
            auth.generate()
            # expires_in=0 is already inside the expiry buffer, so a new token is issued.
            auth.generate()

        assert m.call_count == 2

    def test_generate_raises_on_http_error(self, auth):
        with requests_mock.Mocker() as m:
            m.post(TOKEN_URL, status_code=401, json={"error": "invalid_client"})
            with pytest.raises(requests.HTTPError):
                auth.generate()


class TestRevoke:
    def test_revoke_clears_cache(self, auth):
        with requests_mock.Mocker() as m:
            m.post(TOKEN_URL, json=TOKEN_BODY)
            m.post(REVOKE_URL, json={"code": 200, "message": "접근토큰 폐기에 성공하였습니다."})

            auth.generate()
            result = auth.revoke()

        assert result.code == 200
        assert auth._token_data is None
        assert auth.token_manager._token_cache is None
        assert not auth.token_manager.cache_file.exists()

        revoke_request = m.request_history[-1]
        assert "token=TOKEN" in revoke_request.text
        assert "token_type_hint=access_token" in revoke_request.text

    def test_revoke_without_token_raises(self, auth):
        with pytest.raises(ValueError):
            auth.revoke()

    def test_revoke_explicit_token_keeps_unrelated_cache(self, auth):
        with requests_mock.Mocker() as m:
            m.post(TOKEN_URL, json=TOKEN_BODY)
            m.post(REVOKE_URL, json={"code": 200, "message": "ok"})

            auth.generate()
            auth.revoke(token="OTHER_TOKEN")

        # Cached token is a different one — it must survive.
        assert auth.token_manager._token_cache is not None


class TestTokenManager:
    def test_scoped_cache_file_name(self):
        name_a = TokenManager._cache_file_name("app-a")
        name_b = TokenManager._cache_file_name("app-b")
        assert name_a != name_b
        assert name_a.startswith(".nhplug_token_cache_")

    def test_clear_cache_removes_file(self, tmp_path):
        manager = TokenManager(cache_dir=str(tmp_path), app_key="app")
        manager._save_token(TokenResponse(**TOKEN_BODY))
        assert manager.cache_file.exists()

        manager.clear_cache()
        assert manager._token_cache is None
        assert not manager.cache_file.exists()
