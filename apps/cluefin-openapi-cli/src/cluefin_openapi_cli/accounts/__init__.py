"""Standard account tables: account key → XBRL ids and Korean labels, read from TOML files in this package.

`common.toml` holds the accounts every industry shares. A table has three groups — ``income``, ``balance``,
``cash`` — matching the statement sections `statements.py` searches. File order is output order.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from functools import cache
from importlib.resources import files

__all__ = ["GROUPS", "Item", "load_table"]

GROUPS = ("income", "balance", "cash")
_FIELDS = frozenset({"ids", "names"})


@dataclass(frozen=True, slots=True)
class Item:
    """One statement line: XBRL ids first, then Korean labels for filers off the taxonomy."""

    ids: tuple[str, ...]
    names: tuple[str, ...] = ()


def _item(where: str, entry: object) -> Item:
    if not isinstance(entry, dict) or not set(entry) <= _FIELDS:
        raise ValueError(f"{where}: an account takes only {sorted(_FIELDS)}")
    ids = entry.get("ids")
    names = entry.get("names", [])
    # A bare string would pass an element check one character at a time, so both must be lists.
    if not isinstance(ids, list) or not isinstance(names, list) or not ids:
        raise ValueError(f"{where}: ids must be a non-empty list of strings, names a list of strings")
    if not all(isinstance(value, str) for value in (*ids, *names)):
        raise ValueError(f"{where}: ids must be a non-empty list of strings, names a list of strings")
    return Item(tuple(ids), tuple(names))


@cache
def load_table(name: str = "common") -> dict[str, dict[str, Item]]:
    """``{group: {account key: Item}}`` from ``<name>.toml``. Raises ValueError on a malformed table."""
    data = tomllib.loads(files(__package__).joinpath(f"{name}.toml").read_text(encoding="utf-8"))
    unknown = set(data) - set(GROUPS)
    if unknown:
        raise ValueError(f"{name}.toml: unknown groups {sorted(unknown)}; expected {list(GROUPS)}")
    table = {
        group: {key: _item(f"{name}.{group}.{key}", entry) for key, entry in data.get(group, {}).items()}
        for group in GROUPS
    }
    keys = [key for group in table.values() for key in group]
    if len(keys) != len(set(keys)):
        raise ValueError(f"{name}.toml: an account key appears in more than one group")
    return table
