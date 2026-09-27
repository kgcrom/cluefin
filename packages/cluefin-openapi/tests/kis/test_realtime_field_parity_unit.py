"""TS realtime field lists must match these Python lists in order.

Realtime payloads are '^'-joined values, so field names are assigned by position only. The sibling
`cluefin-openapi-ts` lists were copied by hand, and a wrong order with the right count silently puts
values into the wrong fields (2026-09-27: H0BJASP0 bond orderbook). Python is the reference.
"""

from pathlib import Path

import pytest

from cluefin_openapi.kis import _domestic_realtime_quote_types as domestic
from cluefin_openapi.kis import _onmarket_bond_realtime_quote_types as bond
from cluefin_openapi.kis import _overseas_realtime_quote_types as overseas

TS_METADATA = Path(__file__).resolve().parents[3] / "cluefin-openapi-ts" / "src" / "kis" / "metadata"
TS_FILES = {
    "domestic": TS_METADATA / "domestic-realtime-quote.ts",
    "overseas": TS_METADATA / "overseas-realtime-quote.ts",
    "bond": TS_METADATA / "onmarket-bond-realtime-quote.ts",
}

CASES = [
    ("domestic", "EXECUTION_FIELD_NAMES", domestic.EXECUTION_FIELD_NAMES),
    ("domestic", "ORDERBOOK_FIELD_NAMES", domestic.ORDERBOOK_FIELD_NAMES),
    ("domestic", "EXECUTION_NOTIFICATION_FIELD_NAMES", domestic.EXECUTION_NOTIFICATION_FIELD_NAMES),
    ("overseas", "OVERSEAS_ORDERBOOK_FIELD_NAMES", overseas.OVERSEAS_ORDERBOOK_FIELD_NAMES),
    (
        "overseas",
        "OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES",
        overseas.OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES,
    ),
    ("overseas", "OVERSEAS_EXECUTION_FIELD_NAMES", overseas.OVERSEAS_EXECUTION_FIELD_NAMES),
    (
        "overseas",
        "OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES",
        overseas.OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES,
    ),
    ("bond", "BOND_EXECUTION_FIELD_NAMES", bond.BOND_EXECUTION_FIELD_NAMES),
    ("bond", "BOND_ORDERBOOK_FIELD_NAMES", bond.BOND_ORDERBOOK_FIELD_NAMES),
    ("bond", "BOND_INDEX_EXECUTION_FIELD_NAMES", bond.BOND_INDEX_EXECUTION_FIELD_NAMES),
]


def _ts_field_names(source: str, name: str) -> list[str]:
    """Quoted items of `export const NAME = [ ... ] as const;`."""
    start = source.index(f"export const {name} = [")
    block = source[start : source.index("]", start)]
    return [line.strip().strip(",").strip("'") for line in block.splitlines()[1:]]


def _to_camel(name: str) -> str:
    head, *rest = name.split("_")
    return head + "".join(part[:1].upper() + part[1:] for part in rest)


@pytest.mark.skipif(not TS_METADATA.is_dir(), reason="cluefin-openapi-ts sibling not checked out")
@pytest.mark.parametrize(("ts_key", "name", "python_fields"), CASES, ids=[c[1] for c in CASES])
def test_ts_realtime_field_order_matches_python(ts_key, name, python_fields):
    source = TS_FILES[ts_key].read_text(encoding="utf-8")

    assert _ts_field_names(source, name) == [_to_camel(f) for f in python_fields]
