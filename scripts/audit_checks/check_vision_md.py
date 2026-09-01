"""`check_vision_md` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. No logic, naming, formatting or docstring change; `audit.py`
re-exports the name, so `audit.check_vision_md` is the same function object as before.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from ._common import _NA_NOT_APPLICABLE, Finding, _na

# CLOUD-4 v2 (R2 §1.5 GO-b): the canonical filename comes from the one registry, not from a
# literal here. Dual-import mirrors `audit.py`'s own audit_checks import shape — this module
# loads as `scripts.audit_checks.check_vision_md` from the repo root and as
# `audit_checks.check_vision_md` with `scripts/` on sys.path.
try:
    from scripts import canonical_docs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoints
    import canonical_docs


def check_vision_md(repo_path: Path) -> list[Finding]:
    """VISION.md presence + parseable YAML frontmatter per ADR-33.

    RETIREMENT IS REGISTRY-DRIVEN, NEVER HARDCODED ([#614], 2026-09-01). ADR-114 retired
    VISION.md as a canonical MUST and DC-1 (ea1e32a9) built the mechanism that says so --
    `canonical_docs.CANONICAL_RETIRED` -- and moved every registry-reading check off it in
    the same act. This check was the one that never read the registry: written under ADR-33,
    it asserted root presence unconditionally, so it FAILed on a ruled retirement and, being
    a TIER_COMMIT check whose FAIL blocks, refused every commit in the repo. **A check that
    FAILs on a ruled retirement is the defect, not the retirement.** It now asks the registry
    the same question `check_canonical_md_visibility` and `check_adr38_baseline` already ask.

    Absence of a RETIRED name is `n/a` / NOT-APPLICABLE, not `pass` -- the surface is
    legitimately gone, and saying `pass` would claim a file was validated when none was read.
    Absence of a name the registry has NOT retired is still a hard FAIL, unchanged. And the
    frontmatter arm below is untouched: a retired name that is still PRESENT is still fully
    validated, so an archival that stalls half-done is not silently exempted.
    """
    name = canonical_docs.VISION
    vision = repo_path / name
    if not vision.exists():
        if name in canonical_docs.CANONICAL_RETIRED:
            return [_na("vision_md", _NA_NOT_APPLICABLE,
                        f"{name} is registry-RETIRED (canonical_docs.CANONICAL_RETIRED) -- "
                        f"root presence is no longer required")]
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
