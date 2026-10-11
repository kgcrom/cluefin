"""실서버에서 받은 Form 3·4·4/A를 읽는다.

받기는 cluefin-openapi로 한다(이 패키지는 openapi에 의존하지 않는다). 저장소 루트 `.env.test`의 SEC_USER_AGENT가
없으면 건너뛴다:
    uv run pytest packages/cluefin-sec-notes/tests/test_ownership_integration.py -m integration
"""

import os
from datetime import date
from decimal import Decimal
from pathlib import Path

import dotenv
import pytest

from cluefin_sec_notes.ownership import OwnershipDocument, load_ownership

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / ".env.test")
_USER_AGENT = os.getenv("SEC_USER_AGENT")

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not _USER_AGENT, reason="SEC_USER_AGENT 미설정 (.env.test)"),
]

APPLE_CIK = 320193


def _download(tmp_path_factory, accession: str, primary_document: str) -> OwnershipDocument:
    """제출 이력의 주 문서명은 XSL 렌더링 경로(`xslF345X05/…`)라 파일명만 떼어 원본 XML을 받는다."""
    sec = pytest.importorskip("cluefin_openapi.sec")
    client = sec.Client(user_agent=_USER_AGENT)
    try:
        path = client.archives.download_filing_document(
            APPLE_CIK,
            accession,
            primary_document.rsplit("/", 1)[-1],
            destination=tmp_path_factory.mktemp(accession),
        )
    finally:
        client.close()
    return load_ownership(path)


def test_form4_option_exercise_and_planned_sales(tmp_path_factory):
    doc = _download(tmp_path_factory, "0000320193-24-000049", "xslF345X05/wk-form4_1712183493.xml")

    assert (doc.document_type, doc.issuer.trading_symbol, doc.period_of_report) == ("4", "AAPL", date(2024, 4, 1))
    assert doc.aff10b5_one is True
    (owner,) = doc.reporting_owners
    assert owner.is_officer is True

    exercise, first_sale = doc.non_derivative_transactions[:2]
    # The exercise price is given only as a footnote.
    assert (exercise.code, exercise.shares, exercise.price, exercise.acquired_disposed) == (
        "M",
        Decimal("196410"),
        None,
        "A",
    )
    assert exercise.shares_owned_after == Decimal("3476590")
    assert doc.footnotes[exercise.footnote_ids["price"][0]]
    assert (first_sale.code, first_sale.shares, first_sale.price) == ("S", Decimal("99183"), Decimal("170.03"))
    assert all(note in doc.footnotes for row in doc.transactions for ids in row.footnote_ids.values() for note in ids)


def test_form3_restricted_stock_units_filed_by_an_agent(tmp_path_factory):
    """The accession prefix is the filing agent's, but the folder is reachable under the issuer's CIK."""
    doc = _download(tmp_path_factory, "0001780525-26-000003", "xslF345X02/wk-form3_1772839848.xml")

    assert doc.document_type == "3"
    assert doc.transactions == ()
    assert [(h.derivative, h.security_title) for h in doc.derivative_holdings][:2] == [
        (True, "Restricted Stock Unit"),
        (True, "Restricted Stock Unit"),
    ]
    assert doc.derivative_holdings[0].underlying_shares == Decimal("301040")


def test_form4_amendment(tmp_path_factory):
    doc = _download(tmp_path_factory, "0000320193-22-000078", "xslF345X03/wf-form4a_166120817922787.xml")

    assert doc.document_type == "4/A"
    assert doc.is_amendment is True
    assert doc.date_of_original_submission is not None
    assert [(t.code, t.shares, t.price) for t in doc.non_derivative_transactions[:2]] == [
        ("S", Decimal("66390"), Decimal("174.66")),
        ("S", Decimal("30345"), Decimal("175.60")),
    ]
