"""Unit tests for the 13F cover page and information table parser.

Documents are synthetic but follow the shapes measured on real filings (2013–2026): namespaced XML, MM-DD-YYYY
dates, integer cells, comma-separated other-manager numbers, and `value` in thousands before 2023-01-03 filings.
"""

from datetime import date

import pytest

from cluefin_sec_notes.ownership import (
    DOLLAR_VALUES_FROM,
    Form13FManager,
    load_13f,
    parse_13f_cover,
    parse_13f_table,
)

COVER_NS = "http://www.sec.gov/edgar/thirteenffiler"
TABLE_NS = "http://www.sec.gov/edgar/document/thirteenf/informationtable"

AMENDMENT_COVER = f"""<?xml version="1.0" encoding="UTF-8"?>
<edgarSubmission xmlns="{COVER_NS}" xmlns:ns1="http://www.sec.gov/edgar/common">
  <schemaVersion>X0202</schemaVersion>
  <headerData>
    <submissionType>13F-HR/A</submissionType>
    <filerInfo>
      <liveTestFlag>LIVE</liveTestFlag>
      <filer><credentials><cik>0000000001</cik><ccc>XXXXXXXX</ccc></credentials></filer>
      <periodOfReport>09-30-2023</periodOfReport>
    </filerInfo>
  </headerData>
  <formData>
    <coverPage>
      <reportCalendarOrQuarter>09-30-2023</reportCalendarOrQuarter>
      <isAmendment>true</isAmendment>
      <amendmentNo>2</amendmentNo>
      <amendmentInfo>
        <amendmentType>RESTATEMENT</amendmentType>
        <confDeniedExpired>false</confDeniedExpired>
      </amendmentInfo>
      <filingManager>
        <name>Example Advisers LLC</name>
        <address><ns1:street1>1 Main St</ns1:street1><ns1:city>Springfield</ns1:city></address>
      </filingManager>
      <reportType>13F COMBINATION REPORT</reportType>
      <form13FFileNumber>028-00001</form13FFileNumber>
      <otherManagersInfo>
        <otherManager>
          <cik>0000000002</cik>
          <form13FFileNumber>028-00002</form13FFileNumber>
          <name>Outside Manager Inc</name>
        </otherManager>
      </otherManagersInfo>
      <provideInfoForInstruction5>N</provideInfoForInstruction5>
    </coverPage>
    <signatureBlock>
      <name>Jane Doe</name>
      <title>Chief Compliance Officer</title>
      <phone>555-0100</phone>
      <signature>Jane Doe</signature>
      <city>Springfield</city>
      <stateOrCountry>IL</stateOrCountry>
      <signatureDate>04-09-2024</signatureDate>
    </signatureBlock>
    <summaryPage>
      <otherIncludedManagersCount>2</otherIncludedManagersCount>
      <tableEntryTotal>3</tableEntryTotal>
      <tableValueTotal>1234567</tableValueTotal>
      <isConfidentialOmitted>false</isConfidentialOmitted>
      <otherManagers2Info>
        <otherManager2>
          <sequenceNumber>1</sequenceNumber>
          <otherManager>
            <cik>0000000003</cik>
            <form13FFileNumber>028-00003</form13FFileNumber>
            <name>Affiliate One LLC</name>
          </otherManager>
        </otherManager2>
        <otherManager2>
          <sequenceNumber>2</sequenceNumber>
          <otherManager>
            <crdNumber>000123456</crdNumber>
            <secFileNumber>801-00004</secFileNumber>
            <name>Affiliate Two LP</name>
          </otherManager>
        </otherManager2>
      </otherManagers2Info>
    </summaryPage>
  </formData>
</edgarSubmission>
"""

NOTICE_COVER = f"""<?xml version="1.0" encoding="UTF-8"?>
<edgarSubmission xmlns="{COVER_NS}">
  <headerData>
    <submissionType>13F-NT</submissionType>
    <filerInfo>
      <filer><credentials><cik>0000000005</cik><ccc>XXXXXXXX</ccc></credentials></filer>
      <periodOfReport>12-31-2022</periodOfReport>
    </filerInfo>
  </headerData>
  <formData>
    <coverPage>
      <reportCalendarOrQuarter>12-31-2022</reportCalendarOrQuarter>
      <filingManager><name>Notice Filer LLC</name></filingManager>
      <reportType>13F NOTICE</reportType>
      <form13FFileNumber>028-00005</form13FFileNumber>
    </coverPage>
    <signatureBlock><name>John Roe</name><signatureDate>02-14-2023</signatureDate></signatureBlock>
  </formData>
</edgarSubmission>
"""


