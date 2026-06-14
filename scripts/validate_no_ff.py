#!/usr/bin/env python
"""validate_no_ff.py — #153 read-only `--no-ff` merge guard (core-invariants rule 5).

The rule (operator ruling 2026-06-06): EVERY change goes branch → merge `--no-ff`;
never commit direct to `main`. Its `verify:` line is "`git log --first-parent main`
shows change arcs as merges, not direct feature commits". This module mechanizes
exactly that verify line.

A `--no-ff` merge puts a MERGE commit on main's first-parent spine and keeps the
feature commits OFF it (second-parent). So a NON-merge commit on the first-parent
line is the violation signature — it got there either by a direct `git commit` on
`main`, OR by a fast-forward merge (which replays the branch commits onto the spine
with no merge commit). `git log --first-parent --no-merges main` lists exactly
those, and is the detector.

DETECT-AND-SURFACE, NOT PREVENT (honest limit, per state-honest-enforcement-limits):
git fires no commit-hook on a fast-forward merge (it creates no commit), so a
pre-commit hook structurally cannot block the FF itself. This guard instead
SURFACES the violation at the next audit-health / ship-gate / SessionStart — the
rule is no longer prose-only and "silent". True prevention would need a pre-push
hook (new install machinery), deferred under #153.

Precision lever (precision over recall — one false positive kills adoption):
  Enforcement baseline = BASELINE_DATE. The mechanical guard grandfathers commits
  authored before the baseline; post-Q9 (ADR-84) the baseline IS the automation-
  isolation cutover, so the legacy ADR-80 fleet-audit baselines + the conformance
  digest that landed on main BEFORE isolation (all <= 2026-06-14) stay
  grandfathered ("legacy left in place, forward-only"), while every non-merge
  commit at/after the baseline is a violation. The guard enforces from the
  baseline FORWARD (author date `%as`, rebase-stable like #10/A2).

ADR-84 (Q9) REMOVED the former automation allowlist. The two unattended writers
now commit only to dedicated `automation/*` branches (never main), so a
marker-based exemption on main would be dead code AND a spoofable backdoor.
The gate is now ONE rule — every non-merge commit on main >= the baseline is a
violation, no exceptions.

Scope: HUB-ONLY (mirrors validate_git_backlog / doc_claims). ALL_CHECKS runs
per-repo across the fleet, but this first ship is scoped to `.dev-knowledge`; a
fleet-wide expansion is deferred under #153 (child repos carry pre-existing direct
histories that would each need their own baseline).

Layer-2 / read-only contract (ADR-28/36): reads git only; writes NOTHING; never
gates (the audit adapter emits WARN, never FAIL, so it cannot wedge audit-health).
Fail-soft: any git error degrades to "no violations" (skip), never raises.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# Mechanical enforcement baseline. Bumped to the Q9 cutover (ADR-84) so the legacy
# automation commits that landed on main BEFORE isolation (the ADR-80 fleet-audit
# baselines + the conformance digest, all <= 2026-06-14) stay grandfathered —
# "legacy left in place, forward-only" (ADR-84 decision 4). Post-Q9 there is NO
# automation exemption: every non-merge commit on main >= this baseline is a
# violation, no exceptions.
BASELINE_DATE = "2026-06-15"

# Record / field separators (control chars) so subjects/bodies survive newlines —
# same convention as propose_closures.git_log_commits.
_FMT = "%x1e%H%x1f%as%x1f%s%x1f%b"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def parse_log(raw: str) -> list:
    """Parse control-char-delimited `git log` output into (sha, adate, subject, body) tuples. Pure."""
    out = []
    for rec in raw.split("\x1e"):
        if not rec.strip():
            continue
        parts = rec.split("\x1f")
        if len(parts) < 4:
            continue
        out.append((parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3]))
    return out


def filter_violations(records: list, baseline: str = BASELINE_DATE) -> list:
    """Keep on/after-baseline records → [(sha, adate, subject), ...]. Pure.

    ISO `%as` dates compare lexically, so `adate < baseline` is the grandfather cut.
    No automation exemption (ADR-84 / Q9): every non-merge commit on main at/after
    the baseline is a violation, full stop.
    """
    viol = []
    for sha, adate, subject, _body in records:
        if adate < baseline:
            continue
        viol.append((sha, adate, subject))
    return viol


def find_violations(repo: Path, branch: str = "main", baseline: str = BASELINE_DATE) -> list:
    """Non-merge commits on `branch`'s first-parent spine since `baseline`, automation excluded.

    Read-only; fail-soft — a missing branch / non-repo / git error returns [] so the
    guard never wedges the audit-health gate.
    """
    r = _git(repo, "log", branch, "--first-parent", "--no-merges", f"--format={_FMT}")
    if r.returncode != 0:
        return []
    return filter_violations(parse_log(r.stdout), baseline)


def format_one(violation: tuple) -> str:
    """One flat line for a violation (cheap to scan; safe in a markdown table cell)."""
    sha, adate, subject = violation
    return f"{sha[:9]} ({adate}) {subject}"


def format_findings(violations: list) -> str:
    """One flat line per violation."""
    return "; ".join(format_one(v) for v in violations)


def main() -> int:
    """CLI: print non-merge-on-main violations; exit 0 always (awareness layer, never a gate)."""
    r = _git(_REPO_ROOT, "rev-parse", "--verify", "--quiet", "main^{commit}")
    if r.returncode != 0:
        print("validate_no_ff: no `main` ref or not a git repo — skipped", file=sys.stderr)
        return 0
    violations = find_violations(_REPO_ROOT)
    if not violations:
        print(f"validate_no_ff: OK — no non-merge commits on main since {BASELINE_DATE} "
              "(--no-ff rule, core-invariants #5; one rule, no exemptions — ADR-84)")
        return 0
    print(f"validate_no_ff: {len(violations)} non-merge commit(s) on main since "
          f"{BASELINE_DATE} (--no-ff rule — expected a `--no-ff` merge, not a direct/FF commit):")
    for v in violations:
        print(f"  FF/DIRECT  {format_one(v)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
