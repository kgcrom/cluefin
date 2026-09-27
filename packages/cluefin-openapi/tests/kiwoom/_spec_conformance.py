"""키움 통합테스트용 스펙 대조: 응답 키 정확 대조 + 요청·응답 Length 대조.

`isinstance`/`is not None` 검사는 모델이 틀려도 통과한다 — pydantic 은 모델에 없는 키를 버리고
서버가 안 보낸 키는 기본값으로 채운다. 그래서 서버 원문을 모델·포털 스펙과 직접 비교한다.

- 원문: 키움 클라이언트엔 KIS 같은 디버그 artifact 가 없다. `record_exchanges` 가 테스트 클라이언트의
  `_post` 를 감싸 마지막 요청 body 와 응답 JSON 을 붙잡는다 (운영 코드 무변경).
- 키 대조 규칙은 `tests/kis/_response_shape.py` 와 같다 (배열은 모든 행의 키 합집합). importlib 모드에선
  브로커 테스트 패키지끼리 import 가 안 돼 복사해 뒀다 — 규칙을 바꾸면 두 곳을 같이 고친다.
- Length 기준은 `spec_lengths.json` (포털 요청/응답 Body 표의 Length 열). 값의 **문자 수**로 비교한다 —
  문서가 바이트 기준이라도 문자 수 ≤ 바이트 수라 오탐은 없다. 부호(`+`/`-`, 키움의 겹친 `--`)와 선행 0
  패딩도 서버가 보낸 그대로 센다: 문서 Length 는 wire 값의 길이이기 때문이다.
- 실패 메시지엔 **값을 넣지 않는다** — 계좌 TR 응답엔 계좌번호가 섞인다. 필드명과 길이만 남긴다.
"""

import json
import types
import typing
import warnings
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import AliasChoices, BaseModel
from pydantic.fields import FieldInfo

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import KiwoomHttpResponse

SPEC_LENGTHS: dict[str, dict[str, dict[str, int]]] = {
    k: v for k, v in json.loads(Path(__file__).with_name("spec_lengths.json").read_text("utf-8")).items() if k[0] != "_"
}

# 응답 봉투. 모델은 `KiwoomHttpBody` 믹스인(pydantic 필드 아님)으로만 들고 있다.
ENVELOPE_KEYS = frozenset({"return_code", "return_msg"})


class EmptyBlockWarning(UserWarning):
    """배열 블록이 비어 항목 키·길이를 판정하지 못했다 — 휴장일·조회 조건 탓. 통과를 검증으로 착각하지 말 것."""


@dataclass
class Exchange:
    api_id: str | None
    body: dict[str, Any]
    raw: Any


def record_exchanges(client: Client) -> Client:
    """``client._post`` 를 감싸 마지막 요청·응답을 ``client._last_exchange`` 에 남긴다."""
    original = client._post

    def _post(path, headers, body, use_cache=True):
        client._last_exchange = None
        response = original(path, headers, body, use_cache)
        try:
            raw = response.json()
        except ValueError:
            raw = None
        client._last_exchange = Exchange(headers.get("api-id"), dict(body), raw)
        return response

    client._last_exchange = None
    client._post = _post
    return client


def _wire_names(name: str, field: FieldInfo) -> tuple[str, ...]:
    alias = field.validation_alias
    if isinstance(alias, AliasChoices):
        return tuple(c for c in alias.choices if isinstance(c, str))
    if isinstance(alias, str):
        return (alias,)
    return (field.alias or name,)


def _unwrap(annotation: Any) -> tuple[str, type[BaseModel] | None]:
    """Return ("object" | "array" | "scalar", nested model) for a field annotation."""
    origin = typing.get_origin(annotation)
    if origin in (typing.Union, types.UnionType):
        args = [a for a in typing.get_args(annotation) if a is not type(None)]
        if len(args) == 1:
            return _unwrap(args[0])
        return "scalar", None
    if origin in (list, Sequence):
        _, item = _unwrap(typing.get_args(annotation)[0])
        return "array", item
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return "object", annotation
    return "scalar", None


_KINDS = {list: "array", dict: "object"}


