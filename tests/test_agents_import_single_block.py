"""N1 lane 12 (ruling O-11): `CLAUDE.md` imports `@AGENTS.md` instead of restating it.

Before this lane, two Conventions bullets -- "Never restate a count or roster in prose"
and "Resolve a locator before acting on it" -- were typed out in BOTH `CLAUDE.md` and
`AGENTS.md`, in slightly different words. Every session paid for the block twice: once
read directly, once again through the `@AGENTS.md` import. This module is the regression
gate: each shared rule must exist exactly once across the pair, never zero (the rule would
be lost) and never two (the session pays for it twice).
"""
from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"
AGENTS_MD = _REPO_ROOT / "AGENTS.md"

#: Marker substrings for the rules N1 lane 12 found stated in both files. Each must appear
#: in exactly one of CLAUDE.md / AGENTS.md now that CLAUDE.md relies on the import.
_SHARED_BLOCK_MARKERS = (
    "Never restate a count or roster in prose",
    "Resolve a locator before",
)


def test_claude_md_imports_agents_md() -> None:
    """CLAUDE.md carries the `@AGENTS.md` import line rather than re-typing its content."""
    assert "@AGENTS.md" in CLAUDE_MD.read_text(encoding="utf-8")


def test_shared_rules_exist_exactly_once_across_the_pair() -> None:
    """Each rule the two files used to both carry now appears in exactly one of them."""
    claude_text = CLAUDE_MD.read_text(encoding="utf-8")
    agents_text = AGENTS_MD.read_text(encoding="utf-8")
    for marker in _SHARED_BLOCK_MARKERS:
        count = claude_text.count(marker) + agents_text.count(marker)
        assert count == 1, (
            f"{marker!r} appears {count} times across CLAUDE.md + AGENTS.md -- expected "
            "exactly once now that CLAUDE.md imports AGENTS.md instead of restating it."
        )
