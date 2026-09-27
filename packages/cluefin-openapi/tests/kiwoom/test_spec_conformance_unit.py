"""`_spec_conformance` 헬퍼 자체를 검증한다 — 헬퍼가 느슨하면 통합테스트가 스키마 회귀를 못 잡는다."""

from types import SimpleNamespace

import pytest
from pydantic import AliasChoices, BaseModel, Field

from cluefin_openapi.kiwoom._model import KiwoomHttpBody

from . import _spec_conformance
from ._spec_conformance import (
    SPEC_LENGTHS,
    EmptyBlockWarning,
    Exchange,
    assert_spec_conformance,
    length_diff,
    record_exchanges,
    response_shape_diff,
)


class Row(BaseModel):
    dt: str = ""
    name: str = Field(default="", validation_alias=AliasChoices("name", "stk_nm"))


class Body(BaseModel, KiwoomHttpBody):
    cur_prc: str = ""
    rows: list[Row] = Field(default_factory=list)


def _raw(**overrides):
    raw = {
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
        "cur_prc": "+1000",
        "rows": [{"dt": "20260925", "name": "삼성전자"}, {"dt": "20260924", "name": "삼성전자"}],
    }
    raw.update(overrides)
    return raw


def _client(raw, body=None, api_id="ka99999"):
    return SimpleNamespace(_last_exchange=Exchange(api_id, body or {}, raw))


def _response(raw):
    return SimpleNamespace(body=Body.model_validate(raw))


def test_exact_match_ignores_envelope():
    assert response_shape_diff(_raw(), Body) == []


def test_alias_choice_counts_as_present():
    assert response_shape_diff(_raw(rows=[{"dt": "1", "stk_nm": "x"}]), Body) == []


def test_missing_extra_and_row_union_are_reported():
    raw = _raw(rows=[{"dt": "1", "name": "x"}, {"dt": "2", "name": "y", "pipe1": "z"}])
    del raw["cur_prc"]
    raw["acc_trde_qty"] = "1"

    assert response_shape_diff(raw, Body) == [
        "missing: cur_prc (model declares it, server did not send it)",
        "extra: rows.pipe1 (server sent it, model does not declare it)",
        "extra: acc_trde_qty (server sent it, model does not declare it)",
    ]


def test_kind_mismatch_is_reported():
    assert response_shape_diff(_raw(rows={"dt": "1", "name": "x"}), Body) == [
        "kind: rows is object on the server, model expects array"
    ]


def test_empty_array_is_collected_not_passed_silently():
    empty: list[str] = []
    assert response_shape_diff(_raw(rows=[]), Body, empty=empty) == []
    assert empty == ["rows"]


def test_length_uses_longest_row_and_counts_signs():
    data = {"cur_prc": "--1000", "rows": [{"dt": "20260925"}, {"dt": "2026092512"}]}

    assert length_diff(data, {"cur_prc": 5, "rows.dt": 8}, "response") == [
        "length: response cur_prc is 6 chars, spec Length is 5",
        "length: response rows.dt is 10 chars, spec Length is 8",
    ]


def test_length_counts_characters_not_bytes():
    assert length_diff({"name": "가" * 20}, {"name": 20}, "response") == []


def test_length_skips_fields_without_spec_length():
    assert length_diff({"unknown": "x" * 100}, {}, "request") == []


def test_length_checks_request_list_of_scalars():
    assert length_diff({"stk_cd": ["AAPL", "TOOLONGTICKER"]}, {"stk_cd": 12}, "request") == [
        "length: request stk_cd is 13 chars, spec Length is 12"
    ]


def test_assert_passes_on_exact_match(monkeypatch):
    monkeypatch.setitem(SPEC_LENGTHS, "ka99999", {"request": {"stk_cd": 20}, "response": {"rows.dt": 8}})
    raw = _raw()
    assert_spec_conformance(_client(raw, {"stk_cd": "005930"}), _response(raw))


def test_assert_fails_without_leaking_values(monkeypatch):
    monkeypatch.setitem(SPEC_LENGTHS, "ka99999", {"request": {}, "response": {"cur_prc": 3}})
    raw = _raw(cur_prc="8888888888", acnt_no="1234567890")

    with pytest.raises(AssertionError) as exc:
        assert_spec_conformance(_client(raw), _response(raw))

    message = str(exc.value)
    assert "extra: acnt_no" in message
    assert "length: response cur_prc is 10 chars" in message
    assert "1234567890" not in message and "8888888888" not in message


def test_ignore_lists_are_separate(monkeypatch):
    monkeypatch.setitem(SPEC_LENGTHS, "ka99999", {"request": {}, "response": {"cur_prc": 3}})
    raw = _raw(cur_prc="12345", pipe1="x")
    client, response = _client(raw), _response(raw)

    assert_spec_conformance(client, response, ignore=["pipe1"], ignore_length=["cur_prc"])
    with pytest.raises(AssertionError, match="length: response cur_prc"):
        assert_spec_conformance(client, response, ignore=["pipe1", "cur_prc"])


def test_empty_block_warns():
    raw = _raw(rows=[])
    with pytest.warns(EmptyBlockWarning, match="rows"):
        assert_spec_conformance(_client(raw), _response(raw))


def test_assert_requires_recorded_exchange():
    with pytest.raises(AssertionError, match="record_exchanges"):
        assert_spec_conformance(SimpleNamespace(), _response(_raw()))


def test_record_exchanges_captures_api_id_body_and_raw_json():
    raw = _raw()
    calls = []

    def fake_post(path, headers, body, use_cache=True):
        calls.append((path, use_cache))
        return SimpleNamespace(json=lambda: raw)

    client = record_exchanges(SimpleNamespace(_post=fake_post))
    client._post("/api/dostk/stkinfo", {"api-id": "ka10001"}, {"stk_cd": "005930"}, False)

    assert calls == [("/api/dostk/stkinfo", False)]
    assert client._last_exchange == Exchange("ka10001", {"stk_cd": "005930"}, raw)


def test_record_exchanges_clears_stale_exchange_on_error():
    def failing_post(path, headers, body, use_cache=True):
        raise RuntimeError("boom")

    client = record_exchanges(SimpleNamespace(_post=failing_post))
    client._last_exchange = Exchange("old", {}, {})
    with pytest.raises(RuntimeError):
        client._post("/p", {"api-id": "ka10001"}, {})

    assert client._last_exchange is None


def test_spec_lengths_file_covers_known_tr():
    assert SPEC_LENGTHS["ka10008"]["request"]["stk_cd"] == 20
    assert SPEC_LENGTHS["ka10008"]["response"]["stk_frgnr.dt"] == 20
    assert not any(k.startswith("_") for k in _spec_conformance.SPEC_LENGTHS)
