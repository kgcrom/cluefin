"""서식별 Item 카탈로그. 데이터만 둔다.

새 Item(예: 2023년 신설 1C)이나 새 제목 표기를 만나면 여기 한 줄을 더하는 것으로 끝나야 한다. 탐지기는 카탈로그를
보고 Item을 찾고, 카탈로그에 없는 Item 표기는 `unknown_item`으로, 있어야 하는데 못 찾은 Item은 `missing_item`으로
보고한다(`_model.py`의 Finding 코드).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ItemSpec:
    """Item 하나.

    Attributes:
        part: 로마 숫자 Part(`I`·`II`…). 8-K처럼 Part가 없는 서식은 None.
        number: Item 번호(`1A`, `7`, `2.02`). 대문자.
        title: 현행 표준 제목.
        aliases: 예전 제목이나 흔한 다른 표기. 제목만으로 Item을 알아볼 때(번호 없는 목차 행) 쓴다.
        since: 이 Item이 생긴 기준일(보고 기간 말 기준). 그 전 공시에는 없어도 누락이 아니다.
        optional: 있어도 되고 없어도 되는 Item(예: 10-K Item 16 Form 10-K Summary).
        may_be_incorporated: 위임장(DEF 14A) 등에서 참조로 편입해 본문이 한 줄뿐인 것이 정상인 Item(Part III).
    """

    part: str | None
    number: str
    title: str
    aliases: tuple[str, ...] = ()
    since: date | None = None
    optional: bool = False
    may_be_incorporated: bool = False

    @property
    def titles(self) -> tuple[str, ...]:
        return (self.title, *self.aliases)

    def applies_to(self, period_end: date | None) -> bool:
        """보고 기간 말이 `since` 이후인지. 기간을 모르면 적용한다고 본다."""
        return self.since is None or period_end is None or period_end >= self.since


@dataclass(frozen=True)
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
        _item("II", "7", "Management's Discussion and Analysis of Financial Condition and Results of Operations"),
        _item("II", "7A", "Quantitative and Qualitative Disclosures About Market Risk"),
        _item("II", "8", "Financial Statements and Supplementary Data"),
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
        ),
        _item("IV", "16", "Form 10-K Summary", since=date(2016, 6, 9), optional=True),
    ),
)

CATALOGS: tuple[FormCatalog, ...] = (FORM_10K,)


def catalog_for(form: str | None) -> FormCatalog | None:
    """서식 이름(`10-K/A` 포함)에 맞는 카탈로그. 지원하지 않는 서식이면 None."""
    if not form:
        return None
    base = form.upper().removesuffix("/A")
    return next((catalog for catalog in CATALOGS if base in catalog.forms), None)
