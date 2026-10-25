"""HTML을 읽으며 고쳐 읽은 곳의 기록.

브라우저가 말없이 고쳐 읽는 것(안 닫힌 `<p>`, 짝 없는 닫는 태그)과 이 패키지가 일부러 건너뛴 것(숨김 요소)을
종류별 개수와 원문 위치 견본으로 남긴다. 결과가 이상할 때 원인을 찾는 출발점이고, 처음 보는 종류(`unknown_tag`)는
새 마크업이 나타났다는 신호다.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

MAX_SAMPLES = 5
_CONTEXT_LENGTH = 80

# 고쳐 읽은 곳의 종류. 새 종류를 만들면 여기에 더하고 설명을 단다.
IMPLICIT_CLOSE = "implicit_close"
"""여는 태그가 앞의 태그를 닫았다(`<p>a<p>b`, `<td>` 연속). 정상 HTML에도 흔하다."""
MISNESTED_END = "misnested_end"
"""닫는 태그가 그 안의 안 닫힌 태그까지 닫았다(`<div><span>…</div>`)."""
STRAY_END_TAG = "stray_end_tag"
"""여는 태그 없는 닫는 태그. 무시했다."""
UNCLOSED_AT_EOF = "unclosed_at_eof"
"""문서 끝까지 닫히지 않은 태그(html·head·body 제외)."""
UNKNOWN_TAG = "unknown_tag"
"""아는 HTML·인라인 XBRL 태그가 아니다. 내용은 그대로 읽었다. 새 마크업이면 태그 목록에 더한다."""
HIDDEN_CONTENT = "hidden_content"
"""`display:none` 요소와 `ix:header`. 본문에서 뺐다(인라인 XBRL 메타라 화면에 안 보인다)."""
LAYOUT_TABLE = "layout_table"
"""배치용 표(칸 하나, 또는 칸 안에 표). 표로 만들지 않고 안의 내용을 본문 흐름으로 읽었다."""
PAGE_FURNITURE = "page_furniture"
"""쪽 머리말·꼬리말(반복되는 짧은 줄, 쪽 번호). 본문에서 뺐다."""
ENCODING_FALLBACK = "encoding_fallback"
"""선언한 인코딩으로 읽히지 않아 다른 인코딩으로 읽었다."""

FIX_KINDS = (
    IMPLICIT_CLOSE,
    MISNESTED_END,
    STRAY_END_TAG,
    UNCLOSED_AT_EOF,
    UNKNOWN_TAG,
    HIDDEN_CONTENT,
    LAYOUT_TABLE,
    PAGE_FURNITURE,
    ENCODING_FALLBACK,
)


@dataclass(frozen=True, slots=True)
class SourceSample:
    """원문 위치 하나. `line`·`column`은 1부터 센다(원문 디코딩 후 문자 기준)."""

    line: int
    column: int
    context: str


@dataclass(frozen=True, slots=True)
class ParseFix:
    """한 종류의 고쳐 읽기. `samples`는 앞쪽 몇 개만 남긴다."""

    kind: str
    count: int
    samples: tuple[SourceSample, ...] = ()


@dataclass(frozen=True, slots=True)
class ParseReport:
    """문서 하나를 읽으며 고쳐 읽은 것 전부.

    Attributes:
        encoding: 실제로 디코딩에 쓴 인코딩.
        declared_encoding: 원문이 선언한 인코딩. 없으면 None.
        fixes: 한 번이라도 일어난 종류만, 종류 이름 순.
        unknown_tags: 처음 보는 태그 이름별 개수.
    """

    encoding: str
    declared_encoding: str | None = None
    fixes: tuple[ParseFix, ...] = ()
    unknown_tags: tuple[tuple[str, int], ...] = ()

    def count(self, kind: str) -> int:
        return next((fix.count for fix in self.fixes if fix.kind == kind), 0)

    def fix(self, kind: str) -> ParseFix | None:
        return next((fix for fix in self.fixes if fix.kind == kind), None)


@dataclass
class ReportCollector:
    """파서 구현용: 종류별로 세고 앞쪽 몇 개만 견본으로 남긴다."""

    counts: Counter[str] = field(default_factory=Counter)
    samples: dict[str, list[SourceSample]] = field(default_factory=dict)
    unknown_tags: Counter[str] = field(default_factory=Counter)

    def add(self, kind: str, line: int, column: int, context: str) -> None:
        self.counts[kind] += 1
        kept = self.samples.setdefault(kind, [])
        if len(kept) < MAX_SAMPLES:
            kept.append(SourceSample(line=line, column=column, context=_shorten(context)))

    def build(self, encoding: str, declared_encoding: str | None) -> ParseReport:
        fixes = tuple(
            ParseFix(kind=kind, count=self.counts[kind], samples=tuple(self.samples.get(kind, ())))
            for kind in sorted(self.counts)
        )
        return ParseReport(
            encoding=encoding,
            declared_encoding=declared_encoding,
            fixes=fixes,
            unknown_tags=tuple(sorted(self.unknown_tags.items())),
        )


def _shorten(text: str) -> str:
    text = " ".join(text.split())
    return text if len(text) <= _CONTEXT_LENGTH else text[: _CONTEXT_LENGTH - 1] + "…"
