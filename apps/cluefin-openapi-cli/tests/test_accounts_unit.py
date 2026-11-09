"""`accounts` standard tables and `statements.match_items`: synthetic rows, no real filings."""

from __future__ import annotations

import pytest

from cluefin_openapi_cli import accounts
from cluefin_openapi_cli import statements as s


def test_common_table_has_the_three_groups_in_file_order() -> None:
    table = accounts.load_table()

    assert list(table) == ["income", "balance", "cash", "notes"]
    assert next(iter(table["income"])) == "revenue"
    assert table["income"]["revenue"] == accounts.Item(
        ("ifrs-full_Revenue",), ("수익(매출액)", "매출액", "영업수익", "매출")
    )
    # Owners' share labels must say 당기순이익: the bare label also names the comprehensive-income split.
    assert all("당기순이익" in name for name in table["income"]["net_income_owners"].names)


def test_statements_reads_its_items_from_the_table() -> None:
    table = accounts.load_table()

    assert s.INCOME_ITEMS == table["income"]
    assert s.BALANCE_ITEMS == table["balance"]
    assert s.CASH_ITEMS == table["cash"]


@pytest.mark.parametrize(
    ("entry", "message"),
    [
        pytest.param({"names": ["매출액"]}, "ids must be", id="no_ids"),
        pytest.param({"ids": [], "names": ["매출액"]}, "ids must be", id="empty_ids"),
        pytest.param({"ids": ["x"], "label": "y"}, "takes only", id="unknown_field"),
        pytest.param({"ids": [1]}, "ids must be", id="non_string_id"),
        pytest.param({"ids": "ifrs-full_Revenue"}, "ids must be", id="ids_not_a_list"),
        pytest.param({"ids": ["x"], "names": "매출액"}, "ids must be", id="names_not_a_list"),
    ],
)
def test_malformed_account_is_rejected(entry, message) -> None:
    with pytest.raises(ValueError, match=message):
        accounts._item("t.income.revenue", entry)


def test_match_items_says_how_each_account_was_found() -> None:
    rows = [
        {"sj_div": "CIS", "account_id": "ifrs-full_Revenue", "account_nm": "매출", "thstrm_amount": "100"},
        {"sj_div": "BS", "account_id": "-표준계정코드 미사용-", "account_nm": "자산 총계", "thstrm_amount": "500"},
        {"sj_div": "CF", "account_id": "ifrs-full_DividendsPaidClassifiedAsFinancingActivities", "thstrm_amount": ""},
    ]

    matched = s.match_items(rows, "thstrm_amount")

    assert matched["revenue"] == "id"
    assert matched["assets"] == "label"
    assert matched["dividends_paid"] == "empty"
    assert matched["inventories"] == "missing"
    assert set(matched) == {*s.INCOME_ITEMS, *s.BALANCE_ITEMS, *s.CASH_ITEMS}


def test_marker_must_be_a_bool() -> None:
    with pytest.raises(ValueError, match="marker must be"):
        accounts._item("t.income.fee_income", {"ids": ["x"], "marker": "yes"})


def test_financial_table_keys_do_not_reuse_common_keys_and_have_markers() -> None:
    financial = accounts.load_table("financial")

    assert list(financial) == ["income", "balance", "cash", "notes"]
    assert not financial["cash"]
    assert {*financial["income"], *financial["balance"]}.isdisjoint({*s.INCOME_ITEMS, *s.BALANCE_ITEMS, *s.CASH_ITEMS})
    assert {"fee_income", "loans", "insurance_revenue"} <= s.FINANCIAL_MARKERS
    # Filed by general companies too (bonds, FVOCI assets), so never a marker.
    assert not {"bonds_issued", "fvoci_financial_assets", "borrowed_funds"} & s.FINANCIAL_MARKERS


def _annual_report(rows: list[dict]) -> s.Report:
    return s.Report(year=2025, reprt_code="11011", rcept_no="20260301000001", rows=rows)


_GENERAL_ROWS = [
    {"sj_div": "CIS", "account_id": "ifrs-full_Revenue", "thstrm_amount": "100"},
    # A general filer's 사채 also matches a financial account, but it isn't a marker.
    {"sj_div": "BS", "account_id": "ifrs-full_BondsIssued", "thstrm_amount": "30"},
]

