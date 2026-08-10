import pytest

from cluefin_openapi.kiwoom._client import Client
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

from ._integration_helpers import real_account_only


@pytest.mark.integration
@real_account_only("usa21670", "8104:모의투자에서 지원하지 않는 API")
def test_get_daily_account_profit_rate(client: Client):
    response = client.overseas_account.get_daily_account_profit_rate(from_dt="20240102", to="20240131")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountDailyProfitRate)


@pytest.mark.integration
@real_account_only("usa21680", "8104:모의투자에서 지원하지 않는 API")
def test_get_monthly_account_profit_rate(client: Client):
    response = client.overseas_account.get_monthly_account_profit_rate(from_dt="202401", to="202406")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountMonthlyProfitRate)


@pytest.mark.integration
@real_account_only("usa21690", "8104:모의투자에서 지원하지 않는 API")
def test_get_yearly_account_profit_rate(client: Client):
    response = client.overseas_account.get_yearly_account_profit_rate(from_dt="2023", to="2024")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountYearlyProfitRate)


@pytest.mark.integration
@real_account_only("usa21730", "8104:모의투자에서 지원하지 않는 API")
def test_get_daily_stock_profit_rate(client: Client):
    response = client.overseas_account.get_daily_stock_profit_rate(
        from_dt="20240102", to="20240131", stk_cd="AAPL", stex_tp="ND"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountDailyStockProfitRate)


@pytest.mark.integration
@real_account_only("usa21731", "8104:모의투자에서 지원하지 않는 API")
def test_get_monthly_stock_profit_rate(client: Client):
    response = client.overseas_account.get_monthly_stock_profit_rate(
        from_dt="202401", to="202406", stk_cd="AAPL", stex_tp="ND"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountMonthlyStockProfitRate)


@pytest.mark.integration
@real_account_only("usa21732", "8104:모의투자에서 지원하지 않는 API")
def test_get_yearly_stock_profit_rate(client: Client):
    response = client.overseas_account.get_yearly_stock_profit_rate(
        from_dt="2023", to="2024", stk_cd="AAPL", stex_tp="ND"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountYearlyStockProfitRate)


@pytest.mark.integration
def test_get_ledger_unfilled_orders(client: Client):
    response = client.overseas_account.get_ledger_unfilled_orders(
        ord_dt="20240102", slby_tp="0", stex_tp="ND", stk_cd="AAPL"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountLedgerUnfilledOrders)


@pytest.mark.integration
def test_get_ledger_balance(client: Client):
    response = client.overseas_account.get_ledger_balance(stex_tp="ND", stk_cd="AAPL")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountLedgerBalance)


@pytest.mark.integration
@real_account_only("ust21100", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_transaction_history(client: Client):
    response = client.overseas_account.get_transaction_history(
        strt_dt="20240102",
        end_dt="20240131",
        tp="0",
        stex_tp="ND",
        stk_cd="AAPL",
        krw_repl_skip_yn="N",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountTransactionHistory)


@pytest.mark.integration
def test_get_deposit(client: Client):
    response = client.overseas_account.get_deposit()

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountDeposit)


@pytest.mark.integration
def test_get_krw_withdrawable_amount(client: Client):
    response = client.overseas_account.get_krw_withdrawable_amount()

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountKrwWithdrawableAmount)


@pytest.mark.integration
def test_get_deposit_and_securities_valuation_by_currency(client: Client):
    response = client.overseas_account.get_deposit_and_securities_valuation_by_currency(cmsn_incl_tp="0", exrt_tp="0")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountDepositAndSecuritiesValuationByCurrency)


@pytest.mark.integration
def test_get_ledger_valuation_amount(client: Client):
    response = client.overseas_account.get_ledger_valuation_amount(cmsn_incl_tp="0", exrt_tp="0")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountLedgerValuationAmount)


