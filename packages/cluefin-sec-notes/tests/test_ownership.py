"""Unit tests for the Form 3/4/5 ownership XML parser.

Documents are synthetic but follow the shapes measured on 477 real filings (2004–2026): `<value>` plus optional
`<footnoteId>`, footnotes on the transaction coding, price given only as a footnote, booleans as 1/0 or true/false.
"""

from datetime import date
from decimal import Decimal

import pytest

from cluefin_sec_notes.ownership import OwnershipDocument, load_ownership, parse_ownership

FORM4 = """<?xml version="1.0"?>
<ownershipDocument>
    <schemaVersion>X0508</schemaVersion>
    <documentType>4</documentType>
    <periodOfReport>2025-04-01</periodOfReport>
    <notSubjectToSection16>0</notSubjectToSection16>
    <aff10b5One>true</aff10b5One>
    <issuer>
        <issuerCik>0000000001</issuerCik>
        <issuerName>Example Corp</issuerName>
        <issuerTradingSymbol>EXMP</issuerTradingSymbol>
    </issuer>
    <reportingOwner>
        <reportingOwnerId>
            <rptOwnerCik>0000000099</rptOwnerCik>
            <rptOwnerName>Doe Jane</rptOwnerName>
        </reportingOwnerId>
        <reportingOwnerRelationship>
            <isDirector>0</isDirector>
            <isOfficer>1</isOfficer>
            <officerTitle>Chief Executive Officer</officerTitle>
        </reportingOwnerRelationship>
    </reportingOwner>
    <nonDerivativeTable>
        <nonDerivativeTransaction>
            <securityTitle><value>Common Stock</value></securityTitle>
            <transactionDate><value>2025-04-01</value></transactionDate>
            <transactionCoding>
                <transactionFormType>4</transactionFormType>
                <transactionCode>S</transactionCode>
                <equitySwapInvolved>0</equitySwapInvolved>
                <footnoteId id="F1"/>
            </transactionCoding>
            <transactionAmounts>
                <transactionShares><value>1200</value></transactionShares>
                <transactionPricePerShare><value>.20</value><footnoteId id="F2"/></transactionPricePerShare>
                <transactionAcquiredDisposedCode><value>D</value></transactionAcquiredDisposedCode>
            </transactionAmounts>
            <postTransactionAmounts>
                <sharesOwnedFollowingTransaction><value>98800</value></sharesOwnedFollowingTransaction>
            </postTransactionAmounts>
            <ownershipNature><directOrIndirectOwnership><value>D</value></directOrIndirectOwnership></ownershipNature>
        </nonDerivativeTransaction>
        <nonDerivativeTransaction>
            <securityTitle><value>Common Stock</value></securityTitle>
            <transactionDate><value>2025-04-01-05:00</value></transactionDate>
            <deemedExecutionDate></deemedExecutionDate>
            <transactionCoding>
                <transactionFormType>4</transactionFormType>
                <transactionCode>M</transactionCode>
                <equitySwapInvolved>false</equitySwapInvolved>
            </transactionCoding>
            <transactionAmounts>
                <transactionShares><value>5000</value></transactionShares>
                <transactionPricePerShare><footnoteId id="F3"/></transactionPricePerShare>
                <transactionAcquiredDisposedCode><value>A</value></transactionAcquiredDisposedCode>
            </transactionAmounts>
            <postTransactionAmounts>
                <sharesOwnedFollowingTransaction><value>103800</value></sharesOwnedFollowingTransaction>
            </postTransactionAmounts>
            <ownershipNature><directOrIndirectOwnership><value>D</value></directOrIndirectOwnership></ownershipNature>
        </nonDerivativeTransaction>
        <nonDerivativeHolding>
            <securityTitle><value>Common Stock</value></securityTitle>
            <postTransactionAmounts>
                <sharesOwnedFollowingTransaction><value>2500</value></sharesOwnedFollowingTransaction>
            </postTransactionAmounts>
            <ownershipNature>
                <directOrIndirectOwnership><value>I</value></directOrIndirectOwnership>
                <natureOfOwnership><value>By Trust</value><footnoteId id="F4"/></natureOfOwnership>
            </ownershipNature>
        </nonDerivativeHolding>
    </nonDerivativeTable>
    <derivativeTable>
        <derivativeTransaction>
            <securityTitle><value>Employee Stock Option (right to buy)</value></securityTitle>
            <conversionOrExercisePrice><value>12.50</value></conversionOrExercisePrice>
            <transactionDate><value>2025-04-01</value></transactionDate>
            <transactionCoding>
                <transactionFormType>4</transactionFormType>
                <transactionCode>M</transactionCode>
                <equitySwapInvolved>0</equitySwapInvolved>
            </transactionCoding>
            <transactionAmounts>
                <transactionShares><value>5000</value></transactionShares>
                <transactionPricePerShare><value>0</value></transactionPricePerShare>
                <transactionAcquiredDisposedCode><value>D</value></transactionAcquiredDisposedCode>
            </transactionAmounts>
            <exerciseDate><footnoteId id="F5"/></exerciseDate>
            <expirationDate><value>2030-02-15</value></expirationDate>
            <underlyingSecurity>
                <underlyingSecurityTitle><value>Common Stock</value></underlyingSecurityTitle>
                <underlyingSecurityShares><value>5000</value></underlyingSecurityShares>
            </underlyingSecurity>
            <postTransactionAmounts>
                <sharesOwnedFollowingTransaction><value>15000</value></sharesOwnedFollowingTransaction>
            </postTransactionAmounts>
            <ownershipNature><directOrIndirectOwnership><value>D</value></directOrIndirectOwnership></ownershipNature>
        </derivativeTransaction>
    </derivativeTable>
    <footnotes>
        <footnote id="F1">The sale was effected pursuant to a Rule 10b5-1 trading plan.</footnote>
        <footnote id="F2">Weighted average price; the shares were sold at prices ranging from $0.19 to $0.21.</footnote>
        <footnote id="F3">Exercise of the option reported in Table II.</footnote>
        <footnote id="F4">Held by a family trust.</footnote>
        <footnote id="F5">The option vested in four equal annual installments.</footnote>
    </footnotes>
    <remarks>Exhibit 24 - Power of Attorney</remarks>
    <ownerSignature>
        <signatureName>/s/ Jane Doe</signatureName>
        <signatureDate>2025-04-03</signatureDate>
    </ownerSignature>
</ownershipDocument>
"""


