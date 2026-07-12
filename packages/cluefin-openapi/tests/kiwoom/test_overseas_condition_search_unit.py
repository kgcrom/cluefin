"""미국주식 조건검색(웹소켓) 메시지 모델 unit 테스트.

usa20280/usa20281/usa20290/usa20291 4개 TR은 웹소켓 API이므로 HTTP 클라이언트
테스트(run_post_case)를 적용할 수 없고, 클라이언트 구현도 아직 stub
(``_overseas_condition_search.py``)이다. 따라서 요청 모델의 wire 포맷 dump와 응답
모델의 field/alias 매핑만 검증한다.
"""

import pytest

from cluefin_openapi.kiwoom._overseas_condition_search_types import (
    OverseasConditionSearchListItem,
    OverseasConditionSearchListRequest,
    OverseasConditionSearchListResponse,
    OverseasConditionSearchRealtimeCancelRequest,
    OverseasConditionSearchRealtimeCancelResponse,
    OverseasConditionSearchRealtimeRequest,
    OverseasConditionSearchRealtimeResponse,
    OverseasConditionSearchRealtimeResultItem,
    OverseasConditionSearchRequest,
    OverseasConditionSearchResponse,
    OverseasConditionSearchResultItem,
)

# ---------------------------------------------------------------------------
# usa20280 미국주식 조건검색 목록조회
# ---------------------------------------------------------------------------


class TestOverseasConditionSearchList:
    def test_request_dump_matches_wire_format(self):
        request = OverseasConditionSearchListRequest(trnm="GCNSRLST")
        assert request.model_dump(by_alias=True) == {"trnm": "GCNSRLST"}

    def test_invalid_trnm_raises(self):
        with pytest.raises(ValueError):
            OverseasConditionSearchListRequest(trnm="INVALID")

    def test_response_validates_and_maps_fields(self):
        payload = {
            "return_code": 0,
            "return_msg": "",
            "trnm": "GCNSRLST",
            "data": [
                {"seq": "0", "name": "조건식1"},
                {"seq": "1", "name": "조건식2"},
            ],
        }

        response = OverseasConditionSearchListResponse.model_validate(payload)

        assert response.return_code == 0
        assert response.trnm == "GCNSRLST"
        assert len(response.data) == 2
        assert response.data[0] == OverseasConditionSearchListItem(seq="0", name="조건식1")
        assert response.data[1].seq == "1"
        assert response.data[1].name == "조건식2"


# ---------------------------------------------------------------------------
# usa20281 미국주식 조건검색 요청 일반
# ---------------------------------------------------------------------------


class TestOverseasConditionSearchRequest:
    def test_request_dump_matches_wire_format(self):
        request = OverseasConditionSearchRequest(
            trnm="GCNSRREQ",
            seq="0",
            search_type="0",
            cont_yn="N",
            next_key="",
        )

        assert request.model_dump(by_alias=True) == {
            "trnm": "GCNSRREQ",
            "seq": "0",
            "search_type": "0",
            "cont_yn": "N",
            "next_key": "",
        }

    def test_request_default_cont_yn_and_next_key(self):
        request = OverseasConditionSearchRequest(trnm="GCNSRREQ", seq="0", search_type="0")
        assert request.cont_yn == "N"
        assert request.next_key == ""

    def test_invalid_search_type_raises(self):
        """usa20281은 search_type이 반드시 '0' (일반조회)."""
        with pytest.raises(ValueError):
            OverseasConditionSearchRequest(trnm="GCNSRREQ", seq="0", search_type="1")

    def test_response_maps_fid_keys_by_alias(self):
        """usa20281 결과 항목: FID 숫자키(9001→stock_code 등) 매핑, stex_tp는 alias 없음."""
        payload = {
            "return_code": 0,
            "return_msg": "",
            "trnm": "GCNSRREQ",
            "seq": "0",
            "cont_yn": "N",
            "next_key": "",
            "data": [
                {
                    "9001": "NVDA",
                    "302": "엔비디아",
                    "10": "500.00",
                    "25": "2",
                    "11": "10.00",
                    "12": "2.04",
                    "13": "1000000",
                    "16": "495.00",
                    "17": "505.00",
                    "18": "490.00",
                    "318": "반도체",
                    "stex_tp": "ND",
                }
            ],
        }

        response = OverseasConditionSearchResponse.model_validate(payload)

        assert response.trnm == "GCNSRREQ"
        assert response.cont_yn == "N"
        item = response.data[0]
        assert item.stock_code == "NVDA"
        assert item.stock_name == "엔비디아"
        assert item.current_price == "500.00"
        assert item.prev_day_diff_sign == "2"
        assert item.prev_day_diff == "10.00"
        assert item.fluctuation_rate == "2.04"
        assert item.acc_trade_volume == "1000000"
        assert item.open_price == "495.00"
        assert item.high_price == "505.00"
        assert item.low_price == "490.00"
        assert item.sub_industry == "반도체"
        assert item.stex_tp == "ND"

    def test_populate_by_name_round_trip(self):
        item = OverseasConditionSearchResultItem(stock_code="NVDA", stock_name="엔비디아", current_price="500.00")
        dumped = item.model_dump(by_alias=True)
        assert dumped["9001"] == "NVDA"
        assert dumped["302"] == "엔비디아"
        assert dumped["10"] == "500.00"

    def test_response_continuation_frame(self):
        """cont_yn=Y 인 연속조회 프레임 - next_key 채워짐."""
        payload = {
            "return_code": 0,
            "return_msg": "",
            "trnm": "GCNSRREQ",
            "seq": "0",
            "cont_yn": "Y",
            "next_key": "000123",
            "data": [],
        }
        response = OverseasConditionSearchResponse.model_validate(payload)
        assert response.cont_yn == "Y"
        assert response.next_key == "000123"


# ---------------------------------------------------------------------------
# usa20290 미국주식 조건검색 요청 실시간
# ---------------------------------------------------------------------------


class TestOverseasConditionSearchRealtimeRequest:
    def test_request_dump_matches_wire_format(self):
        request = OverseasConditionSearchRealtimeRequest(trnm="GCNSRREQ", seq="0", search_type="1")
        assert request.model_dump(by_alias=True) == {
            "trnm": "GCNSRREQ",
            "seq": "0",
            "search_type": "1",
        }

    def test_invalid_search_type_raises(self):
        """usa20290은 search_type이 반드시 '1' (조건검색+실시간조건검색)."""
        with pytest.raises(ValueError):
            OverseasConditionSearchRealtimeRequest(trnm="GCNSRREQ", seq="0", search_type="0")

    def test_response_maps_stex_tp_alias(self):
        """usa20290 결과 항목: jmcode는 별도 alias 없이 필드명 그대로, stexTp→stex_tp."""
        payload = {
            "return_code": 0,
            "return_msg": "",
            "trnm": "GCNSRREQ",
            "seq": "0",
            "data": [{"jmcode": "AAPL", "stexTp": "ND"}],
        }

        response = OverseasConditionSearchRealtimeResponse.model_validate(payload)

        assert response.trnm == "GCNSRREQ"
        assert response.seq == "0"
        item = response.data[0]
        assert item.jmcode == "AAPL"
        assert item.stex_tp == "ND"

    def test_populate_by_name_round_trip(self):
        item = OverseasConditionSearchRealtimeResultItem(jmcode="AAPL", stex_tp="ND")
        dumped = item.model_dump(by_alias=True)
        assert dumped == {"jmcode": "AAPL", "stexTp": "ND"}

    def test_response_empty_data_real_push(self):
        """실시간 편입/이탈 이벤트가 없을 때도 data는 빈 리스트로 검증 가능."""
        payload = {"trnm": "GCNSRREQ", "seq": "0", "data": []}
        response = OverseasConditionSearchRealtimeResponse.model_validate(payload)
        assert response.return_code is None
        assert response.data == []


# ---------------------------------------------------------------------------
# usa20291 미국주식 조건검색 실시간 해제
# ---------------------------------------------------------------------------


class TestOverseasConditionSearchRealtimeCancel:
    def test_request_dump_matches_wire_format(self):
        request = OverseasConditionSearchRealtimeCancelRequest(trnm="GCNSRCLR", seq="0")
        assert request.model_dump(by_alias=True) == {"trnm": "GCNSRCLR", "seq": "0"}

    def test_invalid_trnm_raises(self):
        with pytest.raises(ValueError):
            OverseasConditionSearchRealtimeCancelRequest(trnm="INVALID", seq="0")

    def test_response_requires_all_fields(self):
        """스펙상 4개 필드 모두 Required=Y (단순 ACK 프레임) - 누락시 검증 실패."""
        response = OverseasConditionSearchRealtimeCancelResponse.model_validate(
            {"return_code": 0, "return_msg": "", "trnm": "GCNSRCLR", "seq": "0"}
        )
        assert response.return_code == 0
        assert response.trnm == "GCNSRCLR"
        assert response.seq == "0"

        with pytest.raises(ValueError):
            OverseasConditionSearchRealtimeCancelResponse.model_validate(
                {"return_code": 0, "return_msg": "", "trnm": "GCNSRCLR"}
            )
