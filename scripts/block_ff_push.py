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
  scope boundary). Fail **CLOSED**: any internal error → exit 2, refusing the push (ADR-85
  amendment 2026-08-03 §A6). This organ returned 0 on any git error until that amendment,
  which made a FAILED scan indistinguishable from a CLEAN one and silently auto-allowed the
  exact push it exists to refuse; refusing cannot wedge legitimate work because the explicit
  `git push --no-verify` is the escape hatch. The MODULE posture is what closed — the leaf
  helpers `_rev_parse` / `_reconstruct_main_range` stay fail-soft BY DESIGN (they degrade to
  `''` / `None`, values the callers still reason about correctly); do not "fix" those.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# Single-source the FF-signature: the gate delegates the actual violation SCAN to
# validate_no_ff.find_violations (see violations_in_range) and reuses its leaf helpers
# as the SAME objects — so the detector and the gate can never disagree about what a
# violation IS, at the whole-scan level, not just the leaves. Prefer the bare import
# (the sibling is guaranteed on sys.path by the insert above) so every invocation mode
# — pre-push hook, `python -m pytest`, direct run — resolves ONE module object; a
# `from scripts import` first branch would yield a second copy (`scripts.validate_no_ff`
# vs `validate_no_ff`) whenever the repo root is also on the path, breaking that
# guarantee (and the reuse-integrity test).
try:
    import validate_no_ff as _vnf
except ImportError:
    from scripts import validate_no_ff as _vnf

_git = _vnf._git              # used by _repo_root
format_one = _vnf.format_one  # used to render a refused violation
BASELINE_DATE = _vnf.BASELINE_DATE

PROTECTED_REF = "refs/heads/main"


def _is_zero(sha: str) -> bool:
    """True for git's all-zeros sentinel (a created/deleted ref), any hash length."""
    return bool(sha) and set(sha) == {"0"}


