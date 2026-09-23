"""Unit tests for the atomic JSON cache helpers in _atomic_file.py."""

import concurrent.futures
import json

import pytest

from cluefin_openapi._atomic_file import read_json_locked, write_json_atomic


def test_write_then_read_roundtrip(tmp_path):
    path = tmp_path / "cache.json"
    payload = {"a": 1, "b": ["x", "y"], "한글": "값"}

    write_json_atomic(path, payload)

    assert read_json_locked(path) == payload


def test_write_creates_no_leftover_temp_files(tmp_path):
    path = tmp_path / "cache.json"
    write_json_atomic(path, {"a": 1})

    entries = list(tmp_path.iterdir())
    names = {p.name for p in entries}
    # Only the final file and its lock file should remain; the NamedTemporaryFile
    # used for the atomic swap must have been renamed away, not left behind.
    assert names == {"cache.json", "cache.json.lock"}


def test_overwrite_replaces_content_atomically(tmp_path):
    path = tmp_path / "cache.json"
    write_json_atomic(path, {"version": 1})
    write_json_atomic(path, {"version": 2})

    assert read_json_locked(path) == {"version": 2}
    # Still no stray temp files after a second write.
    names = {p.name for p in tmp_path.iterdir()}
    assert names == {"cache.json", "cache.json.lock"}


def test_read_missing_file_raises_file_not_found(tmp_path):
    path = tmp_path / "does-not-exist.json"

    with pytest.raises(FileNotFoundError):
        read_json_locked(path)


def test_read_missing_file_still_creates_lock_file(tmp_path):
    path = tmp_path / "does-not-exist.json"

    with pytest.raises(FileNotFoundError):
        read_json_locked(path)

    assert (tmp_path / "does-not-exist.json.lock").exists()


def test_concurrent_writes_leave_valid_json(tmp_path):
    path = tmp_path / "cache.json"
    write_json_atomic(path, {"version": 0})

    def writer(n: int) -> None:
        write_json_atomic(path, {"version": n})

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(writer, n) for n in range(1, 21)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # The file must always contain a single, complete, parseable JSON document -
    # never a half-written or interleaved one - regardless of which writer won.
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    assert "version" in data
    assert isinstance(data["version"], int)
