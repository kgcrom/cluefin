"""미 재무부 금리 XML 피드 — Daily Treasury Par Yield Curve (명목 국채 수익률 곡선)."""

from __future__ import annotations

import re

from defusedxml.ElementTree import ParseError, fromstring

from .._exceptions import FeedParseError
from .._http import HttpClient
from ._types import ParYieldCurveRate

RATES_XML_URL = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml"

# Atom 피드 안 OData 속성: <m:properties><d:NEW_DATE>…</d:NEW_DATE><d:BC_1MONTH>…</d:BC_1MONTH>…
_METADATA_NS = "{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}"
_DATA_NS = "{http://schemas.microsoft.com/ado/2007/08/dataservices}"
_PERIOD = re.compile(r"^\d{4}(\d{2})?$")


class Client:
    """미 재무부 금리 데이터. 키 없이 공개 XML(Atom) 피드를 GET 한다."""

    def __init__(self, http: HttpClient | None = None):
        self.http = http or HttpClient(headers={"Accept": "application/xml"})

    def par_yield_curve(self, period: str) -> list[ParYieldCurveRate]:
        """명목 국채 수익률 곡선을 한 달(`YYYYMM`) 또는 한 해(`YYYY`) 단위로 받는다.

        영업일 오름차순. 아직 자료가 없는 달(달 초·미래)이나 없는 기간은 빈 목록이다 — 서버가 오류 대신 빈 피드를 준다.
        최근 값이 필요하면 이번 달이 비었을 때 지난달을 다시 묻는다.
        """
        if not _PERIOD.match(period):
            raise ValueError(f"period 는 YYYY 또는 YYYYMM 이어야 합니다. 받은 값: {period!r}")
        key = "field_tdr_date_value_month" if len(period) == 6 else "field_tdr_date_value"
        response = self.http.get(RATES_XML_URL, {"data": "daily_treasury_yield_curve", key: period})
        rows = [ParYieldCurveRate.model_validate(props) for props in parse_properties(response.content)]
        return sorted(rows, key=lambda row: row.date)


def parse_properties(payload: bytes) -> list[dict[str, str]]:
    """피드의 `<m:properties>` 마다 {필드명: 텍스트}. 빈 요소(값 없음)는 넣지 않는다."""
    try:
        root = fromstring(payload)
    except ParseError as exc:
        raise FeedParseError("재무부 금리 XML 을 읽지 못했습니다", url=RATES_XML_URL) from exc
    return [_fields(props) for props in root.iter(f"{_METADATA_NS}properties")]


def _fields(props) -> dict[str, str]:
    return {
        child.tag.removeprefix(_DATA_NS): child.text.strip()
        for child in props
        if child.tag.startswith(_DATA_NS) and child.text and child.text.strip()
    }