_BANK_ROWS = [
    {"sj_div": "CIS", "account_id": "ifrs-full_FeeAndCommissionIncome", "thstrm_amount": "8"},
    {"sj_div": "CIS", "account_id": "ifrs-full_ProfitLossFromOperatingActivities", "thstrm_amount": "37"},
    {"sj_div": "BS", "account_id": "ifrs-full_DepositsFromCustomers", "thstrm_amount": "1682"},
    {"sj_div": "BS", "account_id": "ifrs-full_BondsIssued", "thstrm_amount": "900"},
]


def test_general_filer_output_has_no_financial_accounts() -> None:
    latest = s.latest(_annual_report(_GENERAL_ROWS))

    assert "bonds_issued" not in latest
    assert "bonds_issued" not in latest["account_match"]
    assert all("bonds_issued" not in year for year in s.annual(_annual_report(_GENERAL_ROWS)))


def test_financial_filer_gets_financial_accounts_and_operating_income() -> None:
    report = _annual_report(_BANK_ROWS)

    latest = s.latest(report)

    assert latest["fee_income"] == 8
    assert latest["deposits"] == 1682
    assert latest["bonds_issued"] == 900
    assert latest["operating_income"] == 37
    assert latest["revenue"] is None
    assert latest["account_match"]["deposits"] == "id"
    assert latest["account_match"]["loans"] == "missing"
    assert s.annual(report)[-1]["deposits"] == 1682
    assert s.to_eok(latest)["deposits"] == 1682 / s.EOK


def test_latest_reads_financial_income_year_to_date() -> None:
    rows = [
        {
            "sj_div": "CIS",
            "account_id": "ifrs-full_FeeAndCommissionIncome",
            "thstrm_amount": "3",
            "thstrm_add_amount": "9",
        }
    ]
    report = s.Report(year=2025, reprt_code="11014", rcept_no="20251101000001", rows=rows)

    assert s.latest(report)["fee_income"] == 9


def test_quarters_keep_a_bank_quarter_without_revenue() -> None:
    rows = [{"sj_div": "CIS", "account_id": "ifrs-full_ProfitLoss", "thstrm_amount": "5", "thstrm_add_amount": "5"}]
    report = s.Report(year=2025, reprt_code="11013", rcept_no="20250515000001", rows=rows)

    quarter_list = s.quarters([report])

    assert [q["period"] for q in quarter_list] == ["2025Q1"]
    assert quarter_list[0]["net_income"] == 5
    assert quarter_list[0]["revenue"] is None


@pytest.mark.parametrize(
    ("key", "group", "row"),
    [
        pytest.param(
            "dividends_paid",
            "cash",
            {"sj_div": "CF", "account_id": "ifrs-full_DividendsPaidClassifiedAsOperatingActivities"},
            id="dividends_paid_under_operating",
        ),
        pytest.param(
            "net_income_owners",
            "income",
            {
                "sj_div": "IS",
                "account_id": "-표준계정코드 미사용-",
                "account_nm": "지배기업의 소유주에게 귀속되는 당기순이익",
            },
            id="owners_profit_off_taxonomy",
        ),
    ],
)
def test_reviewed_common_additions_match(key, group, row) -> None:
    sections = {"income": s.INCOME, "balance": s.BALANCE, "cash": s.CASH}[group]
    items = {"income": s.INCOME_ITEMS, "balance": s.BALANCE_ITEMS, "cash": s.CASH_ITEMS}[group]

    assert s.find_row([row], sections, items[key]) is row


def test_owners_share_label_without_net_income_does_not_match() -> None:
    # The bare label also names the comprehensive-income split, so it stays unmatched.
    row = {"sj_div": "CIS", "account_id": "-표준계정코드 미사용-", "account_nm": "지배기업소유주지분"}

    assert s.find_row([row], s.INCOME, s.INCOME_ITEMS["net_income_owners"]) is None


def test_zero_filed_insurer_loan_label_is_not_a_loan() -> None:
    row = {"sj_div": "BS", "account_id": "-표준계정코드 미사용-", "account_nm": "대출채권및기타수취채권"}

    assert s.find_row([row], s.BALANCE, s.FINANCIAL_BALANCE_ITEMS["loans"]) is None
