"""Freshness check: compare a markdown file's inline TOC against fresh generation.

Mirrors scripts/codemap/check.py — same fail-on-stale model and exit codes.
"""
from __future__ import annotations

import difflib
from pathlib import Path

from .generator import generate_toc

_START_MARKER = "<!-- TOC:START -->"
_END_MARKER = "<!-- TOC:END -->"


def check_toc(md_file: Path) -> tuple[int, str]:
    """Compare the file's TOC block against a fresh generation.

    Returns (exit_code, output):
      0 — clean (no drift)
      1 — drift detected (output contains unified diff)
      2 — file missing / unreadable
      3 — TOC markers missing
    """
    if not md_file.exists():
        return 2, f"error: file not found at {md_file}"

    try:
        content = md_file.read_text(encoding="utf-8")
    except OSError as exc:
        return 2, f"error: cannot read {md_file}: {exc}"

    start_idx = content.find(_START_MARKER)
    end_idx = content.find(_END_MARKER)

    if start_idx == -1 or end_idx == -1:
        return 3, (
            f"error: TOC markers not found in {md_file}\n"
            f"Expected '{_START_MARKER}' and '{_END_MARKER}'"
        )

    current = content[start_idx + len(_START_MARKER) : end_idx]
    fresh = "\n" + generate_toc(md_file)

    if current == fresh:
        return 0, ""

    diff_lines = list(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            fresh.splitlines(keepends=True),
            fromfile=f"{md_file.name} (current)",
            tofile=f"{md_file.name} (fresh)",
        )
    )
    return 1, "".join(diff_lines)
