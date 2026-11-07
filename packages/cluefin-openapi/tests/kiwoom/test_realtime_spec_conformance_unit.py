"""`_realtime_spec_conformance` 헬퍼 자체를 검증한다.

헬퍼가 느슨하면 WS 통합테스트가 FID 매핑 회귀(엉뚱한 alias, 복사 실수)를 못 잡는다.
"""

import pytest
from pydantic import BaseModel, Field

from cluefin_openapi.kiwoom._socket_client import KiwoomWebSocketMessage

from ._realtime_spec_conformance import (
    EmptyValuesWarning,
    RealKeyDiff,
    assert_real_frame_key_conformance,
    real_frame_key_diff,
)


class _ExecutionValues(BaseModel):
    model_config = {"populate_by_name": True}

    current_price: str = Field(default="", alias="10")
    execution_time: str = Field(default="", alias="20")


class _QuoteValues(BaseModel):
    model_config = {"populate_by_name": True}

    ask_price_1: str = Field(default="", alias="41")


_MODELS = {"0B": _ExecutionValues, "0D": _QuoteValues}


def _real(data: list[dict]) -> KiwoomWebSocketMessage:
    return KiwoomWebSocketMessage(trnm="REAL", body={"trnm": "REAL", "data": data})


class TestRealFrameKeyDiff:
    def test_matching_keys_yield_no_diff(self):
        message = _real([{"type": "0B", "name": "005930", "values": {"10": "70000", "20": "093000"}}])

        diffs = real_frame_key_diff(message, _MODELS)

        assert diffs == []

    def test_non_real_frame_is_ignored(self):
        message = KiwoomWebSocketMessage(trnm="REG", body={"trnm": "REG", "return_code": 0})

        assert real_frame_key_diff(message, _MODELS) == []

    def test_type_not_in_models_is_skipped(self):
        message = _real([{"type": "0A", "name": "005930", "values": {"unmapped": "1"}}])

        assert real_frame_key_diff(message, _MODELS) == []

    def test_server_only_key_is_reported(self):
        """서버가 모델에 없는 FID 를 보내면 ``server_only`` 에 담긴다 (예: 복사 실수로 뺀 필드)."""
        message = _real([{"type": "0B", "name": "005930", "values": {"10": "70000", "20": "093000", "667": "1"}}])

        diffs = real_frame_key_diff(message, _MODELS)

        assert diffs == [RealKeyDiff(type="0B", model_only=frozenset(), server_only=frozenset({"667"}))]

    def test_model_only_key_is_reported(self):
        """모델이 선언한 FID 를 서버가 안 보내면 ``model_only`` 에 담긴다."""
        message = _real([{"type": "0B", "name": "005930", "values": {"10": "70000"}}])

        diffs = real_frame_key_diff(message, _MODELS)

        assert diffs == [RealKeyDiff(type="0B", model_only=frozenset({"20"}), server_only=frozenset())]

    def test_mixed_types_in_one_frame_each_compared_separately(self):
        message = _real(
            [
                {"type": "0B", "name": "005930", "values": {"10": "70000", "20": "093000"}},
                {"type": "0D", "name": "005930", "values": {"41": "70100", "extra": "x"}},
            ]
        )

        diffs = real_frame_key_diff(message, _MODELS)

        assert diffs == [RealKeyDiff(type="0D", model_only=frozenset(), server_only=frozenset({"extra"}))]

    def test_empty_values_is_reported_via_empty_list_not_diff(self):
        message = _real([{"type": "0B", "name": "005930", "values": {}}])
        empty: list[str] = []

        diffs = real_frame_key_diff(message, _MODELS, empty=empty)

        assert diffs == []
        assert empty == ["0B"]


class TestAssertRealFrameKeyConformance:
    def test_matching_frame_passes(self):
        message = _real([{"type": "0B", "name": "005930", "values": {"10": "70000", "20": "093000"}}])

        assert_real_frame_key_conformance(message, _MODELS)

    def test_non_real_frame_passes(self):
        message = KiwoomWebSocketMessage(trnm="REG", body={"trnm": "REG", "return_code": 0})

        assert_real_frame_key_conformance(message, _MODELS)

    def test_server_only_key_fails(self):
        message = _real([{"type": "0B", "name": "005930", "values": {"10": "70000", "20": "093000", "667": "1"}}])

        with pytest.raises(AssertionError, match=r"extra: 0B\.values\.667"):
            assert_real_frame_key_conformance(message, _MODELS)

    def test_model_only_key_fails(self):
        message = _real([{"type": "0B", "name": "005930", "values": {"10": "70000"}}])

        with pytest.raises(AssertionError, match=r"missing: 0B\.values\.20"):
            assert_real_frame_key_conformance(message, _MODELS)

    def test_ignored_key_does_not_fail(self):
        message = _real([{"type": "0B", "name": "005930", "values": {"10": "70000", "20": "093000", "667": "1"}}])

        assert_real_frame_key_conformance(message, _MODELS, ignore=["667"])

    def test_empty_values_warns_but_does_not_fail(self):
        message = _real([{"type": "0B", "name": "005930", "values": {}}])

        with pytest.warns(EmptyValuesWarning, match="0B"):
            assert_real_frame_key_conformance(message, _MODELS)
