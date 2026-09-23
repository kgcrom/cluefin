"""Shared helpers for DART periodic-report unit tests.

Both ``test_periodic_report_key_information_unit.py`` and
``test_periodic_report_financial_statement_unit.py`` build a fake DART JSON
body (``status``/``message``/``list``) from a pydantic item type, filling in
any field not explicitly overridden with a type-appropriate placeholder value.
"""

import types
from typing import Any, Literal, Type, Union, get_args, get_origin

from pydantic import BaseModel


def default_value(annotation: Any, field_name: str) -> Any:
    """Produce a placeholder value matching the field's declared type."""
    origin = get_origin(annotation)
    if origin is None:
        if annotation is int:
            return 1
        if annotation is float:
            return 1.0
        return f"{field_name}-value"
    if origin is Literal:
        return get_args(annotation)[0]
    if origin in (types.UnionType, Union):
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if not args:
            return None
        return default_value(args[0], field_name)
    return f"{field_name}-value"


def build_payload(
    item_type: Type[BaseModel],
    overrides: dict[str, Any] | None = None,
    common_values: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a fake DART response body containing one ``list`` item of ``item_type``.

    ``overrides`` wins over ``common_values``, which wins over the generic
    type-based placeholder from :func:`default_value`.
    """
    overrides = overrides or {}
    common_values = common_values or {}
    list_item: dict[str, Any] = {}
    for field_name, field in item_type.model_fields.items():
        if field_name in overrides:
            list_item[field_name] = overrides[field_name]
            continue
        if field_name in common_values:
            list_item[field_name] = common_values[field_name]
            continue
        list_item[field_name] = default_value(field.annotation, field_name)
    return {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "list": [list_item],
    }
