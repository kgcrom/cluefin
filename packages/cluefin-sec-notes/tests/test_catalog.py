from datetime import date

from cluefin_sec_notes import FORM_10K, catalog_for, parse_date, parse_filing


def test_catalog_for_forms_and_amendments():
    assert catalog_for("10-K") is FORM_10K
    assert catalog_for("10-k/a") is FORM_10K
    assert catalog_for("10-K405") is FORM_10K
    assert catalog_for("20-F") is None
    assert catalog_for(None) is None


def test_item_applies_from_since_date():
    cybersecurity = FORM_10K.spec("I", "1C")
    assert not cybersecurity.applies_to(date(2023, 6, 30))
    assert cybersecurity.applies_to(date(2023, 12, 31))
    assert cybersecurity.applies_to(None)


def test_10k_catalog_is_in_document_order_and_unique():
    numbers = [spec.number for spec in FORM_10K.items]
    assert numbers[:4] == ["1", "1A", "1B", "1C"]
    assert numbers[-2:] == ["15", "16"]
    assert len(set(numbers)) == len(numbers)


def test_parse_date_formats():
    assert parse_date("September 27, 2025") == date(2025, 9, 27)
    assert parse_date("Sept. 30, 2024") == date(2024, 9, 30)
    assert parse_date("2025-12-31") == date(2025, 12, 31)
    assert parse_date("Dec 31 2025") == date(2025, 12, 31)
    assert parse_date("FY") is None


def test_period_end_from_dei_then_cover():
    dei = parse_filing('<ix:nonNumeric name="dei:DocumentPeriodEndDate">December 31, 2025</ix:nonNumeric>')
    assert dei.period_end == date(2025, 12, 31)
    cover = parse_filing("<p>FORM 10-K</p><p>For the fiscal year ended June 30, 2005</p>")
    assert cover.period_end == date(2005, 6, 30)
