"""Financial statement note (disclosure) extraction from parsed XBRL data."""

from __future__ import annotations

import re

from cluefin_xbrl._types import (
    NoteLineItem,
    NoteSection,
    ParsedNotes,
    PresentationNode,
    XbrlDocument,
    XbrlFact,
    XbrlPeriod,
)

_NOTE_ROLE_PATTERN = re.compile(r"role-(D8\d+)")


def _identify_note_role(linkrole: str) -> tuple[str, bool] | None:
    """Identify a note (disclosure) role code and consolidated flag from a linkrole URI.

    DART note linkroles carry a role code of the form ``D8xxxxx``. By DART convention a
    code ending in ``0`` is the consolidated note and one ending in ``5`` is the separate note.

    Returns:
        ``(role_code, is_consolidated)`` if the linkrole is a note role, else ``None``.
    """
    match = _NOTE_ROLE_PATTERN.search(linkrole)
    if match is None:
        return None
    role_code = match.group(1)
    is_consolidated = not role_code.endswith("5")
    return role_code, is_consolidated
