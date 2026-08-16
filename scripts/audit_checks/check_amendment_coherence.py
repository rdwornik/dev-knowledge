"""`check_amendment_coherence` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL, together with the `CoupledSet` dataclass, the `_COUPLED_VERSION_SETS`
manifest and the `_norm_version` helper it exclusively owns. The `# rule: coherence-amendment`
annotation directly above the `def` travels WITH it and must stay there: `_markers_for_check`
walks back from the `def` line through the contiguous comment block to collect rule IDs, so
losing that line would silently drop the check's doc→code edge. No logic, naming, formatting or
docstring change; `audit.py` re-exports every name — `tests/test_audit.py` builds `aud.CoupledSet`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ._common import Finding


@dataclass
class CoupledSet:
    """A family of hand-maintained surfaces that must share one authority version (#11).

    A *straggler* — a surface left at a stale version after a multi-surface amendment — is
    the v3.4-abort failure class (LESSONS.md 2026-05-29: the skill announced v3.3.3 while the
    spec was v3.4). `anchor` is the source of truth; every `surface` must agree with it at
    `granularity`. Each regex carries exactly one capture group yielding a dotted version.
    Membership criterion is SEMANTIC intent-to-mirror, not mere co-occurrence of a version.
    """
    name: str
    anchor: tuple[str, str]                  # (path, regex with one capture group)
    surfaces: list[tuple[str, str]]          # [(path, regex with one capture group), ...]
    granularity: str = "full"                # "full" (X.Y[.Z], trailing-zero-normalized) | "major"


# The live coupled-surface manifest — the cross-case "checklist as data" (#11). Add a set
# when a new family of surfaces must track one authority version. Honest limit: this guards
# only surfaces that still HAND-MAINTAIN a version; surfaces de-hardcoded to interpolate the
# spec ({{VERSION}}) carry no static token and are out of scope by design.
_COUPLED_VERSION_SETS: list[CoupledSet] = [
    CoupledSet(
        name="handoff-major-version",
        anchor=("protocols/HANDOFF_PROCESS.md", r"(?m)^Version:\s+v?(\d+(?:\.\d+)*)"),
        surfaces=[
            # The major the command declares it implements — mirrors the spec's major
            # (the full version/status is de-hardcoded to {{VERSION}}, out of scope).
            # Keyed on the NORMATIVE "handoff per HANDOFF_PROCESS.md vN" declaration so a
            # non-authority mention (e.g. a historical "HANDOFF_PROCESS.md v4.2 Amendment"
            # note) does NOT false-match (Codex HIGH-2 / the semantic-coupling criterion).
            ("CLAUDE.md", r"handoff per `?HANDOFF_PROCESS\.md`?\s+v(\d+)\b"),
            (".claude/commands/handoff.md", r"handoff per `?HANDOFF_PROCESS\.md`?\s+v(\d+)\b"),
        ],
        granularity="major",
    ),
]


def _norm_version(raw: str, granularity: str) -> tuple[int, ...]:
    """Parse a dotted version to an int tuple at `granularity`.

    "major" -> (X,); "full" -> (X, Y, ...) with trailing zeros stripped so 3.4 == 3.4.0.
    """
    parts = [int(p) for p in raw.split(".") if p.isdigit()]
    if not parts:
        return ()
    if granularity == "major":
        return (parts[0],)
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


# rule: coherence-amendment
def check_amendment_coherence(
    repo_path: Path, _sets: Optional[list[CoupledSet]] = None) -> list[Finding]:
    """#11 multi-surface amendment gate: coupled surfaces must share one authority version.

    Converts LESSON-#9's advisory "cross-case trace before a multi-surface amendment" guard
    into an enforced gate (the v3.4 self-handoff abort: the skill announced v3.3.3 while the
    spec was v3.4 — a version STRAGGLER that mis-signalled authority). For each set in the
    manifest (_COUPLED_VERSION_SETS): read the anchor's authority version; every coupled
    surface must agree at the set's granularity. A disagreement is a straggler -> FAIL.

    Child-repo-safe: a set whose anchor file is absent is skipped; an absent surface file is
    skipped; the hub anchors are absent on child repos -> all sets skip -> PASS. An anchor
    present-but-unparseable is reported as drift (WARN), never a FAIL.

    Honest enforcement limit (state-honest-enforcement-limits): guards only surfaces that
    still HAND-MAINTAIN a version. De-hardcoded surfaces (handoff skill/templates interpolate
    {{VERSION}}) carry no static token and are out of scope by design — de-hardcoding, not
    this gate, prevents their straggler class. The narrow `check_handoff_version_stamp` owns
    the full `stamp vX.Y` mirrors in _STAMP_FILES; this is the generalized manifest for other
    coupled families. Read-only.
    """
    sets = _COUPLED_VERSION_SETS if _sets is None else _sets
    stragglers: list[str] = []
    drift: list[str] = []
    checked = 0
    for cset in sets:
        anchor_path, anchor_re = cset.anchor
        ap = repo_path / anchor_path
        if not ap.exists():
            continue  # child-repo-safe skip
        am = re.search(anchor_re, ap.read_text(encoding="utf-8", errors="replace"))
        if not am:
            drift.append(f"{cset.name}: anchor {anchor_path} has no parseable version")
            continue
        canonical = _norm_version(am.group(1), cset.granularity)
        if not canonical:
            drift.append(f"{cset.name}: anchor {anchor_path} version unparseable {am.group(1)!r}")
            continue
        for spath, sre in cset.surfaces:
            fp = repo_path / spath
            if not fp.exists():
                continue
            rx = re.compile(sre)
            lines = fp.read_text(encoding="utf-8", errors="replace").splitlines()
            surface_hits = 0
            for lineno, line in enumerate(lines, 1):
                m = rx.search(line)
                if not m:
                    continue
                surface_hits += 1
                checked += 1
                if _norm_version(m.group(1), cset.granularity) != canonical:
                    stragglers.append(
                        f"{spath}:{lineno}: {m.group(1)!r} != anchor "
                        f"{am.group(1)!r} (set {cset.name})")
            if surface_hits == 0:
                # Present surface, no normative mention -> the coupling marker vanished
                # (reworded/removed). Surface it as drift, never silently PASS (Codex
                # HIGH-1). WARN not FAIL: a removed mention may be legitimate. Anchor-
                # absent (child) repos never reach here, so this cannot false-WARN a child.
                drift.append(
                    f"{cset.name}: surface {spath} present but no normative version "
                    f"mention matched (coupling marker missing/reworded?)")

    if stragglers:
        ev = f"{len(stragglers)} version straggler(s): " + "; ".join(stragglers)
        if drift:
            ev += " | drift: " + "; ".join(drift)
        return [Finding("amendment_coherence", "fail", ev)]
    if drift:
        return [Finding("amendment_coherence", "warn", "; ".join(drift))]
    return [Finding("amendment_coherence", "pass",
                    f"{checked} coupled-surface version mention(s) coherent across "
                    f"{len(sets)} set(s)")]
