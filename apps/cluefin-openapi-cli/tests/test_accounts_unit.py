"""`accounts` standard tables and `statements.match_items`: synthetic rows, no real filings."""

from __future__ import annotations

import pytest

from cluefin_openapi_cli import accounts
from cluefin_openapi_cli import statements as s


def test_common_table_has_the_three_groups_in_file_order() -> None:
    table = accounts.load_table()

    assert list(table) == ["income", "balance", "cash"]
    assert next(iter(table["income"])) == "revenue"
    assert table["income"]["revenue"] == accounts.Item(
        ("ifrs-full_Revenue",), ("수익(매출액)", "매출액", "영업수익", "매출")
    )
    # Owners' share is id-only on purpose (its label also names the comprehensive-income split).
    assert table["income"]["net_income_owners"].names == ()


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
