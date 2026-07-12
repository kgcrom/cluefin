"""미국주식 실시간 시세(웹소켓) 메시지 모델 unit 테스트.

F4/F5/FE/FT 4개 TR은 웹소켓 API이므로 HTTP 클라이언트 테스트(run_post_case)를 적용할 수
없고, 클라이언트 구현도 아직 stub(``_overseas_realtime.py``)이다. 따라서 등록/해지 요청
프레임과 TR별 응답(values) 프레임의 pydantic 직렬화/역직렬화만 검증한다.
"""

import pytest

from cluefin_openapi.kiwoom._overseas_realtime_types import (
    OverseasRealtimeExecution,
    OverseasRealtimeExecutionDataItem,
    OverseasRealtimeExecutionPrice,
    OverseasRealtimeExecutionPriceDataItem,
    OverseasRealtimeExecutionPriceValues,
    OverseasRealtimeExecutionValues,
    OverseasRealtimeOrderConfirmation,
    OverseasRealtimeOrderConfirmationDataItem,
    OverseasRealtimeOrderConfirmationValues,
    OverseasRealtimeRegisterData,
    OverseasRealtimeRegisterItem,
    OverseasRealtimeRequest,
    OverseasRealtimeTenQuotes,
    OverseasRealtimeTenQuotesDataItem,
    OverseasRealtimeTenQuotesValues,
)

# ---------------------------------------------------------------------------
# 등록/해지 요청 프레임 (F4/F5/FE/FT 공통)
# ---------------------------------------------------------------------------


class TestOverseasRealtimeRequest:
    def test_register_request_dump_matches_wire_format(self):
        """REG 요청: trnm/grp_no/refresh/data[item[jmcode,stex_tp],type] 그대로 dump."""
        request = OverseasRealtimeRequest(
            trnm="REG",
            grp_no="1",
            refresh="1",
            data=[
                OverseasRealtimeRegisterData(
                    item=[OverseasRealtimeRegisterItem(jmcode="NVDA", stex_tp="ND")],
                    type=["F4"],
                )
            ],
        )

        assert request.model_dump(by_alias=True) == {
            "trnm": "REG",
            "grp_no": "1",
            "refresh": "1",
            "data": [{"item": [{"jmcode": "NVDA", "stex_tp": "ND"}], "type": ["F4"]}],
        }

    def test_remove_request_dump_matches_wire_format(self):
        """REMOVE 요청: 해지시 refresh 값은 스펙상 불필요하지만 필수 필드이므로 그대로 전달."""
        request = OverseasRealtimeRequest(
            trnm="REMOVE",
            grp_no="1",
            refresh="0",
            data=[
                OverseasRealtimeRegisterData(
                    item=[OverseasRealtimeRegisterItem(jmcode="AAPL", stex_tp="NA")],
                    type=["FT"],
                )
            ],
        )

        assert request.model_dump(by_alias=True) == {
            "trnm": "REMOVE",
            "grp_no": "1",
            "refresh": "0",
            "data": [{"item": [{"jmcode": "AAPL", "stex_tp": "NA"}], "type": ["FT"]}],
        }

    def test_register_request_multiple_items_and_types(self):
        """복수 종목/복수 TR type 등록 요청도 wire 포맷대로 dump."""
        request = OverseasRealtimeRequest(
            trnm="REG",
            grp_no="1",
            refresh="1",
            data=[
                OverseasRealtimeRegisterData(
                    item=[
                        OverseasRealtimeRegisterItem(jmcode="NVDA", stex_tp="ND"),
                        OverseasRealtimeRegisterItem(jmcode="AAPL", stex_tp="ND"),
                    ],
                    type=["FE", "FT"],
                )
            ],
        )

        dumped = request.model_dump(by_alias=True)
        assert dumped["data"][0]["item"] == [
            {"jmcode": "NVDA", "stex_tp": "ND"},
            {"jmcode": "AAPL", "stex_tp": "ND"},
        ]
        assert dumped["data"][0]["type"] == ["FE", "FT"]

    def test_invalid_trnm_raises(self):
        with pytest.raises(ValueError):
            OverseasRealtimeRequest(trnm="INVALID", grp_no="1", refresh="1")

    def test_invalid_refresh_raises(self):
        with pytest.raises(ValueError):
            OverseasRealtimeRequest(trnm="REG", grp_no="1", refresh="2")


# ---------------------------------------------------------------------------
# F4 미국주식 실시간 주문 확인
# ---------------------------------------------------------------------------


