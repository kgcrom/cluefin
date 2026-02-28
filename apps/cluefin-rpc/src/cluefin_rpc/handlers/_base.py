from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def extract_output(response, field="output"):
    """KIS 응답에서 지정된 output 필드를 추출하여 dict/list로 변환.

    - output: Optional[Item] → dict or None
    - output: Sequence[Item] → list[dict]
    - output1 + output2: 요약 + 상세 리스트
    """
    body = response.body
    data = getattr(body, field, None)
    if data is None:
        return None
    if isinstance(data, (list, tuple)):
        return [item.model_dump() if hasattr(item, "model_dump") else item for item in data]
    return data.model_dump() if hasattr(data, "model_dump") else data


def extract_body(response):
    """응답 body 전체를 model_dump(). Kiwoom 응답에 적합."""
    return response.body.model_dump() if hasattr(response.body, "model_dump") else {}


@dataclass
class MethodSchema:
    name: str
    description: str
    parameters: dict[str, Any]
    returns: dict[str, Any]
    category: str = ""
    requires_session: bool = True
    broker: str | None = None


def rpc_method(
    name: str,
    description: str,
    parameters: dict[str, Any],
    returns: dict[str, Any],
    category: str = "",
    requires_session: bool = True,
    broker: str | None = None,
):
    """Decorator that attaches _rpc_schema metadata to handler functions."""

    def decorator(fn):
        fn._rpc_schema = MethodSchema(
            name=name,
            description=description,
            parameters=parameters,
            returns=returns,
            category=category,
            requires_session=requires_session,
            broker=broker,
        )
        return fn

    return decorator
