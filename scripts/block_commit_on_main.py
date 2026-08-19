#!/usr/bin/env python
"""block_commit_on_main.py — [#527] pre-commit GATE: refuse a NON-MERGE commit whose
current branch is `main`. The commit-time half of core-invariant #5; sibling of — not a
replacement for — the push-time `block_ff_push.py`.

WHY COMMIT-TIME AND NOT PUSH-TIME (the gap this closes): `block_ff_push` is real but
  LATE. The 2026-08-13 incident landed three direct-to-main commits (e15c97f6 / b0f5eda5 /
  3d97d5c5) that the pre-push gate caught only once they already existed locally, which
  forced a `commit-tree` git-surgery re-land to clear the spine. A pre-commit refusal
  fires before a single bad commit exists to unwind. #153 owns server-side/push-time
  teeth; this owns local commit-time, and the two do not overlap.

THE PREDICATE IS UPSTREAM'S, COPIED NOT INVENTED (ruling D5.3): `current_branch` is
  pre-commit-hooks' `no_commit_to_branch.is_on_branch` — `git symbolic-ref HEAD`, split on
  `/`, drop the leading `refs/heads` chunks. Copying a predicate that a fleet already runs
  means this gate cannot disagree with the upstream one about what "on main" means.

THE ONE ADDED CARVE-OUT — `MERGE_HEAD` present => ALLOW: a merge is exactly the commit
  core-invariant #5 WANTS on main, so refusing it would invert the rule. It matters only
  for the CONFLICTED case, because of how git routes the two:
    * clean `--no-ff` merge  -> git runs the `pre-merge-commit` hook, never `pre-commit`
      (git-merge docs), and this repo installs only pre-commit / commit-msg / pre-push —
      so this hook is never invoked at all. Nothing to carve out.
    * conflicted merge       -> resolution is a separate `git commit`, which DOES run
      pre-commit, on branch `main`, with no merge parent yet visible in history. Without
      the carve-out the gate would refuse every conflicted integration merge — and a gate
      that blocks legitimate work teaches `--no-verify` as a habit, which costs more than
      the invariant it guards.
  `MERGE_HEAD` is resolved through `git rev-parse --git-path MERGE_HEAD` rather than a
  hardcoded `.git/MERGE_HEAD`, because it is PER-WORKTREE state: in a linked worktree the
  real file lives under `.git/worktrees/<name>/`, and the literal path would miss it.

STATED HOLES, BY DESIGN (per state-honest-enforcement-limits — what this does NOT catch):
  * DETACHED HEAD passes. `git symbolic-ref HEAD` fails there, so the branch is unknown and
    the gate declines to guess — upstream's behaviour, kept deliberately. A commit made
    detached and later fast-forwarded onto main is not refused here; `block_ff_push` and
    the `no_ff_merges` audit WARN remain the backstops for that path.
  * ONLY `MERGE_HEAD` is a carve-out. A cherry-pick, revert, or rebase resolving on main is
    refused like any other non-merge commit, because it IS one.
  * A client-side hook is bypassable — `git commit --no-verify`, an unset core.hooksPath, or
    a checkout that never ran `pre-commit install`. Pragmatic teeth for a single-operator
    hub, not a guarantee.

ARMING: no new mechanism. This is a `.pre-commit-config.yaml` local hook at the `pre-commit`
  stage, so the existing SessionStart `arm_hooks.py` self-arm installs it and
  `audit.py::check_hooks_armed` asserts it stays armed.

Scope: HUB-ONLY, like its pre-push sibling. Fail **CLOSED** (exit 2) on internal error, per
  the ADR-85 amendment 2026-08-03 §A6 and check_seal_identity.py:73-77 — an error is never a
  silent pass. Refusing cannot wedge legitimate work: `git commit --no-verify` is the
  explicit escape, and `block_ff_push` still refuses the push afterwards.

Exit codes: 0 allow · 1 refuse (a direct commit on main) · 2 internal error, refuse.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import telemetry_emit as _te        # noqa: E402  -- [#529] Stage-1 emit

PROTECTED_BRANCH = "main"

#: The organ's name in the [#529] store -- the pre-commit hook id, as in the two push organs.
HOOK_NAME = "block-commit-on-main"

# --- [#529] telemetry: switch + destination -------------------------------------------------
#
# DELIBERATELY A SECOND COPY of the four lines `block_ff_push` also carries, and the duplication
# is the cheaper of two costs. This organ imports NO sibling by design: it runs at pre-commit,
# on every commit, and reaching `block_ff_push` for a truthiness predicate would drag
# `validate_no_ff` and its transitive imports into that path. The predicate is four lines and
# pinned by a test that asserts BOTH copies agree
# (`tests/test_hook_telemetry.py::test_the_env_switch_predicate_is_explicit_about_what_counts_as_on`),
# so a drift between them reddens rather than hides. The two PUSH organs do share one object,
# because they already share a range resolver and an anchoring predicate.
TELEMETRY_ENV = "DEV_KNOWLEDGE_TELEMETRY"

#: Enumerated, not truthiness: `bool("0")` is True, and `DEV_KNOWLEDGE_TELEMETRY=0` means OFF.
_TELEMETRY_ON_VALUES = frozenset({"1", "true", "yes", "on"})


def telemetry_enabled() -> bool:
    """Is [#529] emission on for this hook run? Off unless the env switch says otherwise."""
    return os.environ.get(TELEMETRY_ENV, "").strip().lower() in _TELEMETRY_ON_VALUES


def telemetry_db(repo: Path) -> Path:
    """The store for THIS hook's repo — never `telemetry_emit.default_db_path()`, which resolves
    the library's own root and would write outside the tree a sandbox is watching."""
    override = os.environ.get(_te.DB_PATH_ENV)
    if override:
        return Path(override)
    return repo / _te.DEFAULT_DB_RELPATH


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    """Run a read-only git command in `repo`. Never raises on a non-zero exit — callers
    decide what a failure means, because the two failure sites mean opposite things."""
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, timeout=10,
    )


