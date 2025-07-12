import os
import time

import dotenv
import pytest

from cluefin_openapi.kiwoom._auth import Auth
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


@pytest.fixture
def auth() -> Auth:
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Auth(
        app_key=os.getenv("APP_KEY"),
        secret_key=os.getenv("SECRET_KEY"),
        env="dev",
    )


@pytest.fixture
def client(auth: Auth) -> Client:
    """Create a Client instance for testing.

    Args:
        auth (Auth): The authenticated Auth instance.

    Returns:
        Client: A configured Client instance.
    """
    token = auth.generate_token()
    return Client(token=token.token, env="dev")


def test_get_daily_stock_realized_profit_loss_by_date(client: Client):
    time.sleep(1)

    response = client.account.get_daily_stock_realized_profit_loss_by_date("005930", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyStockRealizedProfitLossByDate)


def test_get_daily_stock_realized_profit_loss_by_period(client: Client):
    time.sleep(1)

    response = client.account.get_daily_stock_realized_profit_loss_by_period("005930", "20240601", "20240630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyStockRealizedProfitLossByPeriod)


def test_get_daily_realized_profit_loss(client: Client):
    time.sleep(1)

    response = client.account.get_daily_realized_profit_loss("20240601", "20240630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyRealizedProfitLoss)


# 일자별실현손익요청	ka10074	get_daily_realized_profit_loss
# strt_dt	시작일자	String	Y	8	YYYYMMDD
# end_dt	종료일자	String	Y	8	YYYYMMDD


def test_get_unexecuted(client: Client):
    time.sleep(1)

    response = client.account.get_unexecuted("0", "0", "005930", "0")

    assert response is not None
    assert isinstance(response.body, DomesticAccountUnexecuted)


def test_get_executed(client: Client):
    time.sleep(1)

    response = client.account.get_executed("005930", "0", "0", "0", "0")

    assert response is not None
    assert isinstance(response.body, DomesticAccountExecuted)


def test_get_daily_realized_profit_loss_details(client: Client):
    time.sleep(1)

    response = client.account.get_daily_realized_profit_loss_details("005930")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyRealizedProfitLossDetails)


# 당일실현손익상세요청	ka10077	get_daily_realized_profit_loss_details
# stk_cd	종목코드	String	Y	6


def test_get_account_profit_rate(client: Client):
    time.sleep(1)

    response = client.account.get_account_profit_rate("20240601", "20240630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticAccountProfitRate)


# 계좌수익률요청	ka10085	get_account_profit_rate
# stex_tp	거래소구분	String	Y	1	0 : 통합, 1 : KRX, 2 : NXT


def test_get_unexecuted_split_order_details(client: Client):
    time.sleep(1)

    response = client.account.get_unexecuted_split_order_details("1234567890")

    assert response is not None
    assert isinstance(response.body, DomesticAccountUnexecutedSplitOrderDetails)


# 미체결분할주문상세	ka10088	get_unexecuted_split_order_details
# ord_no	주문번호	String	Y	20


def test_get_current_day_trading_journal(client: Client):
    time.sleep(1)

    response = client.account.get_current_day_trading_journal("20240630", "1", "0")

    assert response is not None
    assert isinstance(response.body, DomesticAccountCurrentDayTradingJournal)


def test_get_deposit_balance_details(client: Client):
    time.sleep(1)

    response = client.account.get_deposit_balance_details("3")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDepositBalanceDetails)


# 예수금상세현황요청	kt00001	get_deposit_balance_details
# qry_tp	조회구분	String	Y	1	3:추정조회, 2:일반조회


def test_get_daily_estimated_deposit_asset_balance(client: Client):
    time.sleep(1)

    response = client.account.get_daily_estimated_deposit_asset_balance("20240601", "20240630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyEstimatedDepositAssetBalance)


def test_get_estimated_asset_balance(client: Client):
    time.sleep(1)

    response = client.account.get_estimated_asset_balance("0")

    assert response is not None
    assert isinstance(response.body, DomesticAccountEstimatedAssetBalance)


def test_get_account_evaluation_status(client: Client):
    time.sleep(1)

    response = client.account.get_account_evaluation_status("0", "KRX")

    assert response is not None
    assert isinstance(response.body, DomesticAccountEvaluationStatus)


def test_get_execution_balance(client: Client):
    time.sleep(1)

    response = client.account.get_execution_balance("KRX")

    assert response is not None
    assert isinstance(response.body, DomesticAccountExecutionBalance)


# 체결잔고요청	kt00005	get_execution_balance
# dmst_stex_tp	국내거래소구분	String	Y	6	KRX:한국거래소,NXT:넥스트트레이드


def test_get_account_order_execution_details(client: Client):
    time.sleep(1)

    response = client.account.get_account_order_execution_details(
        ord_dt="20240630", qry_tp="1", stk_bond_tp="0", sell_tp="0", stk_cd="005930", fr_ord_no="0", dmst_stex_tp="%"
    )

    assert response is not None
    assert isinstance(response.body, DomesticAccountOrderExecutionDetails)


def test_get_account_next_day_settlement_details(client: Client):
    time.sleep(1)

    response = client.account.get_account_next_day_settlement_details()

    assert response is not None
    assert isinstance(response.body, DomesticAccountNextDaySettlementDetails)


def test_get_account_order_execution_status(client: Client):
    time.sleep(1)

    response = client.account.get_account_order_execution_status(
        ord_dt="20240630",
        stk_bond_tp="0",
        mrkt_tp="0",
        sell_tp="0",
        qry_tp="0",
        stk_cd="005930",
        fr_ord_no="0",
        dmst_stex_tp="%",
    )

    assert response is not None
    assert isinstance(response.body, DomesticAccountOrderExecutionStatus)


# 계좌별주문체결현황요청	kt00009	get_account_order_execution_status
# ord_dt	주문일자	String	N	8	YYYYMMDD
# stk_bond_tp	주식채권구분	String	Y	1	0:전체, 1:주식, 2:채권
# mrkt_tp	시장구분	String	Y	1	0:전체, 1:코스피, 2:코스닥, 3:OTCBB, 4:ECN
# sell_tp	매도수구분	String	Y	1	0:전체, 1:매도, 2:매수
# qry_tp	조회구분	String	Y	1	0:전체, 1:체결
# stk_cd	종목코드	String	N	12	전문 조회할 종목코드
# fr_ord_no	시작주문번호	String	N	7
# dmst_stex_tp	국내거래소구분	String	Y	6	%:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행


def test_get_available_withdrawal_amount(client: Client):
    time.sleep(1)

    response = client.account.get_available_withdrawal_amount(
        io_amt="1000000", stk_cd="005930", trde_tp="1", trde_qty="10", uv="50000", exp_buy_unp="60000"
    )

    assert response is not None
    assert isinstance(response.body, DomesticAccountAvailableWithdrawalAmount)


def test_get_available_order_quantity_by_margin_rate(client: Client):
    time.sleep(1)

    response = client.account.get_available_order_quantity_by_margin_rate(stk_cd="005930", uv="50000")

    assert response is not None
    assert isinstance(response.body, DomesticAccountAvailableOrderQuantityByMarginRate)


def test_get_available_order_quantity_by_margin_loan_stock(client: Client):
    time.sleep(1)

    response = client.account.get_available_order_quantity_by_margin_loan_stock(stk_cd="005930", uv="50000")

    assert response is not None
    assert isinstance(response.body, DomesticAccountAvailableOrderQuantityByMarginLoanStock)


def test_get_margin_details(client: Client):
    time.sleep(1)

    response = client.account.get_margin_details()

    assert response is not None
    assert isinstance(response.body, DomesticAccountMarginDetails)


def test_get_consignment_comprehensive_transaction_history(client: Client):
    time.sleep(1)

    response = client.account.get_consignment_comprehensive_transaction_history(
        strt_dt="20240601",
        end_dt="20240630",
        tp="0",
        stk_cd="005930",
        crnc_cd="KRW",
        gds_tp="0",
        frgn_stex_code="",
        dmst_stex_tp="%",
    )

    assert response is not None
    assert isinstance(response.body, DomesticAccountConsignmentComprehensiveTransactionHistory)


def test_get_daily_account_profit_rate_details(client: Client):
    time.sleep(1)

    response = client.account.get_daily_account_profit_rate_details(fr_dt="20240601", to_dt="20240630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyProfitRateDetails)


def test_get_account_current_day_status(client: Client):
    time.sleep(1)

    response = client.account.get_account_current_day_status()

    assert response is not None
    assert isinstance(response.body, DomesticAccountCurrentDayStatus)


def test_get_account_evaluation_balance_details(client: Client):
    time.sleep(1)

    response = client.account.get_account_evaluation_balance_details(qry_tp="1", dmst_stex_tp="KRX")

    assert response is not None
    assert isinstance(response.body, DomesticAccountEvaluationBalanceDetails)
