"""키움 실시간(WebSocket) REAL 프레임용 스펙 대조: `data[].values` 키 집합만 본다.

REST 헬퍼(`_spec_conformance.assert_spec_conformance`)는 클라이언트의 `_post` 를 감싸
마지막 요청/응답을 붙잡는 방식이라 WS 프레임엔 못 쓴다. 실시간 포털 문서는 Length 칸이
비어 있어(`kiwoom-spec-audit-todo.md` 4절) Length 대조도 하지 않는다 — 여기선 REAL 프레임
`data[].values` 의 wire 키 집합을 TR type 별 `*Values` 모델의 alias 집합과만 비교한다.

REST 헬퍼와 같은 경고/실패 정책을 쓴다: `values` 가 비어 있으면(장중 초반 등) 판정 불가라
경고만 하고 넘어가고(`EmptyValuesWarning`), 모델에만 있는 키("missing")와 서버에만 있는
키("extra")는 구분해 실패시킨다.
"""

import warnings
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from pydantic import AliasChoices, BaseModel

from cluefin_openapi.kiwoom._socket_client import KiwoomWebSocketMessage


class EmptyValuesWarning(UserWarning):
    """REAL 프레임 항목의 ``values`` 가 비어 키 대조를 판정하지 못했다."""


@dataclass(frozen=True)
class RealKeyDiff:
    """한 TR type 항목의 ``values`` 키 차이. 둘 다 비어 있으면 일치."""

    type: str
    model_only: frozenset[str]
    server_only: frozenset[str]


def _alias_keys(model: type[BaseModel]) -> frozenset[str]:
    """모델이 wire 에서 읽는 키 집합 (``_spec_conformance._wire_names`` 와 같은 규칙)."""
    keys: set[str] = set()
    for name, field in model.model_fields.items():
        alias = field.validation_alias
        if isinstance(alias, AliasChoices):
            keys.update(choice for choice in alias.choices if isinstance(choice, str))
        elif isinstance(alias, str):
            keys.add(alias)
        else:
            keys.add(field.alias or name)
    return frozenset(keys)


def real_frame_key_diff(
    message: KiwoomWebSocketMessage,
    values_models: Mapping[str, type[BaseModel]],
    *,
    empty: list[str] | None = None,
) -> list[RealKeyDiff]:
    """``message`` 가 REAL 프레임이면 ``data[].values`` 키를 ``values_models`` 와 비교한다.

    ``values_models`` 에 없는 ``type`` 의 항목은 건너뛴다(그 TR 은 이 호출의 관심사가 아님).
    빈 ``values`` 는 ``empty`` (전달했다면) 에 그 type 을 appends 하고 diff 에는 넣지 않는다.
    차이가 없는 type 은 결과 리스트에 나타나지 않는다.
    """
    diffs: list[RealKeyDiff] = []
    if message.trnm != "REAL":
        return diffs
    for item in message.body.get("data") or []:
        if not isinstance(item, dict):
            continue
        tr_type = item.get("type")
        if not isinstance(tr_type, str):
            continue
        model = values_models.get(tr_type)
        if model is None:
            continue
        values = item.get("values")
        if not isinstance(values, dict):
            continue
        if not values:
            if empty is not None:
                empty.append(tr_type)
            continue
        model_keys = _alias_keys(model)
        server_keys = set(values)
        model_only = model_keys - server_keys
        server_only = server_keys - model_keys
        if model_only or server_only:
            diffs.append(
                RealKeyDiff(type=tr_type, model_only=frozenset(model_only), server_only=frozenset(server_only))
            )
    return diffs


def assert_real_frame_key_conformance(
    message: KiwoomWebSocketMessage,
    values_models: Mapping[str, type[BaseModel]],
    *,
    ignore: Iterable[str] = (),
) -> None:
    """``message`` 가 REAL 프레임이고 키가 어긋나면 실패한다. REAL 이 아니면 그냥 통과.

    ``ignore`` 는 FID(wire 키, 예: ``"667"``)를 받아 그 키의 missing/extra 차이를 무시한다.
    실측해 `VENDOR_DOC_ERRATA.md` 에 적은 것만 넣는다 (REST 헬퍼의 ``ignore`` 와 같은 용법).
    """
    empty: list[str] = []
    diffs = real_frame_key_diff(message, values_models, empty=empty)
    ignored = set(ignore)
    problems: list[str] = []
    for diff in diffs:
        for key in sorted(diff.model_only - ignored):
            problems.append(f"missing: {diff.type}.values.{key} (model declares it, server did not send it)")
        for key in sorted(diff.server_only - ignored):
            problems.append(f"extra: {diff.type}.values.{key} (server sent it, model does not declare it)")
    if empty:
        warnings.warn(
            EmptyValuesWarning(f"empty values, keys unchecked for type(s): {', '.join(sorted(set(empty)))}"),
            stacklevel=2,
        )
    assert not problems, "REAL frame values keys do not match the spec:\n" + "\n".join(f"  - {p}" for p in problems)