@pytest.mark.integration
@real_account_only("ust21131", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_valuation_amount_by_date(client: Client):
    response = client.overseas_account.get_valuation_amount_by_date(base_dt="20240102")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountValuationAmountByDate)


@pytest.mark.integration
@real_account_only("ust21132", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_deposit_and_securities_valuation_by_currency_on_date(client: Client):
    response = client.overseas_account.get_deposit_and_securities_valuation_by_currency_on_date(base_dt="20240102")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountDepositAndSecuritiesValuationByCurrencyByDate)


@pytest.mark.integration
def test_get_daily_order_execution_history(client: Client):
    response = client.overseas_account.get_daily_order_execution_history(
        query_tp="1",
        slby_tp="0",
        ord_dt="20240102",
        stex_tp="ND",
        stk_cd="AAPL",
        oppo_trde_tp="0",
        fr_ord_no="0001",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountDailyOrderExecutionHistory)


@pytest.mark.integration
def test_get_deposit_detail(client: Client):
    response = client.overseas_account.get_deposit_detail()

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountDepositDetail)


@pytest.mark.integration
def test_get_today_realized_profit_loss_by_stock(client: Client):
    response = client.overseas_account.get_today_realized_profit_loss_by_stock(fc_krw_tp="0")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountTodayRealizedProfitLossByStock)


@pytest.mark.integration
@real_account_only("ust21180", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_order_history_by_period(client: Client):
    response = client.overseas_account.get_order_history_by_period(
        strt_dt="20240102",
        end_dt="20240131",
        slby_tp="0",
        stex_tp="ND",
        stk_cd="AAPL",
        oppo_trde_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountOrderHistoryByPeriod)


@pytest.mark.integration
def test_get_today_order_execution(client: Client):
    response = client.overseas_account.get_today_order_execution(slby_tp="0", stex_tp="ND", stk_cd="AAPL")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountTodayOrderExecution)


@pytest.mark.integration
def test_get_realized_profit_loss(client: Client):
    response = client.overseas_account.get_realized_profit_loss(strt_dt="20240102", end_dt="20240131", fc_krw_tp="0")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountRealizedProfitLoss)


@pytest.mark.integration
def test_get_today_trading(client: Client):
    response = client.overseas_account.get_today_trading(qry_tp="0", fc_krw_tp="0", base_dt="20240102")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountTodayTrading)


@pytest.mark.integration
def test_get_today_trading_summary(client: Client):
    response = client.overseas_account.get_today_trading_summary(fc_krw_tp="0", stex_tp="ND", stk_cd="AAPL")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountTodayTradingSummary)


@pytest.mark.integration
def test_get_today_realized_profit_loss(client: Client):
    response = client.overseas_account.get_today_realized_profit_loss(fc_krw_tp="0", stex_tp="ND", stk_cd="AAPL")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountTodayRealizedProfitLoss)


@pytest.mark.integration
def test_get_daily_realized_profit_loss_by_stock(client: Client):
    response = client.overseas_account.get_daily_realized_profit_loss_by_stock(
        cntr_dt="20240102", fc_krw_tp="0", stex_tp="ND", stk_cd="AAPL"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountDailyRealizedProfitLossByStock)


@pytest.mark.integration
@real_account_only("ust21650", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_profit_rate_by_period(client: Client):
    response = client.overseas_account.get_profit_rate_by_period(fr_dt="20240102", to_dt="20240131")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountProfitRateByPeriod)


@pytest.mark.integration
def test_get_daily_realized_profit_loss(client: Client):
    response = client.overseas_account.get_daily_realized_profit_loss(strt_dt="20240102", end_dt="20240131")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountDailyRealizedProfitLoss)


@pytest.mark.integration
@real_account_only("ust21661", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_monthly_realized_profit_loss(client: Client):
    response = client.overseas_account.get_monthly_realized_profit_loss(strt_dt="202401", end_dt="202406")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasAccountMonthlyRealizedProfitLoss)
