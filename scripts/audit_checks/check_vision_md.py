"""`check_vision_md` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. No logic, naming, formatting or docstring change; `audit.py`
re-exports the name, so `audit.check_vision_md` is the same function object as before.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from ._common import Finding

# CLOUD-4 v2 (R2 §1.5 GO-b): the canonical filename comes from the one registry, not from a
# literal here. Dual-import mirrors `audit.py`'s own audit_checks import shape — this module
# loads as `scripts.audit_checks.check_vision_md` from the repo root and as
# `audit_checks.check_vision_md` with `scripts/` on sys.path.
try:
    from scripts import canonical_docs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoints
    import canonical_docs


def check_vision_md(repo_path: Path) -> list[Finding]:
    """VISION.md presence + parseable YAML frontmatter per ADR-33."""
    name = canonical_docs.VISION
    vision = repo_path / name
    if not vision.exists():
        return [Finding("vision_md", "fail", f"{name} absent at repo root")]
    text = vision.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return [Finding("vision_md", "fail", f"{name} has no YAML frontmatter (must start with '---')")]
    # Extract frontmatter between first two ---
    parts = text.split("---", 2)
    if len(parts) < 3:
        return [Finding("vision_md", "fail", f"{name} frontmatter not closed (missing closing '---')")]
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return [Finding("vision_md", "fail", f"{name} frontmatter YAML parse error: {e}")]
    if not isinstance(fm, dict):
        return [Finding("vision_md", "fail", f"{name} frontmatter is not a YAML mapping")]
    required_keys = {"version", "last_reviewed", "owner", "status"}
    missing = required_keys - fm.keys()
    if missing:
        return [Finding("vision_md", "warn", f"{name} frontmatter missing keys: {sorted(missing)}")]
    return [Finding("vision_md", "pass", f"{name} present; frontmatter keys: {sorted(fm.keys())}")]
