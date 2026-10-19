import time
from typing import Any, Dict, List, Literal, Optional, Tuple
from urllib.parse import quote

import requests
from loguru import logger

from cluefin_openapi._http_base import BaseHttpClient
from cluefin_openapi._rate_limiter import TokenBucket

from ._exceptions import (
    RETRYABLE_RESULT_CODES,
    EcosAPIError,
    EcosNetworkError,
    EcosNotFoundError,
    EcosRateLimitError,
    EcosServerError,
    EcosTimeoutError,
    raise_for_result,
)

BASE_URL = "https://ecos.bok.or.kr/api"

# 가입 없이 쓰는 공개 시험 키. 한 번에 10행까지지만 쪽 넘김(1/10 → 11/20 …)은 된다.
SAMPLE_AUTH_KEY = "sample"
SAMPLE_PAGE_SIZE = 10
# 문서상 실키 한 번 상한. 실서버는 더 큰 범위도 받지만(2026-10-19 실측) 문서를 따른다.
PAGE_SIZE = 1000

NO_DATA_CODE = "INFO-200"

# 서버는 60초를 넘는 조회를 ERROR-400 으로 끊는다. 클라이언트가 먼저 끊으면 그 답을 못 보고 같은 요청을 재시도한다.
DEFAULT_TIMEOUT = 75

Lang = Literal["kr", "en"]


