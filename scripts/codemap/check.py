"""Freshness check: compare ARCHITECTURE.md inline codemap against fresh generation."""
from __future__ import annotations

import difflib
import sys
from pathlib import Path

from .generator import generate_codemap

_START_MARKER = "<!-- CODEMAP:START -->"
_END_MARKER = "<!-- CODEMAP:END -->"


def check_codemap(repo_path: Path, source_root: str = "src") -> tuple[int, str]:
    """Compare ARCHITECTURE.md codemap section against fresh generation.

    Returns (exit_code, output):
      0 — clean (no drift)
      1 — drift detected (output contains unified diff)
      2 — ARCHITECTURE.md missing
      3 — CODEMAP markers missing
    """
    arch_file = repo_path / "ARCHITECTURE.md"
    if not arch_file.exists():
        return 2, f"error: ARCHITECTURE.md not found at {arch_file}"

    content = arch_file.read_text(encoding="utf-8")

    start_idx = content.find(_START_MARKER)
    end_idx = content.find(_END_MARKER)

    if start_idx == -1 or end_idx == -1:
        return 3, (
            f"error: CODEMAP markers not found in {arch_file}\n"
            f"Expected '{_START_MARKER}' and '{_END_MARKER}'"
        )

    current = content[start_idx + len(_START_MARKER) : end_idx]

    fresh_mermaid, warnings = generate_codemap(repo_path, source_root)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)

    fresh = "\n" + fresh_mermaid

    if current == fresh:
        return 0, ""

    diff_lines = list(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            fresh.splitlines(keepends=True),
            fromfile="ARCHITECTURE.md (current)",
            tofile="ARCHITECTURE.md (fresh)",
        )
    )
    return 1, "".join(diff_lines)
