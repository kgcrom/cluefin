"""Tests for XBRL parser."""

from datetime import date, datetime
from decimal import Decimal

import pytest

from cluefin_xbrl._types import PeriodType
from cluefin_xbrl.parser import (
    XbrlParseError,
    _exclusive_to_date,
    _try_parse_decimal,
    parse_xbrl_directory,
    parse_xbrl_file,
)


class TestParseXbrlFile:
    def test_extracts_facts(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        assert len(doc.facts) == 7

        local_names = {f.concept_local_name for f in doc.facts}
        assert local_names == {"Assets", "Equity", "Revenue", "Liabilities", "EarningsPerShare", "AuditorName"}

    def test_instant_period_extraction(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        assets = next(f for f in doc.facts if f.concept_local_name == "Assets")
        assert assets.period is not None
        assert assets.period.period_type == PeriodType.INSTANT
        assert assets.period.instant == date(2023, 12, 31)

    def test_duration_period_extraction(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        revenue = next(f for f in doc.facts if f.concept_local_name == "Revenue")
        assert revenue.period is not None
        assert revenue.period.period_type == PeriodType.DURATION
        assert revenue.period.start_date == date(2023, 1, 1)
        assert revenue.period.end_date == date(2023, 12, 31)

    def test_numeric_values(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        assets = next(f for f in doc.facts if f.concept_local_name == "Assets")
        assert assets.numeric_value == Decimal("1000000000000")
        assert assets.decimals == "-6"
        assert assets.unit is not None
        assert "KRW" in assets.unit

    def test_entity_id(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        assert doc.entity_id == "00126380"
        for fact in doc.facts:
            assert fact.entity_id == "00126380"

    def test_reporting_period_end(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        assert doc.reporting_period_end == date(2023, 12, 31)

    def test_source_file(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        assert doc.source_file.endswith("sample.xbrl")

    def test_nil_fact(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        liabilities = next(f for f in doc.facts if f.concept_local_name == "Liabilities")
        assert liabilities.is_nil is True
        assert liabilities.value is None
        assert liabilities.numeric_value is None
        assert liabilities.decimals is None

    def test_string_fact(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        auditor = next(f for f in doc.facts if f.concept_local_name == "AuditorName")
        assert auditor.value == "삼일회계법인"
        assert auditor.numeric_value is None
        assert auditor.unit is None

    def test_divide_unit(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        eps = next(f for f in doc.facts if f.concept_local_name == "EarningsPerShare")
        assert eps.numeric_value == Decimal("1234.56")
        assert eps.unit is not None
        assert "KRW" in eps.unit
        assert "/" in eps.unit
        assert "shares" in eps.unit

    def test_explicit_and_typed_dimensions(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path)

        revenue_facts = [f for f in doc.facts if f.concept_local_name == "Revenue"]
        assert len(revenue_facts) == 2

        dimensioned = next(f for f in revenue_facts if f.dimensions)
        assert dimensioned.dimensions["sample:SegmentAxis"] == "sample:SeoulMember"
        assert dimensioned.dimensions["sample:RegionAxis"] == "Seoul"

        plain = next(f for f in revenue_facts if not f.dimensions)
        assert plain.numeric_value == Decimal("300000000000")

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            parse_xbrl_file(tmp_path / "nonexistent.xbrl")


class TestParseXbrlDirectory:
    def test_finds_xbrl(self, sample_xbrl_dir):
        doc = parse_xbrl_directory(sample_xbrl_dir)

        assert len(doc.facts) == 7
        local_names = {f.concept_local_name for f in doc.facts}
        assert "Assets" in local_names

    def test_no_xbrl_files(self, tmp_path):
        with pytest.raises(XbrlParseError, match="XBRL 파일이 없습니다"):
            parse_xbrl_directory(tmp_path)

    def test_directory_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            parse_xbrl_directory(tmp_path / "nonexistent")


class TestExclusiveToDate:
    def test_midnight_shifts_back_one_day(self):
        # Arelle stores 2023-12-31 as exclusive midnight 2024-01-01T00:00:00
        assert _exclusive_to_date(datetime(2024, 1, 1, 0, 0, 0)) == date(2023, 12, 31)

    def test_non_midnight_keeps_same_day(self):
        assert _exclusive_to_date(datetime(2023, 12, 31, 15, 30, 0)) == date(2023, 12, 31)

    def test_plain_date_passthrough(self):
        assert _exclusive_to_date(date(2023, 12, 31)) == date(2023, 12, 31)


class TestTryParseDecimal:
    def test_valid_integer(self):
        assert _try_parse_decimal("1000000") == Decimal("1000000")

    def test_valid_decimal(self):
        assert _try_parse_decimal("123.45") == Decimal("123.45")

    def test_negative(self):
        assert _try_parse_decimal("-500") == Decimal("-500")

    def test_none(self):
        assert _try_parse_decimal(None) is None

    def test_invalid(self):
        assert _try_parse_decimal("not_a_number") is None

    def test_empty_string(self):
        assert _try_parse_decimal("") is None
