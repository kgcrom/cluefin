"""Tests for extract_output() and extract_body() helpers in _base.py."""

from __future__ import annotations

from cluefin_rpc.handlers._base import extract_body, extract_output

# ---------------------------------------------------------------------------
# Fake helpers – avoid MagicMock which pollutes hasattr()
# ---------------------------------------------------------------------------


class FakeModel:
    """Mimics a Pydantic model with model_dump()."""

    def __init__(self, data: dict):
        self._data = data

    def model_dump(self) -> dict:
        return self._data


class FakeResponse:
    """Wraps a body object to look like an API response."""

    def __init__(self, body):
        self.body = body


# ---------------------------------------------------------------------------
# TestExtractOutput
# ---------------------------------------------------------------------------


class TestExtractOutput:
    def test_none_field_returns_none(self):
        body = type("B", (), {"output": None})()
        resp = FakeResponse(body)
        assert extract_output(resp) is None

    def test_missing_field_returns_none(self):
        body = type("B", (), {})()
        resp = FakeResponse(body)
        assert extract_output(resp) is None

    def test_single_pydantic_model(self):
        model = FakeModel({"price": 100, "volume": 5000})
        body = type("B", (), {"output": model})()
        resp = FakeResponse(body)
        result = extract_output(resp)
        assert result == {"price": 100, "volume": 5000}

    def test_single_plain_dict(self):
        plain = {"key": "value"}
        body = type("B", (), {"output": plain})()
        resp = FakeResponse(body)
        result = extract_output(resp)
        assert result is plain  # returned as-is

    def test_list_of_pydantic_models(self):
        models = [FakeModel({"a": 1}), FakeModel({"a": 2})]
        body = type("B", (), {"output": models})()
        resp = FakeResponse(body)
        result = extract_output(resp)
        assert result == [{"a": 1}, {"a": 2}]

    def test_empty_list(self):
        body = type("B", (), {"output": []})()
        resp = FakeResponse(body)
        result = extract_output(resp)
        assert result == []

    def test_tuple_of_models(self):
        models = (FakeModel({"x": 10}), FakeModel({"x": 20}))
        body = type("B", (), {"output": models})()
        resp = FakeResponse(body)
        result = extract_output(resp)
        assert result == [{"x": 10}, {"x": 20}]

    def test_list_of_plain_dicts(self):
        items = [{"k": 1}, {"k": 2}]
        body = type("B", (), {"output": items})()
        resp = FakeResponse(body)
        result = extract_output(resp)
        assert result == [{"k": 1}, {"k": 2}]

    def test_custom_field_name(self):
        model = FakeModel({"val": 42})
        body = type("B", (), {"output2": model})()
        resp = FakeResponse(body)
        result = extract_output(resp, field="output2")
        assert result == {"val": 42}

    def test_custom_field_missing_returns_none(self):
        body = type("B", (), {"output": FakeModel({"a": 1})})()
        resp = FakeResponse(body)
        assert extract_output(resp, field="output3") is None


# ---------------------------------------------------------------------------
# TestExtractBody
# ---------------------------------------------------------------------------


class TestExtractBody:
    def test_body_with_model_dump(self):
        body = FakeModel({"foo": "bar", "count": 3})
        resp = FakeResponse(body)
        assert extract_body(resp) == {"foo": "bar", "count": 3}

    def test_body_without_model_dump(self):
        body = {"raw": True}  # plain dict, no model_dump attribute
        resp = FakeResponse(body)
        assert extract_body(resp) == {}

    def test_nested_data(self):
        body = FakeModel({"items": [{"id": 1}, {"id": 2}], "meta": {"page": 1}})
        resp = FakeResponse(body)
        result = extract_body(resp)
        assert result == {"items": [{"id": 1}, {"id": 2}], "meta": {"page": 1}}
