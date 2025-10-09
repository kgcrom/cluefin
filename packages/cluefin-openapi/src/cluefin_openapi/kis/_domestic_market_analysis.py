from cluefin_openapi.kis._client import Client
from cluefin_openapi.kis._domestic_market_analysis_types import (
    AfterHoursExpectedFluctuation,
    BuySellVolumeByStockDaily,
    ConditionSearchList,
    ConditionSearchResult,
    CreditBalanceTrendDaily,
    ExpectedPriceTrend,
    ForeignBrokerageTradingAggregate,
    ForeignInstitutionalEstimateByStock,
    ForeignNetBuyTrendByStock,
    InstitutionalForeignTradingAggregate,
    InvestorTradingTrendByMarketDaily,
    InvestorTradingTrendByMarketIntraday,
    InvestorTradingTrendByStockDaily,
    LimitPriceStocks,
    MarketFundSummary,
    MemberTradingTrendByStock,
    MemberTradingTrendTick,
    ProgramTradingInvestorTrendToday,
    ProgramTradingSummaryDaily,
    ProgramTradingSummaryIntraday,
    ProgramTradingTrendByStockDaily,
    ProgramTradingTrendByStockIntraday,
    ResistanceLevelTradingWeight,
    ShortSellingTrendDaily,
    StockLoanTrendDaily,
    TradingWeightByAmount,
    WatchlistGroups,
    WatchlistMultiQuote,
    WatchlistStocksByGroup,
)


