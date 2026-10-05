"""원문 정리 규칙. 각 규칙은 상태가 없고 문자열을 받아 문자열을 돌려준다.

규칙은 줄바꿈을 더하거나 빼지 않는다. 그래서 견본과 파싱 오류의 줄 번호가 원문 파일의 줄 번호와 같다.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Protocol

from cluefin_dart_notes.repair._report import RuleOutcome, SampleCollector
from cluefin_dart_notes.repair._tags import KNOWN_TAGS

# `&cr;`이 남기는 줄바꿈 표식. 원문에는 쓰이지 않는다(코퍼스 0건).
LINE_BREAK = "\u2028"


class RepairRule(Protocol):
    """원문 정리 규칙. `name`은 보고서에 남는 이름이고 `DartXmlRepairer.with_rule(before=…)`가 가리키는 이름이다."""

    name: str

    def apply(self, text: str) -> RuleOutcome: ...


def _tag_alternation(tags: Iterable[str]) -> str:
    # 긴 이름부터 시도해야 SECTION-1 이 SECTION 처럼 잘리지 않는다.
    return "|".join(re.escape(tag) for tag in sorted(tags, key=len, reverse=True))


class ReplaceDartEntities:
    """DART 고유 엔티티(`&cr;` 등)를 숫자 문자 참조로 바꾼다.

    `&cr;`은 기본적으로 U+2028(LINE SEPARATOR)이 된다. 원문 소스에는 태그 사이에 서식용 줄바꿈이 많아
    (오래된 공시는 문단 4개 중 1개꼴) 일반 줄바꿈으로 바꾸면 `&cr;`의 줄바꿈과 구별할 수 없다.
    텍스트 추출(`Paragraph`·`Cell`)은 U+2028만 줄바꿈으로 살리고 나머지 공백은 한 칸으로 줄인다.
    값은 리터럴 대신 숫자 참조(`&#8232;`)로 넣어 원문 줄 번호를 바꾸지 않는다.
    """

    name = "dart-entities"

    def __init__(self, entities: Mapping[str, str] | None = None) -> None:
        self.entities = dict(entities) if entities is not None else {"cr": LINE_BREAK}
        names = "|".join(re.escape(name) for name in self.entities)
        self._pattern = re.compile(rf"&({names});") if names else None

    def apply(self, text: str) -> RuleOutcome:
        if self._pattern is None:
            return RuleOutcome(text=text)
        collector = SampleCollector(text)

        def replace(match: re.Match[str]) -> str:
            collector.add(match.start())
            return "".join(f"&#{ord(char)};" for char in self.entities[match.group(1)])

        fixed = self._pattern.sub(replace, text)
        return RuleOutcome(text=fixed, count=collector.count, samples=tuple(collector.samples))


class EscapeBareAmpersand:
    """XML 표준 엔티티나 숫자 참조가 아닌 `&`(`R&D` 등)를 `&amp;`로 바꾼다.

    DART 고유 엔티티보다 뒤에 둔다. 앞에 두면 `&cr;`이 `&amp;cr;`, 즉 글자 그대로 남는다.
    """

    name = "bare-ampersand"
    _pattern = re.compile(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9A-Fa-f]+);)")

    def apply(self, text: str) -> RuleOutcome:
        collector = SampleCollector(text)

        def replace(match: re.Match[str]) -> str:
            collector.add(match.start())
            return "&amp;"

        fixed = self._pattern.sub(replace, text)
        return RuleOutcome(text=fixed, count=collector.count, samples=tuple(collector.samples))


class EscapeUnknownTags:
    """허용 목록에 없는 태그 모양의 `<`를 `&lt;`로 바꾼다.

    `<기후변화>`, `<North Tower>`, `< TV 시장 >`, `<2024>`처럼 본문에 쓰인 꺾쇠가 대상이다. 한글도 XML 이름
    글자라서 파서는 이것을 태그로 읽고, 닫는 태그가 없으니 엉뚱한 곳에서 실패한다.

    허용 목록에 없는 영문 이름은 `unknown_names`로 센다. 그 이름의 닫는 태그(`</NAME>`)도 있으면 진짜 태그가
    목록에서 빠졌을 가능성이 높아 경고를 남긴다(`CORRECTION`이 그렇게 발견됐다).
    """

    name = "unknown-tags"
    _ascii_name = re.compile(r"/?([A-Za-z][A-Za-z0-9_.-]*)")

    def __init__(self, known_tags: Iterable[str] = KNOWN_TAGS) -> None:
        self.known_tags = frozenset(known_tags)
        self._pattern = re.compile(rf"<(?!(?:/?(?:{_tag_alternation(self.known_tags)})[\s>/])|[?!])")

    def apply(self, text: str) -> RuleOutcome:
        collector = SampleCollector(text)
        opened: Counter[str] = Counter()
        closed: Counter[str] = Counter()

        def replace(match: re.Match[str]) -> str:
            collector.add(match.start())
            name = self._ascii_name.match(text, match.end())
            if name:
                (closed if name.group(0).startswith("/") else opened)[name.group(1)] += 1
            return "&lt;"

        fixed = self._pattern.sub(replace, text)
        warnings = tuple(
            f"허용 목록에 없는 태그 {name}이(가) 여닫는 짝으로 {count}번 나왔습니다. 진짜 태그라면 KNOWN_TAGS에 추가하세요."
            for name, count in sorted(opened.items())
            if closed[name]
        )
        return RuleOutcome(text=fixed, count=collector.count, samples=tuple(collector.samples), warnings=warnings)


class NormalizeAttributes:
    """알려진 태그의 여는 태그에서 속성 부분이 잘못되면 `name="value"` 쌍만 뽑아 다시 쓴다.

    `ENG="Provisions … contracts "">`처럼 값 뒤에 따옴표가 하나 더 붙은 경우와 같은 이름이 두 번 나오는 경우를
    고친다. 같은 이름은 처음 값을 남긴다. 속성이 이미 올바른 태그는 건드리지 않는다.
    """

    name = "attributes"
    _attribute = re.compile(r"""([A-Za-z_][\w.:-]*)\s*=\s*("[^"]*"|'[^']*')""")
    _well_formed = re.compile(r"""(?:\s+[A-Za-z_][\w.:-]*\s*=\s*(?:"[^"<]*"|'[^'<]*'))*\s*""")

    def __init__(self, known_tags: Iterable[str] = KNOWN_TAGS) -> None:
        self._pattern = re.compile(rf"<({_tag_alternation(known_tags)})(\s[^<>]*?)?(/?)>")

    def apply(self, text: str) -> RuleOutcome:
        collector = SampleCollector(text)

        def replace(match: re.Match[str]) -> str:
            attributes = match.group(2)
            if not attributes or self._is_clean(attributes):
                return match.group(0)
            collector.add(match.start())
            pairs: dict[str, str] = {}
            for key, value in self._attribute.findall(attributes):
                pairs.setdefault(key, value)
            rebuilt = "".join(f" {key}={value}" for key, value in pairs.items())
            return f"<{match.group(1)}{rebuilt}{match.group(3)}>"

        fixed = self._pattern.sub(replace, text)
        return RuleOutcome(text=fixed, count=collector.count, samples=tuple(collector.samples))

    def _is_clean(self, attributes: str) -> bool:
        if not self._well_formed.fullmatch(attributes):
            return False
        names = [key for key, _ in self._attribute.findall(attributes)]
        return len(names) == len(set(names))


DEFAULT_RULES: tuple[RepairRule, ...] = (
    ReplaceDartEntities(),
    EscapeBareAmpersand(),
    EscapeUnknownTags(),
    NormalizeAttributes(),
)
