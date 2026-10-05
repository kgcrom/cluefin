"""규칙이 모르는 오류를 파서가 알려 준 위치로 고치는 대체 수리."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable
from xml.parsers.expat import errors as expat_errors

from defusedxml.ElementTree import ParseError

from cluefin_dart_notes.repair._report import DartXmlRepairError
from cluefin_dart_notes.repair._tags import KNOWN_TAGS

_TAG_MISMATCH = expat_errors.codes[expat_errors.XML_ERROR_TAG_MISMATCH]
_TAG = re.compile(r"<(/?)([^\s<>/!?]+)[^<>]*?(/?)>")
_NAME_AFTER_LT = re.compile(r"/?([^\s<>/]+)")
_MARKUP = re.compile(r"[<&]")
_VALID_REFERENCE = re.compile(r"&(?:amp|lt|gt|quot|apos|#\d+|#x[0-9A-Fa-f]+);")


class PositionalRepair:
    """파싱 오류 위치 근처의 `<`나 `&` 하나를 escape한다. `DartXmlRepairer`가 최대 `max_fixes`번 반복해 부른다.

    expat의 오류 위치는 원인 글자를 정확히 가리키지 않는다. `R&D`는 `&`보다 두 글자 뒤를 가리키고,
    `<기후변화>`처럼 이름으로 읽히는 가짜 태그는 한참 뒤의 닫는 태그에서 "mismatched tag"로 실패한다.
    그래서 오류 종류에 따라 위치 직전의 `<`·`&`, 또는 닫히지 않은 가장 가까운 여는 태그를 찾는다.

    위치 직전을 찾을 때는 알려진 태그와 올바른 참조를 건너뛴다. 닫히지 않은 태그가 알려진 태그라면 고치지 않고 예외를 낸다. 진짜 태그를 텍스트로 만들면 뒤따르는
    닫는 태그가 다시 실패해 문서가 연쇄적으로 망가지기 때문이다.
    """

    name = "positional"

    def __init__(
        self,
        max_fixes: int = 50,
        *,
        known_tags: Iterable[str] = KNOWN_TAGS,
        token_window: int = 200,
        mismatch_window: int = 5000,
    ) -> None:
        self.max_fixes = max_fixes
        self.known_tags = frozenset(known_tags)
        self.token_window = token_window
        self.mismatch_window = mismatch_window

    def fix(self, text: str, error: ParseError) -> tuple[str, int]:
        """고친 문자열과 고친 위치를 돌려준다. 고칠 수 없으면 `DartXmlRepairError`."""
        index = _char_index(text, *error.position)
        if getattr(error, "code", None) == _TAG_MISMATCH:
            target = self._unclosed_open_tag(text, index)
        else:
            target = self._nearest_markup(text, index)
        if target is None:
            raise _unfixable(error, text, index, "근처에 알려진 태그와 올바른 참조밖에 없습니다")
        if text[target] == "&":
            return f"{text[:target]}&amp;{text[target + 1 :]}", target
        if self._is_markup_start(text, target):
            raise _unfixable(error, text, target, "닫히지 않은 태그가 알려진 태그입니다")
        return f"{text[:target]}&lt;{text[target + 1 :]}", target

    def _nearest_markup(self, text: str, index: int) -> int | None:
        # 오류 위치가 정상 마크업(`R&D</P>`의 `</P>`)을 가리키기도 해서, 알려진 태그와 올바른 참조는 건너뛴다.
        start = max(0, index - self.token_window)
        for match in reversed(list(_MARKUP.finditer(text, start, index + 1))):
            position = match.start()
            if text[position] == "&":
                if not _VALID_REFERENCE.match(text, position):
                    return position
            elif not self._is_markup_start(text, position):
                return position
        return None

    def _is_markup_start(self, text: str, position: int) -> bool:
        if text.startswith(("<?", "<!"), position):
            return True
        name = _NAME_AFTER_LT.match(text, position + 1)
        return bool(name) and name.group(1) in self.known_tags

    def _unclosed_open_tag(self, text: str, index: int) -> int | None:
        start = max(0, index - self.mismatch_window)
        pending_closes: Counter[str] = Counter()
        for match in reversed(list(_TAG.finditer(text, start, index))):
            is_close, name, self_closing = match.group(1), match.group(2), match.group(3)
            if self_closing:
                continue
            if is_close:
                pending_closes[name] += 1
            elif pending_closes[name]:
                pending_closes[name] -= 1
            else:
                return match.start()
        return None


def _char_index(text: str, line: int, column: int) -> int:
    """expat 위치(1부터 세는 줄, 0부터 세는 열)를 문자열 인덱스로 바꾼다. 열은 바이트가 아니라 글자 단위다(실측)."""
    line_start = 0
    for _ in range(line - 1):
        line_start = text.index("\n", line_start) + 1
    return min(line_start + column, len(text) - 1)


def _unfixable(error: ParseError, text: str, index: int, reason: str) -> DartXmlRepairError:
    return DartXmlRepairError(
        f"원문을 파싱할 수 없습니다: {error} — {reason}",
        last_error=error,
        context=text[max(0, index - 40) : index + 40],
    )
