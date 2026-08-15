"""Tests for scripts/block_commit_on_main.py — [#527] pre-commit GATE (the commit-time
half of core-invariant #5; block_ff_push stays the push-time half).

Closure metric (hard, and it is the row's own Done-when): "a seeded direct commit attempt
on `main` is refused BY A PRE-COMMIT HOOK". So the six acceptance cases below do not call
`main()` and inspect an exit code — they install the real script as a real
`.git/hooks/pre-commit` in a throwaway repo and run real `git commit`, then assert on
whether the COMMIT happened. A hook that returns 1 while git commits anyway would pass the
weaker test and fail the row.

The acceptance matrix, verbatim, one test each:
    E1  direct non-merge commit on main .......... REFUSED
    E2  commit on a feature branch ............... ALLOWED
    E3  clean --no-ff merge ...................... NEVER FIRES THE HOOK
    E4  conflicted merge on main ................. ALLOWED via the MERGE_HEAD carve-out
    E5  amend on main ............................ REFUSED
    W1  worktree on a feature branch ............. ALLOWED

E3 and E4 share one rig on purpose, because they are the same claim seen from both sides:
the armed hook writes a marker file before exec'ing the script, so "never fires" (E3, no
marker, merge lands) and "fires and allows" (E4, marker present, merge lands) are read off
the same instrument rather than asserted about git from memory.

Below the matrix: the predicate/limit tests. They pin the STATED HOLES (detached HEAD
passes; only MERGE_HEAD carves out) so a hole stays a decision rather than becoming an
accident, and the per-worktree MERGE_HEAD resolution the docstring claims — proven by a
conflicted merge inside a LINKED worktree, where a hardcoded `.git/MERGE_HEAD` reads a
gitdir pointer file and would refuse a legitimate merge.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import block_commit_on_main as bcm

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "block_commit_on_main.py"


# --- git tmp-repo helpers (mirror test_block_ff_push) -----------------------

def _run(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True, encoding="utf-8", errors="replace")


def _try(repo, *args):
    """Like _run but returns the CompletedProcess — for commands expected to FAIL.

    `errors="replace"` is load-bearing on Windows: the refused-commit path relays the
    hook's own stderr, and a hook writes it in the console's locale encoding (cp1252
    here), so a strict utf-8 decode raises in subprocess's reader thread and hands the
    test `stdout=None` — a crash that looks like an assertion failure about the gate.
    """
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def _rev(repo, ref="HEAD"):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", ref],
                          check=True, capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def _parents(repo):
    """The `<commit> <parent>...` line for HEAD, split — 3 fields == a two-parent merge."""
    return subprocess.run(["git", "-C", str(repo), "rev-list", "--parents", "-n", "1", "HEAD"],
                          check=True, capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.split()


def _commit(repo, msg, fname="f.txt", content=None):
    (Path(repo) / fname).write_text(content if content is not None else msg, encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", msg)


def _init_repo(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    # Pin the hooks dir explicitly: a global/system core.hooksPath on the developer's
    # machine would otherwise silently disarm every hook these tests install, and the
    # suite would go green while proving nothing (the relic-hooksPath failure class).
    #
    # ABSOLUTE, not `.git/hooks`. git resolves a RELATIVE core.hooksPath against the
    # worktree it is invoked from, so the relative spelling points a linked worktree at
    # its own `<wt>/.git/hooks` — which does not exist, because `<wt>/.git` is a pointer
    # file. W1 then commits with no hook armed at all and passes while proving nothing.
    # Caught by mutating the gate to refuse everywhere and finding W1 still green.
    _run(repo, "config", "core.hooksPath", str((repo / ".git" / "hooks").resolve()))
    _commit(repo, "seed", fname="seed.txt")
    _run(repo, "branch", "-M", "main")
    return repo


def _arm(repo, marker=None):
    """Install scripts/block_commit_on_main.py as the repo's real pre-commit hook.

    When `marker` is given the shim appends to it BEFORE exec'ing the script, so a test
    can tell "the hook was never invoked" (E3) apart from "the hook ran and allowed" (E4)
    — two states that look identical from the commit's exit code alone.

    ARM LAST. Once this returns, the repo refuses its own fixture: any later helper that
    commits on main (`_commit`, `_conflict_pair`) fails with a CalledProcessError that
    reads like a broken gate rather than a broken fixture.
    """
    hooks = Path(_rev_git_path(repo, "hooks"))
    hooks.mkdir(parents=True, exist_ok=True)
    hook = hooks / "pre-commit"
    lines = ["#!/bin/sh"]
    if marker is not None:
        lines.append(f'echo fired >> "{Path(marker).as_posix()}"')
    lines.append(f'exec "{Path(sys.executable).as_posix()}" "{_SCRIPT.as_posix()}"')
    hook.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    hook.chmod(0o755)
    return hook


def _rev_git_path(repo, what):
    """Absolute path for `git rev-parse --git-path <what>` run in `repo`."""
    out = subprocess.run(["git", "-C", str(repo), "rev-parse", "--git-path", what],
                         check=True, capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stdout.strip()
    p = Path(out)
    return p if p.is_absolute() else Path(repo) / p


def _stage(repo, fname, content):
    (Path(repo) / fname).write_text(content, encoding="utf-8")
    _run(repo, "add", "-A")


def _conflict_pair(repo, branch="feat/x"):
    """Leave `repo` on main with `branch` diverged on the SAME line, so the next
    `git merge --no-ff <branch>` conflicts and must be resolved by a `git commit`."""
    _commit(repo, "base", fname="c.txt", content="base\n")
    _run(repo, "switch", "-q", "-c", branch)
    _commit(repo, "theirs", fname="c.txt", content="theirs\n")
    _run(repo, "switch", "-q", "main")
    _commit(repo, "ours", fname="c.txt", content="ours\n")
    return branch


# === THE ACCEPTANCE MATRIX =================================================

@requires_git
def test_e1_direct_non_merge_commit_on_main_is_refused(tmp_path):
    """E1 — a direct non-merge commit on main is REFUSED (by the hook, at commit time)."""
    repo = _init_repo(tmp_path)
    _arm(repo)
    before = _rev(repo)
    _stage(repo, "direct.txt", "a direct edit on main\n")

    r = _try(repo, "commit", "-m", "direct on main")

    assert r.returncode != 0, "the commit succeeded — the gate did not refuse"
    assert "block_commit_on_main: REFUSED" in (r.stdout + r.stderr)
    assert _rev(repo) == before, "HEAD moved — a refused commit must not exist"


@requires_git
def test_e2_commit_on_a_feature_branch_is_allowed(tmp_path):
    """E2 — a commit on a feature branch is ALLOWED."""
    repo = _init_repo(tmp_path)
    _arm(repo)
    _run(repo, "switch", "-q", "-c", "feat/x")
    before = _rev(repo)
    _stage(repo, "onfeat.txt", "work on a branch\n")

    r = _try(repo, "commit", "-m", "on a feature branch")

    assert r.returncode == 0, f"the gate refused a feature-branch commit: {r.stderr}"
    assert _rev(repo) != before


@requires_git
def test_e3_clean_no_ff_merge_never_fires_the_hook(tmp_path):
    """E3 — a clean `--no-ff` merge NEVER FIRES the hook.

    git routes an automatic merge through `pre-merge-commit`, not `pre-commit`, and this
    repo installs only pre-commit / commit-msg / pre-push — so the gate is not consulted
    at all. The marker file is the proof: absent means never invoked.
    """
    repo = _init_repo(tmp_path)
    marker = tmp_path / "fired.txt"
    _run(repo, "switch", "-q", "-c", "feat/clean")
    _commit(repo, "their file", fname="theirs.txt", content="theirs\n")
    _run(repo, "switch", "-q", "main")
    _commit(repo, "our file", fname="ours.txt", content="ours\n")
    _arm(repo, marker=marker)   # after the fixture — see _arm

    r = _try(repo, "merge", "--no-ff", "--no-edit", "feat/clean")

    assert r.returncode == 0, f"the clean --no-ff merge did not land: {r.stderr}"
    assert not marker.exists(), "the pre-commit hook fired on a clean merge"
    assert len(_parents(repo)) == 3, "HEAD is not a two-parent merge commit"


@requires_git
def test_e4_conflicted_merge_on_main_is_allowed_via_the_carve_out(tmp_path):
    """E4 — a CONFLICTED merge on main is ALLOWED via the MERGE_HEAD carve-out.

    The other side of E3's rig: here the hook IS invoked (marker present), because a
    conflicted merge resolves through a separate `git commit`. This is the case the whole
    carve-out exists for — refusing it is what would teach `--no-verify` as a habit.
    """
    repo = _init_repo(tmp_path)
    marker = tmp_path / "fired.txt"
    branch = _conflict_pair(repo)
    _arm(repo, marker=marker)   # after the fixture — see _arm

    merged = _try(repo, "merge", "--no-ff", "--no-edit", branch)
    assert merged.returncode != 0, "the fixture did not actually conflict"
    assert _rev_git_path(repo, "MERGE_HEAD").exists(), "no merge is in progress"

    _stage(repo, "c.txt", "resolved\n")
    r = _try(repo, "commit", "--no-edit")

    assert r.returncode == 0, f"the gate refused a conflicted merge on main: {r.stderr}"
    assert marker.exists(), "the hook never ran — E4 would prove nothing"
    assert len(_parents(repo)) == 3, "the resolved commit is not a two-parent merge"


@requires_git
def test_e5_amend_on_main_is_refused(tmp_path):
    """E5 — `git commit --amend` on main is REFUSED (an amend is still a non-merge commit
    landing on main, and rewriting main's tip is the very act the gate exists to stop)."""
    repo = _init_repo(tmp_path)
    _arm(repo)
    before = _rev(repo)

    r = _try(repo, "commit", "--amend", "-m", "amended on main")

    assert r.returncode != 0, "the amend succeeded — the gate did not refuse"
    assert "block_commit_on_main: REFUSED" in (r.stdout + r.stderr)
    assert _rev(repo) == before, "HEAD moved — a refused amend must not rewrite main"


@requires_git
def test_w1_worktree_on_a_feature_branch_is_allowed(tmp_path):
    """W1 — a commit in a LINKED WORKTREE on a feature branch is ALLOWED.

    A linked worktree shares the common hooks dir, so the same armed hook runs there; what
    differs is that `git symbolic-ref HEAD` must resolve THAT worktree's branch, not the
    primary's. Every batch lane commits this way, so a false refusal here would wedge the
    whole parallel protocol.

    The marker is asserted here and not only in E4: "allowed" and "never armed" are the
    same green, and this is the one case where the arming can silently fail to reach the
    tree under test.
    """
    repo = _init_repo(tmp_path)
    marker = tmp_path / "fired.txt"
    _arm(repo, marker=marker)
    wt = tmp_path / "lane"
    _run(repo, "worktree", "add", "-q", "-b", "worktree-lane-z-test", str(wt))
    before = _rev(wt)
    _stage(wt, "lane.txt", "lane work\n")

    r = _try(wt, "commit", "-m", "work in a lane worktree")

    assert r.returncode == 0, f"the gate refused a worktree commit: {r.stderr}"
    assert marker.exists(), "the hook never ran in the worktree — W1 would prove nothing"
    assert _rev(wt) != before


# === PREDICATE + STATED-HOLE TESTS =========================================

@requires_git
def test_current_branch_reads_this_worktrees_branch(tmp_path):
    repo = _init_repo(tmp_path)
    assert bcm.current_branch(repo) == "main"
    _run(repo, "switch", "-q", "-c", "feat/a/b")
    assert bcm.current_branch(repo) == "feat/a/b", "a slashed branch name was truncated"


@requires_git
def test_detached_head_passes_the_stated_hole(tmp_path):
    """A STATED HOLE, pinned so it stays a decision: `git symbolic-ref HEAD` fails when
    HEAD is detached, so the branch is unknown and the gate declines to guess (upstream
    no_commit_to_branch's own behaviour). block_ff_push remains the backstop."""
    repo = _init_repo(tmp_path)
    _run(repo, "checkout", "-q", "--detach")
    assert bcm.current_branch(repo) is None
    assert bcm.refuses(repo) is False


@requires_git
def test_merge_head_carve_out_is_per_worktree(tmp_path):
    """The docstring's per-worktree claim, proven where it actually bites: a conflicted
    merge inside a LINKED worktree writes MERGE_HEAD under `.git/worktrees/<name>/`, while
    `<worktree>/.git` is a POINTER FILE — so a hardcoded `.git/MERGE_HEAD` would never
    exist and the gate would refuse a legitimate integration merge."""
    repo = _init_repo(tmp_path)
    _run(repo, "switch", "-q", "-c", "feat/park")   # free `main` for the linked worktree
    wt = tmp_path / "onmain"
    _run(repo, "worktree", "add", "-q", str(wt), "main")
    branch = _conflict_pair(wt, branch="feat/wt")
    assert _try(wt, "merge", "--no-ff", "--no-edit", branch).returncode != 0

    merge_head = _rev_git_path(wt, "MERGE_HEAD")
    assert merge_head.exists()
    assert "worktrees" in merge_head.parts, "MERGE_HEAD is not per-worktree here"
    assert not (wt / ".git").is_dir(), "the linked worktree's .git is not a pointer file"
    assert bcm.merge_in_progress(wt) is True
    assert bcm.current_branch(wt) == "main"
    assert bcm.refuses(wt) is False, "the carve-out missed a per-worktree merge"


@requires_git
def test_only_merge_head_carves_out_a_cherry_pick_on_main_is_refused(tmp_path):
    """The other STATED HOLE, from the closed side: ONE carve-out means a cherry-pick
    resolving on main is refused like the non-merge commit it is."""
    repo = _init_repo(tmp_path)
    branch = _conflict_pair(repo)
    _arm(repo)   # after the fixture — see _arm
    picked = _rev(repo, branch)
    assert _try(repo, "cherry-pick", picked).returncode != 0   # conflicts on c.txt
    before = _rev(repo)
    _stage(repo, "c.txt", "resolved\n")

    r = _try(repo, "commit", "--no-edit")

    assert r.returncode != 0, "a cherry-pick resolution on main was allowed"
    assert "block_commit_on_main: REFUSED" in (r.stdout + r.stderr)
    assert _rev(repo) == before


def test_internal_error_fails_closed_exit_2(monkeypatch, tmp_path):
    """Fail CLOSED (ADR-85 amendment 2026-08-03 §A6): an unreadable MERGE_HEAD while on
    main is the exact question the gate exists to answer, so it refuses rather than
    guessing. Exit 2 is distinct from 1 so an error is never read as a detected violation."""
    def fake_git(repo, *args):
        if args[:1] == ("symbolic-ref",):
            return subprocess.CompletedProcess(args, 0, "refs/heads/main\n", "")
        if args[:2] == ("rev-parse", "--show-toplevel"):
            return subprocess.CompletedProcess(args, 0, str(tmp_path) + "\n", "")
        return subprocess.CompletedProcess(args, 128, "", "fatal: not a git repository")

    monkeypatch.setattr(bcm, "_git", fake_git)
    with pytest.raises(RuntimeError):
        bcm.merge_in_progress(tmp_path)
    assert bcm.main() == 2


def test_protected_branch_is_main():
    """The gate protects exactly `main` — the branch core-invariant #5 names."""
    assert bcm.PROTECTED_BRANCH == "main"
