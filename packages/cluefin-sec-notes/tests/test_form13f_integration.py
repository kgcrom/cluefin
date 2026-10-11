"""실서버에서 받은 13F-HR을 읽는다: `value` 단위가 바뀐 경계(2023-01-03 제출분) 앞뒤 한 건씩.

받기는 cluefin-openapi로 한다(이 패키지는 openapi에 의존하지 않는다). 저장소 루트 `.env.test`의 SEC_USER_AGENT가
없으면 건너뛴다:
    uv run pytest packages/cluefin-sec-notes/tests/test_form13f_integration.py -m integration
"""

import os
from datetime import date
from pathlib import Path

import dotenv
import pytest

from cluefin_sec_notes.ownership import Form13F, load_13f

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / ".env.test")
_USER_AGENT = os.getenv("SEC_USER_AGENT")

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not _USER_AGENT, reason="SEC_USER_AGENT 미설정 (.env.test)"),
]

BERKSHIRE_CIK = 1067983
APPLE_CUSIP = "037833100"


def _download(tmp_path_factory, accession: str, filed: date) -> Form13F:
    """공시 폴더에는 표지 `primary_doc.xml`과 이름이 제각각인 정보표 XML 하나가 있다."""
    sec = pytest.importorskip("cluefin_openapi.sec")
    client = sec.Client(user_agent=_USER_AGENT)
    folder = tmp_path_factory.mktemp(accession)
    try:
        names = [item.name for item in client.archives.filing_index(BERKSHIRE_CIK, accession).items]
        (table_name,) = [name for name in names if name.lower().endswith(".xml") and name != "primary_doc.xml"]
        cover, table = (
            client.archives.download_filing_document(BERKSHIRE_CIK, accession, name, destination=folder)
            for name in ("primary_doc.xml", table_name)
        )
    finally:
        client.close()
    return load_13f(cover, table, filed=filed)


@pytest.mark.parametrize(
    ("accession", "filed", "period", "multiplier"),
    [
        ("0000950123-22-012275", date(2022, 11, 14), date(2022, 9, 30), 1000),
        ("0000950123-23-002585", date(2023, 2, 14), date(2022, 12, 31), 1),
    ],
)
def test_values_are_dollars_on_both_sides_of_the_boundary(tmp_path_factory, accession, filed, period, multiplier):
    doc = _download(tmp_path_factory, accession, filed)

    assert (doc.cover.submission_type, doc.cover.report_type) == ("13F-HR", "13F COMBINATION REPORT")
    assert doc.cover.period_of_report == period
    assert len(doc.holdings) == doc.cover.table_entry_total
    assert (doc.table.value_multiplier, doc.table.value_unit_suspect) == (multiplier, False)
    total = sum(row.value for row in doc.holdings)
    assert total == doc.cover.table_value_total * multiplier
    assert 250e9 < total < 350e9
    # Apple is split across the affiliated managers that share discretion.
    apple = [row for row in doc.holdings if row.cusip == APPLE_CUSIP]
    assert len(apple) > 1
    assert all(row.other_managers and row.investment_discretion == "DFND" for row in apple)
    numbers = {manager.sequence_number for manager in doc.cover.included_managers}
    assert {number for row in doc.holdings for number in row.other_managers} <= numbers
