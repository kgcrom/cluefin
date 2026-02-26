"""DART disclosure handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


@rpc_method(
    name="dart.disclosure_search",
    description="Search DART disclosures. Supports filtering by corp code, date range, type.",
    parameters={
        "type": "object",
        "properties": {
            "corp_code": {"type": "string", "description": "Corporate unique code (8 digits)"},
            "bgn_de": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_de": {"type": "string", "description": "End date (YYYYMMDD)"},
            "last_reprt_at": {"type": "string", "enum": ["Y", "N"], "description": "Last report only. Default N."},
            "pblntf_ty": {
                "type": "string",
                "enum": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "description": "Disclosure type (A:periodic, B:major, etc.)",
            },
            "corp_cls": {"type": "string", "enum": ["Y", "K", "N", "E"], "description": "Corp class"},
            "page_no": {"type": "integer", "description": "Page number"},
            "page_count": {"type": "integer", "description": "Items per page (1-100)"},
        },
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_disclosure_search(params: dict, session) -> dict:
    dart = session.get_dart()
    kwargs = {}
    for key in ["corp_code", "bgn_de", "end_de", "last_reprt_at", "pblntf_ty", "corp_cls", "page_no", "page_count"]:
        if key in params:
            kwargs[key] = params[key]
    result = dart.public_disclosure.public_disclosure_search(**kwargs)
    return result.model_dump() if hasattr(result, "model_dump") else {}


@rpc_method(
    name="dart.company_overview",
    description="Get company overview from DART.",
    parameters={
        "type": "object",
        "properties": {
            "corp_code": {"type": "string", "description": "Corporate unique code (8 digits)"},
        },
        "required": ["corp_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_company_overview(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.public_disclosure.company_overview(params["corp_code"])
    return result.model_dump() if hasattr(result, "model_dump") else {}


@rpc_method(
    name="dart.corp_code_lookup",
    description="Download DART corporate code list. Returns all registered companies.",
    parameters={"type": "object", "properties": {}},
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_corp_code_lookup(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.public_disclosure.corp_code()
    items = result.list if hasattr(result, "list") else []
    data = []
    for item in items or []:
        data.append(item.model_dump() if hasattr(item, "model_dump") else {})
    return {"total": len(data), "data": data}


@rpc_method(
    name="dart.major_shareholder",
    description="Get major shareholder status from periodic report.",
    parameters={
        "type": "object",
        "properties": {
            "corp_code": {"type": "string", "description": "Corporate unique code (8 digits)"},
            "bsns_year": {"type": "string", "description": "Business year (4 digits, e.g. 2024)"},
            "reprt_code": {
                "type": "string",
                "enum": ["11013", "11012", "11014", "11011"],
                "description": "Report code (11013:Q1, 11012:H1, 11014:Q3, 11011:Annual)",
            },
        },
        "required": ["corp_code", "bsns_year", "reprt_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_major_shareholder(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.periodic_report_key_information.get_major_shareholder_status(
        corp_code=params["corp_code"],
        bsns_year=params["bsns_year"],
        reprt_code=params["reprt_code"],
    )
    return result.model_dump() if hasattr(result, "model_dump") else {}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_disclosure_search,
    handle_company_overview,
    handle_corp_code_lookup,
    handle_major_shareholder,
]


def register_dart_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
