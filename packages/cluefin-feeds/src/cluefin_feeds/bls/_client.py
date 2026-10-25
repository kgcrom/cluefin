"""BLS Public Data API — 시계열 조회 (POST /timeseries/data/)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from .._exceptions import FeedError, FeedParseError, FeedRateLimitError
from .._http import HttpClient
from ._types import BlsObservation, BlsResponse, BlsSeries

API_URL_V1 = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
API_URL_V2 = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# BLS FAQ: 키 없으면(v1) 한 번에 25시리즈·10년·하루 25회, 등록 키(v2)면 50시리즈·20년·하루 500회.
V1_LIMITS = (25, 10)
V2_LIMITS = (50, 20)

SUCCEEDED = "REQUEST_SUCCEEDED"
# 하루 한도 초과 상태 (문서상 — 실측 전)
NOT_PROCESSED = "REQUEST_NOT_PROCESSED"


class BlsAPIError(FeedError):
    """본문 status 가 REQUEST_SUCCEEDED 가 아닐 때 (HTTP 는 200). `status`·`messages` 에 서버 응답."""

    def __init__(self, message: str, status: str, messages: list[str], url: str | None = None):
        super().__init__(message, url=url)
        self.status = status
        self.messages = messages


class BlsDailyLimitError(FeedRateLimitError):
    """REQUEST_NOT_PROCESSED — 하루 호출 한도를 넘었다. 등록 키(v2)는 하루 500회."""


class Client:
    """미 노동통계국(BLS) 시계열. 키 없이 v1, 등록 키가 있으면 v2 로 보낸다."""

    def __init__(self, registration_key: str | None = None, http: HttpClient | None = None):
        self.registration_key = registration_key or None
        self.http = http or HttpClient()

    @property
    def limits(self) -> tuple[int, int]:
        """(한 번에 시리즈 수, 한 번에 연도 수)"""
        return V2_LIMITS if self.registration_key else V1_LIMITS

    def timeseries(
        self,
        series_ids: Sequence[str],
        start_year: int | None = None,
        end_year: int | None = None,
        *,
        annual_average: bool = False,
    ) -> BlsResponse:
        """시계열 값을 받는다. 시점 오름차순.

        Args:
            series_ids: 시리즈 ID (예: `CUUR0000SA0` CPI-U 전 품목). 한도를 넘으면 나눠 보낸다
            start_year, end_year: 둘 다 주거나 둘 다 생략. 생략하면 서버가 최근 3년을 준다.
                한 번 한도(키 없으면 10년)를 넘는 구간은 나눠 보낸다 — 서버는 넘치는 구간을 **앞쪽 10년만** 남기고
                경고 메시지만 붙이므로, 나누지 않으면 최근 값이 조용히 빠진다(2026-10-19 실측)
            annual_average: 연평균 M13 행을 함께 받는다

        호출 수 = 시리즈 묶음 수 × 연도 구간 수. 키 없이 하루 25회라 긴 구간은 등록 키(`BLS_REGISTRATION_KEY`)가 낫다.
        """
        ids = [s.strip() for s in series_ids if s and s.strip()]
        if not ids:
            raise ValueError("series_ids 가 비었습니다")
        if (start_year is None) != (end_year is None):
            raise ValueError("start_year 와 end_year 는 함께 주거나 함께 생략합니다")
        if start_year is not None and end_year is not None and start_year > end_year:
            raise ValueError(f"start_year({start_year}) 가 end_year({end_year}) 보다 큽니다")

        max_series, max_years = self.limits
        merged: dict[str, list[BlsObservation]] = {series_id: [] for series_id in ids}
        messages: list[str] = []
        for batch in _chunks(ids, max_series):
            for years in _year_windows(start_year, end_year, max_years):
                payload = self._post(batch, years, annual_average)
                messages.extend(m for m in payload.get("message") or [] if m not in messages)
                for series in _series_of(payload):
                    merged.setdefault(series.series_id, []).extend(series.data)

        return BlsResponse(
            series=[BlsSeries(series_id=sid, data=_sorted_unique(rows)) for sid, rows in merged.items()],
            messages=messages,
        )

    def _post(self, series_ids: list[str], years: tuple[int, int] | None, annual_average: bool) -> dict[str, Any]:
        body: dict[str, Any] = {"seriesid": series_ids}
        if years:
            body["startyear"], body["endyear"] = str(years[0]), str(years[1])
        if annual_average:
            body["annualaverage"] = True
        if self.registration_key:
            body["registrationkey"] = self.registration_key
        url = API_URL_V2 if self.registration_key else API_URL_V1

        response = self.http.post_json(url, body)
        try:
            payload = response.json()
        except ValueError as exc:
            raise FeedParseError("BLS 응답이 JSON 이 아닙니다", url=url) from exc
        if not isinstance(payload, dict):
            raise FeedParseError("BLS 응답이 JSON 객체가 아닙니다", url=url)

        status = str(payload.get("status") or "")
        if status == SUCCEEDED:
            return payload
        messages = [str(m) for m in payload.get("message") or []]
        text = "; ".join(messages) or status
        if status == NOT_PROCESSED:
            raise BlsDailyLimitError(f"BLS 하루 호출 한도: {text}", url=url)
        raise BlsAPIError(f"BLS 요청 실패 ({status}): {text}", status=status, messages=messages, url=url)


def _chunks(items: list[str], size: int) -> Iterator[list[str]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def _year_windows(start: int | None, end: int | None, size: int) -> Iterator[tuple[int, int] | None]:
    if start is None or end is None:
        yield None
        return
    for first in range(start, end + 1, size):
        yield first, min(first + size - 1, end)


def _series_of(payload: dict[str, Any]) -> list[BlsSeries]:
    results = payload.get("Results") or {}
    return [BlsSeries.model_validate(raw) for raw in results.get("series") or []]


def _sorted_unique(rows: list[BlsObservation]) -> list[BlsObservation]:
    by_key = {(row.year, row.period): row for row in rows}
    return [by_key[key] for key in sorted(by_key)]
