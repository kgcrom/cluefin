"""Shared parametrized-case runner for KIS unit tests.

KIS unit tests use JSON fixture case files (`tests/kis/*_cases.json`) instead of
Kiwoom's `EndpointCase`/`run_post_case` table-driven harness
(`tests/kiwoom/_helpers.py`). Each case describes one wrapper-method call: the
endpoint/method/headers/body it should build against a mocked `HttpClient`, and
the raw response payload the (monkeypatched) response model should be handed.

This module factors out the ~60-line runner that used to be duplicated verbatim
across most `tests/kis/test_*_unit.py` files. Each test file keeps its own case
loading + parametrize + any file-specific tests; only the body of the
`test_*_builds_request` function is shared here.
"""

import json
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import Mock

from cluefin_openapi.kis._model import KisHttpResponse

CASE_FIELDS = (
    "method_name",
    "response_model_attr",
    "endpoint",
    "method",
    "call_kwargs",
    "expected_headers",
    "expected_body",
    "response_payload",
)


def load_cases(case_file_name: str, *, relative_to: str) -> list[tuple]:
    """Load parametrize-ready tuples from a `tests/kis/*_cases.json` file.

    `relative_to` is the calling test module's `__file__`, so each case file is
    still resolved next to the test module that uses it.
    """
    path = Path(relative_to).with_name(case_file_name)
    with path.open(encoding="utf-8") as case_file:
        raw_cases = json.load(case_file)

    return [tuple(case[field] for field in CASE_FIELDS) for case in raw_cases]


def run_case(
    *,
    module: ModuleType,
    wrapper_cls: type,
    monkeypatch: Any,
    method_name: str,
    response_model_attr: str,
    endpoint: str,
    method: str,
    call_kwargs: dict,
    expected_headers: dict,
    expected_body: dict,
    response_payload: dict,
) -> None:
    """Build `wrapper_cls(client)`, call `method_name`, and assert the HTTP call + result.

    The real response model named by `response_model_attr` on `module` is
    monkeypatched with a dummy that just records the kwargs it was validated
    with, so this only exercises request-building — not response-model parsing.
    """
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
    captured_instances: list = []

    class DummyResponseModel:
        def __init__(self, **kwargs: Any) -> None:
            self.kwargs = kwargs
            captured_instances.append(self)

        @classmethod
        def model_validate(cls, data):
            return cls(**data)

    monkeypatch.setattr(module, response_model_attr, DummyResponseModel)

    instance = wrapper_cls(client)
    result = getattr(instance, method_name)(**call_kwargs)

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
    assert isinstance(result, KisHttpResponse)
    assert result.body is captured_instances[0]
    assert captured_instances[0].kwargs == response_payload
