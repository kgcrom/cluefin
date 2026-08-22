"""Integration tests for the NH PLUG OAuth 인증 group (4 APIs).

These tests require real credentials (NHPLUG_APP_KEY / NHPLUG_SECRET_KEY in
`.env.test`) and network access.

NH 특성상 주의:
- 접근토큰발급은 운영 도메인 전용이고 초당 1회로 제한되며, 불필요한 재발급은
  계좌 보안 알림을 유발한다. generate() 는 캐시 우선이라 반복 실행에 안전하다.
- 접근토큰폐기는 실행하면 다음 실행에서 재발급이 강제되므로(보안 알림 누적),
  `NHPLUG_TEST_REVOKE=1` 로 명시적으로 켠 경우에만 실행한다.
"""

import os

import pytest
import requests
from pydantic import SecretStr

from cluefin_openapi.nhplug._auth import Auth
from cluefin_openapi.nhplug._auth_types import TokenResponse, TokenRevokeResponse
from cluefin_openapi.nhplug._token_manager import TokenManager


@pytest.mark.integration
def test_generate_token(auth):
    """접근토큰발급 (`POST /oauth2/token`)."""
    token_response = auth.generate()

    assert isinstance(token_response, TokenResponse)
    assert token_response.access_token
    assert token_response.token_type == "Bearer"
    assert token_response.scope == "oob"
    assert token_response.expires_in > 0


@pytest.mark.integration
def test_generate_reuses_cached_token(auth):
    """반복 호출은 캐시된 토큰을 재사용해야 한다 (재발급 = 보안 알림)."""
    first = auth.generate()
    second = auth.generate()

    assert first.access_token == second.access_token


@pytest.mark.integration
def test_get_account_list(client):
    """계좌목록조회 (`POST /n2/acctinfo`)."""
    response = client.common.get_account_list()

    assert response.body.output_0 is not None
    assert len(response.body.output_0) > 0
    for account in response.body.output_0:
        assert account.acct_no
        assert account.acct_type in ("01", "02", "03")


@pytest.mark.integration
def test_close_websocket_session(client):
    """실시간(Websocket) 세션해제 (`POST /websocket/close/session`).

    문서와 달리 실서버(운영·모의 동일)는 열린 세션이 없으면 500 +
    `IGW50025`("서버에서 일시적인 오류")를 반환한다 (2026-08-22 실측).
    세션이 있을 때의 정상 응답과 세션 없음의 IGW50025 둘 다 허용한다.
    """
    from cluefin_openapi.nhplug._exceptions import NHPlugServerError

    try:
        response = client.common.close_websocket_session()
        assert response.body.rsp_cd is not None
        assert response.body.rsp_msg is not None
    except NHPlugServerError as e:
        assert e.response_data is not None
        assert e.response_data.get("rsp_cd") == "IGW50025"


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("NHPLUG_TEST_REVOKE") != "1",
    reason="폐기하면 다음 실행에서 재발급이 강제됨(보안 알림 누적) — NHPLUG_TEST_REVOKE=1 로 명시 실행",
)
def test_revoke_token(auth):
    """접근토큰폐기 (`POST /oauth2/revoke`) — 캐시도 함께 정리되는지 확인."""
    auth.generate()
    result = auth.revoke()

    assert isinstance(result, TokenRevokeResponse)
    assert result.error_code is None
    assert auth.token_manager._token_cache is None
    assert not auth.token_manager.cache_file.exists()


@pytest.mark.integration
def test_invalid_credentials_handling(tmp_path):
    """잘못된 자격증명은 HTTP 에러로 이어져야 한다 (실제 계좌와 무관한 키 사용)."""
    invalid_auth = Auth(
        "invalid_app_key",
        SecretStr("invalid_secret_key"),
        token_manager=TokenManager(cache_dir=str(tmp_path), app_key="invalid_app_key"),
    )

    with pytest.raises(requests.HTTPError):
        invalid_auth.generate()
