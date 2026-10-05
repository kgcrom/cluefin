"""원문 정리 단계가 남기는 기록."""

from __future__ import annotations

from dataclasses import dataclass, field

MAX_SAMPLES = 5
_CONTEXT_RADIUS = 30


@dataclass(frozen=True)
class RepairSample:
    """고친 자리 하나. `line`·`column`은 1부터 센다. 정리 규칙은 줄 수를 바꾸지 않으므로 줄 번호는 원문과 같다."""

    line: int
    column: int
    context: str


@dataclass(frozen=True)
class RuleOutcome:
    """규칙 하나를 적용한 결과."""

    text: str
    count: int = 0
    samples: tuple[RepairSample, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class RepairReport:
    """규칙 하나가 문서에서 고친 것."""

    rule: str
    count: int
    samples: tuple[RepairSample, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class RepairResult:
    """정리된 XML과 단계별 기록. `reports`에는 실제로 무언가를 고친 단계만 들어 있다."""

    xml: bytes
    encoding: str
    reports: tuple[RepairReport, ...] = ()

    @property
    def used_fallback(self) -> bool:
        """규칙이 모르는 오류를 위치 기반 수리로 넘겼는지. 참이면 새 규칙을 만들 근거가 생긴 것이다."""
        return any(report.rule == "positional" for report in self.reports)

    @property
    def warnings(self) -> tuple[str, ...]:
        return tuple(warning for report in self.reports for warning in report.warnings)


class DartXmlRepairError(Exception):
    """정리해도 파싱할 수 없는 원문."""

    def __init__(
        self,
        message: str,
        *,
        reports: tuple[RepairReport, ...] = (),
        last_error: Exception | None = None,
        context: str = "",
    ) -> None:
        super().__init__(f"{message} (근처: {context!r})" if context else message)
        self.reports = reports
        self.last_error = last_error
        self.context = context


@dataclass
class SampleCollector:
    """규칙 구현용: 고친 위치를 세고 앞쪽 몇 개만 견본으로 남긴다."""

    text: str
    count: int = 0
    samples: list[RepairSample] = field(default_factory=list)

    def add(self, index: int) -> None:
        self.count += 1
        if len(self.samples) < MAX_SAMPLES:
            self.samples.append(sample_at(self.text, index))


def sample_at(text: str, index: int) -> RepairSample:
    line_start = text.rfind("\n", 0, index) + 1
    line = text.count("\n", 0, index) + 1
    context = text[max(0, index - _CONTEXT_RADIUS) : index + _CONTEXT_RADIUS].replace("\n", " ")
    return RepairSample(line=line, column=index - line_start + 1, context=context)
