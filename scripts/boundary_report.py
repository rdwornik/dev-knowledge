#!/usr/bin/env python
"""boundary_report.py — #312 read-only fleet CLAUDE.md methodology-boundary reporter (C1).

A faithful sibling of `fleet_health.py` / `audit.py` (kin to the #132 ORGAN-INDEX
generator): parse each fleet repo's `CLAUDE.md` for the #312 Form-A fenced region
markers (`<!-- methodology:start/end id=… owner=hub|repo -->`), align every consumer's
`owner=hub` regions against the hub baseline by `id`, and REPORT drift. It is a
reporter, NOT a gate (design §4.5 "detects, does not prevent"; ruling: severity=warn) —
deliberately NOT registered in `audit.ALL_CHECKS`, so it never reddens the ship-gate;
it only REUSES the LOCKED `Finding` shape as its output contract.

Layer-2 / read-only contract (ADR-28/36): reads child repos, writes ONLY
`.dev-knowledge/logs/`, never mutates a child file. Fail-soft everywhere (a SessionStart
sibling): ASCII-only output, `main()` always returns 0, an absent/unreadable repo is
`unavailable`, never a crash.

Reuse (no second traversal — the #312 lane constraint): `audit.discover_repos()` (the one
deterministic ecosystem enumerator), `audit.load_state()` (per-repo `state.yaml` path),
and `audit.Finding` (the LOCKED 3-field contract). The hub is the diff BASELINE and is
skipped as a target (design §4.1) — robustly, so a worktree run skips the hub too.

Honest limits (design §4.5): DETECTS, does not prevent; blind to unmarked repos (an
un-grandfathered consumer reports "unmarked", distinguished from "clean"); registration-
scoped; body compare is exact-match now — "modulo declared variables" (repo-name
substitution) is a deferred build decision (TODO), not exercised pre-rollout.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_LOGS_DIR = _REPO_ROOT / "logs"
_BOUNDARY_FILE = _LOGS_DIR / "BOUNDARY-DRIFT.md"

# Reuse the LOCKED audit contract + the single deterministic fleet enumerator.
sys.path.insert(0, str(_SCRIPTS_DIR))
import audit  # noqa: E402

Finding = audit.Finding

_CHECK = "claude_md_boundary"

# A line that is ENTIRELY one methodology marker (strip first; a mid-prose mention of the
# literal marker text — e.g. CLAUDE.md's own §12 history entry — is therefore NOT matched).
_START_RE = re.compile(
    r"^<!--\s*methodology:start\s+id=([a-z0-9-]+)\s+owner=(hub|repo)(?:\s+v=(\S+))?\s*-->$"
)
_END_RE = re.compile(r"^<!--\s*methodology:end\s+id=([a-z0-9-]+)\s*-->$")


# ============================================================================
# Pure helpers (unit-tested directly)
# ============================================================================

@dataclass
class Region:
    id: str
    owner: str          # "hub" | "repo"
    v: Optional[str]    # optional corpus-version attr (informational)
    body: str           # region content between the markers, stripped


def parse_regions(text: str) -> tuple[list[Region], list[str]]:
    """Parse `methodology:start/end` pairs -> (regions, parse_warnings).

    Unbalanced / mismatched-id / nested / orphan-close pairs produce a LOUD warning
    string (never a silent skip; design §4.2 Axis-2 hardening). No markers -> ([], []) —
    the whole file is project by default.
    """
    regions: list[Region] = []
    warnings: list[str] = []
    stack: list[list] = []  # [id, owner, v, start_lineno, body_lines]
    for lineno, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        ms = _START_RE.match(s)
        if ms:
            if stack:
                warnings.append(
                    f"nested methodology:start id={ms.group(1)} inside "
                    f"id={stack[-1][0]} at line {lineno}")
            stack.append([ms.group(1), ms.group(2), ms.group(3), lineno, []])
            continue
        me = _END_RE.match(s)
        if me:
            end_id = me.group(1)
            if not stack:
                warnings.append(f"methodology:end id={end_id} with no open region at line {lineno}")
                continue
            rid, owner, v, _start, body_lines = stack.pop()
            if end_id != rid:
                warnings.append(
                    f"methodology:end id={end_id} does not match open id={rid} at line {lineno}")
            regions.append(Region(rid, owner, v, "\n".join(body_lines).strip()))
            continue
        if stack:
            stack[-1][4].append(line)
    for rid, owner, v, start_lineno, _body in stack:
        warnings.append(f"methodology:start id={rid} at line {start_lineno} never closed")
    return regions, warnings


def build_baseline(hub_regions: list[Region]) -> dict[str, str]:
    """{id -> body} over the hub's `owner=hub` regions (the diff baseline)."""
    return {r.id: r.body for r in hub_regions if r.owner == "hub"}


@dataclass
class Diff:
    match: list[str] = field(default_factory=list)
    drift: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    orphan: list[str] = field(default_factory=list)
    project_n: int = 0
    hub_n: int = 0