class Client(BaseHttpClient):
    """한국은행 ECOS Open API 클라이언트.

    인증키는 URL 경로에 들어간다. 그래서 예외·로그의 request_context 에는 URL 대신 키를 가린 경로만 남긴다.
    """

    def __init__(
        self,
        auth_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = 3,
        rate_limit_requests_per_second: float = 5.0,
        rate_limit_burst: int = 5,
        max_pages: int = 100,
    ):
        self.auth_key = auth_key or SAMPLE_AUTH_KEY
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_pages = max_pages
        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json", "User-Agent": "cluefin-openapi/1.0"})
        self._rate_limiter = TokenBucket(capacity=rate_limit_burst, refill_rate=rate_limit_requests_per_second)

    @property
    def is_sample(self) -> bool:
        return self.auth_key == SAMPLE_AUTH_KEY

    @property
    def page_size(self) -> int:
        return SAMPLE_PAGE_SIZE if self.is_sample else PAGE_SIZE

    @property
    def statistic_search(self):
        from ._statistic_search import StatisticSearch

        return StatisticSearch(self)

    @property
    def statistic_catalog(self):
        from ._statistic_catalog import StatisticCatalog

        return StatisticCatalog(self)

    @property
    def statistic_glossary(self):
        from ._statistic_glossary import StatisticGlossary

        return StatisticGlossary(self)

    def _get_page(self, service: str, start_row: int, end_row: int, segments: Tuple[str, ...], lang: Lang) -> Dict:
        """한 쪽을 받아 `{"list_total_count", "row", …}` 를 돌려준다. 데이터 없음(INFO-200)은 빈 쪽."""
        if start_row < 1 or end_row < start_row:
            raise ValueError(f"행 범위는 1 ≤ start_row ≤ end_row 여야 합니다. 받은 값: {start_row}/{end_row}")
        encoded = [_segment(value) for value in segments]
        tail = "/".join([lang, str(start_row), str(end_row), *encoded])
        url = f"{BASE_URL}/{service}/{quote(self.auth_key, safe='')}/json/{tail}"
        request_context = {"method": "GET", "service": service, "path": f"/{service}/***/json/{tail}"}

        body = self._get_body(url, request_context)
        if body is None:
            return {"list_total_count": 0, "row": []}

        page = body.get(service)
        if not isinstance(page, dict):
            raise EcosAPIError(
                f"ECOS 응답에 '{service}' 블록이 없습니다", response_data=body, request_context=request_context
            )
        return page

    def _get_body(self, url: str, request_context: dict) -> Optional[Dict]:
        """본문을 받아 `RESULT` 를 푼다. 데이터 없음이면 None, 일시 오류(600·602)는 HTTP 5xx·429 처럼 재시도한다."""
        for attempt in range(self.max_retries + 1):
            body = self._safe_json(self._request(url, request_context))
            if not isinstance(body, dict):
                raise EcosAPIError("ECOS 응답이 JSON 객체가 아닙니다", status_code=200, request_context=request_context)
            result = body.get("RESULT")
            if not isinstance(result, dict):
                return body
            code = str(result.get("CODE") or "")
            if code == NO_DATA_CODE:
                return None
            if code in RETRYABLE_RESULT_CODES and attempt < self.max_retries:
                wait_time = 2**attempt
                logger.warning(f"ECOS {code}, retrying in {wait_time}s ({attempt + 1}/{self.max_retries})")
                time.sleep(wait_time)
                continue
            raise_for_result(code, str(result.get("MESSAGE") or ""), body, request_context)
        raise EcosAPIError("ECOS 재시도 횟수를 넘겼습니다", request_context=request_context)

    def _get_rows(
        self,
        service: str,
        segments: Tuple[str, ...],
        lang: Lang,
        start_row: Optional[int] = None,
        end_row: Optional[int] = None,
    ) -> Tuple[int, List[Dict[str, Any]], Optional[int]]:
        """(list_total_count, 행 목록, row_count)를 돌려준다.

        행 범위를 주면 그 쪽만, 안 주면 `list_total_count` 를 다 채울 때까지 쪽 넘김한다.
        """
        if start_row is not None or end_row is not None:
            first = start_row or 1
            page = self._get_page(service, first, end_row or first + self.page_size - 1, segments, lang)
            return int(page.get("list_total_count") or 0), list(page.get("row") or []), page.get("row_count")

        rows: List[Dict[str, Any]] = []
        total = 0
        for index in range(self.max_pages):
            first = index * self.page_size + 1
            page = self._get_page(service, first, first + self.page_size - 1, segments, lang)
            total = int(page.get("list_total_count") or 0)
            batch = list(page.get("row") or [])
            rows.extend(batch)
            if not batch or len(rows) >= total:
                return total, rows, None
        raise EcosAPIError(
            f"쪽 넘김 상한({self.max_pages}쪽 × {self.page_size}행)에 닿았습니다. 전체 {total}행 중 {len(rows)}행만 받았습니다. "
            "기간·항목을 좁히거나 실키(ECOS_AUTH_KEY)를 쓰세요."
        )

    def _dispatch_ecos(self, response: requests.Response, request_context: dict) -> Optional[Exception]:
        """Map a non-200 HTTP response to the appropriate ECOS exception."""
        common = {"status_code": response.status_code, "response_data": None, "request_context": request_context}
        if response.status_code == 404:
            return EcosNotFoundError("ECOS 서비스를 찾을 수 없습니다 (HTTP 404)", **common)
        if response.status_code == 429:
            return EcosRateLimitError(f"Rate limit exceeded after {self.max_retries} retries", **common)
        if 500 <= response.status_code < 600:
            return EcosServerError(f"Server error: {response.status_code}", **common)
        return EcosAPIError(f"Unexpected status code: {response.status_code}", **common)

    def _request(self, url: str, request_context: dict) -> requests.Response:
        try:
            return self._execute_with_retry(
                send_fn=lambda: self._session.get(url, timeout=self.timeout),
                rate_limiter=self._rate_limiter,
                timeout=self.timeout,
                max_retries=self.max_retries,
                request_context=request_context,
                dispatch=lambda resp: self._dispatch_ecos(resp, request_context),
                rate_limit_error=lambda: EcosRateLimitError(
                    "Rate limit timeout - could not acquire token within timeout period",
                    request_context=request_context,
                ),
                timeout_error_cls=EcosTimeoutError,
                network_error_cls=EcosNetworkError,
            )
        except (EcosNetworkError, EcosTimeoutError) as e:
            # requests 의 연결 오류 메시지에는 키가 든 URL 이 그대로 실린다. 가리고, 원인 체인도 끊는다.
            raise type(e)(e.message.replace(self.auth_key, "***"), request_context=request_context) from None

    def close(self):
        """Close the HTTP session."""
        if hasattr(self, "_session"):
            self._session.close()


def _segment(value: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError("ECOS 요청 경로에 빈 값을 넣을 수 없습니다")
    return quote(text, safe="")
