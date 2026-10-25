"""Form 3·4·5 소유 신고(`ownershipDocument`) 모델.

필드명은 SEC XML 요소를 snake_case로 줄인 것이다. 값이 없으면 None이다(가격 대신 각주만 있는 행이 흔하다).
`footnote_ids`는 필드명 → 그 값에 붙은 각주 ID(`F1` …)이고, 본문은 `OwnershipDocument.footnotes`에 있다.
"""

from __future__ import annotations

import datetime
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

DOCUMENT_TYPES = frozenset({"3", "3/A", "4", "4/A", "5", "5/A"})
"""읽는 서식. 셋 다 같은 `ownershipDocument` 스키마다."""


@dataclass(frozen=True, slots=True)
class Issuer:
    """주식을 발행한 회사."""

    cik: str
    name: str | None
    trading_symbol: str | None


@dataclass(frozen=True, slots=True)
class ReportingOwner:
    """신고자. 펀드 공동 신고면 한 문서에 여럿이다."""

    cik: str
    name: str | None
    is_director: bool
    is_officer: bool
    is_ten_percent_owner: bool
    is_other: bool
    officer_title: str | None
    other_text: str | None


@dataclass(frozen=True, slots=True)
class Transaction:
    """거래 한 줄 (비파생 표 I, 파생 표 II).

    `code`는 SEC 거래 코드다: P 장내 매수, S 장내 매도, A 보상 지급, M 옵션 행사, F 세금 원천징수분, G 증여 …
    `acquired_disposed`는 "A"(취득)·"D"(처분), `direct_indirect`는 "D"(직접)·"I"(간접) 보유다.
    `exercise_price`부터 `underlying_value`까지는 파생 행에만 있다.
    """

    derivative: bool
    security_title: str | None
    date: datetime.date | None
    deemed_execution_date: datetime.date | None
    form_type: str | None
    code: str | None
    equity_swap: bool | None
    timeliness: str | None
    shares: Decimal | None
    total_value: Decimal | None
    price: Decimal | None
    acquired_disposed: str | None
    shares_owned_after: Decimal | None
    value_owned_after: Decimal | None
    direct_indirect: str | None
    nature_of_ownership: str | None
    exercise_price: Decimal | None
    exercise_date: datetime.date | None
    expiration_date: datetime.date | None
    underlying_title: str | None
    underlying_shares: Decimal | None
    underlying_value: Decimal | None
    footnote_ids: Mapping[str, tuple[str, ...]]


@dataclass(frozen=True, slots=True)
class Holding:
    """거래 없이 보유만 적은 줄 (Form 3의 보유, Form 4·5의 다른 보유 형태)."""

    derivative: bool
    security_title: str | None
    shares_owned: Decimal | None
    value_owned: Decimal | None
    direct_indirect: str | None
    nature_of_ownership: str | None
    exercise_price: Decimal | None
    exercise_date: datetime.date | None
    expiration_date: datetime.date | None
    underlying_title: str | None
    underlying_shares: Decimal | None
    underlying_value: Decimal | None
    footnote_ids: Mapping[str, tuple[str, ...]]


@dataclass(frozen=True, slots=True)
class Signature:
    name: str | None
    date: datetime.date | None


@dataclass(frozen=True, slots=True)
class OwnershipDocument:
    """Form 3·4·5(정정 포함) 한 건.

    `aff10b5_one`(사전 매매 계획 10b5-1 표시)은 2023년부터 있는 칸이라 그전 공시는 None이다.
    정정(`/A`)이 원본의 모든 행을 다시 싣는지는 공시마다 다르다(서명·비고만 고친 정정도 있다).
    """

    schema_version: str | None
    document_type: str
    period_of_report: datetime.date | None
    date_of_original_submission: datetime.date | None
    issuer: Issuer
    reporting_owners: tuple[ReportingOwner, ...]
    non_derivative_transactions: tuple[Transaction, ...]
    non_derivative_holdings: tuple[Holding, ...]
    derivative_transactions: tuple[Transaction, ...]
    derivative_holdings: tuple[Holding, ...]
    footnotes: Mapping[str, str]
    remarks: str | None
    signatures: tuple[Signature, ...]
    aff10b5_one: bool | None
    not_subject_to_section16: bool | None
    no_securities_owned: bool | None
    form3_holdings_reported: bool | None
    form4_transactions_reported: bool | None

    @property
    def is_amendment(self) -> bool:
        return self.document_type.endswith("/A")

    @property
    def transactions(self) -> tuple[Transaction, ...]:
        """비파생 거래 다음 파생 거래."""
        return self.non_derivative_transactions + self.derivative_transactions

    @property
    def holdings(self) -> tuple[Holding, ...]:
        """비파생 보유 다음 파생 보유."""
        return self.non_derivative_holdings + self.derivative_holdings