def diff_consumer(baseline: dict[str, str], consumer_regions: list[Region]) -> Diff:
    """Align a consumer's regions against the hub baseline (design §4.2)."""
    consumer_hub = {r.id: r.body for r in consumer_regions if r.owner == "hub"}
    d = Diff(project_n=sum(1 for r in consumer_regions if r.owner == "repo"),
             hub_n=len(consumer_hub))
    for cid, body in consumer_hub.items():
        if cid not in baseline:
            d.orphan.append(cid)
        elif body == baseline[cid]:
            d.match.append(cid)
        else:
            d.drift.append(cid)
    for bid in baseline:
        if bid not in consumer_hub:
            d.missing.append(bid)
    for lst in (d.match, d.drift, d.missing, d.orphan):
        lst.sort()
    return d


def _safe(evidence: str) -> str:
    """Markdown-table-safe (the Finding contract: no literal '|')."""
    return evidence.replace("|", "/")


def to_finding(name: str, diff: Optional[Diff], *, unavailable: bool = False,
               parse_warnings: Optional[list[str]] = None) -> Finding:
    """One per-repo Finding — the LOCKED audit.py contract. Reporter policy: `warn`,
    never `fail` (a reporter, not a gate). Status: `unavailable` (no file) / `warn`
    (unmarked, drift/missing/orphan, or parse warning) / `pass` (all hub regions match)."""
    if unavailable:
        return Finding(_CHECK, "unavailable", _safe(f"{name}: CLAUDE.md not found on disk (skipped)"))
    assert diff is not None
    pw = f" [parse: {'; '.join(parse_warnings)}]" if parse_warnings else ""
    if diff.hub_n == 0:
        return Finding(_CHECK, "warn", _safe(
            f"{name}: unmarked -- 0 hub regions (grandfathering pending); "
            f"{diff.project_n} project regions{pw}"))
    if diff.drift or diff.missing or diff.orphan or parse_warnings:
        parts = [f"{len(diff.match)} match", f"{len(diff.drift)} drift",
                 f"{len(diff.missing)} missing"]
        if diff.orphan:
            parts.append(f"{len(diff.orphan)} orphan")
        detail = ", ".join(parts) + f"; {diff.project_n} project"
        spec = []
        if diff.drift:
            spec.append("drift: " + "/".join(diff.drift))
        if diff.missing:
            spec.append("missing: " + "/".join(diff.missing))
        if diff.orphan:
            spec.append("orphan: " + "/".join(diff.orphan))
        tail = ("; " + "; ".join(spec)) if spec else ""
        return Finding(_CHECK, "warn", _safe(f"{name}: {detail}{tail}{pw}"))
    return Finding(_CHECK, "pass", _safe(
        f"{name}: {len(diff.match)} hub regions match, 0 drift; {diff.project_n} project regions"))


@dataclass
class Row:
    name: str
    status: str          # pass | warn | unavailable
    hub_n: int = 0
    match_n: int = 0
    drift_n: int = 0
    missing_n: int = 0
    project_n: int = 0


def build_digest(rows: list[Row], baseline_n: int, run_date: str) -> str:
    """A `fleet_health.build_digest`-style digest: frontmatter counts + a flat table.

    ASCII-only. The table is fenced-free markdown (the TUI paints borders client-side;
    this file is not copied into browser chat) — one row per registered non-hub repo.
    """
    unmarked = sum(1 for r in rows if r.status == "warn" and r.hub_n == 0)
    drifted = sum(1 for r in rows if r.status == "warn" and r.hub_n > 0)
    clean = sum(1 for r in rows if r.status == "pass")
    unavailable = sum(1 for r in rows if r.status == "unavailable")
    out: list[str] = []
    out.append("---")
    out.append(f"run_date: {run_date}")
    out.append(f"baseline_hub_regions: {baseline_n}")
    out.append(f"consumers_total: {len(rows)}")
    out.append(f"consumers_unmarked: {unmarked}")
    out.append(f"consumers_drift: {drifted}")
    out.append(f"consumers_clean: {clean}")
    out.append(f"consumers_unavailable: {unavailable}")
    out.append("---")
    out.append("")
    out.append("# Fleet CLAUDE.md boundary-marker drift")
    out.append("")
    out.append(f"Baseline: hub `CLAUDE.md` ({baseline_n} `owner=hub` regions). "
               f"Read-only reporter (#312); DETECTS, does not prevent.")
    out.append("")
    out.append("| Repo | Hub regions | Match | Drift | Missing | Project | Status |")
    out.append("|------|-------------|-------|-------|---------|---------|--------|")
    for r in rows:
        out.append(f"| {r.name} | {r.hub_n} | {r.match_n} | {r.drift_n} | "
                   f"{r.missing_n} | {r.project_n} | {r.status} |")
    out.append("")
    if unmarked:
        out.append(f"> {unmarked} consumer(s) UNMARKED (grandfathering pending) — the "
                   f"expected pre-rollout state, not drift.")
    out.append("")
    return "\n".join(out)


