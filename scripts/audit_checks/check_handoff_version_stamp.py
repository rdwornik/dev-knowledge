"""`check_handoff_version_stamp` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL, together with `_STAMP_RE` and `_STAMP_FILES`, which it exclusively
owns. No logic, naming, formatting or docstring change; `audit.py` re-exports all three names.
"""

from __future__ import annotations

import re
from pathlib import Path

from ._common import _na, Finding


_STAMP_RE = re.compile(r"stamp\s+v?(\d+\.\d+(?:\.\d+)?)", re.IGNORECASE)
_STAMP_FILES = ["ARCHITECTURE.md", "CONTRIBUTING.md"]


def check_handoff_version_stamp(repo_path: Path) -> list[Finding]:
    """HANDOFF_PROCESS.md version header matches 'stamp v?X.Y' occurrences in living docs.

    Parses the canonical version from the `Version:` line in
    protocols/HANDOFF_PROCESS.md, then greps ARCHITECTURE.md and CONTRIBUTING.md
    for `stamp v?X.Y` patterns. FAILs if any stamp's version does not match the
    canonical version — the S1 recurrence class surfaced in nightly arc #81.
    Read-only; child-repo-safe (HANDOFF_PROCESS.md absent → pass-with-skip).
    """
    spec = repo_path / "protocols" / "HANDOFF_PROCESS.md"
    if not spec.exists():
        return [_na("handoff_version_stamp", "NOT-APPLICABLE",
                        "no protocols/HANDOFF_PROCESS.md — nothing to validate")]

    spec_text = spec.read_text(encoding="utf-8")
    version_match = re.search(r"^Version:\s+v?(\d+\.\d+(?:\.\d+)?)", spec_text, re.MULTILINE)
    if not version_match:
        return [Finding("handoff_version_stamp", "warn",
                        "protocols/HANDOFF_PROCESS.md: no parseable 'Version:' line")]
    canonical = version_match.group(1)

    mismatches: list[str] = []
    found_any = False
    for fname in _STAMP_FILES:
        fpath = repo_path / fname
        if not fpath.exists():
            continue
        for lineno, line in enumerate(fpath.read_text(encoding="utf-8").splitlines(), start=1):
            m = _STAMP_RE.search(line)
            if m:
                found_any = True
                stamp_ver = m.group(1)
                if stamp_ver != canonical:
                    mismatches.append(
                        f"{fname}:{lineno}: stamp {stamp_ver!r} != canonical {canonical!r}"
                    )

    if mismatches:
        return [Finding("handoff_version_stamp", "fail",
                        f"{len(mismatches)} stamp mismatch(es): " + "; ".join(mismatches))]
    if not found_any:
        return [Finding("handoff_version_stamp", "warn",
                        f"No 'stamp vX.Y' patterns found in {_STAMP_FILES} — "
                        "convention may have drifted")]
    return [Finding("handoff_version_stamp", "pass",
                    f"All stamp occurrences in {_STAMP_FILES} match "
                    f"canonical HANDOFF_PROCESS v{canonical}")]
