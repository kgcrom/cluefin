"""서식별 Item 카탈로그. 데이터만 둔다.

새 Item(예: 2023년 신설 1C)이나 새 제목 표기를 만나면 여기 한 줄을 더하는 것으로 끝나야 한다. 탐지기는 카탈로그를
보고 Item을 찾고, 카탈로그에 없는 Item 표기는 `unknown_item`으로, 있어야 하는데 못 찾은 Item은 `missing_item`으로
보고한다(`_model.py`의 Finding 코드).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class ItemSpec:
    """Item 하나.

    Attributes:
        part: 로마 숫자 Part(`I`·`II`…). 8-K처럼 Part가 없는 서식은 None.
        number: Item 번호(`1A`, `7`, `2.02`). 대문자.
        title: 현행 표준 제목.
        aliases: 예전 제목이나 흔한 다른 표기. 제목만으로 Item을 알아볼 때(번호 없는 목차 행) 쓴다.
        since: 이 Item이 생긴 기준일(보고 기간 말 기준). 그 전 공시에는 없어도 누락이 아니다.
        until: 이 Item이 없어진 기준일(그날부터 적용 안 함). 2004-08-23 전 8-K 번호 체계 등.
        optional: 있어도 되고 없어도 되는 Item(예: 10-K Item 16 Form 10-K Summary).
        may_be_incorporated: 위임장(DEF 14A) 등에서 참조로 편입해 본문이 한 줄뿐인 것이 정상인 Item(Part III).
        lists_documents: 본문이 다른 Item에 실린 문서의 목록이다(10-K Item 15). 쪽 참조("pages F-1 through F-30")를
            이 Item의 본문 위치로 보지 않는다.
        mandatory: 모든 제출자가 써야 해서 생략할 수 없는 Item(10-Q Part I Item 1·2·4). 못 찾으면 문서에 표기가 없어도
            생략(`omitted`)이 아니라 `missing_item`이다. 표기가 목차에만 있고 본문은 헤딩 없이 시작하는 공시가 있어서다.
        financial_statements: 재무제표 Item(10-K Item 8). 본문이 참조 몇 줄뿐이고 문서에 F-쪽이 따로 있으면, 쪽 번호를
            적지 않았어도("appears following Item 15") F-쪽을 본문으로 본다.
        min_chars, max_chars: 본문 길이(`Item.text`)의 그럴듯한 범위. 벗어나면 이웃 Item과의 경계가 틀린 것이다
            (`implausible_length`). 코퍼스 분포가 확실히 갈리는 Item에만 둔다(값의 근거는 패키지 AGENTS.md).
    """

    part: str | None
    number: str
    title: str
    aliases: tuple[str, ...] = ()
    since: date | None = None
    until: date | None = None
    optional: bool = False
    may_be_incorporated: bool = False
    lists_documents: bool = False
    financial_statements: bool = False
    mandatory: bool = False
    min_chars: int | None = None
    max_chars: int | None = None

    @property
    def titles(self) -> tuple[str, ...]:
        return (self.title, *self.aliases)

    def applies_to(self, period_end: date | None) -> bool:
        """보고 기간 말이 `[since, until)` 안인지. 기간을 모르면 적용한다고 본다."""
        if period_end is None:
            return True
        return (self.since is None or period_end >= self.since) and (self.until is None or period_end < self.until)


@dataclass(frozen=True, slots=True)
class FormCatalog:
    """서식 하나의 Item 목록(문서에 나오는 순서).

    Attributes:
        forms: 이 카탈로그를 쓰는 서식(정정 `/A`는 자동으로 포함).
        part_scoped: Item 번호가 Part마다 다시 시작해 (Part, Item)으로만 유일한지(10-Q).
    """

    name: str
    forms: tuple[str, ...]
    items: tuple[ItemSpec, ...]
    part_scoped: bool = False

    def index(self, part: str | None, number: str) -> int | None:
        for index, spec in enumerate(self.items):
            if spec.number == number and (part is None or not self.part_scoped or spec.part == part):
                return index
        return None

    def spec(self, part: str | None, number: str) -> ItemSpec | None:
        index = self.index(part, number)
        return None if index is None else self.items[index]

    def resolve(self, part: str | None, number: str) -> ItemSpec | None:
        """`spec`과 같되, Part마다 번호가 다시 시작하는 서식에서 그 Part에 없는 번호가 다른 Part 하나에만 있으면 그
        Item(10-Q의 5·6·1A는 Part II에만 있다). Part 헤딩을 놓쳐 현재 Part가 틀려도 이런 번호는 바로 읽힌다."""
        spec = self.spec(part, number)
        if spec is not None or not self.part_scoped:
            return spec
        matches = [spec for spec in self.items if spec.number == number]
        return matches[0] if len(matches) == 1 else None


def _item(part: str | None, number: str, title: str, *aliases: str, **options) -> ItemSpec:
    return ItemSpec(part=part, number=number, title=title, aliases=aliases, **options)


# 기준일은 SEC 규칙 시행일을 보고 기간 말로 옮긴 근사값이다(1A·1B: 2005-12-01 이후 끝나는 회계연도,
# 1C: 2023-12-15 이후, 9C: 2022년 초 시행, 16: 2016-06 시행).
FORM_10K = FormCatalog(
    name="10-K",
    forms=("10-K", "10-K405", "10-KT", "10-KSB"),
    items=(
        _item("I", "1", "Business"),
        _item("I", "1A", "Risk Factors", since=date(2005, 12, 1)),
        _item("I", "1B", "Unresolved Staff Comments", since=date(2005, 12, 1)),
        _item("I", "1C", "Cybersecurity", since=date(2023, 12, 15)),
        _item("I", "2", "Properties"),
        _item("I", "3", "Legal Proceedings"),
        _item(
            "I",
            "4",
            "Mine Safety Disclosures",
            "Submission of Matters to a Vote of Security Holders",
            "Removed and Reserved",  # 2010–2011. 제목만 "Reserved"인 것은 Item 6이다.
        ),
        _item(
            "II",
            "5",
            "Market for Registrant's Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities",
            "Market for the Registrant's Common Equity, Related Stockholder Matters and Issuer Purchases of Equity "
            "Securities",
            "Market for Registrant's Common Equity and Related Stockholder Matters",
            "Market for the Registrant's Common Equity and Related Stockholder Matters",
        ),
        _item("II", "6", "Reserved", "Selected Financial Data", "Selected Consolidated Financial Data"),
        _item(
            "II",
            "7",
            "Management's Discussion and Analysis of Financial Condition and Results of Operations",
            min_chars=3_000,
        ),
        _item(
            "II",
            "7A",
            "Quantitative and Qualitative Disclosures About Market Risk",
            "Quantitative and Qualitative Disclosures About Risk",
            max_chars=150_000,
        ),
        _item("II", "8", "Financial Statements and Supplementary Data", financial_statements=True),
        # SEC 서식에는 없고 일부 회사가 붙이는 Item(스모크 코퍼스에서 unknown_item으로 발견, 2개 연도에 반복).
        _item("II", "8A", "Unaudited Supplemental Presentation of Statements of Financial Condition", optional=True),
        _item("II", "9", "Changes in and Disagreements With Accountants on Accounting and Financial Disclosure"),
        _item("II", "9A", "Controls and Procedures", since=date(2003, 8, 14)),
        _item("II", "9B", "Other Information", since=date(2004, 8, 23)),
        _item(
            "II",
            "9C",
            "Disclosure Regarding Foreign Jurisdictions that Prevent Inspections",
            since=date(2021, 12, 31),
        ),
        _item(
            "III",
            "10",
            "Directors, Executive Officers and Corporate Governance",
            "Directors and Executive Officers of the Registrant",
            may_be_incorporated=True,
        ),
        _item("III", "11", "Executive Compensation", may_be_incorporated=True),
        _item(
            "III",
            "12",
            "Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters",
            "Security Ownership of Certain Beneficial Owners and Management",
            may_be_incorporated=True,
        ),
        _item(
            "III",
            "13",
            "Certain Relationships and Related Transactions, and Director Independence",
            "Certain Relationships and Related Transactions",
            may_be_incorporated=True,
        ),
        _item("III", "14", "Principal Accountant Fees and Services", may_be_incorporated=True),
        _item(
            "IV",
            "15",
            "Exhibits and Financial Statement Schedules",
            "Exhibits, Financial Statement Schedules",
            "Exhibits, Financial Statement Schedules, and Reports on Form 8-K",
            lists_documents=True,
        ),
        _item("IV", "16", "Form 10-K Summary", since=date(2016, 6, 9), optional=True),
    ),
)

# 10-Q는 Part마다 Item 번호가 다시 시작한다(Part I Item 1 재무제표, Part II Item 1 소송).
FORM_10Q = FormCatalog(
    name="10-Q",
    forms=("10-Q", "10-QT", "10-QSB"),
    part_scoped=True,
    items=(
        _item(
            "I",
            "1",
            "Financial Statements",
            "Condensed Consolidated Financial Statements",
            "Consolidated Financial Statements",
            "Unaudited Condensed Consolidated Financial Statements",
            "Condensed Consolidated Financial Statements (Unaudited)",
            "Financial Statements (Unaudited)",
            financial_statements=True,
            mandatory=True,
        ),
        _item(
            "I",
            "2",
            "Management's Discussion and Analysis of Financial Condition and Results of Operations",
            mandatory=True,
        ),
        _item(
            "I",
            "3",
            "Quantitative and Qualitative Disclosures About Market Risk",
            "Quantitative and Qualitative Disclosure About Market Risk",
            max_chars=50_000,
        ),
        _item(
            "I", "4", "Controls and Procedures", mandatory=True, max_chars=30_000
        ),  # "Item 4T"도 이 Item이다(`parse_item_label`)
        _item("II", "1", "Legal Proceedings"),
        _item("II", "1A", "Risk Factors", since=date(2005, 12, 1)),
        _item(
            "II",
            "2",
            "Unregistered Sales of Equity Securities and Use of Proceeds",
            "Changes in Securities and Use of Proceeds",
            "Changes in Securities",
        ),
        _item("II", "3", "Defaults Upon Senior Securities"),
        _item(
            "II",
            "4",
            "Mine Safety Disclosures",
            "Submission of Matters to a Vote of Security Holders",
            "Removed and Reserved",
        ),
        _item("II", "5", "Other Information"),
        _item("II", "6", "Exhibits", "Exhibits and Reports on Form 8-K", lists_documents=True),
    ),
)

# 8-K는 공시마다 사건에 해당하는 Item만 있다. 전부 optional이고, 어떤 Item이 있어야 하는지는 제출 이력의 Item 목록이
# 정답이다. 2004-08-23 시행 개정 전에는 번호 체계가 달랐다(Item 1–12). 번호가 겹치지 않아("5" ↔ "5.02") 한 카탈로그에 둔다.
_8K_SINCE = date(2004, 8, 23)


def _event(number: str, title: str, *aliases: str, since: date = _8K_SINCE, **options) -> ItemSpec:
    return _item(None, number, title, *aliases, since=since, optional=True, **options)


def _legacy_event(number: str, title: str, *aliases: str) -> ItemSpec:
    return _item(None, number, title, *aliases, until=_8K_SINCE, optional=True)


FORM_8K = FormCatalog(
    name="8-K",
    forms=("8-K", "8-K12B", "8-K12G3", "8-K15D5"),
    items=(
        _event("1.01", "Entry into a Material Definitive Agreement"),
        _event("1.02", "Termination of a Material Definitive Agreement"),
        _event("1.03", "Bankruptcy or Receivership"),
        _event("1.04", "Mine Safety - Reporting of Shutdowns and Patterns of Violations", since=date(2010, 8, 27)),
        _event("1.05", "Material Cybersecurity Incidents", since=date(2023, 12, 18)),
        _event("2.01", "Completion of Acquisition or Disposition of Assets"),
        _event("2.02", "Results of Operations and Financial Condition"),
        _event(
            "2.03",
            "Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a "
            "Registrant",
        ),
        _event(
            "2.04",
            "Triggering Events That Accelerate or Increase a Direct Financial Obligation or an Obligation under an "
            "Off-Balance Sheet Arrangement",
        ),
        _event("2.05", "Costs Associated with Exit or Disposal Activities"),
        _event("2.06", "Material Impairments"),
        _event(
            "3.01",
            "Notice of Delisting or Failure to Satisfy a Continued Listing Rule or Standard; Transfer of Listing",
        ),
        _event("3.02", "Unregistered Sales of Equity Securities"),
        _event("3.03", "Material Modification to Rights of Security Holders"),
        _event("4.01", "Changes in Registrant's Certifying Accountant"),
        _event(
            "4.02",
            "Non-Reliance on Previously Issued Financial Statements or a Related Audit Report or Completed Interim "
            "Review",
        ),
        _event("5.01", "Changes in Control of Registrant"),
        _event(
            "5.02",
            "Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; "
            "Compensatory Arrangements of Certain Officers",
            "Departure of Directors or Principal Officers; Election of Directors; Appointment of Principal Officers",
        ),
        _event("5.03", "Amendments to Articles of Incorporation or Bylaws; Change in Fiscal Year"),
        _event("5.04", "Temporary Suspension of Trading Under Registrant's Employee Benefit Plans"),
        _event(
            "5.05",
            "Amendment to Registrant's Code of Ethics, or Waiver of a Provision of the Code of Ethics",
            "Amendments to the Registrant's Code of Ethics, or Waiver of a Provision of the Code of Ethics",
        ),
        _event("5.06", "Change in Shell Company Status"),
        _event("5.07", "Submission of Matters to a Vote of Security Holders", since=date(2010, 2, 28)),
        _event("5.08", "Shareholder Director Nominations", since=date(2011, 9, 14)),
        _event("6.01", "ABS Informational and Computational Material"),
        _event("6.02", "Change of Servicer or Trustee"),
        _event("6.03", "Change in Credit Enhancement or Other External Support"),
        _event("6.04", "Failure to Make a Required Distribution"),
        _event("6.05", "Securities Act Updating Disclosure"),
        _event("6.06", "Static Pool", since=date(2016, 11, 23)),
        _event("6.10", "Alternative Filings of Asset-Backed Issuers", since=date(2016, 11, 23)),
        _event("7.01", "Regulation FD Disclosure"),
        _event("8.01", "Other Events"),
        _event("9.01", "Financial Statements and Exhibits", lists_documents=True),
        _legacy_event("1", "Changes in Control of Registrant"),
        _legacy_event("2", "Acquisition or Disposition of Assets"),
        _legacy_event("3", "Bankruptcy or Receivership"),
        _legacy_event("4", "Changes in Registrant's Certifying Accountant"),
        _legacy_event(
            "5", "Other Events", "Other Events and Regulation FD Disclosure", "Other Events and Required FD Disclosure"
        ),
        _legacy_event("6", "Resignations of Registrant's Directors"),
        _legacy_event(
            "7",
            "Financial Statements and Exhibits",
            "Financial Statements, Pro Forma Financial Information and Exhibits",
        ),
        _legacy_event("8", "Change in Fiscal Year"),
        _legacy_event("9", "Regulation FD Disclosure"),
        _legacy_event(
            "10", "Amendments to the Registrant's Code of Ethics, or Waiver of a Provision of the Code of Ethics"
        ),
        _legacy_event("11", "Temporary Suspension of Trading Under Registrant's Employee Benefit Plans"),
        _legacy_event("12", "Results of Operations and Financial Condition"),
    ),
)

CATALOGS: tuple[FormCatalog, ...] = (FORM_10K, FORM_10Q, FORM_8K)


def catalog_for(form: str | None) -> FormCatalog | None:
    """서식 이름(`10-K/A` 포함)에 맞는 카탈로그. 지원하지 않는 서식이면 None."""
    if not form:
        return None
    base = form.upper().removesuffix("/A")
    return next((catalog for catalog in CATALOGS if base in catalog.forms), None)