def _range_for(local_sha: str, remote_sha: str) -> str | None:
    """git-log range for a push to the protected ref, or None to skip. Pure.

    A missing/all-zeros local sha — deleting main, or an empty PRE_COMMIT_TO_REF on a
    delete via the env path — is out of scope → skip (an empty left side would let git
    silently resolve `remote_sha..` to `remote_sha..HEAD` and falsely REFUSE). A
    missing/all-zeros remote sha (new main on a fresh remote) scans the full local
    history; otherwise the range is the commits the push would ADD: remote_sha..local_sha.
    """
    if not local_sha or _is_zero(local_sha):
        return None
    if not remote_sha or _is_zero(remote_sha):
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
    (the pre-commit path) — never blocks on an interactive terminal.

    A genuine READ FAILURE now RAISES rather than degrading to '' (terra CRITICAL,
    2026-08-03; ADR-85 amendment §A6). The two states are not the same: 'no stdin' is the
    legitimate pre-commit/tty wiring, while an OSError mid-read means the hook does not know
    what is being pushed — and an empty string there resolves to "not a push to main" and
    returns 0, silently allowing the exact push both gates exist to refuse. The callers'
    outer handler turns this into exit 2.
    """
    if sys.stdin is None or sys.stdin.isatty():
        return ""
    return sys.stdin.read()


def _repo_root() -> Path:
    """The repo being pushed = git toplevel of CWD (where git / pre-commit run the
    hook). Falls back to CWD on any error."""
    r = _git(Path.cwd(), "rev-parse", "--show-toplevel")
    if r.returncode == 0 and r.stdout.strip():
        return Path(r.stdout.strip())
    return Path.cwd()


def _under_precommit(env) -> bool:
    """True when pre-commit is driving the hook — it exports PRE_COMMIT_* vars AND has
    already consumed the native pre-push stdin (so our own stdin is empty). The signal
    that the env fallback, not the native-stdin path, is the only ref source we have."""
    return any(k.startswith("PRE_COMMIT_") for k in env)


def _rev_parse(repo: Path, ref: str) -> str:
    """Resolved commit sha for `ref`, or '' if it does not resolve. Read-only; fail-soft
    (a missing ref / non-repo / git error yields '', never raises)."""
    r = _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    return r.stdout.strip() if r.returncode == 0 else ""


def _reconstruct_main_range(repo: Path, env, protected: str = PROTECTED_REF) -> str | None:
    """Rebuild the protected-`main` push range from LOCAL git refs when pre-commit's env
    hid it. pre-commit forwards only ONE parsed ref pair, so it cannot express main in two
    shapes: a MULTI-REF push where main is not the forwarded ref, and an EMPTY-REMOTE
    INITIAL push (all_files path) that sets neither PRE_COMMIT_TO_REF nor FROM_REF. Rather
    than trust the forwarded ref, read main's own tips:
        local  = refs/heads/main
        remote = refs/remotes/<PRE_COMMIT_REMOTE_NAME>/main (its tracking tip),
                 or absent/unknown -> full local history (the fresh-remote scan).
    Reuses `_range_for` so the range is built identically to every other path. Read-only;
    fail-soft — no local main -> None (nothing to protect); no tracking ref -> full
    history. Precision note: on a rule-clean main this range is empty (or merges-only), so
    a clean repo is NEVER refused; it only surfaces a genuine non-merge commit that already
    sits on local main."""
    local_sha = _rev_parse(repo, protected)
    if not local_sha:
        return None
    remote_name = env.get("PRE_COMMIT_REMOTE_NAME", "").strip()
    branch = protected.rsplit("/", 1)[-1]  # refs/heads/main -> main
    remote_sha = _rev_parse(repo, f"refs/remotes/{remote_name}/{branch}") if remote_name else ""
    return _range_for(local_sha, remote_sha)


# rule: governance-no-ff
def violations_in_range(repo: Path, rng: str, baseline: str = BASELINE_DATE) -> list:
    """Non-merge commits on the first-parent spine within `rng`, since `baseline`.

    Delegates to validate_no_ff.find_violations — a revision range (`remote..local`)
    is a valid `git log` positional exactly like a branch name, so the gate and the
    detector share ONE scan, not just the leaf helpers.

    THE DELEGATE IS FAIL-SOFT AND THIS GATE IS NOT (terra CRITICAL, 2026-08-03).
    `find_violations` documents "a missing branch / non-repo / git error returns []" so it can
    never wedge the audit-health WARN it was written for. Reused verbatim here that contract
    makes a FAILED SCAN indistinguishable from A CLEAN ONE, and `main()` returns 0 — the
    fail-closed posture of ADR-85 §A6 defeated one layer down. So the range is proved
    READABLE first; a git failure raises and `main()` turns it into exit 2. The shared
    signature is preserved (still ONE scan, ONE definition of a violation) — only the
    unknown-vs-clean distinction is added, which the detector does not need and the gate
    cannot do without."""
    probe = _git(repo, "rev-list", "--count", rng)
    if probe.returncode != 0:
        raise RuntimeError(
            f"could not read the push range {rng!r}: git rev-list exited "
            f"{probe.returncode}: {probe.stderr.strip()}")
    return _vnf.find_violations(repo, branch=rng, baseline=baseline)


def main(argv=None) -> int:
    """Refuse (1) a push that adds a non-merge commit to main; allow (0) otherwise.

    Exit codes: 0 = clean scan, allow · 1 = violation detected, refuse · 2 = internal
    error, refuse. Fail **CLOSED** on error per the ADR-85 amendment 2026-08-03 §A6 —
    the escape hatch is the explicit `git push --no-verify`, so an error need never
    brick work and must never be a silent allow."""
    reconstructed = False
    try:
        repo = _repo_root()
        lines = parse_stdin_lines(_read_stdin())
        rng = resolve_push_range(lines, os.environ)
        # pre-commit consumed the native stdin (lines empty) and re-exposes only ONE ref
        # pair, so it can hide main on a multi-ref or empty-remote-initial push. When the
        # forwarded ref gave no main range, reconstruct main's range from local git refs.
        if rng is None and not lines and _under_precommit(os.environ):
            rng = _reconstruct_main_range(repo, os.environ)
            reconstructed = rng is not None
        if rng is None:
            return 0  # not a push to main (or a main deletion) — nothing to gate
        violations = violations_in_range(repo, rng)
    except Exception as exc:  # noqa: BLE001 — ADR-85 amendment 2026-08-03 §A6: fail CLOSED
        # An organ with an explicit escape hatch (`git push --no-verify`) must fail closed:
        # a crash cannot brick work, so a silent auto-allow buys nothing and costs the
        # invariant. This organ is the PREVENT half of core-invariant #5, and until this
        # fix it printed "degraded — allowing push" and returned 0, silently auto-allowing
        # the exact push it exists to refuse — which is what made ADR-85 §A9's foreclosure
        # conditional. Model: check_seal_identity.py:73-77 ("an error is never a silent
        # pass"). Exit 2 = internal error, distinct from 1 = detected violation.
        print(f"block_ff_push: INTERNAL ERROR ({exc!r}) — refusing the push; an error is "
              "never a silent allow. Fix the hook, or bypass explicitly with "
              "`git push --no-verify` (the audit WARN still flags it post-hoc).",
              file=sys.stderr)
        return 2
    if not violations:
        return 0
    print(f"block_ff_push: REFUSED — {len(violations)} non-merge commit(s) would land "
          "on main's first-parent spine (core-invariant #5 wants a `--no-ff` merge, "
          "not a direct/FF commit):", file=sys.stderr)
    if reconstructed:
        print("  core-invariant #5 violation on local 'main' (surfaced by this push; "
              "main's range was reconstructed for this push — the refusal names main, "
              "not the ref you pushed):", file=sys.stderr)
    for v in violations:
        print(f"  FF/DIRECT  {format_one(v)}", file=sys.stderr)
    print("  fix: redo as a --no-ff merge — "
          "`git checkout main && git merge --no-ff <branch>`", file=sys.stderr)
    print("  bypass: `git push --no-verify` "
          "(the audit WARN still flags it post-hoc)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
