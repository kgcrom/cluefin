"""Tests for XBRL parser."""

import shutil
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import pytest

import cluefin_xbrl.parser as parser_module
from cluefin_xbrl._types import PeriodType, XbrlFact, XbrlPeriod
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

    def test_no_model_loaded_raises(self, sample_xbrl_path, monkeypatch):
        """Arelle 이 모델을 하나도 돌려주지 않으면 XbrlParseError 로 알린다."""

        class _EmptySession:
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def run(self, options):
                pass

            def get_models(self):
                return []

        monkeypatch.setattr("arelle.api.Session.Session", _EmptySession)

        with pytest.raises(XbrlParseError, match="XBRL 모델을 로드할 수 없습니다"):
            parse_xbrl_file(sample_xbrl_path)

    @pytest.mark.parametrize("content", ["not xml at all", ""], ids=["not_xml", "empty"])
    def test_unreadable_file_raises(self, tmp_path, content):
        """XML 로 읽히지 않는 파일은 fact 0건 문서가 아니라 XbrlParseError 다."""
        path = tmp_path / "broken.xbrl"
        path.write_text(content)

        with pytest.raises(XbrlParseError, match="XBRL 문서를 읽을 수 없습니다"):
            parse_xbrl_file(path)

    def test_non_instance_xml_raises(self, tmp_path):
        """XML 이지만 XBRL 인스턴스가 아닌 파일도 XbrlParseError 다."""
        path = tmp_path / "other.xbrl"
        path.write_text('<?xml version="1.0"?><root><a>1</a></root>')

        with pytest.raises(XbrlParseError, match="XBRL 인스턴스 문서가 아닙니다"):
            parse_xbrl_file(path)

    def test_forever_period_extraction(self, fixtures_dir, tmp_path):
        for name in ("sample.xsd", "sample_lab-ko.xml", "sample_lab-en.xml", "sample_pre.xml"):
            shutil.copy(fixtures_dir / name, tmp_path / name)
        forever_context = """
    <xbrli:context id="ctx_forever">
        <xbrli:entity>
            <xbrli:identifier scheme="http://www.dart.fss.or.kr">00126380</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:forever/>
        </xbrli:period>
    </xbrli:context>
    <sample:AuditorName contextRef="ctx_forever">forever-auditor</sample:AuditorName>
</xbrli:xbrl>"""
        instance = (fixtures_dir / "sample.xbrl").read_text(encoding="utf-8")
        (tmp_path / "sample.xbrl").write_text(instance.replace("</xbrli:xbrl>", forever_context), encoding="utf-8")

        doc = parse_xbrl_file(tmp_path / "sample.xbrl")

        fact = next(f for f in doc.facts if f.value == "forever-auditor")
        assert fact.period is not None
        assert fact.period.period_type == PeriodType.FOREVER
        assert fact.period.instant is None
        assert fact.period.start_date is None
        assert fact.period.end_date is None


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

    def test_multiple_xbrl_files_picks_sorted_first(self, fixtures_dir, tmp_path):
        """디렉토리에 .xbrl 파일이 여러 개면 이름순으로 정렬해 첫 번째만 파싱한다."""
        for name in ("sample.xsd", "sample_lab-ko.xml", "sample_lab-en.xml", "sample_pre.xml"):
            shutil.copy(fixtures_dir / name, tmp_path / name)
        # "aaa_first.xbrl" < "zzz_second.xbrl" 이름순 정렬로 first가 선택되어야 한다.
        shutil.copy(fixtures_dir / "sample.xbrl", tmp_path / "aaa_first.xbrl")
        shutil.copy(fixtures_dir / "sample.xbrl", tmp_path / "zzz_second.xbrl")

        doc = parse_xbrl_directory(tmp_path)

        assert doc.source_file.endswith("aaa_first.xbrl")


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


_SEC_INSTANCE_HEAD = (
    b'<?xml version="1.0" encoding="utf-8"?>\n'
    b"<!--XBRL document created with Workiva-->\n"
    b'<xbrli:xbrl xmlns:xbrli="http://www.xbrl.org/2003/instance" xml:lang="en-US">\n</xbrli:xbrl>\n'
)
_LINKBASE_HEAD = b'<?xml version="1.0"?>\n<link:linkbase xmlns:link="http://www.xbrl.org/2003/linkbase"/>\n'


def _write_sec_folder(folder, instance_name):
    for name in ("aapl-20230930_cal.xml", "aapl-20230930_def.xml", "aapl-20230930_lab.xml", "aapl-20230930_pre.xml"):
        (folder / name).write_bytes(_LINKBASE_HEAD)
    (folder / "aapl-20230930.xsd").write_bytes(b"<xs:schema/>")
    (folder / "FilingSummary.xml").write_bytes(b"<FilingSummary/>")
    (folder / "R1.xml").write_bytes(b"<InstanceReport/>")
    (folder / instance_name).write_bytes(_SEC_INSTANCE_HEAD)