_FM_RE = re.compile(r"^(\w+):\s*(.+?)\s*$")


def surface_line(boundary_file: Path) -> str:
    """A one-line ASCII SessionStart summary; distinguishes UNMARKED from clean
    (design §4.5). Always returns a non-empty string (fail-soft)."""
    if not boundary_file.exists():
        return "[boundary] no report yet -- run scripts/boundary_report.py"
    fm: dict[str, str] = {}
    try:
        text = boundary_file.read_text(encoding="utf-8")
        in_fm = False
        for line in text.splitlines():
            if line.strip() == "---":
                if in_fm:
                    break
                in_fm = True
                continue
            if in_fm:
                m = _FM_RE.match(line)
                if m:
                    fm[m.group(1)] = m.group(2)
    except OSError:
        return "[boundary] report unreadable"
    total = fm.get("consumers_total", "?")
    unmarked = fm.get("consumers_unmarked", "?")
    drift = fm.get("consumers_drift", "?")
    base = fm.get("baseline_hub_regions", "?")
    rd = fm.get("run_date", "?")
    return (f"[boundary] {total} consumers: {unmarked} unmarked (rollout pending), "
            f"{drift} drift as of {rd} (baseline {base} hub regions)")


# ============================================================================
# Impure: traverse the fleet + write the digest
# ============================================================================

def _git_common_dir(path: Path) -> Optional[Path]:
    """The repo's shared git dir (worktrees of one repo share it) — for a robust hub-skip
    that survives a worktree run. Fail-soft: None on any error."""
    try:
        out = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--git-common-dir"],
            capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    g = Path(out.stdout.strip())
    return (g if g.is_absolute() else (path / g)).resolve()


def _is_hub(root: Path, repo_root: Path) -> bool:
    """True if `root` is the same logical repo as the hub `repo_root` (design §4.1 hub-skip,
    hardened for worktrees: same resolved path OR same git-common-dir)."""
    if root.resolve() == repo_root.resolve():
        return True
    a, b = _git_common_dir(root), _git_common_dir(repo_root)
    return a is not None and a == b


def _resolve_root(name: str) -> Optional[Path]:
    """On-disk root for a registered repo: its `state.yaml` `path:`, fallback
    `<repo_root.parent>/<name>` (mirrors audit/fleet_health). None if unresolvable."""
    st = audit.load_state(name)
    if st is not None and getattr(st, "path", None):
        return Path(st.path)
    cand = _REPO_ROOT.parent / name
    return cand if cand.exists() else None


def run_report(repo_root: Path = _REPO_ROOT, *, today: Optional[str] = None
               ) -> tuple[list[Finding], str]:
    """Read the hub baseline, diff every registered non-hub consumer, return
    (findings, digest_text). Read-only; resolves consumer paths, skips the hub, fail-soft."""
    run_date = today or date.today().isoformat()
    findings: list[Finding] = []
    rows: list[Row] = []

    hub_text = (repo_root / "CLAUDE.md").read_text(encoding="utf-8")
    hub_regions, hub_warns = parse_regions(hub_text)
    baseline = build_baseline(hub_regions)
    if hub_warns:
        findings.append(Finding(_CHECK, "warn", _safe("hub baseline: parse: " + "; ".join(hub_warns))))

    for name in audit.discover_repos():
        root = _resolve_root(name)
        if root is None:
            findings.append(to_finding(name, None, unavailable=True))
            rows.append(Row(name, "unavailable"))
            continue
        if _is_hub(root, repo_root):
            continue  # the baseline is not a diff target
        cpath = root / "CLAUDE.md"
        if not cpath.exists():
            findings.append(to_finding(name, None, unavailable=True))
            rows.append(Row(name, "unavailable"))
            continue
        try:
            ctext = cpath.read_text(encoding="utf-8")
        except OSError:
            findings.append(to_finding(name, None, unavailable=True))
            rows.append(Row(name, "unavailable"))
            continue
        cregions, cwarns = parse_regions(ctext)
        diff = diff_consumer(baseline, cregions)
        f = to_finding(name, diff, parse_warnings=cwarns or None)
        findings.append(f)
        rows.append(Row(name, f.status, hub_n=diff.hub_n, match_n=len(diff.match),
                        drift_n=len(diff.drift), missing_n=len(diff.missing),
                        project_n=diff.project_n))

    digest = build_digest(rows, len(baseline), run_date)
    return findings, digest


def _atomic_write(path: Path, text: str) -> None:
    """Process-unique temp + os.replace, so a concurrent reader never sees a half write
    (mirrors fleet_health._atomic_write). The digest is gitignored."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".boundary-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def main() -> int:
    """CLI / SessionStart entry — write the digest, print the surface line. Always 0."""
    try:
        _findings, digest = run_report()
        _atomic_write(_BOUNDARY_FILE, digest)
        print(surface_line(_BOUNDARY_FILE))
    except Exception as exc:  # fail-soft: a reporter never breaks the caller
        print(f"[boundary] reporter error (fail-soft): {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
