#!/usr/bin/env python
"""block_ff_push.py — #153 pre-push GATE: refuse a push that would put a non-merge
commit on main's first-parent spine (a direct-to-main commit OR a true fast-forward
merge). The PREVENT half of core-invariant #5; complements — does NOT replace — the
WARN-only detector validate_no_ff.py.

WHY A SEPARATE FILE FROM validate_no_ff.py:
  validate_no_ff documents itself as "DETECT-AND-SURFACE, NOT PREVENT / never gates /
  WARN-only awareness layer". A blocking mode there would contradict its own contract.
  So the two organs stay distinct — DETECT = audit WARN, PREVENT = pre-push BLOCK —
  but share ONE FF-signature (every reused helper below is the SAME object from
  validate_no_ff), so the detector and the gate can never disagree about what a
  violation IS.

WHY PRE-PUSH (not pre-commit): git fires no commit-hook on a fast-forward merge (it
  creates no commit), so a pre-commit hook structurally cannot block an FF. A push,
  however, is a single observable event carrying the refs about to land on the remote
  — so a pre-push hook CAN refuse the FF / direct-commit before it reaches main.

RANGE RESOLUTION (the one live-verified piece): a pre-push hook learns which commits
  are headed to which ref two ways, and this script reads BOTH so either wiring works:
    * NATIVE git: one line per ref on stdin —
      `<local_ref> <local_sha> <remote_ref> <remote_sha>`.
    * pre-commit: pre-commit consumes that stdin itself and re-exposes the refs as
      PRE_COMMIT_REMOTE_BRANCH / PRE_COMMIT_TO_REF (local/new) / PRE_COMMIT_FROM_REF
      (remote/old) env vars, so the script's own stdin is already at EOF.
  Only refs/heads/main is protected; every other ref (feature branches, automation/*
  per ADR-84) passes untouched.

HONEST LIMIT (per state-honest-enforcement-limits): a client-side hook is bypassable —
  `git push --no-verify`, an unset core.hooksPath, or a clone that never ran
  `pre-commit install --hook-type pre-push`. Pragmatic teeth for a single-operator
  hub, NOT a guarantee. Bypass-proof teeth would be a server-side / CI check running
  the same `--first-parent --no-merges` signature; that reaches into remote/fleet infra
  — the methodology-reach question #153's done-when leaves open — deferred there. The
  audit WARN (validate_no_ff) still catches anything a bypass slips through.

Scope: HUB-ONLY (the hub installs this hook; child-repo reach is the undecided #153
  scope boundary). Fail-soft: any git error → return 0 (never wedge a legitimate push).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# Single-source the FF-signature: every name below is the SAME object validate_no_ff
# (and the audit WARN adapter) use, so the detector and the gate can never drift apart.
try:
    from scripts import validate_no_ff as _vnf
except ImportError:
    import validate_no_ff as _vnf

_git = _vnf._git
parse_log = _vnf.parse_log
filter_violations = _vnf.filter_violations
format_one = _vnf.format_one
BASELINE_DATE = _vnf.BASELINE_DATE
_FMT = _vnf._FMT

PROTECTED_REF = "refs/heads/main"


def _is_zero(sha: str) -> bool:
    """True for git's all-zeros sentinel (a created/deleted ref), any hash length."""
    return bool(sha) and set(sha) == {"0"}


def _range_for(local_sha: str, remote_sha: str) -> str | None:
    """git-log range for a push to the protected ref, or None to skip. Pure.

    Deleting main (local all-zeros) is out of scope. A new main on a fresh remote
    (remote all-zeros) scans the full local history; otherwise the range is the
    commits the push would ADD: remote_sha..local_sha.
    """
    if _is_zero(local_sha):
        return None
    if _is_zero(remote_sha):
        return local_sha
    return f"{remote_sha}..{local_sha}"


def parse_stdin_lines(text: str) -> list:
    """Parse git's native pre-push stdin into (local_ref, local_sha, remote_ref,
    remote_sha) tuples. Pure; silently drops malformed lines."""
    out = []
    for raw in text.splitlines():
        parts = raw.split()
        if len(parts) == 4:
            out.append((parts[0], parts[1], parts[2], parts[3]))
    return out


def resolve_push_range(stdin_lines: list, env, protected: str = PROTECTED_REF) -> str | None:
    """The git-log range for commits headed to `protected`, or None to skip. Pure.

    Reads the native-stdin ref lines first, then falls back to pre-commit's
    PRE_COMMIT_* env vars (pre-commit consumes stdin, so the script sees none).
    """
    for _local_ref, local_sha, remote_ref, remote_sha in stdin_lines:
        if remote_ref == protected:
            return _range_for(local_sha, remote_sha)
    if env.get("PRE_COMMIT_REMOTE_BRANCH", "") == protected:
        return _range_for(env.get("PRE_COMMIT_TO_REF", ""),
                          env.get("PRE_COMMIT_FROM_REF", ""))
    return None


def _read_stdin() -> str:
    """Native pre-push refs from stdin, or '' when stdin is a tty / already consumed
    (the pre-commit path) — never blocks on an interactive terminal."""
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return ""
        return sys.stdin.read()
    except (OSError, ValueError):
        return ""


def _repo_root() -> Path:
    """The repo being pushed = git toplevel of CWD (where git / pre-commit run the
    hook). Falls back to CWD on any error."""
    r = _git(Path.cwd(), "rev-parse", "--show-toplevel")
    if r.returncode == 0 and r.stdout.strip():
        return Path(r.stdout.strip())
    return Path.cwd()


def violations_in_range(repo: Path, rng: str, baseline: str = BASELINE_DATE) -> list:
    """Non-merge commits on the first-parent spine within `rng`, since `baseline`.
    Read-only; fail-soft — a git error returns [] (never wedge a legitimate push)."""
    r = _git(repo, "log", "--first-parent", "--no-merges", rng, f"--format={_FMT}")
    if r.returncode != 0:
        return []
    return filter_violations(parse_log(r.stdout), baseline)


def main(argv=None) -> int:
    """Refuse (1) a push that adds a non-merge commit to main; allow (0) otherwise.
    Fail-soft to 0 on any error — a hook bug must never block a legitimate push."""
    try:
        rng = resolve_push_range(parse_stdin_lines(_read_stdin()), os.environ)
        if rng is None:
            return 0  # not a push to main (or a main deletion) — nothing to gate
        violations = violations_in_range(_repo_root(), rng)
    except Exception as exc:  # noqa: BLE001 — fail-soft is the contract
        print(f"block_ff_push: degraded ({exc}) — allowing push", file=sys.stderr)
        return 0
    if not violations:
        return 0
    print(f"block_ff_push: REFUSED — {len(violations)} non-merge commit(s) would land "
          "on main's first-parent spine (core-invariant #5 wants a `--no-ff` merge, "
          "not a direct/FF commit):", file=sys.stderr)
    for v in violations:
        print(f"  FF/DIRECT  {format_one(v)}", file=sys.stderr)
    print("  fix: redo as a --no-ff merge — "
          "`git checkout main && git merge --no-ff <branch>`", file=sys.stderr)
    print("  bypass: `git push --no-verify` "
          "(the audit WARN still flags it post-hoc)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
