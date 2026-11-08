"""Kiwoom reads the continuation flag only from the ``cont-yn`` header.

Measured 2026-11-08 on ka90001: page two sent with ``cond-yn: Y`` came back as page one again,
the same request with ``cont-yn: Y`` returned the next page. ``con-yn``/``cond-yn`` are typos copied
from the vendor docs.
"""

import re
from pathlib import Path

import cluefin_openapi.kiwoom as kiwoom

_TYPO = re.compile(r"[\"'](con|cond)-yn[\"']")


def test_no_misspelled_continuation_header() -> None:
    root = Path(kiwoom.__file__).parent
    offenders = [
        f"{path.name}:{lineno}"
        for path in sorted(root.glob("*.py"))
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        if _TYPO.search(line)
    ]
    assert offenders == []
