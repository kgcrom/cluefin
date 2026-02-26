"""Tests for JSON-RPC 2.0 protocol helpers."""

import json
from io import StringIO
from unittest.mock import patch

import pytest

from cluefin_rpc.protocol import (
    INTERNAL_ERROR,
    INVALID_REQUEST,
    PARSE_ERROR,
    parse_request,
    write_error,
    write_response,
)


class TestWriteResponse:
    def test_basic_response(self):
        buf = StringIO()
        with patch("sys.stdout", buf):
            write_response({"jsonrpc": "2.0", "id": 1, "result": {"status": "ok"}})
        output = buf.getvalue()
        assert output.endswith("\n")
        data = json.loads(output.strip())
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        assert data["result"]["status"] == "ok"

    def test_korean_text(self):
        buf = StringIO()
        with patch("sys.stdout", buf):
            write_response({"jsonrpc": "2.0", "id": 1, "result": {"name": "삼성전자"}})
        output = buf.getvalue()
        assert "삼성전자" in output

    def test_null_id(self):
        buf = StringIO()
        with patch("sys.stdout", buf):
            write_response({"jsonrpc": "2.0", "id": None, "result": None})
        data = json.loads(buf.getvalue().strip())
        assert data["id"] is None


class TestWriteError:
    def test_basic_error(self):
        buf = StringIO()
        with patch("sys.stdout", buf):
            write_error(1, PARSE_ERROR, "Invalid JSON")
        data = json.loads(buf.getvalue().strip())
        assert data["error"]["code"] == PARSE_ERROR
        assert data["error"]["message"] == "Invalid JSON"
        assert "data" not in data["error"]

    def test_error_with_data(self):
        buf = StringIO()
        with patch("sys.stdout", buf):
            write_error(1, INTERNAL_ERROR, "Server error", {"detail": "stack trace"})
        data = json.loads(buf.getvalue().strip())
        assert data["error"]["data"]["detail"] == "stack trace"

    def test_null_request_id(self):
        buf = StringIO()
        with patch("sys.stdout", buf):
            write_error(None, INVALID_REQUEST, "Bad request")
        data = json.loads(buf.getvalue().strip())
        assert data["id"] is None


class TestParseRequest:
    def test_valid_request(self):
        result = parse_request('{"jsonrpc":"2.0","id":1,"method":"rpc.ping","params":{}}')
        assert result["method"] == "rpc.ping"
        assert result["id"] == 1
        assert result["params"] == {}

    def test_valid_notification(self):
        result = parse_request('{"jsonrpc":"2.0","method":"rpc.ping"}')
        assert result["method"] == "rpc.ping"
        assert "id" not in result

    def test_invalid_json(self):
        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_request("not json")

    def test_not_object(self):
        with pytest.raises(ValueError, match="JSON object"):
            parse_request("[1, 2, 3]")

    def test_missing_jsonrpc(self):
        with pytest.raises(ValueError, match="jsonrpc"):
            parse_request('{"id":1,"method":"test"}')

    def test_wrong_jsonrpc_version(self):
        with pytest.raises(ValueError, match="jsonrpc"):
            parse_request('{"jsonrpc":"1.0","id":1,"method":"test"}')

    def test_missing_method(self):
        with pytest.raises(ValueError, match="method"):
            parse_request('{"jsonrpc":"2.0","id":1}')

    def test_method_not_string(self):
        with pytest.raises(ValueError, match="method"):
            parse_request('{"jsonrpc":"2.0","id":1,"method":123}')

    def test_params_invalid_type(self):
        with pytest.raises(ValueError, match="params"):
            parse_request('{"jsonrpc":"2.0","id":1,"method":"test","params":"bad"}')

    def test_params_as_array(self):
        result = parse_request('{"jsonrpc":"2.0","id":1,"method":"test","params":[1,2]}')
        assert result["params"] == [1, 2]
