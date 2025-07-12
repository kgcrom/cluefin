from typing import Literal, Optional

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_account_types import (
    DomesticAccountAvailableOrderQuantityByMarginLoanStock,
    DomesticAccountAvailableOrderQuantityByMarginRate,
    DomesticAccountAvailableWithdrawalAmount,
    DomesticAccountConsignmentComprehensiveTransactionHistory,
    DomesticAccountCurrentDayStatus,
    DomesticAccountCurrentDayTradingJournal,
    DomesticAccountDailyEstimatedDepositAssetBalance,
    DomesticAccountDailyProfitRateDetails,
    DomesticAccountDailyRealizedProfitLoss,
    DomesticAccountDailyRealizedProfitLossDetails,
    DomesticAccountDailyStockRealizedProfitLossByDate,
    DomesticAccountDailyStockRealizedProfitLossByPeriod,
    DomesticAccountDepositBalanceDetails,
    DomesticAccountEstimatedAssetBalance,
    DomesticAccountEvaluationBalanceDetails,
    DomesticAccountEvaluationStatus,
    DomesticAccountExecuted,
    DomesticAccountExecutionBalance,
    DomesticAccountMarginDetails,
    DomesticAccountNextDaySettlementDetails,
    DomesticAccountOrderExecutionDetails,
    DomesticAccountOrderExecutionStatus,
    DomesticAccountProfitRate,
    DomesticAccountUnexecuted,
    DomesticAccountUnexecutedSplitOrderDetails,
)
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticAccount:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/dostk/acnt"

    def get_daily_stock_realized_profit_loss_by_date(
        self,
        stk_cd: str,
        strt_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountDailyStockRealizedProfitLossByDate]:
        """일자별 종목별 실현 손익 요청 (일자)

        Args:
            stk_cd (str): 종목 코드 (6자리)
            strt_dt (str): 시작 일자 (YYYYMMDD)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountDailyStockRealizedProfitLossByDate]: 일자별 종목별 실현 손익 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10072",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountDailyStockRealizedProfitLossByDate.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_stock_realized_profit_loss_by_period(
        self,
        stk_cd: str,
        strt_dt: str,
        end_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountDailyStockRealizedProfitLossByPeriod]:
        """일자별 종목별 실현 손익 요청 (기간)

        Args:
            stk_cd (str): 종목 코드 (6자리)
            strt_dt (str): 시작 일자 (YYYYMMDD)
            end_dt (str): 종료 일자 (YYYYMMDD)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountDailyStockRealizedProfitLossByPeriod]: 일자별 종목별 실현 손익 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10073",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "end_dt": end_dt,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountDailyStockRealizedProfitLossByPeriod.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_realized_profit_loss(
        self,
        strt_dt: str,
        end_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountDailyRealizedProfitLoss]:
        """일자별 실현 손익 요청

        Args:
            strt_dt (str): 시작 일자 (YYYYMMDD)
            end_dt (str): 종료 일자 (YYYYMMDD)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountDailyRealizedProfitLoss]: 일자별 실현 손익 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10074",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountDailyRealizedProfitLoss.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_unexecuted(
        self,
        all_stk_tp: str,
        trde_tp: str,
        stex_tp: str,
        stk_cd: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountUnexecuted]:
        """미체결 요청

        Args:
            all_stk_tp (str): 전체종목구분 (0:전체, 1:종목)
            trde_tp (str): 매매구분 (0:전체, 1:매도, 2:매수)
            stex_tp (str): 거래소구분 (0:통합, 1:KRX, 2:NXT)
            stk_cd (Optional[str], optional): 종목코드. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountUnexecuted]: 미체결 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10075",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "all_stk_tp": all_stk_tp,
            "trde_tp": trde_tp,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd if stk_cd else "",
        }

        if stk_cd:
            body["stk_cd"] = stk_cd

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountUnexecuted.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_executed(
        self,
        qry_tp: str,
        sell_tp: str,
        stex_tp: str,
        stk_cd: Optional[str] = None,
        ord_no: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountExecuted]:
        """체결 요청

        Args:
            qry_tp (str): 조회구분 (0:전체, 1:종목)
            sell_tp (str): 매도수구분 (0:전체, 1:매도, 2:매수)
            stex_tp (str): 거래소구분 (0:통합, 1:KRX, 2:NXT)
            stk_cd (Optional[str], optional): 종목코드. Defaults to None.
            ord_no (Optional[str], optional): 주문번호. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountExecuted]: 체결 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10076",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "qry_tp": qry_tp,
            "sell_tp": sell_tp,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd if stk_cd else "",
            "ord_no": ord_no if ord_no else "",
        }

        if stk_cd:
            body["stk_cd"] = stk_cd

        if ord_no:
            body["ord_no"] = ord_no

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountExecuted.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_realized_profit_loss_details(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountDailyRealizedProfitLossDetails]:
        """당일실현손익상세요청

        Args:
            stk_cd (str): 종목코드 (6자리)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountDailyRealizedProfitLossDetails]: 당일실현손익상세 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10077",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountDailyRealizedProfitLossDetails.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_account_profit_rate(
        self,
        stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountProfitRate]:
        """계좌수익률요청

        Args:
            stex_tp (str): 거래소구분 (0:통합, 1:KRX, 2:NXT)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountProfitRate]: 계좌수익률 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10085",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "stex_tp": stex_tp,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountProfitRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_unexecuted_split_order_details(
        self,
        ord_no: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountUnexecutedSplitOrderDetails]:
        """미체결분할주문상세

        Args:
            ord_no (str): 주문번호 (20자리)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountUnexecutedSplitOrderDetails]: 미체결분할주문상세 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10088",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "ord_no": ord_no,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountUnexecutedSplitOrderDetails.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_current_day_trading_journal(
        self,
        ottks_tp: str,
        ch_crd_tp: str,
        base_dt: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountCurrentDayTradingJournal]:
        """당일매매일지조회

        Args:
            ottks_tp (str): 단주구분 (1:당일매수에 대한 당일매도, 2:당일매도 전체)
            ch_crd_tp (str): 현금신용구분 (0:전체, 1:현금매매만, 2:신용매매만)
            base_dt (Optional[str], optional): 기준일자 YYYYMMDD (공백입력시 금일데이터, 최근 2개월까지 제공). Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountCurrentDayTradingJournal]: 당일매매일지 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10170",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "ottks_tp": ottks_tp,
            "ch_crd_tp": ch_crd_tp,
        }

        if base_dt:
            body["base_dt"] = base_dt

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountCurrentDayTradingJournal.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_deposit_balance_details(
        self,
        qry_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountDepositBalanceDetails]:
        """예수금상세현황요청

        Args:
            qry_tp (str): 조회구분 (3:추정조회, 2:일반조회)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountDepositBalanceDetails]: 예수금상세현황 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00001",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "qry_tp": qry_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountDepositBalanceDetails.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_estimated_deposit_asset_balance(
        self,
        start_dt: str,
        end_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountDailyEstimatedDepositAssetBalance]:
        """일별추정예탁자산현황요청

        Args:
            start_dt (str): 시작조회기간 (YYYYMMDD)
            end_dt (str): 종료조회기간 (YYYYMMDD)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountDailyEstimatedDepositAssetBalance]: 일별추정예탁자산현황 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00002",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "start_dt": start_dt,
            "end_dt": end_dt,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountDailyEstimatedDepositAssetBalance.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_estimated_asset_balance(
        self,
        qry_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountEstimatedAssetBalance]:
        """추정자산조회요청

        Args:
            qry_tp (str): 상장폐지조회구분 (0:전체, 1:상장폐지종목제외)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountEstimatedAssetBalance]: 추정자산 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00003",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "qry_tp": qry_tp,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountEstimatedAssetBalance.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_account_evaluation_status(
        self,
        qry_tp: str,
        dmst_stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountEvaluationStatus]:
        """계좌평가현황요청

        Args:
            qry_tp (str): 상장폐지조회구분 (0:전체, 1:상장폐지종목제외)
            dmst_stex_tp (str): 국내거래소구분 (KRX:한국거래소, NXT:넥스트트레이드)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountEvaluationStatus]: 계좌평가현황 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00004",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "qry_tp": qry_tp,
            "dmst_stex_tp": dmst_stex_tp,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountEvaluationStatus.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_execution_balance(
        self,
        dmst_stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountExecutionBalance]:
        """체결잔고요청

        Args:
            dmst_stex_tp (str): 국내거래소구분 (KRX:한국거래소, NXT:넥스트트레이드)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountExecutionBalance]: 체결잔고 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00005",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "dmst_stex_tp": dmst_stex_tp,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountExecutionBalance.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_account_order_execution_details(
        self,
        qry_tp: str,
        stk_bond_tp: str,
        sell_tp: str,
        dmst_stex_tp: str,
        ord_dt: str = "",
        stk_cd: str = "",
        fr_ord_no: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountOrderExecutionDetails]:
        """계좌별주문체결내역상세요청

        Args:
            qry_tp (str): 조회구분 (1:주문순, 2:역순, 3:미체결, 4:체결내역만)
            stk_bond_tp (str): 주식채권구분 (0:전체, 1:주식, 2:채권)
            sell_tp (str): 매도수구분 (0:전체, 1:매도, 2:매수)
            dmst_stex_tp (str): 국내거래소구분 (%:(전체), KRX:한국거래소, NXT:넥스트트레이드, SOR:최선주문집행)
            ord_dt (str): 주문일자 (YYYYMMDD). Defaults to "".
            stk_cd (str): 종목코드. Defaults to "".
            fr_ord_no (str): 시작주문번호. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountOrderExecutionDetails]: 계좌별주문체결내역상세 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00007",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "qry_tp": qry_tp,
            "stk_bond_tp": stk_bond_tp,
            "sell_tp": sell_tp,
            "dmst_stex_tp": dmst_stex_tp,
            "ord_dt": ord_dt,
            "stk_cd": stk_cd,
            "fr_ord_no": fr_ord_no,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountOrderExecutionDetails.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_account_next_day_settlement_details(
        self,
        strt_dcd_seq: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountNextDaySettlementDetails]:
        """계좌별익일결제예정내역요청

        Args:
            strt_dcd_seq (str, optional): 시작결제번호. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountNextDaySettlementDetails]: 계좌별익일결제예정내역 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00008",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "strt_dcd_seq": strt_dcd_seq,
        }

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountNextDaySettlementDetails.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_account_order_execution_status(
        self,
        stk_bond_tp: str,
        mrkt_tp: str,
        sell_tp: str,
        qry_tp: str,
        dmst_stex_tp: str,
        ord_dt: Optional[str] = None,
        stk_cd: Optional[str] = None,
        fr_ord_no: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountOrderExecutionStatus]:
        """계좌별주문체결현황요청

        Args:
            stk_bond_tp (str): 주식채권구분 (0:전체, 1:주식, 2:채권)
            mrkt_tp (str): 시장구분 (0:전체, 1:코스피, 2:코스닥, 3:OTCBB, 4:ECN)
            sell_tp (str): 매도수구분 (0:전체, 1:매도, 2:매수)
            qry_tp (str): 조회구분 (0:전체, 1:체결)
            dmst_stex_tp (str): 국내거래소구분 (%:(전체), KRX:한국거래소, NXT:넥스트트레이드, SOR:최선주문집행)
            ord_dt (Optional[str], optional): 주문일자 (YYYYMMDD). Defaults to None.
            stk_cd (Optional[str], optional): 종목코드. Defaults to None.
            fr_ord_no (Optional[str], optional): 시작주문번호. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountOrderExecutionStatus]: 계좌별주문체결현황 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00009",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "stk_bond_tp": stk_bond_tp,
            "mrkt_tp": mrkt_tp,
            "sell_tp": sell_tp,
            "qry_tp": qry_tp,
            "dmst_stex_tp": dmst_stex_tp,
        }

        if ord_dt:
            body["ord_dt"] = ord_dt

        if stk_cd:
            body["stk_cd"] = stk_cd

        if fr_ord_no:
            body["fr_ord_no"] = fr_ord_no

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountOrderExecutionStatus.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_available_withdrawal_amount(
        self,
        stk_cd: str,
        trde_tp: str,
        uv: str,
        io_amt: Optional[str] = None,
        trde_qty: Optional[str] = None,
        exp_buy_unp: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountAvailableWithdrawalAmount]:
        """주문인출가능금액요청

        Args:
            stk_cd (str): 종목번호
            trde_tp (str): 매매구분 (1:매도, 2:매수)
            uv (str): 매수가격
            io_amt (Optional[str], optional): 입출금액. Defaults to None.
            trde_qty (Optional[str], optional): 매매수량. Defaults to None.
            exp_buy_unp (Optional[str], optional): 예상매수단가. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountAvailableWithdrawalAmount]: 주문인출가능금액 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00010",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "stk_cd": stk_cd,
            "trde_tp": trde_tp,
            "uv": uv,
        }

        if io_amt:
            body["io_amt"] = io_amt

        if trde_qty:
            body["trde_qty"] = trde_qty

        if exp_buy_unp:
            body["exp_buy_unp"] = exp_buy_unp

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountAvailableWithdrawalAmount.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_available_order_quantity_by_margin_rate(
        self,
        stk_cd: str,
        uv: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountAvailableOrderQuantityByMarginRate]:
        """증거금율별주문가능수량조회요청

        Args:
            stk_cd (str): 종목번호
            uv (Optional[str], optional): 매수가격. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountAvailableOrderQuantityByMarginRate]: 증거금율별주문가능수량 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00011",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "stk_cd": stk_cd,
        }

        if uv:
            body["uv"] = uv

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountAvailableOrderQuantityByMarginRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_available_order_quantity_by_margin_loan_stock(
        self,
        stk_cd: str,
        uv: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountAvailableOrderQuantityByMarginLoanStock]:
        """신용융자증권별주문가능수량요청

        Args:
            stk_cd (str): 종목번호
            uv (Optional[str], optional): 매수가격. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountAvailableOrderQuantityByMarginLoanStock]: 신용융자증권별주문가능수량 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00012",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "stk_cd": stk_cd,
        }

        if uv:
            body["uv"] = uv

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountAvailableOrderQuantityByMarginLoanStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_margin_details(
        self,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountMarginDetails]:
        """증거금세부내역조회요청
        Args:
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountMarginDetails]: 증거금세부내역 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00013",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        response = self.client._post(self.path, headers, {})

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountMarginDetails.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_consignment_comprehensive_transaction_history(
        self,
        strt_dt: str,
        end_dt: str,
        tp: str,
        gds_tp: str,
        dmst_stex_tp: str,
        stk_cd: Optional[str] = None,
        crnc_cd: Optional[str] = None,
        frgn_stex_code: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountConsignmentComprehensiveTransactionHistory]:
        """위탁종합거래내역요청

        Args:
            strt_dt (str): 시작일자
            end_dt (str): 종료일자
            tp (str): 구분 (0:전체,1:입출금,2:입출고,3:매매,4:매수,5:매도,6:입금,7:출금,A:예탁담보대출입금,B:매도담보대출입금,C:현금상환(융자,담보상환),F:환전,M:입출금+환전,G:외화매수,H:외화매도,I:환전정산입금,J:환전정산출금)
            gds_tp (str): 상품구분 (0:전체, 1:국내주식, 2:수익증권, 3:해외주식, 4:금융상품)
            dmst_stex_tp (str): 국내거래소구분 (%:(전체),KRX:한국거래소,NXT:넥스트트레이드)
            stk_cd (Optional[str], optional): 종목코드. Defaults to None.
            crnc_cd (Optional[str], optional): 통화코드. Defaults to None.
            frgn_stex_code (Optional[str], optional): 해외거래소코드. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountConsignmentComprehensiveTransactionHistory]: 위탁종합거래내역 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00015",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "tp": tp,
            "gds_tp": gds_tp,
            "dmst_stex_tp": dmst_stex_tp,
        }

        if stk_cd:
            body["stk_cd"] = stk_cd

        if crnc_cd:
            body["crnc_cd"] = crnc_cd

        if frgn_stex_code:
            body["frgn_stex_code"] = frgn_stex_code

        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountConsignmentComprehensiveTransactionHistory.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_account_profit_rate_details(
        self,
        fr_dt: str,
        to_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountDailyProfitRateDetails]:
        """일별계좌수익률상세현황요청

        Args:
            fr_dt (str): 평가시작일
            to_dt (str): 평가종료일
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountDailyProfitRateDetails]: 일별계좌수익률상세현황 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00016",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "fr_dt": fr_dt,
            "to_dt": to_dt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountDailyProfitRateDetails.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_account_current_day_status(
        self,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountCurrentDayStatus]:
        """계좌별당일현황요청

        Args:
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountCurrentDayStatus]: 계좌별당일현황 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00017",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        response = self.client._post(self.path, headers, {})

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountCurrentDayStatus.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_account_evaluation_balance_details(
        self,
        qry_tp: str,
        dmst_stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticAccountEvaluationBalanceDetails]:
        """계좌평가잔고내역요청

        Args:
            qry_tp (str): 조회구분 (1:합산, 2:개별)
            dmst_stex_tp (str): 국내거래소구분 (KRX:한국거래소,NXT:넥스트트레이드)
            cont_yn (Literal["Y", "N"], optional): 연속 조회 여부. Defaults to "N".
            next_key (str, optional): 다음 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticAccountEvaluationBalanceDetails]: 계좌평가잔고내역 데이터
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "kt00018",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "qry_tp": qry_tp,
            "dmst_stex_tp": dmst_stex_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticAccountEvaluationBalanceDetails.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)