class TestParseSecDirectory:
    @pytest.fixture
    def captured(self, monkeypatch):
        calls = {}

        def fake_parse(path, *, include_taxonomy=False, http_user_agent=None):
            calls.update(path=Path(path), include_taxonomy=include_taxonomy, http_user_agent=http_user_agent)
            return "parsed"

        monkeypatch.setattr(parser_module, "parse_xbrl_file", fake_parse)
        return calls

    def test_picks_inline_extracted_instance(self, tmp_path, captured):
        _write_sec_folder(tmp_path, "aapl-20230930_htm.xml")

        result = parse_xbrl_directory(tmp_path, include_taxonomy=True, http_user_agent="Jane jane@example.com")

        assert result == "parsed"
        assert captured == {
            "path": tmp_path / "aapl-20230930_htm.xml",
            "include_taxonomy": True,
            "http_user_agent": "Jane jane@example.com",
        }

    def test_picks_pre_inline_instance_by_root_element(self, tmp_path, captured):
        _write_sec_folder(tmp_path, "aapl-20180929.xml")

        parse_xbrl_directory(tmp_path)

        assert captured["path"] == tmp_path / "aapl-20180929.xml"

    def test_unprefixed_root_is_an_instance(self, tmp_path, captured):
        (tmp_path / "abc-20101231.xml").write_bytes(
            b'<?xml version="1.0"?>\n<xbrl xmlns="http://www.xbrl.org/2003/instance">'
        )

        parse_xbrl_directory(tmp_path)

        assert captured["path"] == tmp_path / "abc-20101231.xml"

    def test_dart_xbrl_file_wins(self, tmp_path, captured):
        _write_sec_folder(tmp_path, "aapl-20230930_htm.xml")
        (tmp_path / "entity.xbrl").write_bytes(_SEC_INSTANCE_HEAD)

        parse_xbrl_directory(tmp_path)

        assert captured["path"] == tmp_path / "entity.xbrl"

    def test_folder_with_only_linkbases_has_no_instance(self, tmp_path):
        _write_sec_folder(tmp_path, "aapl-20230930_htm.xml")
        (tmp_path / "aapl-20230930_htm.xml").unlink()

        with pytest.raises(XbrlParseError, match="XBRL 파일이 없습니다"):
            parse_xbrl_directory(tmp_path)


def _fact(local_name, value, namespace, period=None):
    return XbrlFact(
        concept_local_name=local_name,
        concept_qname=f"x:{local_name}",
        namespace=namespace,
        value=value,
        period=period,
    )


class TestReportingPeriodEnd:
    DEI = "http://xbrl.sec.gov/dei/2023"

    def test_sec_document_period_end_date_wins_over_later_instants(self):
        facts = [
            _fact("DocumentPeriodEndDate", "2023-09-30", self.DEI),
            # Shares outstanding on the cover page are measured weeks after the period end.
            _fact(
                "EntityCommonStockSharesOutstanding",
                "15550061000",
                self.DEI,
                XbrlPeriod(period_type=PeriodType.INSTANT, instant=date(2023, 10, 20)),
            ),
        ]
        assert parser_module._reporting_period_end(facts) == date(2023, 9, 30)

    def test_falls_back_to_latest_instant(self):
        facts = [
            _fact("Assets", "1", "ifrs", XbrlPeriod(period_type=PeriodType.INSTANT, instant=date(2023, 12, 31))),
            _fact("Assets", "1", "ifrs", XbrlPeriod(period_type=PeriodType.INSTANT, instant=date(2022, 12, 31))),
        ]
        assert parser_module._reporting_period_end(facts) == date(2023, 12, 31)

    def test_non_dei_document_period_end_date_is_ignored(self):
        instant = XbrlPeriod(period_type=PeriodType.INSTANT, instant=date(2024, 6, 30))
        facts = [
            _fact("DocumentPeriodEndDate", "2023-09-30", "http://example.com/other"),
            _fact("A", "1", "x", instant),
        ]
        assert parser_module._reporting_period_end(facts) == date(2024, 6, 30)

    def test_unparseable_value_falls_back(self):
        instant = XbrlPeriod(period_type=PeriodType.INSTANT, instant=date(2024, 6, 30))
        facts = [_fact("DocumentPeriodEndDate", "--09-30", self.DEI), _fact("A", "1", "x", instant)]
        assert parser_module._reporting_period_end(facts) == date(2024, 6, 30)

    def test_no_facts(self):
        assert parser_module._reporting_period_end([]) is None


class TestHttpUserAgentOption:
    def test_user_agent_reaches_arelle_runtime_options(self, monkeypatch, sample_xbrl_path):
        import arelle.api.Session as session_module

        seen = []
        real_session = session_module.Session

        class SpySession(real_session):
            def run(self, options, *args, **kwargs):
                seen.append(options.httpUserAgent)
                return super().run(options, *args, **kwargs)

        monkeypatch.setattr(session_module, "Session", SpySession)

        parse_xbrl_file(sample_xbrl_path, http_user_agent="Jane jane@example.com")
        parse_xbrl_file(sample_xbrl_path)

        assert seen[0] == "Jane jane@example.com"
        assert seen[1] != "Jane jane@example.com"