class TestOverseasRealtimeOrderConfirmation:
    def test_register_ack_frame_validates(self):
        """등록/해지 요청에 대한 ACK 프레임 (return_code 존재)."""
        frame = OverseasRealtimeOrderConfirmation.model_validate(
            {"return_code": 0, "return_msg": "", "trnm": "REG", "data": []}
        )

        assert frame.return_code == 0
        assert frame.return_msg == ""
        assert frame.trnm == "REG"
        assert frame.data == []

    def test_real_frame_maps_fid_values_by_alias(self):
        """실시간 수신 프레임(REAL): FID 숫자키 values → 필드 alias 매핑."""
        payload = {
            "return_msg": "",
            "trnm": "REAL",
            "data": [
                {
                    "type": "F4",
                    "name": "미국주식실시간주문확인",
                    "stexTp": "ND",
                    "item": "NVDA",
                    "values": {
                        "9201": "1234567890",
                        "9203": "000001",
                        "9001": "NVDA",
                        "905": "10",
                        "907": "02",
                        "904": "",
                        "900": "10",
                        "901": "500.00",
                        "906": "1",
                        "913": "접수",
                        "908": "20250102103000",
                        "50810": "",
                        "8043": "USD",
                        "50841": "0",
                        "55190": "US",
                        "1091": "미국",
                        "50072": "매수",
                        "302": "엔비디아",
                        "50073": "지정가",
                    },
                }
            ],
        }

        frame = OverseasRealtimeOrderConfirmation.model_validate(payload)

        assert frame.return_code is None
        assert frame.trnm == "REAL"
        item = frame.data[0]
        assert item.type == "F4"
        assert item.stex_tp == "ND"
        assert item.item == "NVDA"

        values = item.values
        assert values.account_no == "1234567890"
        assert values.order_no == "000001"
        assert values.stock_code == "NVDA"
        assert values.order_type == "10"
        assert values.sell_buy_type == "02"
        assert values.order_quantity == "10"
        assert values.order_price == "500.00"
        assert values.order_status == "접수"
        assert values.currency_code == "USD"
        assert values.country_code == "US"
        assert values.country_name == "미국"
        assert values.sell_buy_type_name == "매수"
        assert values.stock_name == "엔비디아"
        assert values.trade_type_name == "지정가"

    def test_populate_by_name_round_trip(self):
        """필드명으로 생성 → by_alias dump시 FID 키로 나오는지 확인."""
        values = OverseasRealtimeOrderConfirmationValues(
            account_no="1234567890",
            order_no="000001",
            stock_code="NVDA",
        )

        dumped = values.model_dump(by_alias=True)
        assert dumped["9201"] == "1234567890"
        assert dumped["9203"] == "000001"
        assert dumped["9001"] == "NVDA"

    def test_data_item_default_factory(self):
        """values 미지정시 default_factory로 빈 values가 채워짐."""
        item = OverseasRealtimeOrderConfirmationDataItem(type="F4", item="NVDA")
        assert item.values.account_no == ""


# ---------------------------------------------------------------------------
# F5 미국주식 실시간 체결
# ---------------------------------------------------------------------------


class TestOverseasRealtimeExecution:
    def test_real_frame_maps_fid_values_by_alias(self):
        payload = {
            "trnm": "REAL",
            "data": [
                {
                    "type": "F5",
                    "name": "미국주식실시간체결",
                    "item": "AAPL",
                    "values": {
                        "1091": "미국",
                        "8046": "NAS",
                        "9001": "AAPL",
                        "302": "애플",
                        "904": "",
                        "9203": "000002",
                        "905": "10",
                        "907": "01",
                        "908": "20250102103000",
                        "913": "체결완료",
                        "900": "5",
                        "901": "190.00",
                        "902": "0",
                        "909": "000010",
                        "910": "190.00",
                        "911": "5",
                        "930": "100",
                        "931": "180.00",
                        "8018": "50.00",
                        "8019": "2.5",
                        "8043": "USD",
                        "9201": "1234567890",
                        "50072": "매도",
                        "50073": "지정가",
                    },
                }
            ],
        }

        frame = OverseasRealtimeExecution.model_validate(payload)
        assert frame.return_code is None
        assert frame.trnm == "REAL"

        values = frame.data[0].values
        assert values.country_name == "미국"
        assert values.exchange_code == "NAS"
        assert values.stock_code == "AAPL"
        assert values.stock_name == "애플"
        assert values.order_no == "000002"
        assert values.order_status == "체결완료"
        assert values.execution_no == "000010"
        assert values.execution_price == "190.00"
        assert values.execution_quantity == "5"
        assert values.holding_quantity == "100"
        assert values.purchase_unit_price == "180.00"
        assert values.profit_loss_amount == "50.00"
        assert values.profit_loss_rate == "2.5"
        assert values.account_no == "1234567890"
        assert values.sell_buy_type_name == "매도"
        assert values.trade_type_name == "지정가"

    def test_register_ack_frame_return_code_present(self):
        frame = OverseasRealtimeExecution.model_validate(
            {"return_code": 1, "return_msg": "오류", "trnm": "REG", "data": []}
        )
        assert frame.return_code == 1
        assert frame.return_msg == "오류"

    def test_data_item_default_values(self):
        item = OverseasRealtimeExecutionDataItem(type="F5", item="AAPL")
        assert isinstance(item.values, OverseasRealtimeExecutionValues)
        assert item.values.stock_code == ""


