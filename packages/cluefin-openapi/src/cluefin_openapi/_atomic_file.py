"""Atomic JSON cache helpers for multi-process CLI access."""

from __future__ import annotations

import fcntl
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


@contextmanager
def _locked(lock_path: Path, mode: int) -> Iterator[None]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), mode)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON to disk atomically while holding an exclusive lock."""
    text = json.dumps(payload, indent=2, ensure_ascii=False, default=str)
    lock_path = path.with_name(f"{path.name}.lock")

    with _locked(lock_path, fcntl.LOCK_EX):
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
            tmp_path = Path(handle.name)

        os.replace(tmp_path, path)


def read_json_locked(path: Path) -> dict[str, Any]:
    """Read JSON while holding a shared lock when the file exists."""
    lock_path = path.with_name(f"{path.name}.lock")
    with _locked(lock_path, fcntl.LOCK_SH):
        return json.loads(path.read_text(encoding="utf-8"))