def _row(
    cusip: str,
    value: str,
    shares: str,
    *,
    kind: str = "SH",
    extra: str = "",
    other_manager: str | None = None,
) -> str:
    manager = f"<otherManager>{other_manager}</otherManager>" if other_manager is not None else ""
    return f"""
  <infoTable>
    <nameOfIssuer>Issuer {cusip}</nameOfIssuer>
    <titleOfClass>COM</titleOfClass>
    <cusip>{cusip}</cusip>
    <value>{value}</value>
    <shrsOrPrnAmt><sshPrnamt>{shares}</sshPrnamt><sshPrnamtType>{kind}</sshPrnamtType></shrsOrPrnAmt>
    {extra}
    <investmentDiscretion>DFND</investmentDiscretion>
    {manager}
    <votingAuthority><Sole>{shares}</Sole><Shared>0</Shared><None>0</None></votingAuthority>
  </infoTable>"""


def _table(*rows: str) -> str:
    return f'<?xml version="1.0" ?>\n<informationTable xmlns="{TABLE_NS}">{"".join(rows)}\n</informationTable>\n'


# Dollar-era table: prices 100, 50 and a bond row.
DOLLAR_TABLE = _table(
    _row("037833100", "1000000", "10000", other_manager="1,2"),
    _row("594918104", "500000", "10000", extra="<putCall>Call</putCall><figi>BBG000BPH459</figi>"),
    _row("912828zq6", "990000", "1000000", kind="PRN", other_manager=" "),
)


def test_cover_of_a_restated_combination_report():
    cover = parse_13f_cover(AMENDMENT_COVER)

    assert (cover.submission_type, cover.report_type) == ("13F-HR/A", "13F COMBINATION REPORT")
    assert (cover.is_amendment, cover.is_notice) == (True, False)
    assert (cover.amendment_no, cover.amendment_type, cover.conf_denied_expired) == (2, "RESTATEMENT", False)
    assert (cover.period_of_report, cover.signature_date) == (date(2023, 9, 30), date(2024, 4, 9))
    assert (cover.filer_cik, cover.manager_name, cover.form13f_file_number) == (
        "0000000001",
        "Example Advisers LLC",
        "028-00001",
    )
    assert (cover.signature_name, cover.signature_title) == ("Jane Doe", "Chief Compliance Officer")
    assert (cover.table_entry_total, cover.table_value_total, cover.other_included_managers_count) == (3, 1234567, 2)
    assert cover.is_confidential_omitted is False
    assert cover.other_managers == (Form13FManager(None, "0000000002", "Outside Manager Inc", "028-00002", None, None),)
    assert cover.included_managers == (
        Form13FManager(1, "0000000003", "Affiliate One LLC", "028-00003", None, None),
        Form13FManager(2, None, "Affiliate Two LP", None, "000123456", "801-00004"),
    )


def test_notice_cover_has_no_summary():
    cover = parse_13f_cover(NOTICE_COVER)

    assert (cover.submission_type, cover.report_type, cover.is_notice) == ("13F-NT", "13F NOTICE", True)
    assert cover.period_of_report == date(2022, 12, 31)
    assert (cover.table_entry_total, cover.table_value_total, cover.included_managers) == (None, None, ())


def test_table_in_dollars_after_the_boundary():
    table = parse_13f_table(DOLLAR_TABLE, filed=DOLLAR_VALUES_FROM)

    assert (table.value_multiplier, table.value_unit_suspect) == (1, False)
    first, option, bond = table.holdings
    assert (first.cusip, first.value, first.shares, first.shares_type) == ("037833100", 1000000, 10000, "SH")
    assert (first.other_managers, first.put_call, first.figi) == ((1, 2), None, None)
    assert (first.voting_sole, first.voting_shared, first.voting_none) == (10000, 0, 0)
    assert (first.investment_discretion, first.name_of_issuer, first.title_of_class) == (
        "DFND",
        "Issuer 037833100",
        "COM",
    )
    assert (option.put_call, option.figi, option.other_managers) == ("Call", "BBG000BPH459", ())
    # Lower-case CUSIPs exist in real filings; blank otherManager cells too.
    assert (bond.cusip, bond.shares_type, bond.other_managers) == ("912828ZQ6", "PRN", ())


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1,2,15", (1, 2, 15)),
        ("1 2", (1, 2)),
        ("1, 2", (1, 2)),
        ("None", ()),
        ("N/A", ()),
        ("-", ()),
        ("Example Advisers", ()),
        ("1;2", ()),
    ],
)
def test_other_managers_is_free_text(raw, expected):
    table = parse_13f_table(_table(_row("037833100", "1000", "10", other_manager=raw)), filed=DOLLAR_VALUES_FROM)

    assert (table.holdings[0].other_managers, table.holdings[0].other_managers_text) == (expected, raw)