def response_shape_diff(
    raw: dict[str, Any], model: type[BaseModel], path: str = "", empty: list[str] | None = None
) -> list[str]:
    """Describe every difference between raw response keys and ``model``; empty means exact match.

    Array blocks are compared over the union of all rows' keys. Empty arrays are appended to ``empty``.
    """
    problems: list[str] = []
    claimed: set[str] = set(ENVELOPE_KEYS) if not path else set()

    for name, field in model.model_fields.items():
        names = _wire_names(name, field)
        claimed.update(names)
        present = next((n for n in names if n in raw), None)
        label = f"{path}{names[0]}"
        if present is None:
            problems.append(f"missing: {label} (model declares it, server did not send it)")
            continue

        kind, nested = _unwrap(field.annotation)
        actual = _KINDS.get(type(raw[present]), "scalar")
        if nested is None:
            continue
        if actual != kind:
            problems.append(f"kind: {label} is {actual} on the server, model expects {kind}")
            continue
        rows = raw[present] if kind == "array" else [raw[present]]
        keys = {key: None for row in rows for key in row}
        if keys:
            problems.extend(response_shape_diff(keys, nested, f"{label}.", empty))
        elif empty is not None:
            empty.append(label)

    for key in sorted(set(raw) - claimed):
        problems.append(f"extra: {path}{key} (server sent it, model does not declare it)")
    return problems


def _scalar_len(value: Any) -> int | None:
    if value is None or isinstance(value, (dict, list)):
        return None
    return len(str(value))


def length_diff(data: dict[str, Any], lengths: dict[str, int], side: str) -> list[str]:
    """Fields in ``data`` longer than the spec Length. Array blocks use the longest value over all rows."""
    observed: dict[str, int] = {}
    for key, value in data.items():
        if isinstance(value, list):
            for row in value:
                items = row.items() if isinstance(row, dict) else [("", row)]
                for child, v in items:
                    n = _scalar_len(v)
                    label = f"{key}.{child}" if child else key
                    if n is not None:
                        observed[label] = max(observed.get(label, 0), n)
        else:
            n = _scalar_len(value)
            if n is not None:
                observed[key] = n
    return [
        f"length: {side} {label} is {n} chars, spec Length is {lengths[label]}"
        for label, n in sorted(observed.items())
        if label in lengths and n > lengths[label]
    ]


def _problem_key(problem: str) -> str:
    """``"length: response foo.bar is ..."`` → ``"foo.bar"``, ``"extra: foo (..."`` → ``"foo"``."""
    parts = problem.split(" ")
    return parts[2] if parts[0] == "length:" else parts[1]


def assert_spec_conformance(
    client: Client,
    response: KiwoomHttpResponse,
    *,
    ignore: Iterable[str] = (),
    ignore_length: Iterable[str] = (),
) -> None:
    """마지막 요청·응답이 모델(키)과 포털 스펙(Length)에 맞지 않으면 실패한다.

    ``ignore`` 는 키 차이, ``ignore_length`` 는 Length 초과를 wire 경로(``"stk_frgnr.dt"``)로 받는다.
    둘 다 실측해 `VENDOR_DOC_ERRATA.md` 에 적은 건만 넣고, 호출부에 근거 주석을 단다.
    """
    exchange: Exchange | None = getattr(client, "_last_exchange", None)
    if exchange is None or not isinstance(exchange.raw, dict):
        raise AssertionError("no recorded Kiwoom exchange; is the client wrapped with record_exchanges()?")

    empty: list[str] = []
    ignored, ignored_length = set(ignore), set(ignore_length)
    spec = SPEC_LENGTHS.get(exchange.api_id or "", {})
    shape = response_shape_diff(exchange.raw, type(response.body), empty=empty)
    lengths = length_diff(exchange.body, spec.get("request", {}), "request")
    lengths += length_diff(exchange.raw, spec.get("response", {}), "response")
    problems = [p for p in shape if _problem_key(p) not in ignored]
    problems += [p for p in lengths if _problem_key(p) not in ignored_length]
    if empty:
        warnings.warn(
            EmptyBlockWarning(f"{exchange.api_id}: empty blocks, item keys/lengths unchecked: {', '.join(empty)}"),
            stacklevel=2,
        )
    assert not problems, f"{exchange.api_id} {type(response.body).__name__} does not match the spec:\n" + "\n".join(
        f"  - {p}" for p in problems
    )