@pytest.fixture(scope="module")
def form4() -> OwnershipDocument:
    return parse_ownership(FORM4)


def test_header_and_issuer(form4):
    assert form4.schema_version == "X0508"
    assert form4.document_type == "4"
    assert form4.is_amendment is False
    assert form4.period_of_report == date(2025, 4, 1)
    assert form4.date_of_original_submission is None
    assert (form4.issuer.cik, form4.issuer.name, form4.issuer.trading_symbol) == (
        "0000000001",
        "Example Corp",
        "EXMP",
    )
    assert form4.aff10b5_one is True
    assert form4.not_subject_to_section16 is False
    assert form4.no_securities_owned is None
    assert form4.remarks == "Exhibit 24 - Power of Attorney"
    assert [(s.name, s.date) for s in form4.signatures] == [("/s/ Jane Doe", date(2025, 4, 3))]


def test_reporting_owner_relationship(form4):
    (owner,) = form4.reporting_owners
    assert (owner.cik, owner.name) == ("0000000099", "Doe Jane")
    assert owner.is_officer is True
    assert owner.is_director is False
    # Omitted relationship flags mean "not that relationship".
    assert owner.is_ten_percent_owner is False
    assert owner.is_other is False
    assert owner.officer_title == "Chief Executive Officer"


def test_open_market_sale_with_weighted_average_price(form4):
    sale = form4.non_derivative_transactions[0]
    assert sale.derivative is False
    assert (sale.code, sale.form_type, sale.equity_swap) == ("S", "4", False)
    assert (sale.shares, sale.price, sale.acquired_disposed) == (Decimal("1200"), Decimal("0.20"), "D")
    assert sale.shares_owned_after == Decimal("98800")
    assert sale.direct_indirect == "D"
    assert sale.date == date(2025, 4, 1)
    assert sale.footnote_ids == {"code": ("F1",), "price": ("F2",)}
    assert form4.footnotes["F2"].startswith("Weighted average price")
    assert sale.exercise_price is None and sale.underlying_title is None


def test_price_given_only_as_a_footnote(form4):
    exercise = form4.non_derivative_transactions[1]
    assert exercise.code == "M"
    assert exercise.price is None
    assert exercise.footnote_ids == {"price": ("F3",)}
    # An XML date may carry a time zone; only the date is kept. An empty cell is None.
    assert exercise.date == date(2025, 4, 1)
    assert exercise.deemed_execution_date is None
    assert exercise.equity_swap is False


def test_holding_row(form4):
    (holding,) = form4.non_derivative_holdings
    assert (holding.shares_owned, holding.direct_indirect, holding.nature_of_ownership) == (
        Decimal("2500"),
        "I",
        "By Trust",
    )
    assert holding.footnote_ids == {"nature_of_ownership": ("F4",)}
    assert holding.derivative is False


def test_derivative_transaction(form4):
    (option,) = form4.derivative_transactions
    assert option.derivative is True
    assert option.security_title == "Employee Stock Option (right to buy)"
    assert option.exercise_price == Decimal("12.50")
    assert option.exercise_date is None
    assert option.expiration_date == date(2030, 2, 15)
    assert (option.underlying_title, option.underlying_shares) == ("Common Stock", Decimal("5000"))
    assert option.footnote_ids == {"exercise_date": ("F5",)}


def test_transactions_list_non_derivative_first(form4):
    assert [t.derivative for t in form4.transactions] == [False, False, True]
    assert [h.derivative for h in form4.holdings] == [False]


