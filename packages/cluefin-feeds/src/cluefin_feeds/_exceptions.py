"""cluefin-feeds 공통 예외. 공급처별 예외(예: BLS 본문 status 실패)는 FeedError 를 상속한다."""

from typing import Optional


class FeedError(Exception):
    """Base exception for every feed."""

    def __init__(self, message: str, status_code: Optional[int] = None, url: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.url = url

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class FeedClientError(FeedError):
    """4xx (429 제외). 다시 보내도 같다."""


class FeedRateLimitError(FeedError):
    """429 가 재시도 뒤에도 계속될 때."""


class FeedServerError(FeedError):
    """5xx 가 재시도 뒤에도 계속될 때."""


class FeedTimeoutError(FeedError):
    """요청 시간 초과가 재시도 뒤에도 계속될 때."""


class FeedNetworkError(FeedError):
    """연결 실패 등 응답을 받지 못했을 때."""


class FeedParseError(FeedError):
    """응답은 왔는데 기대한 형식(XML·JSON·HTML 표·xls)이 아닐 때."""
