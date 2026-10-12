"""Unit tests for the SEC filing detail page (`-index.html`): document types and filer CIKs."""

from datetime import date

import pytest
import requests_mock

from cluefin_openapi.sec import Client, FilingDetail, SecAPIError
from cluefin_openapi.sec._filing_detail import parse_filing_detail

USER_AGENT = "Cluefin Test test@example.com"

# Trimmed from the live page (2026-10): the markup around the parts the parser reads is kept as served.
EIGHT_K_PAGE = """
<div id="formName">
   <strong>Form 8-K</strong> - Current report:
</div>
<div id="secNum"><strong><acronym title="Securities and Exchange Commission">SEC</acronym> Accession No.</strong>
 0000320193-26-000010</div>
<div class="formGrouping">
   <div class="infoHead">Filing Date</div>
   <div class="info">2026-07-30</div>
   <div class="infoHead">Accepted</div>
   <div class="info">2026-07-30 16:30:11</div>
</div>
<div class="formGrouping">
   <div class="infoHead">Period of Report</div>
   <div class="info">2026-07-30</div>
</div>
<div class="formGrouping">
   <div class="infoHead">Items</div>
   <div class="info">Item 2.02: Results of Operations and Financial Condition<br />Item 9.01: Financial Statements
    and Exhibits<br /></div>
</div>
<p>Document Format Files</p>
<table class="tableFile" summary="Document Format Files">
   <tr><th scope="col">Seq</th><th scope="col">Description</th><th scope="col">Document</th>
       <th scope="col">Type</th><th scope="col">Size</th></tr>
   <tr>
      <td scope="row">1</td>
      <td scope="row">8-K</td>
      <td scope="row"><a href="/ix?doc=/Archives/edgar/data/320193/000032019326000010/aapl-20260730.htm">aapl-20260730.htm</a>
       &nbsp;&nbsp;<span style="color: green">iXBRL</span></td>
      <td scope="row">8-K</td>
      <td scope="row">28747</td>
   </tr>
   <tr class="evenRow">
      <td scope="row">2</td>
      <td scope="row">EX-99.1 EARNINGS RELEASE &amp; OUTLOOK</td>
      <td scope="row"><a href="/Archives/edgar/data/320193/000032019326000010/a8-kex991q3.htm">a8-kex991q3.htm</a></td>
      <td scope="row">EX-99.1</td>
      <td scope="row">356891</td>
   </tr>
   <tr>
      <td scope="row">&nbsp;</td>
      <td scope="row">Complete submission text file</td>
      <td scope="row"><a href="/Archives/edgar/data/320193/000032019326000010/0000320193-26-000010.txt">0000320193-26-000010.txt</a></td>
      <td scope="row">&nbsp;</td>
      <td scope="row">557418</td>
   </tr>
</table>
<p>Data Files</p>
<table class="tableFile" summary="Data Files">
   <tr><th scope="col">Seq</th><th scope="col">Description</th><th scope="col">Document</th>
       <th scope="col">Type</th><th scope="col">Size</th></tr>
   <tr>
      <td scope="row">3</td>
      <td scope="row">XBRL TAXONOMY EXTENSION SCHEMA DOCUMENT</td>
      <td scope="row"><a href="/Archives/edgar/data/320193/000032019326000010/aapl-20260730.xsd">aapl-20260730.xsd</a></td>
      <td scope="row">EX-101.SCH</td>
      <td scope="row">1773</td>
   </tr>
</table>
<div class="companyInfo">
  <span class="companyName">Apple Inc. (Filer)
 <acronym title="Central Index Key">CIK</acronym>: <a href="/cgi-bin/browse-edgar?CIK=0000320193&amp;action=getcompany">0000320193 (see all company filings)</a></span>
<p class="identInfo">Type: <strong>8-K</strong> | Act: <strong>34</strong></p>
</div>
"""

