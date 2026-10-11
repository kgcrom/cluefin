"""Identifier normalisation for SEC URLs (CIK, accession number, path segments).

Every value that ends up in a URL path goes through one of these, so a stray
``/`` or ``..`` in caller input can never reach another sec.gov path.
"""

from __future__ import annotations

import re

_CIK_PATTERN = re.compile(r"^(?:CIK)?0*(\d{1,10})$", re.IGNORECASE)
_ACCESSION_PATTERN = re.compile(r"^(\d{10})-?(\d{2})-?(\d{6})$")
_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


def cik_digits(cik: int | str) -> str:
    """CIK without leading zeros, as used in Archives paths (``320193``)."""
    match = _CIK_PATTERN.match(str(cik).strip())
    if match is None or int(match.group(1)) == 0:
        raise ValueError(f"CIK는 1~10자리 숫자여야 합니다: {cik!r}")
    return str(int(match.group(1)))


def cik10(cik: int | str) -> str:
    """CIK zero-padded to 10 digits, as used in data.sec.gov paths (``0000320193``)."""
    return cik_digits(cik).zfill(10)


def accession_dashed(accession_number: str) -> str:
    """Accession number in its display form ``0000320193-23-000106``."""
    match = _ACCESSION_PATTERN.match(accession_number.strip())
    if match is None:
        raise ValueError(f"접수번호는 18자리 숫자(0000320193-23-000106 형식)여야 합니다: {accession_number!r}")
    return "-".join(match.groups())


def accession_plain(accession_number: str) -> str:
    """Accession number without dashes, as used in Archives folder names."""
    return accession_dashed(accession_number).replace("-", "")


def path_segment(value: str, *, what: str) -> str:
    """Validate a single URL path segment such as a taxonomy, tag or file name."""
    if not _SEGMENT_PATTERN.match(value) or ".." in value:
        raise ValueError(f"{what}에 쓸 수 없는 값입니다: {value!r}")
    return value
