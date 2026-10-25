"""13F 기관 보유 보고 모델.

13F 공시는 XML 두 개다: 표지(`primary_doc.xml`, `edgarSubmission`)와 보유 목록인 정보표(`informationTable`).
13F-NT(통지)는 다른 운용사가 대신 보고한다는 표지뿐이라 정보표가 없다.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass

FORM13F_TYPES = frozenset({"13F-HR", "13F-HR/A", "13F-NT", "13F-NT/A"})
"""읽는 서식."""

DOLLAR_VALUES_FROM = datetime.date(2023, 1, 3)
"""이날부터 제출한 정보표는 `value`를 달러로, 그전 제출분은 천 달러로 적는다.

보고 기준일이 아니라 제출일 기준이다: 2023년 이후에 낸 2019·2020년 기간 정정분도 달러였다(2026-10 실측).
"""


@dataclass(frozen=True, slots=True)
class Form13FManager:
    """표지에 적힌 다른 운용사.

    `sequence_number`는 요약 페이지(함께 보고하는 운용사)에만 있고, 정보표 행의 `other_managers`가 이 번호를 가리킨다.
    """

    sequence_number: int | None
    cik: str | None
    name: str | None
    form13f_file_number: str | None
    crd_number: str | None
    sec_file_number: str | None


@dataclass(frozen=True, slots=True)
class Form13FCover:
    """13F 표지(정정·통지 포함).

    `report_type`은 "13F HOLDINGS REPORT"(모두 직접 보고), "13F COMBINATION REPORT"(일부를 다른 운용사가 보고),
    "13F NOTICE"(전부를 다른 운용사가 보고)다. `amendment_type`은 "RESTATEMENT"(전체 재작성)·"NEW HOLDINGS"(보유 추가)다.
    `table_value_total`은 적힌 그대로다. 단위는 정보표와 같은 규칙(`DOLLAR_VALUES_FROM`)이지만 정보표 합계와
    1,000배 어긋난 공시가 있었고, `table_entry_total`도 실제 행 수와 다른 공시가 있었다(표본 92건 중 각 2건, 4건).
    """

    submission_type: str
    report_type: str | None
    period_of_report: datetime.date | None
    filer_cik: str | None
    manager_name: str | None
    form13f_file_number: str | None
    amendment_no: int | None
    amendment_type: str | None
    conf_denied_expired: bool | None
    other_managers: tuple[Form13FManager, ...]
    """이 운용사 몫을 대신 보고하는 다른 운용사 (NOTICE·COMBINATION)."""
    included_managers: tuple[Form13FManager, ...]
    """이 보고에 함께 담긴 운용사 (요약 페이지, 번호 있음)."""
    other_included_managers_count: int | None
    table_entry_total: int | None
    table_value_total: int | None
    is_confidential_omitted: bool | None
    signature_name: str | None
    signature_title: str | None
    signature_date: datetime.date | None

    @property
    def is_amendment(self) -> bool:
        return self.submission_type.endswith("/A")

    @property
    def is_notice(self) -> bool:
        return self.submission_type.startswith("13F-NT")


@dataclass(frozen=True, slots=True)
class Form13FHolding:
    """정보표 한 행.

    `value`는 제출일 기준 규칙으로 달러로 맞춘 값이다. `cusip`은 대문자로 맞추기만 한다(앞자리 0이 빠진 7·8자리도
    그대로 둔다). `shares_type`은 "SH"(주)·"PRN"(채권 원금), `put_call`은 "Put"·"Call", `investment_discretion`은
    "SOLE"·"DFND"(공유)·"OTR"(기타)다. `other_managers`는 표지 `included_managers`의 순번이다. 그 칸은 자유
    텍스트라("None", "N/A", 운용사 이름 …) 숫자로 읽히지 않으면 빈 튜플이고, 원문은 `other_managers_text`에 있다.
    """

    name_of_issuer: str | None
    title_of_class: str | None
    cusip: str | None
    figi: str | None
    value: int | None
    shares: int | None
    shares_type: str | None
    put_call: str | None
    investment_discretion: str | None
    other_managers: tuple[int, ...]
    other_managers_text: str | None
    voting_sole: int | None
    voting_shared: int | None
    voting_none: int | None


@dataclass(frozen=True, slots=True)
class Form13FTable:
    """정보표.

    `value_multiplier`는 적힌 값에 곱한 수다(천 달러 시절 1000, 달러 시절 1).
    `value_unit_suspect`는 제출일 규칙과 다른 단위로 적은 것 같을 때 True다. 경계 뒤에도 천 달러로 낸 공시가
    표본 약 55건 중 3건, 경계 전에 달러로 낸 것이 1건 있었다. 판정은 주식 행의 주당 금액(`value / shares`) 중앙값이
    `SUSPECT_PRICE_RANGE` 밖인지로 한다. 값은 고치지 않는다.
    """

    holdings: tuple[Form13FHolding, ...]
    value_multiplier: int
    value_unit_suspect: bool


@dataclass(frozen=True, slots=True)
class Form13F:
    """13F 한 건: 표지와 정보표. 통지(13F-NT)는 `table`이 None이다."""

    cover: Form13FCover
    table: Form13FTable | None

    @property
    def holdings(self) -> tuple[Form13FHolding, ...]:
        return self.table.holdings if self.table is not None else ()