FORM3 = """<ownershipDocument>
    <schemaVersion>X0206</schemaVersion>
    <documentType>3/A</documentType>
    <periodOfReport>2024-01-02</periodOfReport>
    <dateOfOriginalSubmission>2024-01-04</dateOfOriginalSubmission>
    <noSecuritiesOwned>0</noSecuritiesOwned>
    <issuer><issuerCik>0000000001</issuerCik><issuerName>Example Corp</issuerName><issuerTradingSymbol>EXMP</issuerTradingSymbol></issuer>
    <reportingOwner>
        <reportingOwnerId><rptOwnerCik>0000000100</rptOwnerCik><rptOwnerName>Fund One LP</rptOwnerName></reportingOwnerId>
        <reportingOwnerRelationship><isTenPercentOwner>true</isTenPercentOwner></reportingOwnerRelationship>
    </reportingOwner>
    <reportingOwner>
        <reportingOwnerId><rptOwnerCik>0000000101</rptOwnerCik><rptOwnerName>Fund One GP LLC</rptOwnerName></reportingOwnerId>
        <reportingOwnerRelationship><isTenPercentOwner>1</isTenPercentOwner><isOther>1</isOther><otherText>General partner</otherText></reportingOwnerRelationship>
    </reportingOwner>
    <derivativeTable>
        <derivativeHolding>
            <securityTitle><value>Series A Preferred Stock</value></securityTitle>
            <conversionOrExercisePrice><footnoteId id="F1"/></conversionOrExercisePrice>
            <exerciseDate><footnoteId id="F1"/></exerciseDate>
            <expirationDate><footnoteId id="F1"/></expirationDate>
            <underlyingSecurity>
                <underlyingSecurityTitle><value>Common Stock</value></underlyingSecurityTitle>
                <underlyingSecurityShares><value>2000000</value></underlyingSecurityShares>
            </underlyingSecurity>
            <ownershipNature><directOrIndirectOwnership><value>D</value></directOrIndirectOwnership></ownershipNature>
        </derivativeHolding>
    </derivativeTable>
    <footnotes><footnote id="F1">Convertible at any time; no expiration date.</footnote></footnotes>
</ownershipDocument>"""


def test_form3_amendment_with_joint_filers_and_derivative_holding():
    doc = parse_ownership(FORM3.encode())
    assert doc.document_type == "3/A"
    assert doc.is_amendment is True
    assert doc.date_of_original_submission == date(2024, 1, 4)
    assert doc.no_securities_owned is False
    assert doc.aff10b5_one is None
    assert [(o.name, o.is_ten_percent_owner, o.is_other) for o in doc.reporting_owners] == [
        ("Fund One LP", True, False),
        ("Fund One GP LLC", True, True),
    ]
    assert doc.transactions == ()
    (holding,) = doc.derivative_holdings
    assert holding.derivative is True
    assert holding.exercise_price is None
    assert holding.shares_owned is None
    assert holding.underlying_shares == Decimal("2000000")
    assert holding.footnote_ids == {
        "exercise_price": ("F1",),
        "exercise_date": ("F1",),
        "expiration_date": ("F1",),
    }


def _minimal(document_type: str = "4", extra: str = "") -> str:
    return (
        "<ownershipDocument>"
        f"<documentType>{document_type}</documentType>"
        "<issuer><issuerCik>0000000001</issuerCik></issuer>"
        f"{extra}"
        "</ownershipDocument>"
    )


def test_form5_flags():
    extra = "<form3HoldingsReported>0</form3HoldingsReported><form4TransactionsReported>1</form4TransactionsReported>"
    doc = parse_ownership(_minimal("5", extra))
    assert (doc.form3_holdings_reported, doc.form4_transactions_reported) == (False, True)


def test_load_from_file(tmp_path):
    path = tmp_path / "form4.xml"
    path.write_text(FORM4, encoding="utf-8")
    assert load_ownership(path) == parse_ownership(FORM4)


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("not xml at all", "XML을 읽을 수 없습니다"),
        ("<edgarSubmission><documentType>4</documentType></edgarSubmission>", "소유 신고 XML이 아닙니다"),
        (_minimal("10-K"), "Form 3·4·5가 아닙니다"),
        (_minimal(extra="<aff10b5One>Y</aff10b5One>"), "aff10b5One: 불리언이 아닙니다"),
        (_minimal(extra="<periodOfReport>04/01/2025</periodOfReport>"), "periodOfReport: 날짜가 아닙니다"),
    ],
)
def test_unexpected_documents_raise(source, message):
    with pytest.raises(ValueError, match=message):
        parse_ownership(source)


def test_unexpected_number_names_the_cell():
    row = (
        "<nonDerivativeTable><nonDerivativeTransaction>"
        "<transactionAmounts><transactionShares><value>1,000</value></transactionShares></transactionAmounts>"
        "</nonDerivativeTransaction></nonDerivativeTable>"
    )
    with pytest.raises(ValueError, match="transactionAmounts/transactionShares: 숫자가 아닙니다"):
        parse_ownership(_minimal(extra=row))


def test_entity_declarations_are_refused():
    source = '<?xml version="1.0"?><!DOCTYPE d [<!ENTITY e "x">]><ownershipDocument>&e;</ownershipDocument>'
    with pytest.raises(ValueError):
        parse_ownership(source)
