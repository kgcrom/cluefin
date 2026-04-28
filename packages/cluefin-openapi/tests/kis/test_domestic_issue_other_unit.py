import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from cluefin_openapi.kis import _domestic_issue_other as domestic_issue_other_module
from cluefin_openapi.kis._domestic_issue_other import DomesticIssueOther
from cluefin_openapi.kis._domestic_issue_other_types import InterestRateSummary


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
    assert result.body is captured_instances[0]
    assert captured_instances[0].kwargs == response_payload


def test_interest_rate_summary_accepts_live_output2_shape():
    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": [],
        "output2": [
            {
                "bcdt_code": "Y0102",
                "hts_kor_isnm": "Y0110",
                "bond_mnrt_prpr": "Y0198",
                "prdy_vrss_sign": "Call 지수",
                "bond_mnrt_prdy_vrss": "202.0567",
                "bstp_nmix_prdy_ctrt": "2",
            }
        ],
    }

    body = InterestRateSummary.model_validate(payload)

    assert body.output2[0].prdy_vrss_sign == "Call 지수"
    assert body.output2[0].stck_bsop_date == ""
