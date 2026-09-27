from types import SimpleNamespace
from typing import List, Optional, Union

import pytest
from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.nhplug._model import NHPlugAssetHttpBody

from . import _response_shape
from ._response_shape import assert_matches_spec, length_violations, response_shape_diff, value_length


class Row(BaseModel):
    model_config = ConfigDict(extra="allow")

    iem_cd: str
    iem_nm: Optional[str] = None


class Summary(BaseModel):
    model_config = ConfigDict(extra="allow")

    total: Optional[int] = None


class Body(NHPlugAssetHttpBody):
    output_0: Optional[Summary] = Field(default=None, alias="Output_0")
    output_1: Optional[List[Row]] = Field(default=None, alias="Output_1")


class EitherBody(NHPlugAssetHttpBody):
    output_0: Optional[Union[Summary, List[Summary]]] = Field(default=None, alias="Output_0")


def _raw(**overrides):
    raw = {
        "rsp_cd": "00000",
        "rsp_msg": "ok",
        "Output_0": {"total": 1},
        "Output_1": [{"iem_cd": "005930", "iem_nm": "삼성전자"}],
    }
    raw.update(overrides)
    return raw


def test_exact_match_has_no_problems():
    assert response_shape_diff(_raw(), Body) == []


def test_omitted_top_level_blocks_and_message_are_fine():
    raw = _raw()
    del raw["Output_1"]
    assert response_shape_diff(raw, Body) == []


def test_omitted_envelope_key_is_reported():
    raw = _raw()
    del raw["rsp_msg"]
    assert response_shape_diff(raw, Body) == ["missing: rsp_msg (model declares it, server did not send it)"]


def test_misnamed_block_is_reported_as_extra():
    raw = _raw()
    raw["Output_2"] = raw.pop("Output_1")
    assert response_shape_diff(raw, Body) == ["extra: Output_2 (server sent it, model does not declare it)"]


def test_field_kept_only_by_extra_allow_is_reported():
    raw = _raw(Output_1=[{"iem_cd": "005930", "iem_nm": "삼성전자", "stck_prpr": 1}])
    assert response_shape_diff(raw, Body) == ["extra: Output_1.stck_prpr (server sent it, model does not declare it)"]


def test_array_rows_are_compared_over_the_key_union():
    raw = _raw(Output_1=[{"iem_cd": "005930"}, {"iem_cd": "000660", "iem_nm": "SK하이닉스"}])
    assert response_shape_diff(raw, Body) == []


def test_missing_row_field_is_reported():
    raw = _raw(Output_1=[{"iem_cd": "005930"}])
    assert response_shape_diff(raw, Body) == ["missing: Output_1.iem_nm (model declares it, server did not send it)"]


def test_wrong_kind_is_reported():
    raw = _raw(Output_1={"iem_cd": "005930", "iem_nm": "삼성전자"})
    assert response_shape_diff(raw, Body) == ["kind: Output_1 is object on the server, model expects array"]


@pytest.mark.parametrize("block", [{"total": 1}, [{"total": 1}]])
def test_object_or_array_union_matches_what_the_server_sent(block):
    assert response_shape_diff(_raw(Output_0=block, Output_1=None), EitherBody) == [
        "extra: Output_1 (server sent it, model does not declare it)"
    ]


def test_empty_array_skips_key_check():
    assert response_shape_diff(_raw(Output_1=[]), Body) == []


@pytest.mark.parametrize(
    ("value", "spec", "expected"),
    [
        ("005930", "6", None),
        ("0059301", "6", "7"),
        ("삼성전자", "8", None),  # CP949 2바이트 × 4
        ("삼성전자우", "8", "10"),
        ("�", "1", "2"),  # 쓰레기 바이트 — TS 헬퍼와 같은 결과
        (-1234, "4", None),  # 부호는 세지 않는다
        (12345, "4", "5"),
        (100.0, "3", None),
        (-29.99, "5.2", None),
        (123.45, "5.2", None),  # 정수부 3자리까지
        (1234.5, "5.2", "4.1"),
        (1.234, "5.2", "1.3"),
        (0.5, "5.2", None),
        ("", "1", None),
        (None, "1", None),
    ],
)
def test_value_length(value, spec, expected):
    assert value_length(value, spec) == expected


@pytest.fixture
def spec(monkeypatch):
    monkeypatch.setattr(
        _response_shape,
        "SPEC_LENGTHS",
        {"/x": {"req": {"iem_cd": "6"}, "res": {"Output_1.iem_nm": "4", "Output_0.total": "2"}}},
    )
    monkeypatch.setattr(_response_shape, "KNOWN_EXCEED", {})


def test_length_violations_reports_request_and_worst_row(spec):
    raw = _raw(Output_1=[{"iem_cd": "1", "iem_nm": "가나다"}, {"iem_cd": "2", "iem_nm": "가나다라마"}, {"iem_cd": "3"}])
    assert length_violations("/x", {"iem_cd": "0059301"}, raw) == [
        "length: request iem_cd is 7, spec says 6",
        "length: Output_1.iem_nm is up to 10, spec says 4",
    ]


def test_length_violations_worst_row_compares_numerically(spec):
    raw = _raw(Output_1=[{"iem_cd": "1", "iem_nm": "ABCDEFGHI"}, {"iem_cd": "2", "iem_nm": "ABCDEFGHIJ"}])
    assert length_violations("/x", {}, raw) == ["length: Output_1.iem_nm is up to 10, spec says 4"]


def test_known_exceed_is_skipped(spec, monkeypatch):
    monkeypatch.setattr(_response_shape, "KNOWN_EXCEED", {"/x": {"Output_1.iem_nm": "errata", "req.iem_cd": "errata"}})
    raw = _raw(Output_1=[{"iem_cd": "1", "iem_nm": "가나다라마"}])
    assert length_violations("/x", {"iem_cd": "0059301"}, raw) == []


def test_unknown_path_has_no_length_rules():
    assert length_violations("/nowhere", {"a": "x" * 100}, _raw()) == []


def test_spec_snapshot_covers_implemented_apis():
    assert "/krstock/quote/v1/currentPrice" in _response_shape.SPEC_LENGTHS
    assert _response_shape.SPEC_LENGTHS["/krstock/quote/v1/currentPrice"]["req"]["iem_cd"] == "6"


def _client(raw, request=None, path="/nowhere"):
    return SimpleNamespace(last_exchange={"path": path, "request": request or {}, "response": raw})


def test_assert_matches_spec_passes_and_honours_ignore():
    raw = _raw(Output_1=[{"iem_cd": "005930", "iem_nm": "삼성전자", "kor_name": "삼성전자"}])
    response = SimpleNamespace(body=Body.model_validate(raw))
    with pytest.raises(AssertionError, match="Output_1.kor_name"):
        assert_matches_spec(_client(raw), response)
    assert_matches_spec(_client(raw), response, ignore=["Output_1.kor_name"])


def test_assert_matches_spec_requires_a_captured_exchange():
    with pytest.raises(AssertionError, match="no captured"):
        assert_matches_spec(SimpleNamespace(), SimpleNamespace(body=Body.model_validate(_raw())))