FORM_4_PAGE = """
<div id="formName"><strong>Form 4</strong> - Statement of changes in beneficial ownership of securities:</div>
<div class="formGrouping"><div class="infoHead">Filing Date</div><div class="info">2026-10-02</div></div>
<table class="tableFile" summary="Document Format Files">
   <tr><th>Seq</th><th>Description</th><th>Document</th><th>Type</th><th>Size</th></tr>
   <tr><td>1</td><td>PRIMARY DOCUMENT</td>
       <td><a href="/Archives/edgar/data/320193/000123456726000005/xslF345X06/form4.xml">form4.html</a></td>
       <td>4</td><td>&nbsp;</td></tr>
   <tr><td>1</td><td>PRIMARY DOCUMENT</td>
       <td><a href="/Archives/edgar/data/320193/000123456726000005/form4.xml">form4.xml</a></td>
       <td>4</td><td>3507</td></tr>
</table>
<span class="companyName">Apple Inc. (<a href="/cgi-bin/own-disp?CIK=0000320193&amp;action=getissuer">Issuer</a>)
 <acronym title="Central Index Key">CIK</acronym>: <a href="/cgi-bin/browse-edgar?CIK=0000320193&amp;action=getcompany">0000320193 (see all company filings)</a></span>
<span class="companyName">Doe Jane (A) (<a href="/cgi-bin/own-disp?CIK=0001234567&amp;action=getowner">Reporting</a>)
 <acronym title="Central Index Key">CIK</acronym>: <a href="/cgi-bin/browse-edgar?CIK=0001234567&amp;action=getcompany">0001234567 (see all company filings)</a></span>
"""


def test_parse_eight_k_documents_items_and_filer():
    detail = parse_filing_detail(EIGHT_K_PAGE, "000032019326000010")

    assert detail.accession_number == "0000320193-26-000010"
    assert detail.form == "8-K"
    assert detail.filing_date == date(2026, 7, 30)
    assert detail.period_of_report == date(2026, 7, 30)
    assert detail.items == [
        "Item 2.02: Results of Operations and Financial Condition",
        "Item 9.01: Financial Statements and Exhibits",
    ]
    main, exhibit, full_text, schema = detail.documents
    # The inline XBRL viewer link still yields the plain file name.
    assert (main.sequence, main.type, main.name, main.size, main.data_file) == (
        1,
        "8-K",
        "aapl-20260730.htm",
        28747,
        False,
    )
    assert exhibit.type == "EX-99.1"
    assert exhibit.name == "a8-kex991q3.htm"
    assert exhibit.description == "EX-99.1 EARNINGS RELEASE & OUTLOOK"
    assert (full_text.sequence, full_text.type) == (None, None)
    assert (schema.type, schema.data_file) == ("EX-101.SCH", True)
    assert detail.ciks == [320193]
    assert detail.parties[0].name == "Apple Inc."
    assert detail.parties[0].role == "Filer"


def test_parse_form_4_keeps_rendering_path_and_every_party():
    detail = parse_filing_detail(FORM_4_PAGE, "0001234567-26-000005")

    assert detail.form == "4"
    assert detail.period_of_report is None
    assert detail.items == []
    assert [document.name for document in detail.documents] == ["xslF345X06/form4.xml", "form4.xml"]
    assert detail.documents[0].size is None
    assert detail.ciks == [320193, 1234567]
    # A name with its own parentheses keeps them; the role is the last group.
    assert [(party.name, party.role) for party in detail.parties] == [
        ("Apple Inc.", "Issuer"),
        ("Doe Jane (A)", "Reporting"),
    ]


def test_page_without_form_name_fails_loudly():
    with pytest.raises(SecAPIError, match="서식"):
        parse_filing_detail("<html><body>Not Found</body></html>", "0000320193-26-000010")


def test_filing_detail_fetches_the_index_page():
    client = Client(user_agent=USER_AGENT)
    url = "https://www.sec.gov/Archives/edgar/data/320193/000032019326000010/0000320193-26-000010-index.html"
    with requests_mock.Mocker() as m:
        m.get(url, text=EIGHT_K_PAGE)
        detail = client.archives.filing_detail("0000320193", "000032019326000010")

    assert isinstance(detail, FilingDetail)
    assert [document.type for document in detail.documents] == ["8-K", "EX-99.1", None, "EX-101.SCH"]
