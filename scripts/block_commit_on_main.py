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

import subprocess
import sys
from pathlib import Path

PROTECTED_BRANCH = "main"


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
    """Refuse (1) a non-merge commit on main; allow (0) otherwise; refuse (2) on error."""
    try:
        repo = _repo_root()
        if not refuses(repo):
            return 0
    except Exception as exc:  # noqa: BLE001 — fail CLOSED, per ADR-85 amendment §A6
        print(f"block_commit_on_main: INTERNAL ERROR ({exc!r}) — refusing the commit; an "
              "error is never a silent pass. Fix the hook, or bypass explicitly with "
              "`git commit --no-verify`.", file=sys.stderr)
        return 2
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
