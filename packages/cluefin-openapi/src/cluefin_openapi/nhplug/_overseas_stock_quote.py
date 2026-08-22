from typing import Any, Dict, Literal, Optional

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES, NHPlugHttpHeader, NHPlugHttpResponse
from cluefin_openapi.nhplug._overseas_stock_quote_types import (
    OverseasStockQuoteCurrentPrice,
    OverseasStockQuoteExecutionTrend,
    OverseasStockQuotePeriodPrice,
    OverseasStockQuoteSymbolIndexFxPeriod,
)


class OverseasStockQuote:
    """해외주식 시세 (gbstock quote).

    스펙 정본: https://www.nhplug.com/openapi-docs/gbstock/openapi.json
    시세 조회 API 는 계좌번호가 필요 없다(조회·주문 카테고리와 다름). 4개 API 모두
    스펙에 `CtsHeader` 파라미터가 없어 연속조회를 지원하지 않는다(`cts` 인자 없음).

    4종 모두 모의투자(moapi) 미지원 — 운영 도메인 전용이다. moapi 는 `current` 에
    대해 "종목코드(iem_cd)를 확인해주세요"(IGW40019)로, 나머지 3종은 미지원
    메시지로 거부한다 (2026-08-22 실측: 어떤 종목코드 형식도 통과하지 못함).
    `iem_cd` 는 티커 그대로 넣는다(예: AAPL) — 응답의 `iem_cd` 는 국가 접두어가
    붙은 형태(USAAAPL)로 되돌아온다.
    """

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        """HTTP 200 이어도 body rsp_cd 가 실패일 수 있으므로 여기서 확인한다."""
        rsp_cd = response_data.get("rsp_cd")
        if rsp_cd is not None and rsp_cd not in SUCCESS_RSP_CODES:
            raise NHPlugAPIError(
                f"API error {rsp_cd}: {response_data.get('rsp_msg', '')}",
                status_code=200,
                response_data=response_data,
            )

    @staticmethod
    def _drop_none(body: Dict[str, Any]) -> Dict[str, Any]:
        """선택 파라미터는 값이 있을 때만 전송한다."""
        return {k: v for k, v in body.items() if v is not None}

    def current(
        self,
        iem_cd: str,
    ) -> NHPlugHttpResponse[OverseasStockQuoteCurrentPrice]:
        """해외주식 현재가상세 (`POST /gbstock/quote/v1/current`).

        해외주식 현재가를 조회하는 API 이다. 응답 블록은 데이터가 있을 때만
        내려오므로 존재 여부를 먼저 확인해야 한다.

        시세 API 는 모의투자(moapi) 미지원 — 운영 도메인 전용 (실측 IGW40019).
        `Output_0` 의 종목명은 스펙상 `kor_name` 이지만 실서버는 `iem_nm` 으로
        내려준다 (2026-08-22 운영 실측) — 둘 다 정의해 두었다.

        Args:
            iem_cd: 종목코드 (길이 15). 예: 미국주식 APPLE인 경우 AAPL

        Returns:
            NHPlugHttpResponse[OverseasStockQuoteCurrentPrice]: 현재가상세 조회 결과(`Output_0`)
        """
        body = self._drop_none({"iem_cd": iem_cd})

        response = self.client.post("/gbstock/quote/v1/current", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockQuoteCurrentPrice.model_validate(data))

    def execution_trend(
        self,
        period_type: Literal["1", "2"],
        req_cnt: int,
        iem_cd: str,
    ) -> NHPlugHttpResponse[OverseasStockQuoteExecutionTrend]:
        """해외주식 체결추이 (`POST /gbstock/quote/v1/executionTrend`).

        해외주식 변동거래량을 조회하는 API 이다. 응답 블록은 데이터가 있을 때만
        내려오므로 존재 여부를 먼저 확인해야 한다.

        시세 API 는 모의투자(moapi) 미지원 — 운영 도메인 전용 (실측 IGW40019).

        Args:
            period_type: 기간구분 (길이 1). 1.시간별 2.일별
            req_cnt: 요청건수 (길이 4)
            iem_cd: 종목코드 (길이 15). 예: 미국주식 APPLE인 경우 AAPL

        Returns:
            NHPlugHttpResponse[OverseasStockQuoteExecutionTrend]: 체결추이 조회 결과(`Output_0`)
        """
        body = self._drop_none(
            {
                "period_type": period_type,
                "req_cnt": req_cnt,
                "iem_cd": iem_cd,
            }
        )

        response = self.client.post("/gbstock/quote/v1/executionTrend", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockQuoteExecutionTrend.model_validate(data))

    def period(
        self,
        iem_cd: str,
        end_dt: str,
        count: str,
        maxavg: str,
        gubun: Literal["1", "2", "3", "4", "5"],
        xtick: str,
        today_cls: Literal["0", "1"],
        market_cls: Literal["0", "1"],
    ) -> NHPlugHttpResponse[OverseasStockQuotePeriodPrice]:
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

        Returns:
            NHPlugHttpResponse[OverseasStockQuotePeriodPrice]: 기간별시세 조회 결과(`Output_0`, `Output_1`)
        """
        body = self._drop_none(
            {
                "iem_cd": iem_cd,
                "end_dt": end_dt,
                "count": count,
                "maxavg": maxavg,
                "gubun": gubun,
                "xtick": xtick,
                "today_cls": today_cls,
                "market_cls": market_cls,
            }
        )

        response = self.client.post("/gbstock/quote/v1/period", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockQuotePeriodPrice.model_validate(data))

    def symbol_index_fx_period(
        self,
        iem_cd: str,
        end_dt: str,
        array_cnt: str,
        maxavg: str,
        gubun: Literal["1", "2", "3"],
        today_cls: Literal["0", "1"],
        xtick: Optional[str] = None,
        scale_change: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockQuoteSymbolIndexFxPeriod]:
        """해외주식 기간별시세(지수·환율) (`POST /gbstock/quote/v1/symbolIndexFxPeriod`).

        해외 지수·환율의 기간별 시세를 조회하는 API 이다. `iem_cd` 에는 지수코드/환율코드를
        입력한다(개별종목 아님). 개별종목 조회는 `/gbstock/quote/v1/period` 를 사용해야 한다.
        응답 블록은 데이터가 있을 때만 내려오므로 존재 여부를 먼저 확인해야 한다.

        시세 API 는 모의투자(moapi) 미지원 — 운영 도메인 전용 (실측 IGW40019).

        Args:
            iem_cd: SYMBOL (길이 14). 지수코드/환율코드
            end_dt: 검색종료일 (길이 8, YYYYMMDD)
            array_cnt: 조회건수 (길이 4). 개별종목 API 의 count 와 필드명이 다름
            maxavg: 최대이평 (길이 3)
            gubun: 조회구분 (길이 1). 1.일 2.주 3.월 — 틱·분은 지원하지 않음
            today_cls: 당일조회 (길이 1). 1.당일만조회(분/초/틱에서 사용) 0.전체조회
            xtick: 조회단위 (길이 3). 주기구분 일인 경우 001, 분/초/틱에서는 별도 설정 가능
            scale_change: 단위변경 (길이 1). Output_1에만 적용 1.거래량천단위 그외.단주

        Returns:
            NHPlugHttpResponse[OverseasStockQuoteSymbolIndexFxPeriod]: 기간별시세 조회 결과(`Output_0`, `Output_1`)
        """
        body = self._drop_none(
            {
                "iem_cd": iem_cd,
                "end_dt": end_dt,
                "array_cnt": array_cnt,
                "maxavg": maxavg,
                "gubun": gubun,
                "today_cls": today_cls,
                "xtick": xtick,
                "scale_change": scale_change,
            }
        )

        response = self.client.post("/gbstock/quote/v1/symbolIndexFxPeriod", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockQuoteSymbolIndexFxPeriod.model_validate(data))
