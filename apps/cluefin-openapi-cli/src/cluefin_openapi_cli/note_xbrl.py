"""`sec note-series` 행에 XBRL companyfacts 개념과 값을 붙인다.

HTML 주석 표의 숫자는 companyfacts에도 있다. 태그는 해마다 같아 행 이름·표 순서가 바뀌어도 이어지지만, 차원(세그먼트·
지역) 값은 companyfacts에 없다. 그래서 HTML 행이 기준이고, XBRL은 행마다 맞는 개념을 찾아 덧붙인다.

- 10-K 연간 값만 쓴다(`form == "10-K"`, `fp == "FY"`, 기간이 없거나 350–380일).
- 행 값과 같은 기간말·같은 크기(행 단위의 한 단위 미만 차이, 부호 무시)인 us-gaap USD 개념을 찾는다. 가장 많은 해에서
  맞은 개념을 쓰고, 두 해 이상 값이 있는 행은 두 해 이상 맞아야 한다(작은 값이 우연히 맞는 것을 막는다). 한 해 값만
  있는 행은 그 값에 맞는 개념이 하나뿐일 때만 붙인다(세율 조정표 "Tax credits" (8)이 투자활동 개념에 맞은 일이 있다).
- 같은 기간이 여러 공시에 있으면 가장 늦게 제출된 값을 `values_by_fy`로, 처음 제출된 값이 다르면 `first_filed_by_fy`로.
"""

from __future__ import annotations

import bisect
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

_MILLION = Decimal(1_000_000)
_ANNUAL_DAYS = range(350, 381)
_TO_MILLIONS = {"thousands": Decimal("0.001"), "millions": Decimal(1), "billions": Decimal(1000)}


@dataclass(frozen=True, slots=True)
class _Fact:
    concept: str
    end: date
    instant: bool
    value: Decimal  # 백만 단위
    filed: date


class FactIndex:
    """기간말별로 값 크기순 정렬한 us-gaap USD 연간 값."""

    def __init__(self, facts: list[_Fact]) -> None:
        self._by_end: dict[date, list[tuple[Decimal, _Fact]]] = defaultdict(list)
        self._by_concept: dict[tuple[str, bool], list[_Fact]] = defaultdict(list)
        for fact in facts:
            self._by_end[fact.end].append((abs(fact.value), fact))
            self._by_concept[(fact.concept, fact.instant)].append(fact)
        for values in self._by_end.values():
            values.sort(key=lambda pair: pair[0])

    def __len__(self) -> int:
        return sum(len(values) for values in self._by_end.values())

    def near(self, end: date, value: Decimal, tolerance: Decimal) -> list[_Fact]:
        values = self._by_end.get(end, [])
        target = abs(value)
        start = bisect.bisect_left(values, target - tolerance, key=lambda pair: pair[0])
        found = []
        for magnitude, fact in values[start:]:
            if magnitude >= target + tolerance:
                break
            if abs(magnitude - target) < tolerance:
                found.append(fact)
        return found

    def series(self, concept: str, instant: bool, end: date) -> tuple[Decimal, Decimal] | None:
        """(가장 늦게 제출된 값, 처음 제출된 값)."""
        facts = sorted(
            (fact for fact in self._by_concept[(concept, instant)] if fact.end == end), key=lambda f: f.filed
        )
        if not facts:
            return None
        return facts[-1].value, facts[0].value


def fact_index(company_facts) -> FactIndex:
    """`CompanyFacts`(cluefin-openapi)에서 us-gaap USD 10-K 연간 값을 모은다."""
    facts = []
    for concept, concept_facts in (company_facts.facts or {}).get("us-gaap", {}).items():
        for fact in concept_facts.units.get("USD", []):
            if fact.form != "10-K" or fact.fp != "FY":
                continue
            if fact.start is not None and (fact.end - fact.start).days not in _ANNUAL_DAYS:
                continue
            facts.append(
                _Fact(f"us-gaap:{concept}", fact.end, fact.start is None, Decimal(fact.val) / _MILLION, fact.filed)
            )
    return FactIndex(facts)


def attach_xbrl(notes: list[dict], index: FactIndex, period_ends: dict[int, date]) -> tuple[int, int]:
    """`build_series` 결과의 금액 행마다 `xbrl`을 붙인다. (붙인 행 수, 금액 행 수)."""
    matched = total = 0
    fys = sorted(period_ends, reverse=True)
    for note in notes:
        for table in note["tables"]:
            for row in table["rows"]:
                if row["kind"] != "amount":
                    continue
                total += 1
                block = _row_xbrl(row, index, period_ends, fys)
                if block is not None:
                    row["xbrl"] = block
                    matched += 1
    return matched, total


def _row_xbrl(row: dict, index: FactIndex, period_ends: dict[int, date], fys: list[int]) -> dict | None:
    hits: dict[tuple[str, bool], set[int]] = defaultdict(set)
    nonzero = 0
    for fy_text, value in row["values_by_fy"].items():
        fy = int(fy_text)
        amount = Decimal(str(value))
        if amount == 0 or fy not in period_ends:
            continue
        nonzero += 1
        tolerance = _tolerance(row.get("unit_filed", {}).get(fy_text))
        for fact in index.near(period_ends[fy], amount, tolerance):
            hits[(fact.concept, fact.instant)].add(fy)
    if not hits:
        return None
    counts = Counter({key: len(years) for key, years in hits.items()})
    (best, best_count), *rest = counts.most_common()
    if best_count < min(2, nonzero) or (best_count == 1 and rest and rest[0][1] == 1):
        return None  # 한 해만 맞았는데 같은 값의 다른 개념도 있으면 우연일 수 있다
    concept, instant = best
    values, first_filed = {}, {}
    for fy in fys:
        found = index.series(concept, instant, period_ends[fy])
        if found is None:
            continue
        latest, first = found
        values[str(fy)] = _number(latest)
        if first != latest:
            first_filed[str(fy)] = _number(first)
    block: dict = {"concept": concept, "matched_fy": sorted(hits[best], reverse=True), "values_by_fy": values}
    if first_filed:
        block["first_filed_by_fy"] = first_filed
    alternatives = sorted(key[0] for key, count in rest if count == best_count)
    if alternatives:
        block["alternatives"] = alternatives
    return block


def _tolerance(unit: str | None) -> Decimal:
    """행 단위의 한 단위(백만 단위). 단위를 모르면 백만."""
    lowered = (unit or "").lower()
    return next((scale for word, scale in _TO_MILLIONS.items() if word in lowered), Decimal(1))


def _number(value: Decimal) -> float | int:
    rounded = value.quantize(Decimal("0.001"))
    return int(rounded) if rounded == rounded.to_integral_value() else float(rounded)
