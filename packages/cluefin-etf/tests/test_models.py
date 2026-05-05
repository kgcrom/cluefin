from datetime import date
from decimal import Decimal

from cluefin_etf import EtfDetail, EtfSummary, FetchMetadata, ProviderName


def test_etf_summary_accepts_normalized_optional_fields():
    summary = EtfSummary(
        provider=ProviderName.KODEX,
        code="069500",
        name="KODEX 200",
        isin="KR7069500007",
        category="domestic_equity",
        benchmark="KOSPI 200",
        listing_date=date(2002, 10, 14),
        nav=Decimal("40123.45"),
        aum=Decimal("1000000000000"),
        expense_ratio=Decimal("0.15"),
        as_of_date=date(2026, 5, 5),
        detail_url="https://example.test/detail/069500",
        holdings_url="https://example.test/holdings/069500",
        raw={"provider_specific": "value"},
    )

    assert summary.nav == Decimal("40123.45")
    assert summary.raw["provider_specific"] == "value"


def test_etf_detail_accepts_normalized_optional_fields():
    detail = EtfDetail(
        provider="tiger",
        code="102110",
        name="TIGER 200",
        isin="KR7102110002",
        category="domestic_equity",
        benchmark="KOSPI 200",
        listing_date=date(2008, 4, 3),
        nav=Decimal("39876.54"),
        aum=Decimal("900000000000"),
        expense_ratio=Decimal("0.05"),
        as_of_date=date(2026, 5, 5),
        detail_url="https://example.test/detail/102110",
        holdings_url="https://example.test/holdings/102110",
        raw={"provider_specific": "value"},
    )

    assert detail.provider == ProviderName.TIGER
    assert detail.expense_ratio == Decimal("0.05")
    assert detail.raw["provider_specific"] == "value"


def test_fetch_metadata_accepts_scraping_diagnostics():
    metadata = FetchMetadata(
        provider="kodex",
        url="https://example.test/list",
        strategy="playwright",
        status_code=200,
        final_url="https://example.test/list?rendered=1",
        content_type="text/html; charset=utf-8",
        elapsed_ms=12.3,
        fallback_reason="validator_rejected",
    )

    assert metadata.final_url == "https://example.test/list?rendered=1"
    assert metadata.fallback_reason == "validator_rejected"
