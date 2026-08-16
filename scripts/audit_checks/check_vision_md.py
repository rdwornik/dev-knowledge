"""`check_vision_md` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. No logic, naming, formatting or docstring change; `audit.py`
re-exports the name, so `audit.check_vision_md` is the same function object as before.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from ._common import Finding


def check_vision_md(repo_path: Path) -> list[Finding]:
    """VISION.md presence + parseable YAML frontmatter per ADR-33."""
    vision = repo_path / "VISION.md"
    if not vision.exists():
        return [Finding("vision_md", "fail", "VISION.md absent at repo root")]
    text = vision.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return [Finding("vision_md", "fail", "VISION.md has no YAML frontmatter (must start with '---')")]
    # Extract frontmatter between first two ---
    parts = text.split("---", 2)
    if len(parts) < 3:
        return [Finding("vision_md", "fail", "VISION.md frontmatter not closed (missing closing '---')")]
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return [Finding("vision_md", "fail", f"VISION.md frontmatter YAML parse error: {e}")]
    if not isinstance(fm, dict):
        return [Finding("vision_md", "fail", "VISION.md frontmatter is not a YAML mapping")]
    required_keys = {"version", "last_reviewed", "owner", "status"}
    missing = required_keys - fm.keys()
    if missing:
        return [Finding("vision_md", "warn", f"VISION.md frontmatter missing keys: {sorted(missing)}")]
    return [Finding("vision_md", "pass", f"VISION.md present; frontmatter keys: {sorted(fm.keys())}")]
