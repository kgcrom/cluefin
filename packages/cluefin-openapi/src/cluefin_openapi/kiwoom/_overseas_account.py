from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_account_types import (
    OverseasAccountDailyOrderExecutionHistory,
    OverseasAccountDailyProfitRate,
    OverseasAccountDailyRealizedProfitLoss,
    OverseasAccountDailyRealizedProfitLossByStock,
    OverseasAccountDailyStockProfitRate,
    OverseasAccountDeposit,
    OverseasAccountDepositAndSecuritiesValuationByCurrency,
    OverseasAccountDepositAndSecuritiesValuationByCurrencyByDate,
    OverseasAccountDepositDetail,
    OverseasAccountKrwWithdrawableAmount,
    OverseasAccountLedgerBalance,
    OverseasAccountLedgerUnfilledOrders,
    OverseasAccountLedgerValuationAmount,
    OverseasAccountMonthlyProfitRate,
    OverseasAccountMonthlyRealizedProfitLoss,
    OverseasAccountMonthlyStockProfitRate,
    OverseasAccountOrderHistoryByPeriod,
    OverseasAccountProfitRateByPeriod,
    OverseasAccountRealizedProfitLoss,
    OverseasAccountTodayOrderExecution,
    OverseasAccountTodayRealizedProfitLoss,
    OverseasAccountTodayRealizedProfitLossByStock,
    OverseasAccountTodayTrading,
    OverseasAccountTodayTradingSummary,
    OverseasAccountTransactionHistory,
    OverseasAccountValuationAmountByDate,
    OverseasAccountYearlyProfitRate,
    OverseasAccountYearlyStockProfitRate,
)


