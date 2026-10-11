"""Point-in-time 값 선택: 그 날짜에 이미 공개돼 있던 XBRL 값만 고른다.

companyfacts/companyconcept는 같은 기간 값을 그 값을 실은 공시마다 한 행씩 준다(원공시, 다음 해 비교 표시, 정정,
8-K 재표시). 재작성·재분류로 값이 바뀌기도 하므로, 백테스트에서는 그 시점까지 나온 행 중 가장 늦은 행을 써야 한다.
`frame`이 붙은 행(SEC 대표값)은 대개 가장 늦은 공시의 행이라 과거 시점의 값으로 쓰면 미래 정보가 섞인다.
"""

from datetime import date
from itertools import groupby
from typing import Iterable, List, Tuple

from cluefin_openapi.sec._xbrl_api_types import FactValue


def values_as_of(values: Iterable[FactValue], as_of: date) -> List[FactValue]:
    """`as_of` 날이 시작될 때 이미 공개돼 있던 값을 기간마다 하나씩 고른다.

    - 공개 시점은 `filed`(EDGAR 제출일)다. `filed < as_of`인 행만 본다. EDGAR는 17:30 ET 뒤 접수를 다음 영업일
      제출로 치지만 16:00–17:30 접수는 그날 제출이라, `filed == as_of`인 행은 그날 장 마감 뒤에 나왔을 수 있다.
    - 기간(`start`, `end`)마다 `filed`가 가장 늦은 행을 고른다. `frame`·`fy`·`form`은 보지 않는다.
    - 같은 날 제출된 행이 여럿이면 접수번호 일련번호가 큰 행(늦게 접수된 공시)을 고른다. 접수번호 앞자리(제출자)가
      다르면 순서를 알 수 없으므로 오류를 낸다.

    Args:
        values (Iterable[FactValue]): 개념 하나, 단위 하나의 값들 (예: `concept.units["USD"]`). 단위를 섞지 않는다.
        as_of (date): 기준일. 이 날 이전에 제출된 값만 쓴다.

    Returns:
        List[FactValue]: 기간마다 한 행, `end` 순(같은 `end`면 시점 값이 먼저, 그다음 `start` 순).
            `as_of` 전에 공개된 값이 없는 기간은 빠진다.

    Raises:
        ValueError: 같은 기간·같은 제출일에 앞자리가 다른 접수번호가 섞였거나, 한 공시가 같은 기간에 다른 값을 둘 실었을 때
    """
    known = sorted((value for value in values if value.filed < as_of), key=_period_key)
    return [_latest(list(rows)) for _, rows in groupby(known, key=_period_key)]


def _period_key(value: FactValue) -> Tuple[date, bool, date]:
    """기간 정렬 키. 시점 값(`start` 없음)과 같은 `end`의 기간 값을 가른다."""
    return (value.end, value.start is not None, value.start or date.min)


def _latest(rows: List[FactValue]) -> FactValue:
    """한 기간의 행들 중 가장 늦게 공개된 행."""
    last_filed = max(row.filed for row in rows)
    same_day = [row for row in rows if row.filed == last_filed]
    filers = {_filer(row.accn) for row in same_day}
    if len(filers) > 1:
        raise ValueError(f"같은 날 제출자가 다른 공시가 겹쳐 순서를 알 수 없습니다: {_describe(same_day)}")

    last_accn = max(row.accn for row in same_day)
    picked = [row for row in same_day if row.accn == last_accn]
    if len({row.val for row in picked}) > 1:
        raise ValueError(f"한 공시가 같은 기간에 다른 값을 실었습니다: {_describe(picked)}")
    return picked[0]


def _filer(accn: str) -> str:
    """접수번호 앞자리(제출자 CIK). 같은 제출자 안에서만 뒷자리 일련번호로 접수 순서를 비교할 수 있다."""
    return accn.split("-", 1)[0]


def _describe(rows: List[FactValue]) -> str:
    """오류 메시지용: 기간과 행마다 접수번호·서식·제출일·값."""
    listed = ", ".join(f"{row.accn}({row.form}, {row.filed}, {row.val})" for row in rows)
    return f"기간 {rows[0].start}~{rows[0].end}: {listed}"