def test_whole_numbers_with_zero_decimals_and_unpadded_dates():
    table = parse_13f_table(_table(_row("037833100", "1000", "12300.00")), filed=DOLLAR_VALUES_FROM)
    cover = parse_13f_cover(NOTICE_COVER.replace("<signatureDate>02-14-2023", "<signatureDate>2-8-2018"))

    assert (table.holdings[0].shares, table.holdings[0].voting_sole) == (12300, 12300)
    assert cover.signature_date == date(2018, 2, 8)


def test_table_in_thousands_before_the_boundary():
    table = parse_13f_table(_table(_row("037833100", "1000", "10000")), filed=date(2022, 12, 30))

    assert (table.value_multiplier, table.value_unit_suspect) == (1000, False)
    assert table.holdings[0].value == 1000000


@pytest.mark.parametrize(
    ("value", "filed"),
    [
        ("1000", DOLLAR_VALUES_FROM),  # thousands filed after the boundary: $0.10 a share
        ("1000000", date(2021, 2, 16)),  # dollars filed before the boundary: $100,000 a share
    ],
)
def test_unit_mismatch_is_flagged_not_changed(value, filed):
    table = parse_13f_table(_table(_row("037833100", value, "10000")), filed=filed)

    assert table.value_unit_suspect is True
    assert table.holdings[0].value == int(value) * table.value_multiplier


def test_unit_check_ignores_bonds_and_zero_rows():
    table = parse_13f_table(
        _table(_row("912828ZQ6", "1", "1000000", kind="PRN"), _row("037833100", "0", "0")),
        filed=DOLLAR_VALUES_FROM,
    )

    assert table.value_unit_suspect is False


def test_load_reads_cover_and_table(tmp_path):
    cover_path = tmp_path / "primary_doc.xml"
    cover_path.write_text(AMENDMENT_COVER)
    table_path = tmp_path / "infotable.xml"
    table_path.write_text(DOLLAR_TABLE)

    doc = load_13f(cover_path, table_path, filed=date(2024, 4, 9))

    assert doc.cover.submission_type == "13F-HR/A"
    assert [row.cusip for row in doc.holdings] == ["037833100", "594918104", "912828ZQ6"]


def test_load_notice_without_table(tmp_path):
    cover_path = tmp_path / "primary_doc.xml"
    cover_path.write_text(NOTICE_COVER)

    doc = load_13f(cover_path, filed=date(2023, 2, 14))

    assert (doc.table, doc.holdings) == (None, ())


def test_load_holdings_report_requires_table(tmp_path):
    cover_path = tmp_path / "primary_doc.xml"
    cover_path.write_text(AMENDMENT_COVER)

    with pytest.raises(ValueError, match="정보표"):
        load_13f(cover_path, filed=date(2024, 4, 9))


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("<edgarSubmission>", "XML"),
        ("<edgarSubmission/>", "13F 표지"),
        (
            f'<edgarSubmission xmlns="{COVER_NS}"><headerData><submissionType>D</submissionType></headerData>'
            "</edgarSubmission>",
            "13F가 아닙니다",
        ),
        (NOTICE_COVER.replace("12-31-2022", "2022-12-31"), "periodOfReport"),
        (AMENDMENT_COVER.replace("<amendmentNo>2", "<amendmentNo>two"), "amendmentNo"),
        (AMENDMENT_COVER.replace("<confDeniedExpired>false", "<confDeniedExpired>maybe"), "confDeniedExpired"),
    ],
)
def test_cover_rejects_unexpected_input(source, message):
    with pytest.raises(ValueError, match=message):
        parse_13f_cover(source)


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("<informationTable>", "XML"),
        ("<informationTable/>", "13F 정보표"),
        (_table(_row("037833100", "1,000", "10")), "value"),
        (_table(_row("037833100", "1000", "10.5")), "sshPrnamt"),
        (_table(_row("037833100", "1000", "10", kind="SHS")), "sshPrnamtType"),
        (_table(_row("037833100", "1000", "10", extra="<putCall>CALL</putCall>")), "putCall"),
        (DOLLAR_TABLE.replace("DFND", "SHARED"), "investmentDiscretion"),
    ],
)
def test_table_rejects_unexpected_input(source, message):
    with pytest.raises(ValueError, match=message):
        parse_13f_table(source, filed=DOLLAR_VALUES_FROM)
