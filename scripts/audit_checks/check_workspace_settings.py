"""`check_workspace_settings` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL, together with `_WORKSPACE_REQUIRED_SETTINGS` and the `_strip_jsonc`
helper it exclusively owns. No logic, naming, formatting or docstring change; `audit.py`
re-exports all three names — `tests/test_audit.py` calls `aud._strip_jsonc` directly.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from ._common import Finding

# Required VS Code workspace settings (ADR-59 Decision 3). "upper" (not "default")
# is what clusters ALL-CAPS canonical .md files ahead of lowercase configs.
_WORKSPACE_REQUIRED_SETTINGS = {
    "explorer.sortOrder": "default",
    "explorer.sortOrderLexicographicOptions": "upper",
}


def _strip_jsonc(text: str) -> str:
    """Strip // and /* */ comments and trailing commas from JSON-with-comments.

    VS Code .code-workspace files are JSONC; json.loads cannot parse them. Comment
    stripping respects string literals so a `//` inside a string value survives.
    """
    out: list[str] = []
    i, n = 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def check_workspace_settings(repo_path: Path) -> list[Finding]:
    """Dot-prefixed .code-workspace carrying required sort settings (ADR-59 D3).

    FAIL if absent or unparseable; WARN if present but not dot-prefixed or a
    required setting is missing/wrong; PASS if dot-prefixed with correct settings.
    """
    workspaces = sorted(p for p in repo_path.iterdir()
                        if p.is_file() and p.name.endswith(".code-workspace"))
    if not workspaces:
        return [Finding("workspace_settings", "fail",
                        "No .code-workspace file at repo root")]

    ws = workspaces[0]
    try:
        data = json.loads(_strip_jsonc(ws.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, ValueError) as e:
        return [Finding("workspace_settings", "fail",
                        f"{ws.name} is not parseable JSON(C): {e}")]

    issues = []
    if not ws.name.startswith("."):
        issues.append(f"workspace file '{ws.name}' is not dot-prefixed")

    settings = data.get("settings", {})
    if not isinstance(settings, dict):
        settings = {}
    for key, expected in _WORKSPACE_REQUIRED_SETTINGS.items():
        actual = settings.get(key, "<absent>")
        if actual != expected:
            issues.append(f"{key}={actual!r} (expected {expected!r})")

    if issues:
        return [Finding("workspace_settings", "warn", f"{ws.name}: " + "; ".join(issues))]
    return [Finding("workspace_settings", "pass",
                    f"{ws.name} present, dot-prefixed, required sort settings correct")]
