"""Where review results that outlive a session live: `<repo>/research/`, shared by every worktree.

The root comes from the main checkout, not the current worktree — a record written from `.claude/worktrees/<name>`
must not vanish when that worktree is removed. Git is read from the `.git` entries directly, so no subprocess runs.
"""

from __future__ import annotations

import os
from pathlib import Path

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError

__all__ = ["RESEARCH_DIR_ENV", "research_root"]

RESEARCH_DIR_ENV = "CLUEFIN_RESEARCH_DIR"
_GITDIR_PREFIX = "gitdir:"


def _common_git_dir(start: Path) -> Path | None:
    """The `.git` directory every worktree of the repository containing ``start`` shares."""

    for folder in (start, *start.parents):
        dot_git = folder / ".git"
        if dot_git.is_dir():
            return dot_git
        if not dot_git.is_file():
            continue
        # A linked worktree's `.git` is a file pointing at `<main>/.git/worktrees/<name>`, whose `commondir` names
        # the shared `.git`.
        text = dot_git.read_text(encoding="utf-8").strip()
        if not text.startswith(_GITDIR_PREFIX):
            return None
        gitdir = folder / text[len(_GITDIR_PREFIX) :].strip()
        commondir = gitdir / "commondir"
        if commondir.is_file():
            return (gitdir / commondir.read_text(encoding="utf-8").strip()).resolve()
        return gitdir.resolve()
    return None


def research_root(cwd: Path | None = None) -> Path:
    """`$CLUEFIN_RESEARCH_DIR`, else `<main checkout>/research` of the repository the CLI runs in."""

    env = os.environ.get(RESEARCH_DIR_ENV, "").strip()
    if env:
        return Path(env).expanduser()
    common = _common_git_dir((cwd or Path.cwd()).resolve())
    if common is None:
        raise CliError(
            "Not inside a git repository, so there is no research/ folder to use.",
            exit_code=EXIT_USAGE,
            hint=f"Run from the repository, or set ${RESEARCH_DIR_ENV}.",
        )
    return common.parent / "research"