class DomesticMarketAnalysis:
    """국내주식 시세분석"""

    def __init__(self, client: Client):
        self.client = client

    def get_condition_search_list(self, user_id: str) -> ConditionSearchList:
        """
        종목조건검색 목록조회

        Args:
            user_id (str): 사용자 HTS ID

        Returns:
            ConditionSearchList: 종목조건검색 목록조회 응답 객체
        """
        headers = {
            "tr_id": "HHKST03900300",
        }
        params = {
            "user_id": user_id,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/psearch-title", headers=headers, params=params)
        return ConditionSearchList.model_validate(response.json())

    def get_condition_search_result(self, user_id: str, seq: str) -> ConditionSearchResult:
        """
        종목조건검색조회

        Args:
            user_id (str): 사용자 HTS ID
            seq (str): 사용자조건 키값 (종목조건검색 목록조회 API의 output인 'seq'을 이용, 0부터 시작)

        Returns:
            ConditionSearchResult: 종목조건검색조회 응답 객체
        """
        headers = {
            "tr_id": "HHKST03900400",
        }
        params = {
            "user_id": user_id,
            "seq": seq,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/psearch-result", headers=headers, params=params)
        return ConditionSearchResult.model_validate(response.json())

    def get_watchlist_groups(self, type: str, fid_etc_cls_code: str, user_id: str) -> WatchlistGroups:
        """
        관심종목 그룹조회

        Args:
            type (str): 관심종목구분코드 (Unique key: 1)
            fid_etc_cls_code (str): FID 기타 구분 코드 (Unique key: 00)
            user_id (str): 사용자 ID (HTS_ID 입력)

        Returns:
            WatchlistGroups: 관심종목 그룹조회 응답 객체
        """
        headers = {
            "tr_id": "HHKCM113004C7",
        }
        params = {
            "TYPE": type,
            "FID_ETC_CLS_CODE": fid_etc_cls_code,
            "USER_ID": user_id,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/intstock-grouplist", headers=headers, params=params
        )
        return WatchlistGroups.model_validate(response.json())

    def get_watchlist_multi_quote(
        self,
        fid_cond_mrkt_div_code_1: str,
        fid_input_iscd_1: str,
        fid_cond_mrkt_div_code_2: str,
        fid_input_iscd_2: str,
        fid_cond_mrkt_div_code_3: str,
        fid_input_iscd_3: str,
        fid_cond_mrkt_div_code_4: str,
        fid_input_iscd_4: str,
        fid_cond_mrkt_div_code_5: str,
        fid_input_iscd_5: str,
        fid_cond_mrkt_div_code_6: str,
        fid_input_iscd_6: str,
        fid_cond_mrkt_div_code_7: str,
        fid_input_iscd_7: str,
        fid_cond_mrkt_div_code_8: str,
        fid_input_iscd_8: str,
        fid_cond_mrkt_div_code_9: str,
        fid_input_iscd_9: str,
        fid_cond_mrkt_div_code_10: str,
        fid_input_iscd_10: str,
        fid_cond_mrkt_div_code_11: str,
        fid_input_iscd_11: str,
        fid_cond_mrkt_div_code_12: str,
        fid_input_iscd_12: str,
        fid_cond_mrkt_div_code_13: str,
        fid_input_iscd_13: str,
        fid_cond_mrkt_div_code_14: str,
        fid_input_iscd_14: str,
        fid_cond_mrkt_div_code_15: str,
        fid_input_iscd_15: str,
        fid_cond_mrkt_div_code_16: str,
        fid_input_iscd_16: str,
        fid_cond_mrkt_div_code_17: str,
        fid_input_iscd_17: str,
        fid_cond_mrkt_div_code_18: str,
        fid_input_iscd_18: str,
        fid_cond_mrkt_div_code_19: str,
        fid_input_iscd_19: str,
        fid_cond_mrkt_div_code_20: str,
        fid_input_iscd_20: str,
        fid_cond_mrkt_div_code_21: str,
        fid_input_iscd_21: str,
        fid_cond_mrkt_div_code_22: str,
        fid_input_iscd_22: str,
        fid_cond_mrkt_div_code_23: str,
        fid_input_iscd_23: str,
        fid_cond_mrkt_div_code_24: str,
        fid_input_iscd_24: str,
        fid_cond_mrkt_div_code_25: str,
        fid_input_iscd_25: str,
        fid_cond_mrkt_div_code_26: str,
        fid_input_iscd_26: str,
        fid_cond_mrkt_div_code_27: str,
        fid_input_iscd_27: str,
        fid_cond_mrkt_div_code_28: str,
        fid_input_iscd_28: str,
        fid_cond_mrkt_div_code_29: str,
        fid_input_iscd_29: str,
        fid_cond_mrkt_div_code_30: str,
        fid_input_iscd_30: str,
    ) -> WatchlistMultiQuote:
        """
        관심종목(멀티종목) 시세조회

        Args:
            fid_cond_mrkt_div_code_1 (str): 조건 시장 분류 코드1 (J: KRX, NX: NXT, UN: 통합, 예: J)
            fid_input_iscd_1 (str): 입력 종목코드1 (예: 005930)
            fid_cond_mrkt_div_code_2 (str): 조건 시장 분류 코드2
            fid_input_iscd_2 (str): 입력 종목코드2
            fid_cond_mrkt_div_code_3 (str): 조건 시장 분류 코드3
            fid_input_iscd_3 (str): 입력 종목코드3
            fid_cond_mrkt_div_code_4 (str): 조건 시장 분류 코드4
            fid_input_iscd_4 (str): 입력 종목코드4
            fid_cond_mrkt_div_code_5 (str): 조건 시장 분류 코드5
            fid_input_iscd_5 (str): 입력 종목코드5
            fid_cond_mrkt_div_code_6 (str): 조건 시장 분류 코드6
            fid_input_iscd_6 (str): 입력 종목코드6
            fid_cond_mrkt_div_code_7 (str): 조건 시장 분류 코드7
            fid_input_iscd_7 (str): 입력 종목코드7
            fid_cond_mrkt_div_code_8 (str): 조건 시장 분류 코드8
            fid_input_iscd_8 (str): 입력 종목코드8
            fid_cond_mrkt_div_code_9 (str): 조건 시장 분류 코드9
            fid_input_iscd_9 (str): 입력 종목코드9
            fid_cond_mrkt_div_code_10 (str): 조건 시장 분류 코드10
            fid_input_iscd_10 (str): 입력 종목코드10
            fid_cond_mrkt_div_code_11 (str): 조건 시장 분류 코드11
            fid_input_iscd_11 (str): 입력 종목코드11
            fid_cond_mrkt_div_code_12 (str): 조건 시장 분류 코드12
            fid_input_iscd_12 (str): 입력 종목코드12
            fid_cond_mrkt_div_code_13 (str): 조건 시장 분류 코드13
            fid_input_iscd_13 (str): 입력 종목코드13
            fid_cond_mrkt_div_code_14 (str): 조건 시장 분류 코드14
            fid_input_iscd_14 (str): 입력 종목코드14
            fid_cond_mrkt_div_code_15 (str): 조건 시장 분류 코드15
            fid_input_iscd_15 (str): 입력 종목코드15
            fid_cond_mrkt_div_code_16 (str): 조건 시장 분류 코드16
            fid_input_iscd_16 (str): 입력 종목코드16
            fid_cond_mrkt_div_code_17 (str): 조건 시장 분류 코드17
            fid_input_iscd_17 (str): 입력 종목코드17
            fid_cond_mrkt_div_code_18 (str): 조건 시장 분류 코드18
            fid_input_iscd_18 (str): 입력 종목코드18
            fid_cond_mrkt_div_code_19 (str): 조건 시장 분류 코드19
            fid_input_iscd_19 (str): 입력 종목코드19
            fid_cond_mrkt_div_code_20 (str): 조건 시장 분류 코드20
            fid_input_iscd_20 (str): 입력 종목코드20
            fid_cond_mrkt_div_code_21 (str): 조건 시장 분류 코드21
            fid_input_iscd_21 (str): 입력 종목코드21
            fid_cond_mrkt_div_code_22 (str): 조건 시장 분류 코드22
            fid_input_iscd_22 (str): 입력 종목코드22
            fid_cond_mrkt_div_code_23 (str): 조건 시장 분류 코드23
            fid_input_iscd_23 (str): 입력 종목코드23
            fid_cond_mrkt_div_code_24 (str): 조건 시장 분류 코드24
            fid_input_iscd_24 (str): 입력 종목코드24
            fid_cond_mrkt_div_code_25 (str): 조건 시장 분류 코드25
            fid_input_iscd_25 (str): 입력 종목코드25
            fid_cond_mrkt_div_code_26 (str): 조건 시장 분류 코드26
            fid_input_iscd_26 (str): 입력 종목코드26
            fid_cond_mrkt_div_code_27 (str): 조건 시장 분류 코드27
            fid_input_iscd_27 (str): 입력 종목코드27
            fid_cond_mrkt_div_code_28 (str): 조건 시장 분류 코드28
            fid_input_iscd_28 (str): 입력 종목코드28
            fid_cond_mrkt_div_code_29 (str): 조건 시장 분류 코드29
            fid_input_iscd_29 (str): 입력 종목코드29
            fid_cond_mrkt_div_code_30 (str): 조건 시장 분류 코드30
            fid_input_iscd_30 (str): 입력 종목코드30

        Returns:
            WatchlistMultiQuote: 관심종목(멀티종목) 시세조회 응답 객체
        """
        headers = {
            "tr_id": "FHKST11300006",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE_1": fid_cond_mrkt_div_code_1,
            "FID_INPUT_ISCD_1": fid_input_iscd_1,
            "FID_COND_MRKT_DIV_CODE_2": fid_cond_mrkt_div_code_2,
            "FID_INPUT_ISCD_2": fid_input_iscd_2,
            "FID_COND_MRKT_DIV_CODE_3": fid_cond_mrkt_div_code_3,
            "FID_INPUT_ISCD_3": fid_input_iscd_3,
            "FID_COND_MRKT_DIV_CODE_4": fid_cond_mrkt_div_code_4,
            "FID_INPUT_ISCD_4": fid_input_iscd_4,
            "FID_COND_MRKT_DIV_CODE_5": fid_cond_mrkt_div_code_5,
            "FID_INPUT_ISCD_5": fid_input_iscd_5,
            "FID_COND_MRKT_DIV_CODE_6": fid_cond_mrkt_div_code_6,
            "FID_INPUT_ISCD_6": fid_input_iscd_6,
            "FID_COND_MRKT_DIV_CODE_7": fid_cond_mrkt_div_code_7,
            "FID_INPUT_ISCD_7": fid_input_iscd_7,
            "FID_COND_MRKT_DIV_CODE_8": fid_cond_mrkt_div_code_8,
            "FID_INPUT_ISCD_8": fid_input_iscd_8,
            "FID_COND_MRKT_DIV_CODE_9": fid_cond_mrkt_div_code_9,
            "FID_INPUT_ISCD_9": fid_input_iscd_9,
            "FID_COND_MRKT_DIV_CODE_10": fid_cond_mrkt_div_code_10,
            "FID_INPUT_ISCD_10": fid_input_iscd_10,
            "FID_COND_MRKT_DIV_CODE_11": fid_cond_mrkt_div_code_11,
            "FID_INPUT_ISCD_11": fid_input_iscd_11,
            "FID_COND_MRKT_DIV_CODE_12": fid_cond_mrkt_div_code_12,
            "FID_INPUT_ISCD_12": fid_input_iscd_12,
            "FID_COND_MRKT_DIV_CODE_13": fid_cond_mrkt_div_code_13,
            "FID_INPUT_ISCD_13": fid_input_iscd_13,
            "FID_COND_MRKT_DIV_CODE_14": fid_cond_mrkt_div_code_14,
            "FID_INPUT_ISCD_14": fid_input_iscd_14,
            "FID_COND_MRKT_DIV_CODE_15": fid_cond_mrkt_div_code_15,
            "FID_INPUT_ISCD_15": fid_input_iscd_15,
            "FID_COND_MRKT_DIV_CODE_16": fid_cond_mrkt_div_code_16,
            "FID_INPUT_ISCD_16": fid_input_iscd_16,
            "FID_COND_MRKT_DIV_CODE_17": fid_cond_mrkt_div_code_17,
            "FID_INPUT_ISCD_17": fid_input_iscd_17,
            "FID_COND_MRKT_DIV_CODE_18": fid_cond_mrkt_div_code_18,
            "FID_INPUT_ISCD_18": fid_input_iscd_18,
            "FID_COND_MRKT_DIV_CODE_19": fid_cond_mrkt_div_code_19,
            "FID_INPUT_ISCD_19": fid_input_iscd_19,
            "FID_COND_MRKT_DIV_CODE_20": fid_cond_mrkt_div_code_20,
            "FID_INPUT_ISCD_20": fid_input_iscd_20,
            "FID_COND_MRKT_DIV_CODE_21": fid_cond_mrkt_div_code_21,
            "FID_INPUT_ISCD_21": fid_input_iscd_21,
            "FID_COND_MRKT_DIV_CODE_22": fid_cond_mrkt_div_code_22,
            "FID_INPUT_ISCD_22": fid_input_iscd_22,
            "FID_COND_MRKT_DIV_CODE_23": fid_cond_mrkt_div_code_23,
            "FID_INPUT_ISCD_23": fid_input_iscd_23,
            "FID_COND_MRKT_DIV_CODE_24": fid_cond_mrkt_div_code_24,
            "FID_INPUT_ISCD_24": fid_input_iscd_24,
            "FID_COND_MRKT_DIV_CODE_25": fid_cond_mrkt_div_code_25,
            "FID_INPUT_ISCD_25": fid_input_iscd_25,
            "FID_COND_MRKT_DIV_CODE_26": fid_cond_mrkt_div_code_26,
            "FID_INPUT_ISCD_26": fid_input_iscd_26,
            "FID_COND_MRKT_DIV_CODE_27": fid_cond_mrkt_div_code_27,
            "FID_INPUT_ISCD_27": fid_input_iscd_27,
            "FID_COND_MRKT_DIV_CODE_28": fid_cond_mrkt_div_code_28,
            "FID_INPUT_ISCD_28": fid_input_iscd_28,
            "FID_COND_MRKT_DIV_CODE_29": fid_cond_mrkt_div_code_29,
            "FID_INPUT_ISCD_29": fid_input_iscd_29,
            "FID_COND_MRKT_DIV_CODE_30": fid_cond_mrkt_div_code_30,
            "FID_INPUT_ISCD_30": fid_input_iscd_30,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/intstock-multprice", headers=headers, params=params
        )
        return WatchlistMultiQuote.model_validate(response.json())

    def get_watchlist_stocks_by_group(
        self,
        type: str,
        user_id: str,
        data_rank: str,
        inter_grp_code: str,
        inter_grp_name: str,
        hts_kor_isnm: str,
        cntg_cls_code: str,
        fid_etc_cls_code: str,
    ) -> WatchlistStocksByGroup:
        """
        관심종목 그룹별 종목조회

        Args:
            type (str): 관심종목구분코드 (Unique key: 1)
            user_id (str): 사용자 ID (HTS_ID 입력)
            data_rank (str): 데이터 순위 (공백)
            inter_grp_code (str): 관심 그룹 코드 (관심그룹 조회 결과의 그룹 값 입력)
            inter_grp_name (str): 관심 그룹 명 (공백)
            hts_kor_isnm (str): HTS 한글 종목명 (공백)
            cntg_cls_code (str): 체결 구분 코드 (공백)
            fid_etc_cls_code (str): 기타 구분 코드 (Unique key: 4)

        Returns:
            WatchlistStocksByGroup: 관심종목 그룹별 종목조회 응답 객체
        """
        headers = {
            "tr_id": "HHKCM113004C6",
        }
        params = {
            "TYPE": type,
            "USER_ID": user_id,
            "DATA_RANK": data_rank,
            "INTER_GRP_CODE": inter_grp_code,
            "INTER_GRP_NAME": inter_grp_name,
            "HTS_KOR_ISNM": hts_kor_isnm,
            "CNTG_CLS_CODE": cntg_cls_code,
            "FID_ETC_CLS_CODE": fid_etc_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/intstock-stocklist-by-group", headers=headers, params=params
        )
        return WatchlistStocksByGroup.model_validate(response.json())

    def get_institutional_foreign_trading_aggregate(
        self,
        type: str,
        user_id: str,
        data_rank: str,
        inter_grp_code: str,
        inter_grp_name: str,
        hts_kor_isnm: str,
        cntg_cls_code: str,
        fid_etc_cls_code: str,
    ) -> InstitutionalForeignTradingAggregate:
        """
        국내기관_외국인 매매종목가집계

        Args:
            type (str): 관심종목구분코드 (Unique key: 1)
            user_id (str): 사용자 ID (HTS_ID 입력)
            data_rank (str): 데이터 순위 (공백)
            inter_grp_code (str): 관심 그룹 코드 (관심그룹 조회 결과의 그룹 값 입력)
            inter_grp_name (str): 관심 그룹 명 (공백)
            hts_kor_isnm (str): HTS 한글 종목명 (공백)
            cntg_cls_code (str): 체결 구분 코드 (공백)
            fid_etc_cls_code (str): 기타 구분 코드 (Unique key: 4)

        Returns:
            InstitutionalForeignTradingAggregate: 국내기관_외국인 매매종목가집계 응답 객체
        """
        headers = {
            "tr_id": "HHKCM113004C6",
        }
        params = {
            "TYPE": type,
            "USER_ID": user_id,
            "DATA_RANK": data_rank,
            "INTER_GRP_CODE": inter_grp_code,
            "INTER_GRP_NAME": inter_grp_name,
            "HTS_KOR_ISNM": hts_kor_isnm,
            "CNTG_CLS_CODE": cntg_cls_code,
            "FID_ETC_CLS_CODE": fid_etc_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/intstock-stocklist-by-group", headers=headers, params=params
        )
        return InstitutionalForeignTradingAggregate.model_validate(response.json())

    def get_foreign_brokerage_trading_aggregate(
        self,
        fid_input_iscd: str,
        fid_rank_sort_cls_code: str,
        fid_rank_sort_cls_code_2: str,
    ) -> ForeignBrokerageTradingAggregate:
        """
        외국계 매매종목 가집계

        Args:
            fid_input_iscd (str): 입력 종목코드 (0000: 전체, 0001: 코스피, 1001: 코스닥)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0: 순매수상위, 1: 순매도상위)
            fid_rank_sort_cls_code_2 (str): 순위 정렬 구분 코드2 (0: 매수순, 1: 매도순)

        Returns:
            ForeignBrokerageTradingAggregate: 외국계 매매종목 가집계 응답 객체
        """
        headers = {
            "tr_id": "FHKST644100C0",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_COND_SCR_DIV_CODE": "16441",
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_RANK_SORT_CLS_CODE": fid_rank_sort_cls_code,
            "FID_RANK_SORT_CLS_CODE_2": fid_rank_sort_cls_code_2,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/frgnmem-trade-estimate", headers=headers, params=params
        )
        return ForeignBrokerageTradingAggregate.model_validate(response.json())

    def get_investor_trading_trend_by_stock_daily(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_input_date_1: str,
    ) -> InvestorTradingTrendByStockDaily:
        """
                종목별 투자자매매동향(일별)

                Args:
                    fid_cond_mrkt_div_code (str): 조건시장분류코드 (시장구분코드: J)
                    fid_input_iscd (str): 입력종목코드, 종목번호(6자리)
                    fid_input_date_1 (str): 입력날짜1 (예: 20240517)
                    fid_org_adj_prc (str): 수정주가 원주가 가격 (공란 입력)
                    fid_etc_cls_code (str): 기타 구분 코드 (공란 입력)


                    FID_ORG_ADJ_PRC	수정주가 원주가 가격	String	Y	2	공란 입력
        FID_ETC_CLS_CODE	기타 구분 코드	String	Y	2	공란 입력

                Returns:
                    InvestorTradingTrendByStockDaily: 종목별 투자자매매동향(일별) 응답 객체
        """
        headers = {
            "tr_id": "FHPTJ04160001",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_ORG_ADJ_PRC": "",
            "FID_ETC_CLS_CODE": "",
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/investor-trade-by-stock-daily", headers=headers, params=params
        )
        return InvestorTradingTrendByStockDaily.model_validate(response.json())

    def get_investor_trading_trend_by_market_intraday(
        self, fid_input_iscd: str, fid_input_iscd_2: str
    ) -> InvestorTradingTrendByMarketIntraday:
        """
        시장별 투자자매매동향(시세)

        Args:
            fid_input_iscd (str): 시장구분 (코스피: KSP, 코스닥: KSQ, 선물/콜옵션/풋옵션: K2I, 주식선물: 999, ETF: ETF, ELW: ELW, ETN: ETN, 미니: MKI, 위클리월: WKM, 위클리목: WKI, 코스닥150: KQI)
            fid_input_iscd_2 (str): 업종구분 (코스피: 0001_종합~0027_제조업, 코스닥: 1001_종합~1041_IT부품 등)

        Returns:
            InvestorTradingTrendByMarketIntraday: 시장별 투자자매매동향(시세) 응답 객체
        """
        headers = {
            "tr_id": "FHPTJ04030000",
        }
        params = {
            "fid_input_iscd": fid_input_iscd,
            "fid_input_iscd_2": fid_input_iscd_2,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-investor-time-by-market", headers=headers, params=params
        )
        return InvestorTradingTrendByMarketIntraday.model_validate(response.json())

    def get_investor_trading_trend_by_market_daily(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_input_date_1: str,
        fid_input_iscd_1: str,
        fid_input_date_2: str,
        fid_input_iscd_2: str,
    ) -> InvestorTradingTrendByMarketDaily:
        """
        시장별 투자자매매동향(일별)

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (업종: U)
            fid_input_iscd (str): 입력 종목코드 (코스피, 코스닥: 업종분류코드)
            fid_input_date_1 (str): 입력 날짜1 (예: 20240517)
            fid_input_iscd_1 (str): 입력 종목코드 (코스피: KSP, 코스닥: KSQ)
            fid_input_date_2 (str): 입력 날짜2 (입력 날짜1과 동일날짜 입력)
            fid_input_iscd_2 (str): 하위 분류코드 (코스피, 코스닥: 업종분류코드)

        Returns:
            InvestorTradingTrendByMarketDaily: 시장별 투자자매매동향(일별) 응답 객체
        """
        headers = {
            "tr_id": "FHPTJ04040000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_ISCD_1": fid_input_iscd_1,
            "FID_INPUT_DATE_2": fid_input_date_2,
            "FID_INPUT_ISCD_2": fid_input_iscd_2,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-investor-daily-by-market", headers=headers, params=params
        )
        return InvestorTradingTrendByMarketDaily.model_validate(response.json())

    def get_foreign_net_buy_trend_by_stock(
        self, fid_input_iscd: str, fid_input_iscd_2: str, fid_cond_mrkt_div_code: str
    ) -> ForeignNetBuyTrendByStock:
        """
        종목별 외국계 순매수추이

        Args:
            fid_input_iscd (str): 조건시장분류코드 (종목코드, 예: 005930 삼성전자)
            fid_input_iscd_2 (str): 조건화면분류코드 (외국계 전체: 99999)
            fid_cond_mrkt_div_code (str): 시장구분코드 (J, KRX만 지원)

        Returns:
            ForeignNetBuyTrendByStock: 종목별 외국계 순매수추이 응답 객체
        """
        headers = {
            "tr_id": "FHKST644400C0",
        }
        params = {
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_ISCD_2": fid_input_iscd_2,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/frgnmem-pchs-trend", headers=headers, params=params
        )
        return ForeignNetBuyTrendByStock.model_validate(response.json())

    def get_member_trading_trend_tick(
        self,
        fid_cond_scr_div_code: str,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_input_iscd_2: str,
        fid_mrkt_cls_code: str,
        fid_vol_cnt: str,
    ) -> MemberTradingTrendTick:
        """
        회원사 실시간 매매동향(틱)

        Args:
            fid_cond_scr_div_code (str): 화면분류코드 (20432, primary key)
            fid_cond_mrkt_div_code (str): FID 조건 시장 분류 코드 (J 고정 입력)
            fid_input_iscd (str): 종목코드 (예: 005930 삼성전자, FID_INPUT_ISCD 또는 FID_MRKT_CLS_CODE 둘 중 하나만 입력)
            fid_input_iscd_2 (str): 회원사코드 (예: 99999 전체)
            fid_mrkt_cls_code (str): 시장구분코드 (A: 전체, K: 코스피, Q: 코스닥, K2: 코스피200, W: ELW, FID_INPUT_ISCD 또는 FID_MRKT_CLS_CODE 둘 중 하나만 입력)
            fid_vol_cnt (str): 거래량 (거래량 ~)

        Returns:
            MemberTradingTrendTick: 회원사 실시간 매매동향(틱) 응답 객체
        """
        headers = {
            "tr_id": "FHPST04320000",
        }
        params = {
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_ISCD_2": fid_input_iscd_2,
            "FID_MRKT_CLS_CODE": fid_mrkt_cls_code,
            "FID_VOL_CNT": fid_vol_cnt,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/frgnmem-trade-trend", headers=headers, params=params
        )
        return MemberTradingTrendTick.model_validate(response.json())

    def get_member_trading_trend_by_stock(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_input_iscd_2: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
        fid_sctn_cls_code: str,
    ) -> MemberTradingTrendByStock:
        """
        주식현재가 회원사 종목매매동향

        Args:
            fid_cond_mrkt_div_code (str): 조건시장분류코드 (J: KRX, NX: NXT, UN: 통합)
            fid_input_iscd (str): 입력종목코드 (주식종목코드입력)
            fid_input_iscd_2 (str): 회원사코드
            fid_input_date_1 (str): 입력날짜1 (날짜 ~)
            fid_input_date_2 (str): 입력날짜2 (~ 날짜)
            fid_sctn_cls_code (str): 구간구분코드 (공백)

        Returns:
            MemberTradingTrendByStock: 주식현재가 회원사 종목매매동향 응답 객체
        """
        headers = {
            "tr_id": "FHPST04540000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_ISCD_2": fid_input_iscd_2,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_DATE_2": fid_input_date_2,
            "FID_SCTN_CLS_CODE": fid_sctn_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-member-daily", headers=headers, params=params
        )
        return MemberTradingTrendByStock.model_validate(response.json())

    def get_program_trading_trend_by_stock_intraday(
        self, fid_cond_mrkt_div_code: str, fid_input_iscd: str
    ) -> ProgramTradingTrendByStockIntraday:
        """
        종목별 프로그램매매추이(체결)

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (KRX: J, NXT: NX, 통합: UN)
            fid_input_iscd (str): 입력 종목코드

        Returns:
            ProgramTradingTrendByStockIntraday: 종목별 프로그램매매추이(체결) 응답 객체
        """
        headers = {
            "tr_id": "FHPPG04650101",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/program-trade-by-stock", headers=headers, params=params
        )
        return ProgramTradingTrendByStockIntraday.model_validate(response.json())

    def get_program_trading_trend_by_stock_daily(
        self, fid_cond_mrkt_div_code: str, fid_input_iscd: str, fid_input_date_1: str
    ) -> ProgramTradingTrendByStockDaily:
        """
        종목별 프로그램매매추이(일별)

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (KRX: J, NXT: NX, 통합: UN)
            fid_input_iscd (str): 입력 종목코드
            fid_input_date_1 (str): 입력 날짜1 (기준일, 예: 0020240308, 미입력시 당일부터 조회)

        Returns:
            ProgramTradingTrendByStockDaily: 종목별 프로그램매매추이(일별) 응답 객체
        """
        headers = {
            "tr_id": "FHPPG04650201",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/program-trade-by-stock-daily", headers=headers, params=params
        )
        return ProgramTradingTrendByStockDaily.model_validate(response.json())

    def get_foreign_institutional_estimate_by_stock(self, mksc_shrn_iscd: str) -> ForeignInstitutionalEstimateByStock:
        """
        종목별 외인기관 추정기전계

        Args:
            mksc_shrn_iscd (str): 종목코드

        Returns:
            ForeignInstitutionalEstimateByStock: 종목별 외인기관 추정기전계 응답 객체
        """
        headers = {
            "tr_id": "HHPTJ04160200",
        }
        params = {
            "MKSC_SHRN_ISCD": mksc_shrn_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/investor-trend-estimate", headers=headers, params=params
        )
        return ForeignInstitutionalEstimateByStock.model_validate(response.json())

    def get_buy_sell_volume_by_stock_daily(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
        fid_period_div_code: str,
    ) -> BuySellVolumeByStockDaily:
        """
        종목별일별매수매도체결량

        Args:
            fid_cond_mrkt_div_code (str): FID 조건 시장 분류 코드 (J: KRX, NX: NXT, UN: 통합)
            fid_input_iscd (str): FID 입력 종목코드 (예: 005930)
            fid_input_date_1 (str): FID 입력 날짜1 (from)
            fid_input_date_2 (str): FID 입력 날짜2 (to)
            fid_period_div_code (str): FID 기간 분류 코드 (D)

        Returns:
            BuySellVolumeByStockDaily: 종목별일별매수매도체결량 응답 객체
        """
        headers = {
            "tr_id": "FHKST03010800",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_DATE_2": fid_input_date_2,
            "FID_PERIOD_DIV_CODE": fid_period_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-daily-trade-volume", headers=headers, params=params
        )
        return BuySellVolumeByStockDaily.model_validate(response.json())

    def get_program_trading_summary_intraday(
        self,
        fid_cond_mrkt_div_code: str,
        fid_mrkt_cls_code: str,
        fid_sctn_cls_code: str,
        fid_input_iscd: str,
        fid_cond_mrkt_div_code1: str,
        fid_input_hour_1: str,
    ) -> ProgramTradingSummaryIntraday:
        """
        프로그램매매 종합현황(시간)

        Args:
            fid_cond_mrkt_div_code (str): 시장 분류 코드 (KRX: J, NXT: NX, 통합: UN)
            fid_mrkt_cls_code (str): 시장 구분 코드 (K: 코스피, Q: 코스닥)
            fid_sctn_cls_code (str): 구간 구분 코드 (공백 입력)
            fid_input_iscd (str): 입력 종목코드 (공백 입력)
            fid_cond_mrkt_div_code1 (str): 시장 분류코드1 (공백 입력)
            fid_input_hour_1 (str): 입력 시간1 (공백 입력)

        Returns:
            ProgramTradingSummaryIntraday: 프로그램매매 종합현황(시간) 응답 객체
        """
        headers = {
            "tr_id": "FHPPG04600101",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_MRKT_CLS_CODE": fid_mrkt_cls_code,
            "FID_SCTN_CLS_CODE": fid_sctn_cls_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_MRKT_DIV_CODE1": fid_cond_mrkt_div_code1,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/comp-program-trade-today", headers=headers, params=params
        )
        return ProgramTradingSummaryIntraday.model_validate(response.json())

    def get_program_trading_summary_daily(
        self,
        fid_cond_mrkt_div_code: str,
        fid_mrkt_cls_code: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
    ) -> ProgramTradingSummaryDaily:
        """
        프로그램매매 종합현황(일별)

        Args:
            fid_cond_mrkt_div_code (str): 시장 분류 코드 (J: KRX, NX: NXT, UN: 통합)
            fid_mrkt_cls_code (str): 시장 구분 코드 (K: 코스피, Q: 코스닥)
            fid_input_date_1 (str): 검색시작일 (공백 입력, 입력 시 ~ 입력일자까지 조회됨, 8개월 이상 과거 조회 불가)
            fid_input_date_2 (str): 검색종료일 (공백 입력)

        Returns:
            ProgramTradingSummaryDaily: 프로그램매매 종합현황(일별) 응답 객체
        """
        headers = {
            "tr_id": "FHPPG04600001",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_MRKT_CLS_CODE": fid_mrkt_cls_code,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_DATE_2": fid_input_date_2,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/comp-program-trade-daily", headers=headers, params=params
        )
        return ProgramTradingSummaryDaily.model_validate(response.json())

    def get_program_trading_investor_trend_today(
        self, exch_div_cls_code: str, mrkt_div_cls_code: str
    ) -> ProgramTradingInvestorTrendToday:
        """
        프로그램매매 투자자매매동향(당일)

        Args:
            exch_div_cls_code (str): 거래소 구분 코드 (J: KRX, NX: NXT, UN: 통합)
            mrkt_div_cls_code (str): 시장 구분 코드 (1: 코스피, 4: 코스닥)

        Returns:
            ProgramTradingInvestorTrendToday: 프로그램매매 투자자매매동향(당일) 응답 객체
        """
        headers = {
            "tr_id": "HHPPG046600C1",
        }
        params = {
            "EXCH_DIV_CLS_CODE": exch_div_cls_code,
            "MRKT_DIV_CLS_CODE": mrkt_div_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/investor-program-trade-today", headers=headers, params=params
        )
        return ProgramTradingInvestorTrendToday.model_validate(response.json())

    def get_credit_balance_trend_daily(
        self,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_input_date_1: str,
    ) -> CreditBalanceTrendDaily:
        """
        국내주식 신용잔고 일별추이

        Args:
            fid_cond_mrkt_div_code (str): 시장 분류 코드 (시장구분코드: 주식 J)
            fid_cond_scr_div_code (str): 화면 분류 코드 (Unique key: 20476)
            fid_input_iscd (str): 종목코드 (예: 005930)
            fid_input_date_1 (str): 결제일자 (예: 20240313)

        Returns:
            CreditBalanceTrendDaily: 국내주식 신용잔고 일별추이 응답 객체
        """
        headers = {
            "tr_id": "FHPST04760000",
        }
        params = {
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_input_date_1": fid_input_date_1,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/daily-credit-balance", headers=headers, params=params
        )
        return CreditBalanceTrendDaily.model_validate(response.json())

    def get_expected_price_trend(
        self, fid_mkop_cls_code: str, fid_cond_mrkt_div_code: str, fid_input_iscd: str
    ) -> ExpectedPriceTrend:
        """
        국내주식 예상체결가 추이

        Args:
            fid_mkop_cls_code (str): 장운영 구분 코드 (0: 전체, 4: 체결량 0 제외)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (시장구분코드: 주식 J)
            fid_input_iscd (str): 입력 종목코드 (예: 005930)

        Returns:
            ExpectedPriceTrend: 국내주식 예상체결가 추이 응답 객체
        """
        headers = {
            "tr_id": "FHPST01810000",
        }
        params = {
            "fid_mkop_cls_code": fid_mkop_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_input_iscd": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/exp-price-trend", headers=headers, params=params
        )
        return ExpectedPriceTrend.model_validate(response.json())

    def get_short_selling_trend_daily(
        self,
        fid_input_date_2: str,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_input_date_1: str,
    ) -> ShortSellingTrendDaily:
        """
        국내주식 공매도 일별추이

        Args:
            fid_input_date_2 (str): 입력 날짜2 (~ 누적)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (시장구분코드: 주식 J)
            fid_input_iscd (str): 입력 종목코드
            fid_input_date_1 (str): 입력 날짜1 (공백시 전체, 기간 ~)

        Returns:
            ShortSellingTrendDaily: 국내주식 공매도 일별추이 응답 객체
        """
        headers = {
            "tr_id": "FHPST04830000",
        }
        params = {
            "FID_INPUT_DATE_2": fid_input_date_2,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/daily-short-sale", headers=headers, params=params
        )
        return ShortSellingTrendDaily.model_validate(response.json())

    def get_after_hours_expected_fluctuation(
        self,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_rank_sort_cls_code: str,
        fid_div_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_input_vol_1: str,
    ) -> AfterHoursExpectedFluctuation:
        """
        국내주식 시간외예상체결등락율

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (시장구분코드: J 주식)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (Unique key: 11186)
            fid_input_iscd (str): 입력 종목코드 (0000: 전체, 0001: 코스피, 1001: 코스닥)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0: 상승률, 1: 상승폭, 2: 보합, 3: 하락률, 4: 하락폭)
            fid_div_cls_code (str): 분류 구분 코드 (0: 전체, 1: 관리종목, 2: 투자주의, 3: 투자경고, 4: 투자위험예고, 5: 투자위험, 6: 보통주, 7: 우선주)
            fid_input_price_1 (str): 입력 가격1 (가격 ~)
            fid_input_price_2 (str): 입력 가격2 (공백)
            fid_input_vol_1 (str): 입력 거래량 (거래량 ~)

        Returns:
            AfterHoursExpectedFluctuation: 국내주식 시간외예상체결등락율 응답 객체
        """
        headers = {
            "tr_id": "FHKST11860000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_RANK_SORT_CLS_CODE": fid_rank_sort_cls_code,
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "FID_INPUT_PRICE_1": fid_input_price_1,
            "FID_INPUT_PRICE_2": fid_input_price_2,
            "FID_INPUT_VOL_1": fid_input_vol_1,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/ranking/overtime-exp-trans-fluct", headers=headers, params=params
        )
        return AfterHoursExpectedFluctuation.model_validate(response.json())

    def get_trading_weight_by_amount(
        self, fid_cond_mrkt_div_code: str, fid_cond_scr_div_code: str, fid_input_iscd: str
    ) -> TradingWeightByAmount:
        """
        국내주식 체결금액별 매매비중

        Args:
            fid_cond_mrkt_div_code (str): 조건시장분류코드 (J: KRX, NX: NXT, UN: 통합)
            fid_cond_scr_div_code (str): 조건화면분류코드 (Uniquekey: 11119)
            fid_input_iscd (str): 입력종목코드 (예: 005930 삼성전자)

        Returns:
            TradingWeightByAmount: 국내주식 체결금액별 매매비중 응답 객체
        """
        headers = {
            "tr_id": "FHKST111900C0",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/tradprt-byamt", headers=headers, params=params)
        return TradingWeightByAmount.model_validate(response.json())

    def get_market_fund_summary(self, fid_input_date_1: str) -> MarketFundSummary:
        """
        국내 증시자금 종합

        Args:
            fid_input_date_1 (str): 입력날짜1

        Returns:
            MarketFundSummary: 국내 증시자금 종합 응답 객체
        """
        headers = {
            "tr_id": "FHKST649100C0",
        }
        params = {
            "FID_INPUT_DATE_1": fid_input_date_1,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/mktfunds", headers=headers, params=params)
        return MarketFundSummary.model_validate(response.json())

    def get_stock_loan_trend_daily(
        self, mrkt_div_cls_code: str, mksc_shrn_iscd: str, start_date: str, end_date: str, cts: str
    ) -> StockLoanTrendDaily:
        """
        종목별 일별 대차거래추이

        Args:
            mrkt_div_cls_code (str): 조회구분 (1: 코스피, 2: 코스닥, 3: 종목)
            mksc_shrn_iscd (str): 종목코드
            start_date (str): 조회시작일시 (조회기간 ~)
            end_date (str): 조회종료일시 (~ 조회기간)
            cts (str): 이전조회KEY

        Returns:
            StockLoanTrendDaily: 종목별 일별 대차거래추이 응답 객체
        """
        headers = {
            "tr_id": "HHPST074500C0",
        }
        params = {
            "MRKT_DIV_CLS_CODE": mrkt_div_cls_code,
            "MKSC_SHRN_ISCD": mksc_shrn_iscd,
            "START_DATE": start_date,
            "END_DATE": end_date,
            "CTS": cts,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/daily-loan-trans", headers=headers, params=params
        )
        return StockLoanTrendDaily.model_validate(response.json())

    def get_limit_price_stocks(
        self,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_prc_cls_code: str,
        fid_div_cls_code: str,
        fid_input_iscd: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
    ) -> LimitPriceStocks:
        """
        국내주식 상하한가 표착

        Args:
            fid_cond_mrkt_div_code (str): 조건시장분류코드 (시장구분: J)
            fid_cond_scr_div_code (str): 조건화면분류코드 (11300, Unique key)
            fid_prc_cls_code (str): 상하한가 구분코드 (0: 상한가, 1: 하한가)
            fid_div_cls_code (str): 분류구분코드 (0: 상하한가종목, 6: 8%상하한가 근접, 5: 10%상하한가 근접, 1: 15%상하한가 근접, 2: 20%상하한가 근접, 3: 25%상하한가 근접)
            fid_input_iscd (str): 입력종목코드 (전체: 0000, 코스피: 0001, 코스닥: 1001)
            fid_trgt_cls_code (str): 대상구분코드 (공백 입력)
            fid_trgt_exls_cls_code (str): 대상제외구분코드 (공백 입력)
            fid_input_price_1 (str): 입력가격1 (공백 입력)
            fid_input_price_2 (str): 입력가격2 (공백 입력)
            fid_vol_cnt (str): 거래량수 (공백 입력)

        Returns:
            LimitPriceStocks: 국내주식 상하한가 표착 응답 객체
        """
        headers = {
            "tr_id": "FHKST130000C0",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_PRC_CLS_CODE": fid_prc_cls_code,
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_TRGT_CLS_CODE": fid_trgt_cls_code,
            "FID_TRGT_EXLS_CLS_CODE": fid_trgt_exls_cls_code,
            "FID_INPUT_PRICE_1": fid_input_price_1,
            "FID_INPUT_PRICE_2": fid_input_price_2,
            "FID_VOL_CNT": fid_vol_cnt,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/capture-uplowprice", headers=headers, params=params
        )
        return LimitPriceStocks.model_validate(response.json())

    def get_resistance_level_trading_weight(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_cond_scr_div_code: str,
        fid_input_hour_1: str,
    ) -> ResistanceLevelTradingWeight:
        """
        국내주식 매물대/거래비중

        Args:
            fid_cond_mrkt_div_code (str): 조건시장분류코드 (J: KRX, NX: NXT, UN: 통합)
            fid_input_iscd (str): 입력종목코드 (주식단축종목코드)
            fid_cond_scr_div_code (str): 조건화면분류코드 (Uniquekey: 20113)
            fid_input_hour_1 (str): 입력시간1 (공백)

        Returns:
            ResistanceLevelTradingWeight: 국내주식 매물대/거래비중 응답 객체
        """
        headers = {
            "tr_id": "FHPST01130000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/pbar-tratio", headers=headers, params=params)
        return ResistanceLevelTradingWeight.model_validate(response.json())
