"""원문 바이트를 문자열로. 선언을 먼저 믿되, 안 맞으면 다른 인코딩으로 읽고 기록한다."""

from __future__ import annotations

import codecs
import re

# 선언은 문서 앞쪽에만 있다. XML 선언(`<?xml … encoding='ASCII'?>`, Workiva)과 meta 두 형태.
_HEAD_BYTES = 4096
_DECLARATION = re.compile(
    rb"""<\?xml[^>]*?encoding\s*=\s*["']([A-Za-z0-9._-]+)["']"""
    rb"""|<meta[^>]*?charset\s*=\s*["']?([A-Za-z0-9._-]+)""",
    re.IGNORECASE,
)
# SEC 원문은 ASCII 선언이 흔하지만 실제로는 UTF-8이나 windows-1252 문자가 섞인다(오래된 공시는 cp1252가 흔하다).
_FALLBACKS = ("utf-8", "cp1252")
_BOMS = ((codecs.BOM_UTF8, "utf-8-sig"), (codecs.BOM_UTF16_LE, "utf-16"), (codecs.BOM_UTF16_BE, "utf-16"))


def declared_encoding(data: bytes) -> str | None:
    match = _DECLARATION.search(data[:_HEAD_BYTES])
    if match is None:
        return None
    name = (match.group(1) or match.group(2)).decode("ascii").lower()
    try:
        return codecs.lookup(name).name
    except LookupError:
        return None


def decode_html(data: bytes) -> tuple[str, str, str | None]:
    """`(문자열, 쓴 인코딩, 선언된 인코딩)`. 어느 인코딩으로도 안 읽히면 latin-1(실패하지 않는다)로 읽는다."""
    for bom, encoding in _BOMS:
        if data.startswith(bom):
            return data.decode(encoding), encoding, encoding
    declared = declared_encoding(data)
    candidates = [declared] if declared else []
    candidates += [encoding for encoding in _FALLBACKS if encoding != declared]
    for encoding in candidates:
        try:
            return data.decode(encoding), encoding, declared
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1"), "latin-1", declared
