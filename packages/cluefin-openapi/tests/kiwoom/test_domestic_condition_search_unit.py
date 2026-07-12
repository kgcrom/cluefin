"""국내주식 조건검색(웹소켓) 메시지 모델 unit 테스트.

ka10171/ka10172/ka10173/ka10174 4개 TR은 웹소켓 API이므로 HTTP 클라이언트
테스트(run_post_case)를 적용할 수 없다. 여기서는 요청 모델의 wire 포맷 dump와 응답
모델의 field/alias 매핑을 검증한다. ``DomesticConditionSearch`` 도메인 래퍼의 요청
송신·응답 파싱 동작은 ``test_domestic_condition_search_ws_unit.py``에서 검증한다.
(미국주식 ``test_overseas_condition_search_unit`` 과 대칭.)
"""

import pytest

from cluefin_openapi.kiwoom._domestic_condition_search_types import (
    DomesticConditionSearchListItem,
    DomesticConditionSearchListRequest,
    DomesticConditionSearchListResponse,
    DomesticConditionSearchRealtimeCancelRequest,
    DomesticConditionSearchRealtimeCancelResponse,
    DomesticConditionSearchRealtimePush,
    DomesticConditionSearchRealtimeRequest,
    DomesticConditionSearchRealtimeResponse,
    DomesticConditionSearchRequest,
    DomesticConditionSearchResponse,
    DomesticConditionSearchResultItem,
)

# ---------------------------------------------------------------------------
# ka10171 조건검색 목록조회
# ---------------------------------------------------------------------------


class TestDomesticConditionSearchList:
    def test_request_dump_matches_wire_format(self):
        request = DomesticConditionSearchListRequest(trnm="CNSRLST")
        assert request.model_dump(by_alias=True) == {"trnm": "CNSRLST"}

    def test_invalid_trnm_raises(self):
        with pytest.raises(ValueError):
            DomesticConditionSearchListRequest(trnm="INVALID")

    def test_response_validates_and_maps_fields(self):
        payload = {
            "return_code": 0,
            "return_msg": "",
            "trnm": "CNSRLST",
            "data": [
                {"seq": "0", "name": "조건식1"},
                {"seq": "1", "name": "조건식2"},
            ],
        }

        response = DomesticConditionSearchListResponse.model_validate(payload)

        assert response.return_code == 0
        assert response.trnm == "CNSRLST"
        assert len(response.data) == 2
        assert response.data[0] == DomesticConditionSearchListItem(seq="0", name="조건식1")
        assert response.data[1].seq == "1"
        assert response.data[1].name == "조건식2"


# ---------------------------------------------------------------------------
# ka10172 조건검색 요청 일반
# ---------------------------------------------------------------------------


class TestDomesticConditionSearchRequest:
    def test_request_dump_matches_wire_format(self):
        request = DomesticConditionSearchRequest(
            trnm="CNSRREQ",
            seq="0",
            search_type="0",
            stex_tp="K",
            cont_yn="N",
            next_key="",
        )

        assert request.model_dump(by_alias=True) == {
            "trnm": "CNSRREQ",
            "seq": "0",
            "search_type": "0",
            "stex_tp": "K",
            "cont_yn": "N",
            "next_key": "",
        }

    def test_request_defaults(self):
        request = DomesticConditionSearchRequest(trnm="CNSRREQ", seq="0", search_type="0")
        assert request.stex_tp == "K"
        assert request.cont_yn == "N"
        assert request.next_key == ""

    def test_invalid_search_type_raises(self):
        """ka10172는 search_type이 반드시 '0' (일반조회)."""
        with pytest.raises(ValueError):
            DomesticConditionSearchRequest(trnm="CNSRREQ", seq="0", search_type="1")

    def test_invalid_stex_tp_raises(self):
        with pytest.raises(ValueError):
            DomesticConditionSearchRequest(trnm="CNSRREQ", seq="0", search_type="0", stex_tp="Z")

    def test_response_maps_fid_keys_by_alias(self):
        """ka10172 결과 항목: FID 숫자키(9001→stock_code 등) 매핑."""
        payload = {
            "return_code": 0,
            "return_msg": "",
            "trnm": "CNSRREQ",
            "seq": "0",
            "cont_yn": "N",
            "next_key": "",
            "data": [
                {
                    "9001": "005930",
                    "302": "삼성전자",
                    "10": "70000",
                    "25": "2",
                    "11": "1000",
                    "12": "1.45",
                    "13": "1000000",
                    "16": "69000",
                    "17": "71000",
                    "18": "68500",
                }
            ],
        }

        response = DomesticConditionSearchResponse.model_validate(payload)

        assert response.trnm == "CNSRREQ"
        assert response.cont_yn == "N"
        item = response.data[0]
        assert item.stock_code == "005930"
        assert item.stock_name == "삼성전자"
        assert item.current_price == "70000"
        assert item.prev_day_diff_sign == "2"
        assert item.prev_day_diff == "1000"
        assert item.fluctuation_rate == "1.45"
        assert item.acc_trade_volume == "1000000"
        assert item.open_price == "69000"
        assert item.high_price == "71000"
        assert item.low_price == "68500"

    def test_populate_by_name_round_trip(self):
        item = DomesticConditionSearchResultItem(stock_code="005930", stock_name="삼성전자", current_price="70000")
        dumped = item.model_dump(by_alias=True)
        assert dumped["9001"] == "005930"
        assert dumped["302"] == "삼성전자"
        assert dumped["10"] == "70000"

    def test_response_continuation_frame(self):
        """cont_yn=Y 인 연속조회 프레임 - next_key 채워짐."""
        payload = {
            "return_code": 0,
            "return_msg": "",
            "trnm": "CNSRREQ",
            "seq": "0",
            "cont_yn": "Y",
            "next_key": "000123",
            "data": [],
        }
        response = DomesticConditionSearchResponse.model_validate(payload)
        assert response.cont_yn == "Y"
        assert response.next_key == "000123"


