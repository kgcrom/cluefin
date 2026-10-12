"""키움 국내주식 조건검색(WebSocket) 통합 테스트 — 목록 조회(ka10171, CNSRLST)만.

조건검색 요청·실시간 등록은 저장된 조건식에 따라 결과가 달라 검증 기준을 세울 수 없어 다루지 않는다.
목록 조회는 장 시간과 무관하다. 모의 계좌는 저장된 조건식이 없어 `return_code: 0` 에 빈 목록을 답한다
(2026-10-12 실측) — 그때는 행 형식을 검증할 수 없으므로 skip 한다.
"""

import pytest

from cluefin_openapi.kiwoom._domestic_condition_search import DomesticConditionSearch
from cluefin_openapi.kiwoom._socket_client import KiwoomWebSocketClient

from ._integration_helpers import kiwoom_env

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_get_condition_search_list(auth):
    token = auth.generate_token().get_token()
    async with KiwoomWebSocketClient(token=token, env=kiwoom_env(), market="domestic") as ws:
        response = await DomesticConditionSearch(ws).get_condition_search_list()

    assert response.return_code == 0
    assert response.trnm == "CNSRLST"
    if not response.data:
        pytest.skip("저장된 조건식이 없어 목록 행 형식을 검증할 수 없다 (영웅문에서 조건식을 저장하면 검증된다)")
    for item in response.data:
        assert item.seq
        assert item.name
