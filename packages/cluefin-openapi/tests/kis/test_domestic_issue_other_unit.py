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


def test_interest_rate_summary_parses_domestic_and_foreign_rows():
    """div_cls_code="2" 의 output1 에는 국내(Y01xx)와 해외(Y02xx)가 함께 온다 (2026-09-20 실측)."""
    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": [
            {
                "bcdt_code": "Y0106",
                "hts_kor_isnm": "국고채 10년",
                "bond_mnrt_prpr": "4.4660",
                "prdy_vrss_sign": "5",
                "bond_mnrt_prdy_vrss": "-0.0400",
                "prdy_ctrt": "-0.89",
                "stck_bsop_date": "20260918",
            },
            {
                "bcdt_code": "Y0202",
                "hts_kor_isnm": "미국 10년T-NOTE 수익률",
                "bond_mnrt_prpr": "5.0100",
                "prdy_vrss_sign": "2",
                "bond_mnrt_prdy_vrss": "0.0700",
                "prdy_ctrt": "1.42",
                "stck_bsop_date": "20260918",
            },
        ],
        "output2": [],
    }

    body = InterestRateSummary.model_validate(payload)

    assert [item.bcdt_code for item in body.output1] == ["Y0106", "Y0202"]
    assert body.output1[0].hts_kor_isnm == "국고채 10년"


def test_interest_rate_summary_accepts_degraded_output2_rows():
    """div_cls_code="1" 의 output2 앞부분은 KIS 가 필드를 밀어 보내고 날짜도 빠뜨린다.

    모델은 이 응답을 거부하지 않아야 한다(전체 응답이 통째로 날아가므로). 밀린 행을
    걸러내는 것은 읽는 쪽의 몫이다 — cluefin-openapi-cli 의 market.interest_rate 핸들러.
    """
    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": [],
        "output2": [
            {
                "bcdt_code": "Y0101",
                "hts_kor_isnm": "Y0109",
                "bond_mnrt_prpr": "Y0117",
                "prdy_vrss_sign": "국고채 30년",
                "bond_mnrt_prdy_vrss": "4.5730",
                "bstp_nmix_prdy_ctrt": "5",
                "stck_bsop_date": "-0.0340",
            },
            {
                "bcdt_code": "Y0110",
                "hts_kor_isnm": "Y0198",
                "bond_mnrt_prpr": "Call 지수",
                "prdy_vrss_sign": "204.2551",
                "bond_mnrt_prdy_vrss": "2",
                "bstp_nmix_prdy_ctrt": "0.0346",
            },
        ],
    }

    body = InterestRateSummary.model_validate(payload)

    assert body.output2[0].hts_kor_isnm == "Y0109"
    assert body.output2[1].stck_bsop_date == ""
