from typing import Any, Dict, Literal, Optional

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._krstock_quote_types import (
    KrStockQuoteAfterHoursCurrent,
    KrStockQuoteAfterHoursExpected,
    KrStockQuoteCurrentAfterHoursDaily,
    KrStockQuoteCurrentAfterHoursExecution,
    KrStockQuoteCurrentDaily,
    KrStockQuoteCurrentExecution,
    KrStockQuoteCurrentInvestor,
    KrStockQuoteCurrentPrice,
    KrStockQuoteEtfCurrent,
    KrStockQuotePeriod,
)
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES, NHPlugHttpHeader, NHPlugHttpResponse


class KrStockQuote:
    """국내주식 시세.

    스펙 정본: https://www.nhplug.com/openapi-docs/krstock/openapi.json
    시세 조회 API 는 계좌번호가 필요 없다(조회·주문 카테고리와 다름).
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

    def current_price(
        self,
        market_cd: Literal["KRX", "NXT", "UNT"],
        iem_cd: str,
    ) -> NHPlugHttpResponse[KrStockQuoteCurrentPrice]:
        """주식현재가 시세 (`POST /krstock/quote/v1/currentPrice`).

        스펙상 2개 입력 필드가 모두 required 다. 계좌번호가 필요 없는 시세 조회
        API 다. 스펙에 `CtsHeader` 파라미터가 없어 연속조회를 지원하지 않는다
        (다른 조회 API 와 달리 `cts` 인자가 없다).

        Args:
            market_cd: 시장구분코드 (KRX/NXT/UNT)
            iem_cd: 종목코드 (예: 005930)
        """
        body = self._drop_none(
            {
                "market_cd": market_cd,
                "iem_cd": iem_cd,
            }
        )
        response = self.client.post("/krstock/quote/v1/currentPrice", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteCurrentPrice.model_validate(data))

    def current_execution(
        self,
        market_cd: Literal["KRX", "NXT", "UNT"],
        iem_cd: str,
        array_cnt: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockQuoteCurrentExecution]:
        """주식현재가 체결 (`POST /krstock/quote/v1/currentExecution`).

        `market_cd`/`iem_cd` 가 required, `array_cnt`(읽을갯수)는 선택이다. 계좌번호가
        필요 없는 시세 조회 API 다. 스펙에 `CtsHeader` 파라미터가 없어 연속조회를
        지원하지 않는다(다른 조회 API 와 달리 `cts` 인자가 없다). currentPrice 와
        달리 `Output_0` 이 배열, `Output_1` 이 단일 종합 객체다(반대로 뒤집힌 구조).

        Args:
            market_cd: 시장구분코드 (KRX/NXT/UNT)
            iem_cd: 종목코드 (예: 005930)
            array_cnt: 읽을갯수 (Output_0 시간대별 체결 목록의 조회 건수)
        """
        body = self._drop_none(
            {
                "market_cd": market_cd,
                "iem_cd": iem_cd,
                "array_cnt": array_cnt,
            }
        )
        response = self.client.post("/krstock/quote/v1/currentExecution", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteCurrentExecution.model_validate(data))

    def current_daily(
        self,
        market_cd: Literal["KRX", "NXT", "UNT"],
        iem_cd: str,
        array_cnt: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockQuoteCurrentDaily]:
        """주식현재가 일자별 (`POST /krstock/quote/v1/currentDaily`).

        `market_cd`/`iem_cd` 가 required, `array_cnt`(읽을갯수)는 선택이다. 계좌번호가
        필요 없는 시세 조회 API 다. 스펙에 `CtsHeader` 파라미터가 없어 연속조회를
        지원하지 않는다(다른 조회 API 와 달리 `cts` 인자가 없다). 응답 블록은
        `Output_0` 하나뿐이고 그 자체가 배열이다.

        Args:
            market_cd: 시장구분코드 (KRX/NXT/UNT)
            iem_cd: 종목코드 (예: 005930)
            array_cnt: 읽을갯수 (Output_0 일별 시세 목록의 조회 건수)
        """
        body = self._drop_none(
            {
                "market_cd": market_cd,
                "iem_cd": iem_cd,
                "array_cnt": array_cnt,
            }
        )
        response = self.client.post("/krstock/quote/v1/currentDaily", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteCurrentDaily.model_validate(data))

    def current_investor(
        self,
        market_cd: Literal["KRX", "NXT", "UNT"],
        iem_cd: str,
        array_cnt: str,
    ) -> NHPlugHttpResponse[KrStockQuoteCurrentInvestor]:
        """주식현재가 투자자 (`POST /krstock/quote/v1/currentInvestor`).

        스펙상 3개 입력 필드가 모두 required 다 — `array_cnt`(요청건수)가
        currentDaily/currentExecution 과 달리 선택이 아니다. 계좌번호가 필요 없는
        시세 조회 API 다. 스펙에 `CtsHeader` 파라미터가 없어 연속조회를 지원하지
        않는다(다른 조회 API 와 달리 `cts` 인자가 없다). 응답 블록은 `Output_0`
        하나뿐이고 그 자체가 배열이다.

        Args:
            market_cd: 시장구분코드 (KRX/NXT/UNT)
            iem_cd: 종목코드 (예: 005930)
            array_cnt: 요청건수 (Output_0 투자자별 거래현황 목록의 조회 건수)
        """
        body = self._drop_none(
            {
                "market_cd": market_cd,
                "iem_cd": iem_cd,
                "array_cnt": array_cnt,
            }
        )
        response = self.client.post("/krstock/quote/v1/currentInvestor", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteCurrentInvestor.model_validate(data))

    def period(
        self,
        market_cd: Literal["KRX", "NXT", "UNT"],
        iem_cd: str,
        mrkt_div_cls_code: Optional[Literal["1", "4", "A", "E", "T"]] = None,
        edate: Optional[str] = None,
        array_cnt: Optional[str] = None,
        maxavg: Optional[str] = None,
        gubun: Optional[Literal["1", "2", "3", "4", "5", "6", "7"]] = None,
        xtick: Optional[str] = None,
        today_cls_code: Optional[Literal["0", "1"]] = None,
        fake_tick: Optional[Literal["0", "1"]] = None,
        sur_flag: Optional[Literal["0", "1"]] = None,
        sur_gb_day_cnt: Optional[str] = None,
        sur_bf_end_time: Optional[str] = None,
        out1_scale_change: Optional[Literal["0", "1", "2"]] = None,
        out2_scale_change: Optional[Literal["0", "1", "2"]] = None,
    ) -> NHPlugHttpResponse[KrStockQuotePeriod]:
        """국내주식기간별시세(일/주/월/년) (`POST /krstock/quote/v1/period`).

        `market_cd`/`iem_cd` 만 required 다. 계좌번호가 필요 없는 시세 조회 API 다.
        스펙에 `CtsHeader` 파라미터가 없어 연속조회를 지원하지 않는다(다른 조회
        API 와 달리 `cts` 인자가 없다). `Output_0` 은 스펙상 Array 로 선언되지만
        예시 응답은 Object 다(양쪽 다 허용). `Output_1` 이 실제 주기별(일/주/월/년)
        봉 데이터 배열이다.

        Args:
            market_cd: 시장구분코드 (KRX/NXT/UNT)
            iem_cd: 단축종목코드 (예: 005930)
            mrkt_div_cls_code: 시장분류구분코드 (1.거래소 4.코스닥 A.ETN E.ELW T.K-OTC)
            edate: 종료일 (YYYYMMDD)
            array_cnt: 읽을건수
            maxavg: 최대이평
            gubun: 주기구분 (1.일 2.주 3.월 4.년 5.분 6.초 7.틱)
            xtick: 분구분 (분/초/틱일 때 입력)
            today_cls_code: 당일조회구분 (1.당일만조회 0.전체조회, 분/초/틱에서 사용)
            fake_tick: 거래량0봉제외여부 (0.허봉+실봉 1.실봉)
            sur_flag: 복기구분플래그 (0.복기사용안함 1.복기처리사용함)
            sur_gb_day_cnt: 복기시작n일전 (sur_flag="1"일 때만 의미, 예: 00.D당일
                01.D-1일전 02.D-2일전)
            sur_bf_end_time: 복기시작전종료시각 (HHmmSS, sur_flag="1"일 때)
            out1_scale_change: Out1단위변경 (0.변경안함 1.거래량천단위·거래대금백만단위
                2.거래량단주·거래대금만백만단위)
            out2_scale_change: Out2단위변경 (0.변경안함 1.거래량천단위·거래대금백만단위
                2.거래량단주·거래대금만백만단위)
        """
        body = self._drop_none(
            {
                "market_cd": market_cd,
                "iem_cd": iem_cd,
                "mrkt_div_cls_code": mrkt_div_cls_code,
                "edate": edate,
                "array_cnt": array_cnt,
                "maxavg": maxavg,
                "gubun": gubun,
                "xtick": xtick,
                "today_cls_code": today_cls_code,
                "fake_tick": fake_tick,
                "sur_flag": sur_flag,
                "sur_gb_day_cnt": sur_gb_day_cnt,
                "sur_bf_end_time": sur_bf_end_time,
                "out1_scale_change": out1_scale_change,
                "out2_scale_change": out2_scale_change,
            }
        )
        response = self.client.post("/krstock/quote/v1/period", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuotePeriod.model_validate(data))

    def after_hours_current(
        self,
        iem_cd: str,
    ) -> NHPlugHttpResponse[KrStockQuoteAfterHoursCurrent]:
        """국내주식 시간외현재가 (`POST /krstock/quote/v1/afterHoursCurrent`).

        입력이 `iem_cd` 하나뿐이다 — 다른 quote API 와 달리 `market_cd` 가 없다.
        계좌번호가 필요 없는 시세 조회 API 다. 스펙에 `CtsHeader` 파라미터가 없어
        연속조회를 지원하지 않는다(다른 조회 API 와 달리 `cts` 인자가 없다).
        `Output_0`(시간외 단일가 종합)/`Output_1`(정규장 종합) 모두 단일 객체다
        (배열 아님).

        Args:
            iem_cd: 종목코드 (예: 005930)
        """
        body = self._drop_none({"iem_cd": iem_cd})
        response = self.client.post("/krstock/quote/v1/afterHoursCurrent", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteAfterHoursCurrent.model_validate(data))

    def current_after_hours_daily(
        self,
        iem_cd: str,
        date: str,
        array_cnt: str,
        maxavg: str,
        gubun: str,
    ) -> NHPlugHttpResponse[KrStockQuoteCurrentAfterHoursDaily]:
        """주식현재가 시간외일자별주가 (`POST /krstock/quote/v1/currentAfterHoursDaily`).

        스펙상 5개 입력 필드(`iem_cd`/`date`/`array_cnt`/`maxavg`/`gubun`)가 모두
        required 다 — 다른 quote API 와 달리 선택 필드가 없고 `market_cd` 도 없다.
        계좌번호가 필요 없는 시세 조회 API 다. 스펙에 `CtsHeader` 파라미터가 없어
        연속조회를 지원하지 않는다(다른 조회 API 와 달리 `cts` 인자가 없다).
        `Output_0`/`Output_1` 모두 배열이다.

        Args:
            iem_cd: 종목코드 (예: 005930)
            date: 일자 (YYYYMMDD)
            array_cnt: 읽을갯수
            maxavg: 최대이평
            gubun: 구분 (1.정규장 2.정규장+시간외단일가 이외.정규장+당일시간외단일가)
        """
        body = self._drop_none(
            {
                "iem_cd": iem_cd,
                "date": date,
                "array_cnt": array_cnt,
                "maxavg": maxavg,
                "gubun": gubun,
            }
        )
        response = self.client.post("/krstock/quote/v1/currentAfterHoursDaily", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteCurrentAfterHoursDaily.model_validate(data))

    def current_after_hours_execution(
        self,
        iem_cd: str,
    ) -> NHPlugHttpResponse[KrStockQuoteCurrentAfterHoursExecution]:
        """주식현재가 시간외시간별체결 (`POST /krstock/quote/v1/currentAfterHoursExecution`).

        입력이 `iem_cd` 하나뿐이다 — afterHoursCurrent/currentAfterHoursDaily 와
        같은 패턴으로 `market_cd` 가 없다. 계좌번호가 필요 없는 시세 조회 API 다.
        스펙에 `CtsHeader` 파라미터가 없어 연속조회를 지원하지 않는다(다른 조회
        API 와 달리 `cts` 인자가 없다). `Output_0` 하나만 있고 배열이다.

        Args:
            iem_cd: 종목코드 (예: 005930)
        """
        body = self._drop_none({"iem_cd": iem_cd})
        response = self.client.post("/krstock/quote/v1/currentAfterHoursExecution", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteCurrentAfterHoursExecution.model_validate(data))

    def after_hours_expected(
        self,
        iem_cd: str,
    ) -> NHPlugHttpResponse[KrStockQuoteAfterHoursExpected]:
        """주식현재가 시간외시간별예상 (`POST /krstock/quote/v1/afterHoursExpected`).

        입력이 `iem_cd` 하나뿐이다 — afterHoursCurrent/currentAfterHoursDaily/
        currentAfterHoursExecution 과 같은 패턴으로 `market_cd` 가 없다.
        계좌번호가 필요 없는 시세 조회 API 다. 스펙에 `CtsHeader` 파라미터가 없어
        연속조회를 지원하지 않는다(다른 조회 API 와 달리 `cts` 인자가 없다).
        `Output_0` 하나만 있고 배열이다.

        Args:
            iem_cd: 종목코드 (예: 005930)
        """
        body = self._drop_none({"iem_cd": iem_cd})
        response = self.client.post("/krstock/quote/v1/afterHoursExpected", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteAfterHoursExpected.model_validate(data))

    def etf_current(
        self,
        iem_cd: str,
    ) -> NHPlugHttpResponse[KrStockQuoteEtfCurrent]:
        """ETF/ETN 현재가 (`POST /krstock/quote/v1/etfCurrent`).

        입력이 `iem_cd` 하나뿐이다(market_cd 없음). 계좌번호가 필요 없는 시세
        조회 API 다. 스펙에 `CtsHeader` 파라미터가 없어 연속조회를 지원하지
        않는다(다른 조회 API 와 달리 `cts` 인자가 없다). `Output_3`/`Output_4`
        는 공식 스펙 문서에는 없고 예시 응답에만 존재하는 블록이다(spec 의
        x-schema-warning 이 명시).

        Args:
            iem_cd: 종목코드 (예: 069500 = KODEX 200)
        """
        body = self._drop_none({"iem_cd": iem_cd})
        response = self.client.post("/krstock/quote/v1/etfCurrent", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteEtfCurrent.model_validate(data))
