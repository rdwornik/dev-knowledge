"""`check_floor_integrity` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL, together with `_FLOOR_MD_REF_RE`. The `# rule: governance-child-floor`
annotation above the `def` travels with it (see `check_amendment_coherence` for why that
matters). The `generate_floor` dual-import is reproduced in the SAME `scripts.`-first order
`audit.py` uses, so both spellings resolve to one module under either entry path; `audit.py`
re-exports `_FLOOR_F5` and `_floor_sha256` from HERE rather than importing them again, which
keeps `audit._floor_sha256` and this module's binding the same object.
"""

from __future__ import annotations

import re
from pathlib import Path

from ._common import _na, Finding

# Floor policy is single-sourced in generate_floor.py (the generator owns it; audit enforces).
# Dual import: `scripts.generate_floor` for `python -m scripts.audit`; `generate_floor` for
# `python scripts/audit.py` and the test path (scripts/ on sys.path).
try:
    from scripts.generate_floor import F5_BLACKLIST as _FLOOR_F5
    from scripts.generate_floor import floor_sha256 as _floor_sha256
except ImportError:
    from generate_floor import F5_BLACKLIST as _FLOOR_F5
    from generate_floor import floor_sha256 as _floor_sha256


_FLOOR_MD_REF_RE = re.compile(r"[A-Za-z0-9_-]+\.md")


# rule: governance-child-floor
def check_floor_integrity(repo_path: Path) -> list[Finding]:
    """Child methodology-floor conformance (ADR-78 O2; methodology_surface zone, ADR-75).

    Skipped (PASS) when the repo carries no .claude/CLAUDE-FLOOR.md — the floor rollout is gradual,
    and the hub itself (where `health` runs this) is the floor SOURCE, not a carrier, so it
    has none. Where a floor IS present, three conformance signals (all FAIL on violation):

      - Hash integrity: sha256 of the floor (LF-normalized, autocrlf-proof) must match the
        committed CLAUDE-FLOOR.md.sha256 sidecar. A mismatch means the floor was edited
        without regenerating (run the hub generator) or tampered with (restore it).
      - F5 self-containment: no hub-internal artifact tokens leak into the floor (the
        shared generate_floor.F5_BLACKLIST — ADR-72 self-containment / ADR-78 §3 grep).
      - Pointer existence (T3 fold-in): every same-repo `*.md` the floor names must exist
        in the repo (a zero-URL floor has no external links to check).

    Hash + F5 mirror the generator's emit-time gate so a drifted floor is caught fleet-side;
    the sidecar-match here is the hub-runnable signal the tamper test exercises (`audit repo
    <child>`). Read-only; child-repo-safe.
    """
    floor = repo_path / ".claude" / "CLAUDE-FLOOR.md"
    if not floor.exists():
        return [_na("floor_integrity", "NOT-APPLICABLE",
                        "no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip)")]

    text = floor.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []

    # 1. Hash integrity vs sidecar.
    sidecar = repo_path / ".claude" / "CLAUDE-FLOOR.md.sha256"
    actual = _floor_sha256(text)
    if not sidecar.exists():
        issues.append("CLAUDE-FLOOR.md.sha256 sidecar missing (regenerate via hub generator)")
    else:
        m = re.search(r"[0-9a-f]{64}", sidecar.read_text(encoding="utf-8", errors="replace"))
        expected = m.group(0) if m else ""
        if not expected:
            issues.append("CLAUDE-FLOOR.md.sha256 has no parseable sha256")
        elif actual != expected:
            issues.append(
                f"hash drift: floor sha256 {actual[:12]}… != sidecar {expected[:12]}… — floor "
                "edited without regenerating (run hub generator) OR tampered (restore the floor)")

    # 2. F5 self-containment.
    leaks = [label for label, pat in _FLOOR_F5 if pat.search(text)]
    if leaks:
        issues.append(f"F5 self-containment violation — hub-internal token(s) in floor: {leaks}")

    # 3. Pointer existence (same-repo .md targets the floor names).
    refs = {r for r in _FLOOR_MD_REF_RE.findall(text) if r != "CLAUDE-FLOOR.md"}
    broken = sorted(r for r in refs if not (repo_path / r).exists())
    if broken:
        issues.append(f"floor names same-repo file(s) that do not exist: {broken}")

    if issues:
        return [Finding("floor_integrity", "fail", "; ".join(issues))]
    return [Finding("floor_integrity", "pass",
                    f"CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve "
                    f"(sha256 {actual[:12]}…)")]
