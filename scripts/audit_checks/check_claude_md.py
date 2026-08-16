"""`check_claude_md` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. No logic, naming, formatting or docstring change; `audit.py`
re-exports the name, so `audit.check_claude_md` is the same function object as before.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding


def check_claude_md(repo_path: Path) -> list[Finding]:
    """ADR-31 CLAUDE.md presence and non-empty per authority model baseline."""
    claude = repo_path / "CLAUDE.md"
    if not claude.exists():
        return [Finding("claude_md", "fail", "CLAUDE.md absent at repo root")]
    content = claude.read_text(encoding="utf-8").strip()
    if not content:
        return [Finding("claude_md", "fail", "CLAUDE.md exists but is empty")]
    return [Finding("claude_md", "pass", f"CLAUDE.md present ({len(content)} chars)")]
