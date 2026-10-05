"""원문 바이트를 파싱 가능한 XML로 만드는 파이프라인."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING

from defusedxml.ElementTree import ParseError, fromstring

from cluefin_dart_notes.repair._decoder import Decoder
from cluefin_dart_notes.repair._positional import PositionalRepair
from cluefin_dart_notes.repair._report import (
    MAX_SAMPLES,
    DartXmlRepairError,
    RepairReport,
    RepairResult,
    RepairSample,
    sample_at,
)
from cluefin_dart_notes.repair._rules import DEFAULT_RULES, RepairRule

if TYPE_CHECKING:
    from cluefin_dart_notes._xml import Element

logger = logging.getLogger(__name__)


class DartXmlRepairer:
    """`bytes → Decoder → 규칙 1…N → 파싱`을 거치고, 파싱이 실패하면 `PositionalRepair`로 넘긴다.

    Args:
        decoder: 인코딩 판정. 기본은 utf-8 → cp949.
        rules: 순서대로 적용할 규칙. 기본은 `DEFAULT_RULES`. 순서에 의미가 있다(각 규칙의 설명 참고).
        fallback: 규칙을 거친 뒤에도 파싱이 실패할 때 쓰는 위치 기반 수리.
        strict: 참이면 대체 수리 없이 첫 파싱 오류에서 `DartXmlRepairError`를 낸다. 테스트와 진단용이다.
    """

    def __init__(
        self,
        *,
        decoder: Decoder | None = None,
        rules: Sequence[RepairRule] = DEFAULT_RULES,
        fallback: PositionalRepair | None = None,
        strict: bool = False,
    ) -> None:
        self.decoder = decoder if decoder is not None else Decoder()
        self.rules: tuple[RepairRule, ...] = tuple(rules)
        self.fallback = fallback if fallback is not None else PositionalRepair()
        self.strict = strict

    def with_rule(self, rule: RepairRule, *, before: str | None = None) -> DartXmlRepairer:
        """규칙을 끼워 넣은 새 repairer. `before`가 없으면 맨 뒤에 붙인다."""
        rules = list(self.rules)
        if before is None:
            rules.append(rule)
        else:
            names = [existing.name for existing in rules]
            if before not in names:
                raise ValueError(f"규칙 {before}이(가) 없습니다. 현재 규칙: {', '.join(names)}")
            rules.insert(names.index(before), rule)
        return self._replace(rules)

    def without_rule(self, name: str) -> DartXmlRepairer:
        """이름이 `name`인 규칙을 뺀 새 repairer."""
        rules = [rule for rule in self.rules if rule.name != name]
        if len(rules) == len(self.rules):
            raise ValueError(f"규칙 {name}이(가) 없습니다.")
        return self._replace(rules)

    def repair(self, raw: bytes) -> RepairResult:
        """정리된 utf-8 XML과 기록. 파싱에 성공한 XML만 돌려준다."""
        return self.parse(raw)[1]

    def parse(self, raw: bytes) -> tuple[Element, RepairResult]:
        decoded = self.decoder.decode(raw)
        reports: list[RepairReport] = [decoded.report] if decoded.report else []
        text = decoded.text
        for rule in self.rules:
            outcome = rule.apply(text)
            text = outcome.text
            if outcome.count or outcome.warnings:
                reports.append(RepairReport(rule.name, outcome.count, outcome.samples, outcome.warnings))
                for warning in outcome.warnings:
                    logger.warning(warning)

        root, text, positional = self._parse_with_fallback(text, reports)
        if positional is not None:
            reports.append(positional)
            logger.warning(
                "규칙이 모르는 오류 %d건을 위치 기반으로 고쳤습니다. 보고서의 견본으로 새 규칙을 검토하세요.",
                positional.count,
            )
        return root, RepairResult(xml=text.encode("utf-8"), encoding=decoded.encoding, reports=tuple(reports))

    def _parse_with_fallback(self, text: str, reports: list[RepairReport]) -> tuple[Element, str, RepairReport | None]:
        fixes = 0
        samples: list[RepairSample] = []

        def so_far() -> tuple[RepairReport, ...]:
            positional = (RepairReport(self.fallback.name, fixes, tuple(samples)),) if fixes else ()
            return (*reports, *positional)

        while True:
            try:
                root = fromstring(text.encode("utf-8"))
            except ParseError as error:
                if self.strict or fixes >= self.fallback.max_fixes:
                    reason = "strict 모드" if self.strict else f"위치 기반 수리 {fixes}회 초과"
                    raise DartXmlRepairError(
                        f"원문을 파싱할 수 없습니다({reason}): {error}", reports=so_far(), last_error=error
                    ) from error
                try:
                    text, index = self.fallback.fix(text, error)
                except DartXmlRepairError as unfixable:
                    unfixable.reports = so_far()
                    raise
                fixes += 1
                if len(samples) < MAX_SAMPLES:
                    samples.append(sample_at(text, index))
                continue
            return root, text, so_far()[-1] if fixes else None

    def _replace(self, rules: Sequence[RepairRule]) -> DartXmlRepairer:
        return DartXmlRepairer(decoder=self.decoder, rules=rules, fallback=self.fallback, strict=self.strict)
