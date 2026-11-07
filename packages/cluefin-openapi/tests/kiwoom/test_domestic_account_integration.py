from datetime import date, timedelta

import pytest

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
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

from ._integration_helpers import real_account_only, skip_if_env_blocked
from ._spec_conformance import assert_spec_conformance


@pytest.mark.integration
def test_get_daily_stock_realized_profit_loss_by_date(client: Client):
    response = client.account.get_daily_stock_realized_profit_loss_by_date("005930", "20250630")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyStockRealizedProfitLossByDate)


@pytest.mark.integration
def test_get_daily_stock_realized_profit_loss_by_period(client: Client):
    response = client.account.get_daily_stock_realized_profit_loss_by_period("005930", "20240601", "20240630")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyStockRealizedProfitLossByPeriod)


@pytest.mark.integration
def test_get_daily_realized_profit_loss(client: Client):
    response = client.account.get_daily_realized_profit_loss("20240601", "20240630")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyRealizedProfitLoss)


@pytest.mark.integration
def test_get_unexecuted(client: Client):
    # 위치 인자 순서가 시그니처와 달라 stex_tp 에 종목코드가 가고 있었다 — 문서 요청 예시값
    response = client.account.get_unexecuted(all_stk_tp="1", trde_tp="0", stex_tp="0", stk_cd="005930")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountUnexecuted)


@pytest.mark.integration
def test_get_executed(client: Client):
    # 위치 인자 순서가 시그니처와 달라 qry_tp 에 종목코드가 가고 있었다 — 문서 요청 예시값
    response = client.account.get_executed(qry_tp="1", sell_tp="0", stex_tp="0", stk_cd="005930")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountExecuted)


@pytest.mark.integration
def test_get_daily_realized_profit_loss_details(client: Client):
    response = client.account.get_daily_realized_profit_loss_details("005930")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyRealizedProfitLossDetails)


@pytest.mark.integration
def test_get_account_profit_rate(client: Client):
    # stex_tp 하나만 받는 TR 에 날짜 두 개를 넘겨 cont_yn 에 날짜가 가고 있었다
    response = client.account.get_account_profit_rate(stex_tp="0")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountProfitRate)


@pytest.mark.integration
def test_get_unexecuted_split_order_details(client: Client):
    response = client.account.get_unexecuted_split_order_details("1234567890")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountUnexecutedSplitOrderDetails)


@pytest.mark.integration
def test_get_current_day_trading_journal(client: Client):
    # 위치 인자 순서가 시그니처와 달라 ottks_tp 에 날짜가 가고 있었다. base_dt 공백 = 금일
    response = client.account.get_current_day_trading_journal(ottks_tp="1", ch_crd_tp="0")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountCurrentDayTradingJournal)


@pytest.mark.integration
def test_get_deposit_balance_details(client: Client):
    response = client.account.get_deposit_balance_details("3")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountDepositBalanceDetails)


@pytest.mark.integration
@real_account_only("kt00002", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_daily_estimated_deposit_asset_balance(client: Client):
    # 2024-06 고정 구간은 prod 실계좌에 해당 기간 추정예탁자산 내역이 없어 506476 오류가 난다
    # (2026-11-07 실측). 최근 30일로 바꿔 매 실행 시점에 데이터가 있게 한다.
    today = date.today()
    response = client.account.get_daily_estimated_deposit_asset_balance(
        (today - timedelta(days=30)).strftime("%Y%m%d"), today.strftime("%Y%m%d")
    )
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyEstimatedDepositAssetBalance)


@pytest.mark.integration
def test_get_estimated_asset_balance(client: Client):
    response = client.account.get_estimated_asset_balance("0")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountEstimatedAssetBalance)


@pytest.mark.integration
def test_get_account_evaluation_status(client: Client):
    response = client.account.get_account_evaluation_status("0", "KRX")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountEvaluationStatus)


@pytest.mark.integration
@real_account_only("kt00005", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_execution_balance(client: Client):
    response = client.account.get_execution_balance("KRX")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountExecutionBalance)


@pytest.mark.integration
def test_get_account_order_execution_details(client: Client):
    response = client.account.get_account_order_execution_details(
        ord_dt="20240630", qry_tp="1", stk_bond_tp="0", sell_tp="0", stk_cd="005930", fr_ord_no="0", dmst_stex_tp="%"
    )
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountOrderExecutionDetails)


@pytest.mark.integration
def test_get_account_next_day_settlement_details(client: Client):
    response = client.account.get_account_next_day_settlement_details()
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountNextDaySettlementDetails)


@pytest.mark.integration
def test_get_account_order_execution_status(client: Client):
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
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountOrderExecutionStatus)


@pytest.mark.integration
@real_account_only("kt00010", "RC7006:모의투자 조회실패")
def test_get_available_withdrawal_amount(client: Client):
    # 하드코딩 단가(50000/60000)는 prod 가격밴드 검증에 걸린다(508975, 2026-11-07 실측) — 당일 종가로 맞춘다.
    # trde_tp="1"(매도)는 보유 종목이 없으면 571455 로 거절되므로 매수(trde_tp="2") 로 확인한다.
    price = abs(int(client.market_conditions.get_stock_price(stk_cd="005930").body.close_pric))
    try:
        response = client.account.get_available_withdrawal_amount(
            io_amt="1000000",
            stk_cd="005930",
            trde_tp="2",
            trde_qty="10",
            uv=str(price),
            exp_buy_unp=str(price),
        )
    except KiwoomAPIError as e:
        skip_if_env_blocked(e)
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountAvailableWithdrawalAmount)


@pytest.mark.integration
def test_get_available_order_quantity_by_margin_rate(client: Client):
    response = client.account.get_available_order_quantity_by_margin_rate(stk_cd="005930", uv="50000")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountAvailableOrderQuantityByMarginRate)


@pytest.mark.integration
@real_account_only("kt00012", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_available_order_quantity_by_margin_loan_stock(client: Client):
    # prod 실측(2026-11-07): 일반 위탁 계좌는 503721:신용계좌만 조회가능합니다 로 거절된다 — 신용계좌가
    # 있어야 모양을 검증할 수 있다 (TS domestic-account.integration.test.ts 의 kt00012 와 동일 사유).
    try:
        response = client.account.get_available_order_quantity_by_margin_loan_stock(stk_cd="005930", uv="50000")
    except KiwoomAPIError as e:
        if "503721" in e.message:
            pytest.skip(f"신용계좌가 아니면 조회 불가: {e.message}")
        raise
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountAvailableOrderQuantityByMarginLoanStock)


@pytest.mark.integration
def test_get_margin_details(client: Client):
    response = client.account.get_margin_details()
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountMarginDetails)


@pytest.mark.integration
@real_account_only("kt00015", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_consignment_comprehensive_transaction_history(client: Client):
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
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountConsignmentComprehensiveTransactionHistory)


@pytest.mark.integration
@real_account_only("kt00016", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_daily_account_profit_rate_details(client: Client):
    response = client.account.get_daily_account_profit_rate_details(fr_dt="20240601", to_dt="20240630")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountDailyProfitRateDetails)


@pytest.mark.integration
@real_account_only("kt00017", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_account_current_day_status(client: Client):
    response = client.account.get_account_current_day_status()
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountCurrentDayStatus)


@pytest.mark.integration
def test_get_account_evaluation_balance_details(client: Client):
    response = client.account.get_account_evaluation_balance_details(qry_tp="1", dmst_stex_tp="KRX")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticAccountEvaluationBalanceDetails)
