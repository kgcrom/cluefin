"""국내주식 실시간 시세(웹소켓) 메시지 모델 unit 테스트.

19개 실시간 TR은 웹소켓 API이므로 HTTP 클라이언트 테스트(run_post_case)를 적용할 수
없다. 여기서는 등록/해지 요청 모델의 wire 포맷 dump와 대표 TR 응답 모델의 FID(alias)
매핑을 검증한다. ``DomesticRealtime`` 도메인 래퍼의 송신·파싱 동작은
``test_domestic_realtime_ws_unit.py``에서 검증한다.
(미국주식 ``test_overseas_realtime_unit`` 과 대칭.)
"""

import pytest

from cluefin_openapi.kiwoom._domestic_realtime_types import (
    DomesticRealtimeEtfNavValues,
    DomesticRealtimeIndustryFluctuationValues,
    DomesticRealtimeOrderExecutionValues,
    DomesticRealtimeRegisterData,
    DomesticRealtimeRequest,
    DomesticRealtimeStockExecutionValues,
    DomesticRealtimeStockQuoteRemainingValues,
)

# ---------------------------------------------------------------------------
# 공통 등록/해지 요청
# ---------------------------------------------------------------------------


class TestDomesticRealtimeRequest:
    def test_reg_request_dump_matches_wire_format(self):
        request = DomesticRealtimeRequest(
            trnm="REG",
            grp_no="1",
            refresh="1",
            data=[DomesticRealtimeRegisterData(item=["005930", "000660"], type=["0B", "0D"])],
        )
        assert request.model_dump(by_alias=True) == {
            "trnm": "REG",
            "grp_no": "1",
            "refresh": "1",
            "data": [{"item": ["005930", "000660"], "type": ["0B", "0D"]}],
        }

    def test_invalid_trnm_raises(self):
        with pytest.raises(ValueError):
            DomesticRealtimeRequest(trnm="INVALID", grp_no="1", refresh="1")

    def test_invalid_refresh_raises(self):
        with pytest.raises(ValueError):
            DomesticRealtimeRequest(trnm="REG", grp_no="1", refresh="2")


# ---------------------------------------------------------------------------
# TR별 values FID 매핑
# ---------------------------------------------------------------------------


class TestValuesFidMapping:
    def test_stock_execution_maps_fid_keys_by_alias(self):
        """0B 주식체결: FID 숫자키(20→execution_time 등) 매핑."""
        values = DomesticRealtimeStockExecutionValues.model_validate(
            {"20": "165208", "10": "-20800", "11": "-50", "12": "-0.24", "13": "30379732", "25": "5"}
        )
        assert values.execution_time == "165208"
        assert values.current_price == "-20800"
        assert values.prev_day_diff == "-50"
        assert values.fluctuation_rate == "-0.24"
        assert values.acc_trade_volume == "30379732"
        assert values.prev_day_diff_sign == "5"

    def test_order_execution_maps_account_and_order_fields(self):
        """00 주문체결: 계좌/주문 관련 FID 매핑."""
        values = DomesticRealtimeOrderExecutionValues.model_validate(
            {"9201": "1111111111", "9203": "0000018", "9001": "005930", "913": "접수", "900": "1", "907": "2"}
        )
        assert values.account_no == "1111111111"
        assert values.order_no == "0000018"
        assert values.stock_code == "005930"
        assert values.order_status == "접수"
        assert values.order_quantity == "1"
        assert values.sell_buy_type == "2"

    def test_etf_nav_has_nav_specific_fields(self):
        """0G ETF NAV: 0g(주식종목정보)와 코드는 유사하나 NAV 전용 FID를 가진다."""
        values = DomesticRealtimeEtfNavValues.model_validate(
            {"36": "+7488.27", "37": "+1.20", "38": "+0.02", "39": "0.02", "265": "-0.01", "266": "-0.02"}
        )
        assert values.nav == "+7488.27"
        assert values.nav_prev_day_diff == "+1.20"
        assert values.nav_fluctuation_rate == "+0.02"
        assert values.tracking_error_rate == "0.02"
        assert values.nav_index_gap_rate == "-0.01"
        assert values.nav_etf_gap_rate == "-0.02"

    def test_industry_fluctuation_has_counts(self):
        """0U 업종등락: 상승/하락 종목수 등 업종 전용 FID."""
        values = DomesticRealtimeIndustryFluctuationValues.model_validate(
            {"252": "46", "251": "0", "253": "5", "255": "40", "254": "3", "256": "94"}
        )
        assert values.advancing_count == "46"
        assert values.upper_limit_count == "0"
        assert values.unchanged_count == "5"
        assert values.declining_count == "40"
        assert values.lower_limit_count == "3"
        assert values.traded_stock_count == "94"

    def test_quote_remaining_numbered_series_map_in_order(self):
        """0D 주식호가잔량: 매도/매수 호가 번호 시리즈가 순서대로 매핑."""
        values = DomesticRealtimeStockQuoteRemainingValues.model_validate(
            {"41": "20800", "50": "20300", "51": "20750", "60": "20200", "61": "1000", "71": "2000"}
        )
        assert values.ask_price_1 == "20800"
        assert values.ask_price_10 == "20300"
        assert values.bid_price_1 == "20750"
        assert values.bid_price_10 == "20200"
        assert values.ask_volume_1 == "1000"
        assert values.bid_volume_1 == "2000"

    def test_populate_by_name_round_trip(self):
        values = DomesticRealtimeStockExecutionValues(current_price="-20800", execution_time="165208")
        dumped = values.model_dump(by_alias=True)
        assert dumped["10"] == "-20800"
        assert dumped["20"] == "165208"

    def test_unmapped_fid_keys_are_ignored(self):
        """알 수 없는 FID 키는 무시하고 매핑된 필드만 채운다."""
        values = DomesticRealtimeStockExecutionValues.model_validate({"10": "70000", "99999": "x"})
        assert values.current_price == "70000"
