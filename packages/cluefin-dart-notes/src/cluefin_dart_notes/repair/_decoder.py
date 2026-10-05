"""원문 바이트를 문자열로 바꾼다."""

from __future__ import annotations

import codecs
import re
from dataclasses import dataclass

from cluefin_dart_notes.repair._report import DartXmlRepairError, RepairReport, sample_at

_DECLARED_ENCODING = re.compile(r"""(<\?xml[^>]*?encoding\s*=\s*)(["'])([^"']*)\2""")


@dataclass(frozen=True)
class DecodeResult:
    text: str
    encoding: str
    report: RepairReport | None = None


class Decoder:
    """후보 인코딩을 순서대로 시도해 처음 성공한 것으로 디코딩한다.

    2017~2022년 제출분은 `encoding="utf-8"`로 선언하고 실제로는 cp949다. 선언은 믿지 않는다.
    정리된 XML은 utf-8로 다시 인코딩하므로 선언도 utf-8로 바꾼다. 선언과 실제가 다르면 `decoder` 보고를 남긴다
    (해당 연도에는 늘 있는 일이라 경고로 올리지는 않는다).
    """

    def __init__(self, candidates: tuple[str, ...] = ("utf-8", "cp949")) -> None:
        if not candidates:
            raise ValueError("인코딩 후보가 비어 있습니다.")
        self.candidates = candidates

    def decode(self, raw: bytes) -> DecodeResult:
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        for encoding in self.candidates:
            try:
                text = raw.decode(encoding)
            except UnicodeDecodeError:
                continue
            return self._with_utf8_declaration(text, encoding)
        raise DartXmlRepairError(f"원문을 디코딩할 수 없습니다. 시도한 인코딩: {', '.join(self.candidates)}")

    @staticmethod
    def _with_utf8_declaration(text: str, encoding: str) -> DecodeResult:
        match = _DECLARED_ENCODING.search(text, 0, 200)
        if match is None:
            return DecodeResult(text=text, encoding=encoding)
        declared = match.group(3)
        fixed = f"{text[: match.start(3)]}utf-8{text[match.end(3) :]}"
        if _codec_name(declared) == _codec_name(encoding):
            return DecodeResult(text=fixed, encoding=encoding)
        report = RepairReport(
            rule="decoder",
            count=1,
            samples=(sample_at(text, match.start(3)),),
        )
        return DecodeResult(text=fixed, encoding=encoding, report=report)


def _codec_name(name: str) -> str:
    try:
        return codecs.lookup(name).name
    except LookupError:
        return name.lower()
