"""표 셀의 금액 문자열."""

from __future__ import annotations

import re
from decimal import Decimal

# "1,234" "1,234.5" "(1,234)" "△1,234" "▲ 1,234" "-1,234". 괄호는 짝이 맞아야 한다.
_AMOUNT = re.compile(
    r"(?P<open>\()?\s*(?P<sign>[-−△▲])?\s*(?P<number>\d{1,3}(?:,\d{3})+|\d+)(?P<fraction>\.\d+)?\s*(?P<close>\))?"
)


def parse_amount(text: str) -> Decimal | None:
    """셀 문자열을 숫자로. 괄호·`△`·`▲`·`-`는 음수다. 빈 셀, `-`만 있는 셀, 숫자가 아닌 셀은 None.

    단위는 환산하지 않는다(`Table.unit`을 함께 쓴다).
    """
    match = _AMOUNT.fullmatch(text.strip())
    if match is None or bool(match.group("open")) != bool(match.group("close")):
        return None
    value = Decimal(match.group("number").replace(",", "") + (match.group("fraction") or ""))
    negative = bool(match.group("open")) or bool(match.group("sign"))
    return -value if negative else value