def current_branch(repo: Path) -> str | None:
    """The branch HEAD points at, or None when HEAD is detached / unresolvable.

    Upstream `no_commit_to_branch.is_on_branch`, copied: `git symbolic-ref HEAD` yields
    `refs/heads/<name>`; dropping the first two `/`-chunks leaves `<name>` and keeps a
    slashed branch name (`worktree-lane-o-527-block-main`, `feat/a/b`) intact. A failure
    means detached HEAD (or no repo), which returns None — the stated hole above, not an
    error, so it must not raise.
    """
    r = _git(repo, "symbolic-ref", "HEAD")
    if r.returncode != 0:
        return None
    chunks = r.stdout.strip().split("/")
    return "/".join(chunks[2:]) or None


def merge_in_progress(repo: Path) -> bool:
    """True when a merge is mid-flight — i.e. `MERGE_HEAD` exists for THIS worktree.

    The path comes from `git rev-parse --git-path MERGE_HEAD` so linked worktrees resolve
    to their own `.git/worktrees/<name>/MERGE_HEAD` (a hardcoded `.git/MERGE_HEAD` reads
    the wrong tree's state, or no tree's). git returns the path relative to the CWD when it
    is relative, and the CWD here is `repo`, so joining on `repo` is the same path git meant.

    RAISES on a git failure rather than returning False: this is only ever asked while the
    gate has already decided the commit is on main, so an unknown answer is the difference
    between allowing a merge and refusing a direct commit — exactly the question the gate
    exists to answer, and never one to guess at. `main()` turns it into exit 2.
    """
    r = _git(repo, "rev-parse", "--git-path", "MERGE_HEAD")
    if r.returncode != 0:
        raise RuntimeError(
            f"could not resolve MERGE_HEAD: git rev-parse --git-path exited "
            f"{r.returncode}: {r.stderr.strip()}")
    path = Path(r.stdout.strip())
    if not path.is_absolute():
        path = repo / path
    return path.exists()