# ---------------------------------------------------------------------------
# ka10173 조건검색 요청 실시간
# ---------------------------------------------------------------------------


class TestDomesticConditionSearchRealtimeRequest:
    def test_request_dump_matches_wire_format(self):
        request = DomesticConditionSearchRealtimeRequest(trnm="CNSRREQ", seq="0", search_type="1", stex_tp="K")
        assert request.model_dump(by_alias=True) == {
            "trnm": "CNSRREQ",
            "seq": "0",
            "search_type": "1",
            "stex_tp": "K",
        }

    def test_invalid_search_type_raises(self):
        """ka10173은 search_type이 반드시 '1' (조건검색+실시간조건검색)."""
        with pytest.raises(ValueError):
            DomesticConditionSearchRealtimeRequest(trnm="CNSRREQ", seq="0", search_type="0")

    def test_response_maps_fields(self):
        payload = {
            "return_code": 0,
            "return_msg": "",
            "trnm": "CNSRREQ",
            "seq": "0",
            "data": [{"jmcode": "005930"}],
        }

        response = DomesticConditionSearchRealtimeResponse.model_validate(payload)

        assert response.trnm == "CNSRREQ"
        assert response.seq == "0"
        assert response.data[0].jmcode == "005930"

    def test_response_empty_data_real_push(self):
        """실시간 편입/이탈 이벤트가 없을 때도 data는 빈 리스트로 검증 가능."""
        payload = {"trnm": "CNSRREQ", "seq": "0", "data": []}
        response = DomesticConditionSearchRealtimeResponse.model_validate(payload)
        assert response.return_code is None
        assert response.data == []


class TestDomesticConditionSearchRealtimePush:
    """ka10173 실시간 편입/이탈 푸시 프레임 (trnm=REAL, values FID 매핑)."""

    def test_push_frame_maps_values_fid_keys(self):
        payload = {
            "trnm": "REAL",
            "data": [
                {
                    "type": "0A",
                    "name": "005930",
                    "values": {
                        "841": "1",
                        "9001": "A005930",
                        "843": "I",
                        "20": "093000",
                        "907": "2",
                        "9081": "1",
                    },
                }
            ],
        }

        push = DomesticConditionSearchRealtimePush.model_validate(payload)

        assert push.trnm == "REAL"
        item = push.data[0]
        assert item.type == "0A"
        assert item.name == "005930"
        assert item.values.seq_no == "1"
        assert item.values.stock_code == "A005930"
        assert item.values.insert_delete == "I"
        assert item.values.exec_time == "093000"
        assert item.values.buy_sell == "2"
        assert item.values.exchange == "1"

    def test_invalid_trnm_raises(self):
        with pytest.raises(ValueError):
            DomesticConditionSearchRealtimePush.model_validate({"trnm": "CNSRREQ", "data": []})

    def test_data_required(self):
        """스펙상 data/trnm 모두 Required=Y - data 누락시 검증 실패."""
        with pytest.raises(ValueError):
            DomesticConditionSearchRealtimePush.model_validate({"trnm": "REAL"})


# ---------------------------------------------------------------------------
# ka10174 조건검색 실시간 해제
# ---------------------------------------------------------------------------


class TestDomesticConditionSearchRealtimeCancel:
    def test_request_dump_matches_wire_format(self):
        request = DomesticConditionSearchRealtimeCancelRequest(trnm="CNSRCLR", seq="0")
        assert request.model_dump(by_alias=True) == {"trnm": "CNSRCLR", "seq": "0"}

    def test_invalid_trnm_raises(self):
        with pytest.raises(ValueError):
            DomesticConditionSearchRealtimeCancelRequest(trnm="INVALID", seq="0")

    def test_response_requires_all_fields(self):
        """스펙상 4개 필드 모두 Required=Y (단순 ACK 프레임) - 누락시 검증 실패."""
        response = DomesticConditionSearchRealtimeCancelResponse.model_validate(
            {"return_code": 0, "return_msg": "", "trnm": "CNSRCLR", "seq": "0"}
        )
        assert response.return_code == 0
        assert response.trnm == "CNSRCLR"
        assert response.seq == "0"

        with pytest.raises(ValueError):
            DomesticConditionSearchRealtimeCancelResponse.model_validate(
                {"return_code": 0, "return_msg": "", "trnm": "CNSRCLR"}
            )
