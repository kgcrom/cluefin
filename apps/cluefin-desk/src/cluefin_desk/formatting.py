"""Text helpers shared by the TUI panels."""

from typing import Any

from rich.cells import cell_len


def pad(text: Any, width: int, align: str = "left") -> str:
    """Pad to a terminal *cell* width, not a character count.

    Korean names are double-width, so `f"{name:<20s}"` misaligns every column
    that contains one. `rich.cells.cell_len` measures what the terminal shows.
    Text wider than `width` is never truncated — a clipped 종목명 is worse than
    a nudged column.
    """
    text = "-" if text is None else str(text)
    fill = max(0, width - cell_len(text))
    return text + " " * fill if align == "left" else " " * fill + text