class OverseasAccount:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/acnt"

    def get_daily_account_profit_rate(
        self,
        from_dt: str,
        to: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountDailyProfitRate]:
        """미국주식 일별계좌수익률현황 (usa21670)

        Args:
            from_dt (str): from 일자. YYYYMMDD
            to (str): to 일자. YYYYMMDD
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountDailyProfitRate]: 미국주식 일별계좌수익률현황 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa21670",
        }
        body = {
            "from": from_dt,
            "to": to,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily account profit rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountDailyProfitRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_monthly_account_profit_rate(
        self,
        from_dt: str,
        to: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountMonthlyProfitRate]:
        """미국주식 월별계좌수익률현황 (usa21680)

        Args:
            from_dt (str): from 년월. YYYYMM
            to (str): to 년월. YYYYMM
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountMonthlyProfitRate]: 미국주식 월별계좌수익률현황 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa21680",
        }
        body = {
            "from": from_dt,
            "to": to,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching monthly account profit rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountMonthlyProfitRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_account_profit_rate(
        self,
        from_dt: str,
        to: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountYearlyProfitRate]:
        """미국주식 연도별계좌수익률현황 (usa21690)

        Args:
            from_dt (str): from 년도. YYYY
            to (str): to 년도. YYYY
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountYearlyProfitRate]: 미국주식 연도별계좌수익률현황 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa21690",
        }
        body = {
            "from": from_dt,
            "to": to,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly account profit rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountYearlyProfitRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daily_stock_profit_rate(
        self,
        from_dt: str,
        to: str,
        stk_cd: str,
        stex_tp: Literal["", "NA", "ND", "NY"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountDailyStockProfitRate]:
        """미국주식 일별종목수익률현황 (usa21730)

        Args:
            from_dt (str): from 일자. YYYYMMDD
            to (str): to 일자. YYYYMMDD
            stk_cd (str): 종목코드
            stex_tp (Literal["", "NA", "ND", "NY"], optional): 거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountDailyStockProfitRate]: 미국주식 일별종목수익률현황 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa21730",
        }
        body = {
            "from": from_dt,
            "to": to,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily stock profit rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountDailyStockProfitRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_monthly_stock_profit_rate(
        self,
        from_dt: str,
        to: str,
        stk_cd: str,
        stex_tp: Literal["", "NA", "ND", "NY"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountMonthlyStockProfitRate]:
        """미국주식 월별종목수익률현황 (usa21731)

        Args:
            from_dt (str): from 년월. YYYYMM
            to (str): to 년월. YYYYMM
            stk_cd (str): 종목코드
            stex_tp (Literal["", "NA", "ND", "NY"], optional): 거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountMonthlyStockProfitRate]: 미국주식 월별종목수익률현황 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa21731",
        }
        body = {
            "from": from_dt,
            "to": to,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching monthly stock profit rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountMonthlyStockProfitRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_stock_profit_rate(
        self,
        from_dt: str,
        to: str,
        stk_cd: str,
        stex_tp: Literal["", "NA", "ND", "NY"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountYearlyStockProfitRate]:
        """미국주식 연도별종목수익률현황 (usa21732)

        Args:
            from_dt (str): from 년도. YYYY
            to (str): to 년도. YYYY
            stk_cd (str): 종목코드
            stex_tp (Literal["", "NA", "ND", "NY"], optional): 거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountYearlyStockProfitRate]: 미국주식 연도별종목수익률현황 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa21732",
        }
        body = {
            "from": from_dt,
            "to": to,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly stock profit rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountYearlyStockProfitRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_ledger_unfilled_orders(
        self,
        ord_dt: str = "",
        slby_tp: Literal["", "0", "1", "2"] = "",
        stex_tp: Literal["", "ND", "NY", "NA"] = "",
        stk_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountLedgerUnfilledOrders]:
        """미국주식 원장 미체결 (ust21050)

        Args:
            ord_dt (str, optional): 주문일자. 미입력시 오늘 날짜로 조회. Defaults to "".
            slby_tp (Literal["", "0", "1", "2"], optional): 매도매수구분. 0:전체(기본값),1:매도,2:매수. Defaults to "".
            stex_tp (Literal["", "ND", "NY", "NA"], optional): 거래소구분. 미입력시 전체, ND:NASDAQ,NY:NYSE,NA:AMEX. Defaults to "".
            stk_cd (str, optional): 종목코드. 미입력시 전체. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountLedgerUnfilledOrders]: 미국주식 원장 미체결 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21050",
        }
        body = {
            "ord_dt": ord_dt,
            "slby_tp": slby_tp,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ledger unfilled orders: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountLedgerUnfilledOrders.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_ledger_balance(
        self,
        stex_tp: Literal["", "ND", "NY", "NA"] = "",
        stk_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountLedgerBalance]:
        """미국주식 원장잔고확인 (ust21070)

        Args:
            stex_tp (Literal["", "ND", "NY", "NA"], optional): 거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX. Defaults to "".
            stk_cd (str, optional): 종목코드. 미입력시 전체. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountLedgerBalance]: 미국주식 원장잔고확인 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21070",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ledger balance: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountLedgerBalance.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_transaction_history(
        self,
        strt_dt: str = "",
        end_dt: str = "",
        tp: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "F", "M", "G", "H", "I", "J", "K"] = "",
        stex_tp: Literal["", "ND", "NY", "NA"] = "",
        stk_cd: str = "",
        krw_repl_skip_yn: Literal["", "Y", "N"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountTransactionHistory]:
        """미국주식 거래내역 (ust21100)

        Args:
            strt_dt (str, optional): 시작일자. YYYYMMDD. Defaults to "".
            end_dt (str, optional): 종료일자. YYYYMMDD. Defaults to "".
            tp (Literal, optional): 구분. 0:전체,1:입출금,2:입출고,3:매매,4:매수,5:매도,F:환전, M:입출금+환전(매체전용), G:환전매수, H:환전매도, I:환전정산입금, J:환전정산출금, 6:입금, 7:출금 8:배당금입금 K:환전+환전정산입출금. Defaults to "".
            stex_tp (Literal["", "ND", "NY", "NA"], optional): 거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX. Defaults to "".
            stk_cd (str, optional): 종목코드. Defaults to "".
            krw_repl_skip_yn (Literal["", "Y", "N"], optional): 원화대용입출금제외여부. Y:제외,N:비제외. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountTransactionHistory]: 미국주식 거래내역 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21100",
        }
        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "tp": tp,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "krw_repl_skip_yn": krw_repl_skip_yn,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching transaction history: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountTransactionHistory.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_deposit(
        self,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountDeposit]:
        """해외주식 예수금 (ust21110)

        Args:
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountDeposit]: 해외주식 예수금 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21110",
        }
        body: dict[str, str] = {}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching deposit: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountDeposit.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_krw_withdrawable_amount(
        self,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountKrwWithdrawableAmount]:
        """원화출금가능 금액 조회(원화대용 포함) (ust21111)

        Args:
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountKrwWithdrawableAmount]: 원화출금가능 금액 조회(원화대용 포함) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21111",
        }
        body: dict[str, str] = {}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching krw withdrawable amount: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountKrwWithdrawableAmount.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_deposit_and_securities_valuation_by_currency(
        self,
        cmsn_incl_tp: Literal["", "0", "1"] = "",
        exrt_tp: Literal["", "0", "1", "2"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountDepositAndSecuritiesValuationByCurrency]:
        """통화별 예수금 및 증권 평가금현황 (ust21120)

        Args:
            cmsn_incl_tp (Literal["", "0", "1"], optional): 수수료포함구분. 0:미포함,1:포함. Defaults to "".
            exrt_tp (Literal["", "0", "1", "2"], optional): 환율구분. 0:기준환율,1:계좌적용환율,2:전일최종환율. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountDepositAndSecuritiesValuationByCurrency]: 통화별 예수금 및 증권 평가금현황 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21120",
        }
        body = {
            "cmsn_incl_tp": cmsn_incl_tp,
            "exrt_tp": exrt_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching deposit and securities valuation by currency: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountDepositAndSecuritiesValuationByCurrency.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_ledger_valuation_amount(
        self,
        cmsn_incl_tp: Literal["", "0", "1"] = "",
        exrt_tp: Literal["", "0", "1", "2"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountLedgerValuationAmount]:
        """해외증권 원장 평가금액현황 (ust21121)

        Args:
            cmsn_incl_tp (Literal["", "0", "1"], optional): 수수료포함구분. 0:미포함,1:포함. Defaults to "".
            exrt_tp (Literal["", "0", "1", "2"], optional): 환율구분. 0:기준환율,1:계좌적용환율,2:전일최종환율. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountLedgerValuationAmount]: 해외증권 원장 평가금액현황 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21121",
        }
        body = {
            "cmsn_incl_tp": cmsn_incl_tp,
            "exrt_tp": exrt_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ledger valuation amount: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountLedgerValuationAmount.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_valuation_amount_by_date(
        self,
        base_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountValuationAmountByDate]:
        """해외증권 특정일 평가금액 (ust21131)

        Args:
            base_dt (str): 기준일자. YYYYMMDD
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountValuationAmountByDate]: 해외증권 특정일 평가금액 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21131",
        }
        body = {
            "base_dt": base_dt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching valuation amount by date: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountValuationAmountByDate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_deposit_and_securities_valuation_by_currency_on_date(
        self,
        base_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountDepositAndSecuritiesValuationByCurrencyByDate]:
        """특정일 통화별 예수금 및 증권 평가금 (ust21132)

        Args:
            base_dt (str): 기준일자. YYYYMMDD
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountDepositAndSecuritiesValuationByCurrencyByDate]: 특정일 통화별 예수금 및 증권 평가금 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21132",
        }
        body = {
            "base_dt": base_dt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching deposit and securities valuation by currency on date: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountDepositAndSecuritiesValuationByCurrencyByDate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daily_order_execution_history(
        self,
        query_tp: Literal["1", "2", "3", "4", "5", "6"],
        slby_tp: Literal["0", "1", "2"],
        ord_dt: str = "",
        stex_tp: Literal["", "ND", "NY", "NA"] = "",
        stk_cd: str = "",
        oppo_trde_tp: Literal["", "%", "0", "1"] = "",
        fr_ord_no: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountDailyOrderExecutionHistory]:
        """미국주식 일별 주문체결내역 (ust21150)

        Args:
            query_tp (Literal["1", "2", "3", "4", "5", "6"]): 조회구분. 1:주문순,2:주문역순,3:미체결주문순,4:미체결역순,5:체결주문순,6:체결역순
            slby_tp (Literal["0", "1", "2"]): 매도수구분. 0:전체,1:매도,2:매수
            ord_dt (str, optional): 주문일자. 미입력시 오늘 날짜로 조회. Defaults to "".
            stex_tp (Literal["", "ND", "NY", "NA"], optional): 거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX. Defaults to "".
            stk_cd (str, optional): 종목코드. 미입력시 전체. Defaults to "".
            oppo_trde_tp (Literal["", "%", "0", "1"], optional): 반대매매구분. %:전체,0:일반,1:반대매매. Defaults to "".
            fr_ord_no (str, optional): 시작주문번호. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountDailyOrderExecutionHistory]: 미국주식 일별 주문체결내역 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21150",
        }
        body = {
            "ord_dt": ord_dt,
            "query_tp": query_tp,
            "slby_tp": slby_tp,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "oppo_trde_tp": oppo_trde_tp,
            "fr_ord_no": fr_ord_no,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily order execution history: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountDailyOrderExecutionHistory.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_deposit_detail(
        self,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountDepositDetail]:
        """미국주식 예수금 상세 (ust21160)

        Args:
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountDepositDetail]: 미국주식 예수금 상세 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21160",
        }
        body: dict[str, str] = {}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching deposit detail: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountDepositDetail.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_realized_profit_loss_by_stock(
        self,
        fc_krw_tp: Literal["0", "1"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountTodayRealizedProfitLossByStock]:
        """미국주식 당일 종목별 실현손익 (ust21170)

        Args:
            fc_krw_tp (Literal["0", "1"]): 외화원화구분. 0:외화,1:원화
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountTodayRealizedProfitLossByStock]: 미국주식 당일 종목별 실현손익 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21170",
        }
        body = {
            "fc_krw_tp": fc_krw_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today realized profit loss by stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountTodayRealizedProfitLossByStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_order_history_by_period(
        self,
        strt_dt: str,
        end_dt: str,
        slby_tp: Literal["", "0", "1", "2"] = "",
        stex_tp: Literal["", "ND", "NY", "NA"] = "",
        stk_cd: str = "",
        oppo_trde_tp: Literal["", "%", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountOrderHistoryByPeriod]:
        """미국주식 기간별 주문내역 (ust21180)

        Args:
            strt_dt (str): 시작주문일자. YYYYMMDD
            end_dt (str): 종료주문일자. YYYYMMDD
            slby_tp (Literal["", "0", "1", "2"], optional): 매도수구분. 0:전체(기본값),1:매도,2:매수. Defaults to "".
            stex_tp (Literal["", "ND", "NY", "NA"], optional): 거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX. Defaults to "".
            stk_cd (str, optional): 종목코드. 미입력시 전체. Defaults to "".
            oppo_trde_tp (Literal["", "%", "0", "1"], optional): 반대매매구분. %:전체,0:일반,1:반대매매. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountOrderHistoryByPeriod]: 미국주식 기간별 주문내역 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21180",
        }
        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "slby_tp": slby_tp,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "oppo_trde_tp": oppo_trde_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching order history by period: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountOrderHistoryByPeriod.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_order_execution(
        self,
        slby_tp: Literal["", "0", "1", "2"] = "",
        stex_tp: Literal["", "ND", "NY", "NA"] = "",
        stk_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountTodayOrderExecution]:
        """미국주식 당일 주문체결 확인 (ust21510)

        Args:
            slby_tp (Literal["", "0", "1", "2"], optional): 매도매수구분. 0:전체,1:매도,2:매수. Defaults to "".
            stex_tp (Literal["", "ND", "NY", "NA"], optional): 거래소구분. 종목코드 입력시. Defaults to "".
            stk_cd (str, optional): 종목코드. 미입력시 전체. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountTodayOrderExecution]: 미국주식 당일 주문체결 확인 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21510",
        }
        body = {
            "slby_tp": slby_tp,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today order execution: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountTodayOrderExecution.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_realized_profit_loss(
        self,
        strt_dt: str = "",
        end_dt: str = "",
        fc_krw_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountRealizedProfitLoss]:
        """미국주식 실현손익 (ust21530)

        Args:
            strt_dt (str, optional): 시작일자. YYYYMMDD. Defaults to "".
            end_dt (str, optional): 종료일자. YYYYMMDD. Defaults to "".
            fc_krw_tp (Literal["", "0", "1"], optional): 외화원화구분. 0:외화,1:원화. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountRealizedProfitLoss]: 미국주식 실현손익 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21530",
        }
        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "fc_krw_tp": fc_krw_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching realized profit loss: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountRealizedProfitLoss.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading(
        self,
        qry_tp: Literal["0", "1"],
        fc_krw_tp: Literal["0", "1"],
        base_dt: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountTodayTrading]:
        """미국주식 당일매매 (ust21610)

        Args:
            qry_tp (Literal["0", "1"]): 조회구분. 0:당일매수에대한당일매도,1:당일매도전체
            fc_krw_tp (Literal["0", "1"]): 외화원화구분. 0:외화,1:원화
            base_dt (str, optional): 기준일자. YYYYMMDD. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountTodayTrading]: 미국주식 당일매매 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21610",
        }
        body = {
            "base_dt": base_dt,
            "qry_tp": qry_tp,
            "fc_krw_tp": fc_krw_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountTodayTrading.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading_summary(
        self,
        fc_krw_tp: Literal["0", "1"],
        stex_tp: Literal["", "NA", "ND", "NY"] = "",
        stk_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountTodayTradingSummary]:
        """미국주식 당일매매정리 (ust21620)

        Args:
            fc_krw_tp (Literal["0", "1"]): 외화원화구분. 0:외화,1:원화
            stex_tp (Literal["", "NA", "ND", "NY"], optional): 거래소구분. NA:AMEX, ND:NASDAQ, NY:NYSE. Defaults to "".
            stk_cd (str, optional): 종목코드. 기본값 전체. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountTodayTradingSummary]: 미국주식 당일매매정리 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21620",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "fc_krw_tp": fc_krw_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading summary: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountTodayTradingSummary.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_realized_profit_loss(
        self,
        fc_krw_tp: Literal["0", "1"],
        stex_tp: Literal["", "ND", "NY", "NA"] = "",
        stk_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountTodayRealizedProfitLoss]:
        """미국주식 당일 실현손익 (ust21630)

        Args:
            fc_krw_tp (Literal["0", "1"]): 외화원화구분. 0:외화,1:원화
            stex_tp (Literal["", "ND", "NY", "NA"], optional): 거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX. Defaults to "".
            stk_cd (str, optional): 종목코드. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountTodayRealizedProfitLoss]: 미국주식 당일 실현손익 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21630",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "fc_krw_tp": fc_krw_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today realized profit loss: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountTodayRealizedProfitLoss.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daily_realized_profit_loss_by_stock(
        self,
        cntr_dt: str,
        fc_krw_tp: Literal["0", "1"],
        stex_tp: Literal["", "ND", "NY", "NA"] = "",
        stk_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountDailyRealizedProfitLossByStock]:
        """미국주식 일별 종목별 실현손익 (ust21640)

        Args:
            cntr_dt (str): 체결일자. YYYYMMDD
            fc_krw_tp (Literal["0", "1"]): 외화원화구분. 0:외화,1:원화
            stex_tp (Literal["", "ND", "NY", "NA"], optional): 거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX. Defaults to "".
            stk_cd (str, optional): 종목코드. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountDailyRealizedProfitLossByStock]: 미국주식 일별 종목별 실현손익 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21640",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "cntr_dt": cntr_dt,
            "fc_krw_tp": fc_krw_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily realized profit loss by stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountDailyRealizedProfitLossByStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_profit_rate_by_period(
        self,
        fr_dt: str = "",
        to_dt: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountProfitRateByPeriod]:
        """미국주식 기간별 수익률 현황 (ust21650)

        Args:
            fr_dt (str, optional): 조회시작일자. YYYYMMDD. Defaults to "".
            to_dt (str, optional): 조회종료일자. YYYYMMDD. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountProfitRateByPeriod]: 미국주식 기간별 수익률 현황 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21650",
        }
        body = {
            "fr_dt": fr_dt,
            "to_dt": to_dt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching profit rate by period: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountProfitRateByPeriod.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daily_realized_profit_loss(
        self,
        strt_dt: str = "",
        end_dt: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountDailyRealizedProfitLoss]:
        """미국주식 일별 실현손익 (ust21660)

        Args:
            strt_dt (str, optional): 시작일자. YYYYMMDD. Defaults to "".
            end_dt (str, optional): 종료일자. YYYYMMDD. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountDailyRealizedProfitLoss]: 미국주식 일별 실현손익 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21660",
        }
        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily realized profit loss: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountDailyRealizedProfitLoss.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_monthly_realized_profit_loss(
        self,
        strt_dt: str = "",
        end_dt: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasAccountMonthlyRealizedProfitLoss]:
        """미국주식 월별 실현손익 (ust21661)

        Args:
            strt_dt (str, optional): 시작일자. YYYYMM. Defaults to "".
            end_dt (str, optional): 종료일자. YYYYMM. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasAccountMonthlyRealizedProfitLoss]: 미국주식 월별 실현손익 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust21661",
        }
        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching monthly realized profit loss: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasAccountMonthlyRealizedProfitLoss.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
