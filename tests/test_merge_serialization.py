"""Tests WITNESSING git's native merge/push serialization — the evidentiary basis for
the #200 "merge-serialization gate" close (accepted-prose-only).

#200 asked for "a mechanism [that] rejects a second concurrent merge-to-`main` (with a
test proving the concurrent merge is blocked), OR it is recorded as accepted-prose-only
with a reason." The gap analysis (see PLAYBOOK §8 "Merge serialization") found NO reachable
gap a new hook would close: the concurrent-merge-COMMAND race is already fully serialized
by git itself, plus the existing FF-block (scripts/block_ff_push.py) for the spine.

These tests therefore witness the EXISTING git-native serialization — there is no new
mechanism under test. They are the empirical record that the close rests on observed
behavior, not assertion (witnessed-behavior-outranks-a-code-read):

  1. A second `git merge` while one is in-progress (MERGE_HEAD present) is refused.
  2. A `git merge` while another git process holds `.git/index.lock` is refused.
  3. A push to a `main` that has moved is rejected ("fetch first").

What git does NOT serialize (stated honestly, per state-honest-enforcement-limits): a
single working tree's HEAD shared between two co-located actors (#107 worktree isolation),
and a *primary*-checkout self-merge — byte-identical to a legitimate operator merge, so no
hook can distinguish it. Those are covered by the commit-and-STOP / integrate-from-the-
primary discipline (A1-prose) + the #184 empirical close, NOT by machinery.
"""
from __future__ import annotations

import shutil
import subprocess

import pytest

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")


# --- git tmp-repo helpers (mirror test_block_ff_push / test_validate_no_ff) ---

def _run(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          capture_output=True, text=True, encoding="utf-8")


def _commit(repo, msg, fname="f.txt", content=None):
    (repo / fname).write_text(content if content is not None else msg + "\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", msg)


def _init_repo(tmp_path, name="r"):
    repo = tmp_path / name
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    _commit(repo, "seed", fname="seed.txt")
    _run(repo, "branch", "-M", "main")
    return repo


# --- (1) MERGE_HEAD: a second merge mid-merge is refused ---------------------

@requires_git
def test_merge_head_blocks_second_merge(tmp_path):
    """An in-progress (conflict-paused) merge leaves MERGE_HEAD; a second `git merge`
    is refused by git itself — no project mechanism needed."""
    repo = _init_repo(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat1")
    _commit(repo, "feat1", fname="f.txt", content="feat1\n")
    _run(repo, "checkout", "-q", "main")
    _commit(repo, "mainchange", fname="f.txt", content="mainchange\n")
    # Conflicting merge -> pauses with MERGE_HEAD set.
    paused = _run(repo, "merge", "feat1", check=False)
    assert paused.returncode != 0
    assert (repo / ".git" / "MERGE_HEAD").exists(), "expected an in-progress merge state"
    # A second merge attempt is refused by git natively.
    second = _run(repo, "merge", "feat1", check=False)
    assert second.returncode != 0
    blob = (second.stderr + second.stdout).lower()
    assert "merge" in blob and ("not possible" in blob or "merge_head" in blob
                                or "unmerged" in blob or "not concluded" in blob)


# --- (2) index.lock: a merge while the lock is held is refused ---------------

@requires_git
def test_index_lock_blocks_concurrent_merge(tmp_path):
    """A held `.git/index.lock` (what a concurrent git process owns) makes a merge fail —
    git's built-in serialization for two simultaneous index-mutating commands."""
    repo = _init_repo(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat1")
    _commit(repo, "feat1", fname="g.txt")
    _run(repo, "checkout", "-q", "main")
    lock = repo / ".git" / "index.lock"
    lock.write_text("", encoding="utf-8")
    try:
        res = _run(repo, "merge", "--no-ff", "-m", "Merge feat1", "feat1", check=False)
        assert res.returncode != 0
        assert "index.lock" in (res.stderr + res.stdout)
    finally:
        lock.unlink(missing_ok=True)


# --- (3) push-rejection: a stale push to a moved main is rejected ------------

@requires_git
def test_push_rejected_when_main_moved(tmp_path):
    """Two clones of one remote: after clone A pushes, clone B's stale push is rejected
    ("fetch first") — git serializes the integration point across clones."""
    bare = tmp_path / "remote.git"
    bare.mkdir()
    _run(bare, "init", "--bare", "-q")

    a = _init_repo(tmp_path, name="cloneA")
    _run(a, "remote", "add", "origin", str(bare))
    _run(a, "push", "-q", "origin", "main")

    b = tmp_path / "cloneB"
    subprocess.run(["git", "clone", "-q", str(bare), str(b)], check=True,
                   capture_output=True, text=True, encoding="utf-8")
    _run(b, "config", "user.email", "t@t.t")
    _run(b, "config", "user.name", "t")

    _commit(a, "a2", fname="f.txt", content="a2\n")
    _run(a, "push", "-q", "origin", "main")

    _commit(b, "b2", fname="f.txt", content="b2\n")
    rej = _run(b, "push", "origin", "main", check=False)
    assert rej.returncode != 0
    blob = (rej.stderr + rej.stdout).lower()
    assert "rejected" in blob or "fetch first" in blob
