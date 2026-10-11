"""DartResult 페이지 숫자 변환과 DartHttpBody.parse 의 입력 형태 처리."""

import pytest
from pydantic import BaseModel, ValidationError

from cluefin_openapi.dart._model import DartHttpBody, DartResult


class _SampleItem(BaseModel):
    name: str


def _result(**pagination) -> DartResult[_SampleItem]:
    return DartResult[_SampleItem].model_validate({"status": "000", "message": "정상", **pagination})


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("12", 12),
        (" 7 ", 7),
        (3, 3),
        (4.0, 4),
        ("", None),
        ("   ", None),
        (None, None),
    ],
)
def test_pagination_numbers_are_coerced_to_int(raw, expected):
    result = _result(page_no=raw, page_count=raw, total_count=raw, total_page=raw)

    assert result.page_no == expected
    assert result.page_count == expected
    assert result.total_count == expected
    assert result.total_page == expected


def test_non_numeric_pagination_string_is_rejected():
    with pytest.raises(ValidationError, match="Cannot convert 'abc' to int"):
        _result(page_no="abc")


def test_parse_reads_result_key():
    payload = {"result": {"status": "000", "message": "정상", "total_count": "1", "list": [{"name": "a"}]}}

    body = DartHttpBody.parse(payload, list_model=_SampleItem)

    assert body.result.total_count == 1
    assert body.result.list == [_SampleItem(name="a")]


def test_parse_falls_back_to_top_level_payload():
    payload = {"status": "000", "message": "정상", "list": [{"name": "b"}]}

    body = DartHttpBody.parse(payload, list_model=_SampleItem)

    assert body.result.list == [_SampleItem(name="b")]


@pytest.mark.parametrize("raw_result", [[{"name": "a"}], "error", None])
def test_parse_rejects_non_mapping_result(raw_result):
    with pytest.raises(TypeError, match="does not contain a mapping"):
        DartHttpBody.parse({"result": raw_result}, list_model=_SampleItem)
