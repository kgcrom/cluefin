import json
from collections.abc import Sequence
from types import SimpleNamespace
from typing import Optional

import pytest
from pydantic import AliasChoices, BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody

from ._response_shape import assert_response_shape, response_shape_diff


class Row(BaseModel):
    code: str
    name: str = Field(validation_alias=AliasChoices("name", "knam"))


class Summary(BaseModel):
    total: str


class Body(BaseModel, KisHttpBody):
    output1: Sequence[Row] = Field(default_factory=list)
    output2: Optional[Summary] = None


def _raw(**overrides):
    raw = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "ok",
        "output1": [{"code": "005930", "name": "삼성전자"}],
        "output2": {"total": "1"},
    }
    raw.update(overrides)
    return raw


def test_exact_match_has_no_problems():
    assert response_shape_diff(_raw(), Body) == []


def test_alias_choice_counts_as_present():
    assert response_shape_diff(_raw(output1=[{"code": "005930", "knam": "삼성전자"}]), Body) == []


def test_misnamed_block_reports_missing_and_extra():
    raw = _raw()
    raw["output"] = raw.pop("output1")

    assert response_shape_diff(raw, Body) == [
        "missing: output1 (model declares it, server did not send it)",
        "extra: output (server sent it, model does not declare it)",
    ]


def test_array_object_mismatch_is_reported():
    problems = response_shape_diff(_raw(output2=[{"total": "1"}]), Body)

    assert problems == ["kind: output2 is array on the server, model expects object"]


def test_nested_keys_are_compared_over_all_rows():
    raw = _raw(output1=[{"code": "1", "name": "a"}, {"code": "2", "name": "b", "apprch_rate": "0"}])

    assert response_shape_diff(raw, Body) == ["extra: output1.apprch_rate (server sent it, model does not declare it)"]


def test_nested_missing_key_is_reported():
    problems = response_shape_diff(_raw(output1=[{"code": "1"}]), Body)

    assert problems == ["missing: output1.name (model declares it, server did not send it)"]


def test_empty_array_skips_item_keys():
    assert response_shape_diff(_raw(output1=[]), Body) == []


def _client_with_artifact(tmp_path, raw):
    artifact = tmp_path / "artifact.json"
    artifact.write_text(json.dumps({"request": {}, "response": {"body": raw}}), encoding="utf-8")
    return SimpleNamespace(last_response_debug={"artifact_path": str(artifact)})


def test_assert_response_shape_reads_last_artifact(tmp_path):
    raw = _raw()
    client = _client_with_artifact(tmp_path, raw)
    response = SimpleNamespace(body=Body.model_validate(raw))

    assert_response_shape(client, response)


def test_assert_response_shape_fails_with_every_problem(tmp_path):
    raw = _raw(output1=[{"code": "1", "name": "a", "extra_a": "x"}], extra_b="y")
    client = _client_with_artifact(tmp_path, raw)
    response = SimpleNamespace(body=Body.model_validate(raw))

    with pytest.raises(AssertionError) as exc:
        assert_response_shape(client, response)

    assert "output1.extra_a" in str(exc.value)
    assert "extra_b" in str(exc.value)


def test_assert_response_shape_ignores_listed_paths(tmp_path):
    raw = _raw(output1=[{"code": "1", "name": "a", "extra_a": "x"}])
    client = _client_with_artifact(tmp_path, raw)
    response = SimpleNamespace(body=Body.model_validate(raw))

    assert_response_shape(client, response, ignore=["output1.extra_a"])


def test_assert_response_shape_requires_artifact():
    client = SimpleNamespace(last_response_debug=None)
    response = SimpleNamespace(body=Body.model_validate(_raw()))

    with pytest.raises(AssertionError, match="no KIS debug artifact"):
        assert_response_shape(client, response)
