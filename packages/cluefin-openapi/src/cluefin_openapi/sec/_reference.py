"""회사 참조 데이터 (티커 ↔ CIK)."""

from __future__ import annotations

from typing import List, Optional

from ._client import WWW_BASE_URL, Client
from ._reference_types import CompanyTicker, CompanyTickerExchange

TICKERS_URL = f"{WWW_BASE_URL}/files/company_tickers.json"
TICKERS_EXCHANGE_URL = f"{WWW_BASE_URL}/files/company_tickers_exchange.json"


class Reference:
    """SEC 회사 참조 파일"""

    def __init__(self, client: Client):
        self.client = client

    def company_tickers(self) -> List[CompanyTicker]:
        """티커·CIK·회사명 전체 목록 (`company_tickers.json`, 약 1만 행).

        응답은 `{"0": {...}, "1": {...}}` 처럼 순번을 키로 쓰는 객체라 값만 순서대로 꺼낸다.
        """
        payload = self.client._get_json(TICKERS_URL)
        if not isinstance(payload, dict):
            raise TypeError(f"company_tickers.json 응답은 객체여야 합니다. 수신한 타입: {type(payload)!r}")
        return [CompanyTicker.model_validate(row) for row in payload.values()]

    def company_tickers_exchange(self) -> List[CompanyTickerExchange]:
        """티커·CIK·회사명·거래소 전체 목록 (`company_tickers_exchange.json`).

        응답은 `{"fields": [...], "data": [[...], ...]}` 열 이름 + 행 배열 형태다.
        """
        payload = self.client._get_json(TICKERS_EXCHANGE_URL)
        if not isinstance(payload, dict):
            raise TypeError(f"company_tickers_exchange.json 응답은 객체여야 합니다. 수신한 타입: {type(payload)!r}")
        fields = payload.get("fields") or []
        return [CompanyTickerExchange.model_validate(dict(zip(fields, row, strict=True))) for row in payload["data"]]

    def ticker_to_cik(self, ticker: str) -> Optional[int]:
        """티커로 CIK를 찾는다. 없으면 None.

        대소문자를 가리지 않고, `BRK.B`처럼 점을 쓴 클래스 티커는 SEC 표기(`BRK-B`)로 바꿔 찾는다.
        호출할 때마다 전체 목록을 받으므로, 여러 종목을 찾을 때는 `company_tickers()`를 한 번 받아 쓴다.
        """
        wanted = ticker.strip().upper().replace(".", "-")
        return next((row.cik for row in self.company_tickers() if row.ticker.upper() == wanted), None)