# ---------------------------------------------------------------------------
# FE 미국주식 실시간 체결가
# ---------------------------------------------------------------------------


class TestOverseasRealtimeExecutionPrice:
    def test_real_frame_maps_fid_values_by_alias(self):
        payload = {
            "trnm": "REAL",
            "data": [
                {
                    "type": "FE",
                    "name": "미국주식실시간체결가",
                    "item": "TSLA",
                    "values": {
                        "10": "250.00",
                        "11": "5.00",
                        "12": "2.04",
                        "13": "1000000",
                        "14": "250000000",
                        "15": "10",
                        "16": "245.00",
                        "17": "252.00",
                        "18": "244.00",
                        "20": "103000",
                        "22": "20250102",
                        "25": "2",
                        "27": "250.10",
                        "28": "249.90",
                        "30": "1.2",
                        "228": "120",
                        "290": "1",
                        "51020": "20250101223000",
                    },
                }
            ],
        }

        frame = OverseasRealtimeExecutionPrice.model_validate(payload)
        assert frame.return_code is None

        values = frame.data[0].values
        assert values.current_price == "250.00"
        assert values.prev_day_diff == "5.00"
        assert values.fluctuation_rate == "2.04"
        assert values.acc_trade_volume == "1000000"
        assert values.acc_trade_value == "250000000"
        assert values.execution_volume == "10"
        assert values.open_price == "245.00"
        assert values.high_price == "252.00"
        assert values.low_price == "244.00"
        assert values.time == "103000"
        assert values.execution_date == "20250102"
        assert values.prev_day_diff_sign == "2"
        assert values.best_ask_price == "250.10"
        assert values.best_bid_price == "249.90"
        assert values.prev_day_volume_ratio == "1.2"
        assert values.execution_strength == "120"
        assert values.market_type == "1"
        assert values.local_execution_time == "20250101223000"

    def test_populate_by_name_round_trip(self):
        values = OverseasRealtimeExecutionPriceValues(current_price="250.00", time="103000")
        dumped = values.model_dump(by_alias=True)
        assert dumped["10"] == "250.00"
        assert dumped["20"] == "103000"

    def test_data_item_default_values(self):
        item = OverseasRealtimeExecutionPriceDataItem(type="FE", item="TSLA")
        assert item.values.current_price == ""


# ---------------------------------------------------------------------------
# FT 미국주식 10호가
# ---------------------------------------------------------------------------


class TestOverseasRealtimeTenQuotes:
    def test_real_frame_maps_fid_values_by_alias(self):
        payload = {
            "trnm": "REAL",
            "data": [
                {
                    "type": "FT",
                    "name": "미국주식10호가",
                    "item": "NVDA",
                    "values": {
                        "21": "103000",
                        "41": "500.10",
                        "61": "100",
                        "81": "0",
                        "51": "500.00",
                        "71": "200",
                        "91": "0",
                        "50": "505.10",
                        "70": "10",
                        "90": "0",
                        "60": "504.00",
                        "80": "20",
                        "100": "0",
                        "121": "1000",
                        "122": "10",
                        "125": "1200",
                        "126": "-5",
                    },
                }
            ],
        }

        frame = OverseasRealtimeTenQuotes.model_validate(payload)
        assert frame.return_code is None

        values = frame.data[0].values
        assert values.time == "103000"
        assert values.ask_price_1 == "500.10"
        assert values.ask_volume_1 == "100"
        assert values.ask_prev_diff_1 == "0"
        assert values.bid_price_1 == "500.00"
        assert values.bid_volume_1 == "200"
        assert values.bid_prev_diff_1 == "0"
        assert values.ask_price_10 == "505.10"
        assert values.ask_volume_10 == "10"
        assert values.ask_prev_diff_10 == "0"
        assert values.bid_price_10 == "504.00"
        assert values.bid_volume_10 == "20"
        assert values.bid_prev_diff_10 == "0"
        assert values.total_ask_volume == "1000"
        assert values.total_ask_volume_prev_diff == "10"
        assert values.total_bid_volume == "1200"
        assert values.total_bid_volume_prev_diff == "-5"

    def test_data_item_default_values(self):
        item = OverseasRealtimeTenQuotesDataItem(type="FT", item="NVDA")
        assert item.values.time == ""

    def test_all_65_fields_present(self):
        """스펙상 65개 FID 필드(호가/잔량/직전대비 10단계×6 + 시간 1 + 총잔량류 4) 존재 확인."""
        assert len(OverseasRealtimeTenQuotesValues.model_fields) == 65
