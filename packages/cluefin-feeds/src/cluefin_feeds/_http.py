"""피드 공용 HTTP 도우미: 호출 간격 유지, 429·5xx·타임아웃·연결 오류 재시도, 예외 변환.

피드는 하루 몇 번 부르는 정도라 브로커 클라이언트의 토큰 버킷 대신 최소 호출 간격만 둔다.
"""

import threading
import time
from typing import Any, Dict, Optional

import requests

from ._exceptions import (
    FeedClientError,
    FeedError,
    FeedNetworkError,
    FeedRateLimitError,
    FeedServerError,
    FeedTimeoutError,
)

USER_AGENT = "cluefin-feeds/0.1 (+https://github.com/kgcrom/cluefin)"


class HttpClient:
    def __init__(
        self,
        *,
        timeout: float = 30,
        max_retries: int = 3,
        min_interval: float = 0.5,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.min_interval = min_interval
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": USER_AGENT, **(headers or {})})
        self._lock = threading.Lock()
        self._last_sent = 0.0

    def get(self, url: str, params: Optional[Dict[str, str]] = None) -> requests.Response:
        return self._send("GET", url, params=params)

    def post_json(self, url: str, body: Dict[str, Any]) -> requests.Response:
        return self._send("POST", url, json=body)

    def close(self) -> None:
        self._session.close()

    def _send(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        for attempt in range(self.max_retries + 1):
            last = attempt == self.max_retries
            self._throttle()
            try:
                response = self._session.request(method, url, timeout=self.timeout, **kwargs)
            except requests.exceptions.Timeout:
                if last:
                    raise FeedTimeoutError(f"요청 시간 초과 ({self.max_retries}회 재시도)", url=url) from None
                time.sleep(2**attempt)
                continue
            except requests.exceptions.ConnectionError as e:
                if last:
                    raise FeedNetworkError(f"연결 실패: {e}", url=url) from None
                time.sleep(2**attempt)
                continue
            except requests.exceptions.RequestException as e:
                raise FeedNetworkError(f"요청 실패: {e}", url=url) from None

            status = response.status_code
            if status == 200:
                return response
            retryable = status == 429 or 500 <= status < 600
            if retryable and not last:
                time.sleep(_retry_after(response) or 2**attempt)
                continue
            raise _http_error(status, url)
        raise FeedNetworkError("요청 실패: 재시도 한도 초과", url=url)  # pragma: no cover - 루프가 항상 반환·예외

    def _throttle(self) -> None:
        with self._lock:
            wait = self._last_sent + self.min_interval - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last_sent = time.monotonic()


def _retry_after(response: requests.Response) -> Optional[int]:
    value = response.headers.get("Retry-After", "")
    return int(value) if value.isdigit() else None


def _http_error(status: int, url: str) -> FeedError:
    if status == 429:
        return FeedRateLimitError("요청 한도 초과", status_code=status, url=url)
    if 500 <= status < 600:
        return FeedServerError("서버 오류", status_code=status, url=url)
    if 400 <= status < 500:
        return FeedClientError("요청 오류", status_code=status, url=url)
    return FeedError(f"예상하지 못한 HTTP 상태 {status}", status_code=status, url=url)
