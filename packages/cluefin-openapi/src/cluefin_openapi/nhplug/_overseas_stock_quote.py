from typing import Optional

from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import NHPlugHttpHeader, NHPlugHttpResponse
from cluefin_openapi.nhplug._overseas_stock_quote_types import (
    OverseasStockCurrentPrice,
    OverseasStockExecutionTrend,
    OverseasStockPeriodPrice,
)
from cluefin_openapi.nhplug._response import check_response_error


class OverseasStockQuote:
    """해외주식 시세 (gbstock quote).

    스펙 정본: https://www.nhplug.com/openapi-docs/gbstock/openapi.json
    """

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        check_response_error(response_data)

    def get_current_price(
        self,
        iem_cd: str,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockCurrentPrice]:
        """해외주식 현재가상세 (`POST /gbstock/quote/v1/current`).

        해외주식 현재가를 조회하는 API 이다. 응답 블록은 데이터가 있을 때만
        내려오므로 존재 여부를 먼저 확인해야 한다.

        Args:
            iem_cd: 종목코드 (길이 15). 예: 미국주식 APPLE인 경우 AAPL
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockCurrentPrice]: 현재가상세 조회 결과(`Output_0`)
        """
        body: dict = {
            "iem_cd": iem_cd,
        }

        response = self.client.post("/gbstock/quote/v1/current", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockCurrentPrice.model_validate(data))

    def get_execution_trend(
        self,
        period_type: str,
        req_cnt: int,
        iem_cd: str,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockExecutionTrend]:
        """해외주식 체결추이 (`POST /gbstock/quote/v1/executionTrend`).

        해외주식 변동거래량을 조회하는 API 이다. 응답 블록은 데이터가 있을 때만
        내려오므로 존재 여부를 먼저 확인해야 한다.

        시세 API 는 모의투자(moapi) 미지원 — 운영 도메인 전용 (실측 IGW40019).

        Args:
            period_type: 기간구분 (길이 1). 1.시간별 2.일별
            req_cnt: 요청건수 (길이 4)
            iem_cd: 종목코드 (길이 15). 예: 미국주식 APPLE인 경우 AAPL
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockExecutionTrend]: 체결추이 조회 결과(`Output_0`)
        """
        body: dict = {
            "period_type": period_type,
            "req_cnt": req_cnt,
            "iem_cd": iem_cd,
        }

        response = self.client.post("/gbstock/quote/v1/executionTrend", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockExecutionTrend.model_validate(data))

    def get_period_price(
        self,
        iem_cd: str,
        end_dt: str,
        count: str,
        maxavg: str,
        gubun: str,
        xtick: str,
        today_cls: str,
        market_cls: str,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockPeriodPrice]:
        """해외주식 기간별시세(개별종목) (`POST /gbstock/quote/v1/period`).

        해외 개별종목의 기간별 시세를 조회하는 API 이다. 지수·환율 조회는
        `/gbstock/quote/v1/symbolIndexFxPeriod` 를 사용해야 한다. 응답 블록은
        데이터가 있을 때만 내려오므로 존재 여부를 먼저 확인해야 한다.

        시세 API 는 모의투자(moapi) 미지원 — 운영 도메인 전용 (실측 IGW40019).

        Args:
            iem_cd: 종목코드 (길이 15). 예: 미국주식 APPLE인 경우 AAPL
            end_dt: 검색종료일 (길이 8, YYYYMMDD)
            count: 조회건수 (길이 4)
            maxavg: 최대이평 (길이 3)
            gubun: 조회구분 (길이 1). 1.틱 2.분 3.일 4.주 5.월
            xtick: 조회단위 (길이 4). 주기구분 일인 경우 0001, 분/초/틱에서는 별도 설정 가능
            today_cls: 당일조회 (길이 1). 0.종료일조회 1.당일조회
            market_cls: 장시간구분 (길이 1). 0.전체 1.정규장
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockPeriodPrice]: 기간별시세 조회 결과(`Output_0`, `Output_1`)
        """
        body: dict = {
            "iem_cd": iem_cd,
            "end_dt": end_dt,
            "count": count,
            "maxavg": maxavg,
            "gubun": gubun,
            "xtick": xtick,
            "today_cls": today_cls,
            "market_cls": market_cls,
        }

        response = self.client.post("/gbstock/quote/v1/period", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockPeriodPrice.model_validate(data))