def refuses(repo: Path, protected: str = PROTECTED_BRANCH) -> bool:
    """True when this commit should be refused: on `protected`, and not a merge.

    Order matters — the branch is checked first so a detached HEAD or a feature branch
    never reaches the MERGE_HEAD probe, and therefore can never be refused by its error.
    """
    if current_branch(repo) != protected:
        return False
    return not merge_in_progress(repo)


def _repo_root() -> Path:
    """The repo being committed to = git toplevel of the CWD where the hook runs. Falls
    back to the CWD on any error (mirrors block_ff_push._repo_root)."""
    r = _git(Path.cwd(), "rev-parse", "--show-toplevel")
    if r.returncode == 0 and r.stdout.strip():
        return Path(r.stdout.strip())
    return Path.cwd()


def main(argv: list[str] | None = None) -> int:
    """Refuse (1) a non-merge commit on main; allow (0) otherwise; refuse (2) on error.

    A THIN wrapper over `_verdict` since the [#529] wiring: the decision stays in one place and
    the telemetry sits strictly after it, unable to change the code it is handed. With the switch
    off nothing below the verdict runs at all.

    Exit 2 emits `hook_run(outcome="error")` and NO `blocker_fired`. That distinction is the
    point for THIS organ specifically: `current_branch()` returns `None` on any git failure, a
    documented fail-OPEN hole that has until now been a silent allow. It stays an allow — the
    behaviour is not this lane's to change — but a run that hits it is now countable."""
    started = time.perf_counter()
    verdict: dict = {}
    code = _verdict(argv, verdict)
    if telemetry_enabled():
        repo = verdict.get("repo") or Path.cwd()
        db = telemetry_db(repo)
        duration = int((time.perf_counter() - started) * 1000)
        _te.safe_emit(_te.emit_hook_run, HOOK_NAME, {0: "pass", 1: "block"}.get(code, "error"),
                      duration, db_path=db)
        if code == 1 and verdict.get("reason"):
            _te.safe_emit(_te.emit_blocker_fired, HOOK_NAME, verdict["reason"], db_path=db)
    return code


def _verdict(argv: list[str] | None, verdict: dict) -> int:
    """The organ's actual decision. `verdict` collects what the emitter needs."""
    try:
        repo = _repo_root()
        verdict["repo"] = repo
        if not refuses(repo):
            return 0
    except Exception as exc:  # noqa: BLE001 — fail CLOSED, per ADR-85 amendment §A6
        print(f"block_commit_on_main: INTERNAL ERROR ({exc!r}) — refusing the commit; an "
              "error is never a silent pass. Fix the hook, or bypass explicitly with "
              "`git commit --no-verify`.", file=sys.stderr)
        verdict["reason"] = f"internal error: {type(exc).__name__}"
        return 2
    verdict["reason"] = f"non-merge commit on '{PROTECTED_BRANCH}' (core-invariant #5)"
    print(f"block_commit_on_main: REFUSED — a non-merge commit on '{PROTECTED_BRANCH}'. "
          "Core-invariant #5 wants branch -> `--no-ff` merge, never a direct commit "
          "(the 2026-08-13 incident cost a commit-tree re-land to unwind).",
          file=sys.stderr)
    print("  fix: `git switch -c <feat|fix|docs|chore>/<slug>` and commit there, then "
          "merge with `git merge --no-ff`.", file=sys.stderr)
    print("  note: a merge resolving conflicts on main is ALLOWED (MERGE_HEAD present); "
          "this refusal means no merge is in progress.", file=sys.stderr)
    print("  bypass: `git commit --no-verify` (block_ff_push still refuses the push).",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
