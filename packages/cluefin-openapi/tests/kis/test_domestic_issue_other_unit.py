import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from cluefin_openapi.kis import _domestic_issue_other as domestic_issue_other_module
from cluefin_openapi.kis._domestic_issue_other import DomesticIssueOther


def load_domestic_issue_other_cases():
    path = Path(__file__).with_name("domestic_issue_other_cases.json")
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


DOMESTIC_ISSUE_OTHER_CASES = load_domestic_issue_other_cases()


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
    DOMESTIC_ISSUE_OTHER_CASES,
)
def test_domestic_issue_other_builds_request(
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

    monkeypatch.setattr(domestic_issue_other_module, response_model_attr, DummyResponseModel)

    issue_other = DomesticIssueOther(client)
    result = getattr(issue_other, method_name)(**call_kwargs)

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
    assert result is captured_instances[0]
    assert captured_instances[0].kwargs == response_payload
