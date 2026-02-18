import os
import time

import dotenv
import pytest
from pydantic import SecretStr

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
        app_key=os.getenv("KIWOOM_APP_KEY", ""),
        secret_key=SecretStr(os.getenv("KIWOOM_SECRET_KEY", "")),
        env=os.getenv("KIWOOM_ENV", "dev").lower(),
    )


@pytest.fixture
def client(auth: Auth) -> Client:
    time.sleep(1)
    token = auth.generate_token()
    return Client(token=token.get_token(), env=os.getenv("KIWOOM_ENV", "dev").lower())


@pytest.mark.integration
def test_get_daily_stock_realized_profit_loss_by_date(client: Client):
    time.sleep(1)

    response = client.account.get_daily_stock_realized_profit_loss_by_date("005930", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyStockRealizedProfitLossByDate)


@pytest.mark.integration
def test_get_daily_stock_realized_profit_loss_by_period(client: Client):
    time.sleep(1)

    response = client.account.get_daily_stock_realized_profit_loss_by_period("005930", "20240601", "20240630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyStockRealizedProfitLossByPeriod)


@pytest.mark.integration
def test_get_daily_realized_profit_loss(client: Client):
    time.sleep(1)

    response = client.account.get_daily_realized_profit_loss("20240601", "20240630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyRealizedProfitLoss)


@pytest.mark.integration
def test_get_unexecuted(client: Client):
    time.sleep(1)

    response = client.account.get_unexecuted("0", "0", "005930", "0")

    assert response is not None
    assert isinstance(response.body, DomesticAccountUnexecuted)


@pytest.mark.integration
def test_get_executed(client: Client):
    time.sleep(1)

    response = client.account.get_executed("005930", "0", "0", "0", "0")

    assert response is not None
    assert isinstance(response.body, DomesticAccountExecuted)


@pytest.mark.integration
def test_get_daily_realized_profit_loss_details(client: Client):
    time.sleep(1)

    response = client.account.get_daily_realized_profit_loss_details("005930")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyRealizedProfitLossDetails)


@pytest.mark.integration
def test_get_account_profit_rate(client: Client):
    time.sleep(1)

    response = client.account.get_account_profit_rate("20240601", "20240630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticAccountProfitRate)


@pytest.mark.integration
def test_get_unexecuted_split_order_details(client: Client):
    time.sleep(1)

    response = client.account.get_unexecuted_split_order_details("1234567890")

    assert response is not None
    assert isinstance(response.body, DomesticAccountUnexecutedSplitOrderDetails)


@pytest.mark.integration
def test_get_current_day_trading_journal(client: Client):
    time.sleep(1)

    response = client.account.get_current_day_trading_journal("20240630", "1", "0")

    assert response is not None
    assert isinstance(response.body, DomesticAccountCurrentDayTradingJournal)


@pytest.mark.integration
def test_get_deposit_balance_details(client: Client):
    time.sleep(1)

    response = client.account.get_deposit_balance_details("3")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDepositBalanceDetails)


@pytest.mark.integration
def test_get_daily_estimated_deposit_asset_balance(client: Client):
    time.sleep(1)

    response = client.account.get_daily_estimated_deposit_asset_balance("20240601", "20240630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyEstimatedDepositAssetBalance)


@pytest.mark.integration
def test_get_estimated_asset_balance(client: Client):
    time.sleep(1)

    response = client.account.get_estimated_asset_balance("0")

    assert response is not None
    assert isinstance(response.body, DomesticAccountEstimatedAssetBalance)


@pytest.mark.integration
def test_get_account_evaluation_status(client: Client):
    time.sleep(1)

    response = client.account.get_account_evaluation_status("0", "KRX")

    assert response is not None
    assert isinstance(response.body, DomesticAccountEvaluationStatus)


@pytest.mark.integration
def test_get_execution_balance(client: Client):
    time.sleep(1)

    response = client.account.get_execution_balance("KRX")

    assert response is not None
    assert isinstance(response.body, DomesticAccountExecutionBalance)


@pytest.mark.integration
def test_get_account_order_execution_details(client: Client):
    time.sleep(1)

    response = client.account.get_account_order_execution_details(
        ord_dt="20240630", qry_tp="1", stk_bond_tp="0", sell_tp="0", stk_cd="005930", fr_ord_no="0", dmst_stex_tp="%"
    )

    assert response is not None
    assert isinstance(response.body, DomesticAccountOrderExecutionDetails)


@pytest.mark.integration
def test_get_account_next_day_settlement_details(client: Client):
    time.sleep(1)

    response = client.account.get_account_next_day_settlement_details()

    assert response is not None
    assert isinstance(response.body, DomesticAccountNextDaySettlementDetails)


@pytest.mark.integration
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


@pytest.mark.integration
def test_get_available_withdrawal_amount(client: Client):
    time.sleep(1)

    response = client.account.get_available_withdrawal_amount(
        io_amt="1000000", stk_cd="005930", trde_tp="1", trde_qty="10", uv="50000", exp_buy_unp="60000"
    )

    assert response is not None
    assert isinstance(response.body, DomesticAccountAvailableWithdrawalAmount)


@pytest.mark.integration
def test_get_available_order_quantity_by_margin_rate(client: Client):
    time.sleep(1)

    response = client.account.get_available_order_quantity_by_margin_rate(stk_cd="005930", uv="50000")

    assert response is not None
    assert isinstance(response.body, DomesticAccountAvailableOrderQuantityByMarginRate)


@pytest.mark.integration
def test_get_available_order_quantity_by_margin_loan_stock(client: Client):
    time.sleep(1)

    response = client.account.get_available_order_quantity_by_margin_loan_stock(stk_cd="005930", uv="50000")

    assert response is not None
    assert isinstance(response.body, DomesticAccountAvailableOrderQuantityByMarginLoanStock)


@pytest.mark.integration
def test_get_margin_details(client: Client):
    time.sleep(1)

    response = client.account.get_margin_details()

    assert response is not None
    assert isinstance(response.body, DomesticAccountMarginDetails)


@pytest.mark.integration
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


@pytest.mark.integration
def test_get_daily_account_profit_rate_details(client: Client):
    time.sleep(1)

    response = client.account.get_daily_account_profit_rate_details(fr_dt="20240601", to_dt="20240630")

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyProfitRateDetails)


@pytest.mark.integration
def test_get_account_current_day_status(client: Client):
    time.sleep(1)

    response = client.account.get_account_current_day_status()

    assert response is not None
    assert isinstance(response.body, DomesticAccountCurrentDayStatus)


@pytest.mark.integration
def test_get_account_evaluation_balance_details(client: Client):
    time.sleep(1)

    response = client.account.get_account_evaluation_balance_details(qry_tp="1", dmst_stex_tp="KRX")

    assert response is not None
    assert isinstance(response.body, DomesticAccountEvaluationBalanceDetails)
