import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from cluefin_openapi.kis import _onmarket_bond_basic_quote as onmarket_bond_basic_quote_module
from cluefin_openapi.kis._onmarket_bond_basic_quote import OnmarketBondBasicQuote


def load_onmarket_bond_basic_quote_cases():
    path = Path(__file__).with_name("onmarket_bond_basic_quote_cases.json")
    with path.open(encoding="utf-8") as case_file:
        raw_cases = json.load(case_file)

    return [
        (
            case["method_name"],
            case["response_model_attr"],
            case["endpoint"],
            case["method"],
            case["call_kwargs"],
            case["expected_headers"],
            case["expected_body"],
            case["response_payload"],
        )
        for case in raw_cases
    ]


ONMARKET_BOND_BASIC_QUOTE_CASES = load_onmarket_bond_basic_quote_cases()


@pytest.mark.parametrize(
    (
        "method_name",
        "response_model_attr",
        "endpoint",
        "method",
        "call_kwargs",
        "expected_headers",
        "expected_body",
        "response_payload",
    ),
    ONMARKET_BOND_BASIC_QUOTE_CASES,
)
def test_onmarket_bond_basic_quote_builds_request(
    monkeypatch,
    method_name,
    response_model_attr,
    endpoint,
    method,
    call_kwargs,
    expected_headers,
    expected_body,
    response_payload,
):
    # Mock response object with json() method
    mock_response = Mock()
    mock_response.json.return_value = response_payload
    mock_response.status_code = 200
    mock_response.text = ""
    mock_response.headers = {
        "content-type": "application/json; charset=utf-8",
        "tr_id": expected_headers.get("tr_id", ""),
        "tr_cont": expected_headers.get("tr_cont", ""),
        "gt_uid": None,
    }

    client = Mock()
    client._post.return_value = mock_response
    client._get.return_value = mock_response
    captured_instances = []

    class DummyResponseModel:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            captured_instances.append(self)

        @classmethod
        def model_validate(cls, data):
            return cls(**data)

    monkeypatch.setattr(onmarket_bond_basic_quote_module, response_model_attr, DummyResponseModel)

    basic_quote = OnmarketBondBasicQuote(client)
    result = getattr(basic_quote, method_name)(**call_kwargs)

    if method == "POST":
        client._post.assert_called_once_with(
            endpoint,
            headers=expected_headers,
            body=expected_body,
        )
    else:
        client._get.assert_called_once_with(
            endpoint,
            headers=expected_headers,
            params=expected_body,
        )

    assert len(captured_instances) == 1
    assert result.body is captured_instances[0]
    assert captured_instances[0].kwargs == response_payload
