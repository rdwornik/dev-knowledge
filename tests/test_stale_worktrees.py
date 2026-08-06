"""Tests for `audit.check_stale_worktrees` — the [#505] batch-hygiene organ.

THE GAP (intake #26, the operator's stated #1 pain): unclosed parallel work. A batch that
ends without its integrator walking the close-out leaves worktrees registered and lane
branches unmerged, and nothing in the repo notices. `check_no_sibling_orphans` is the
nearest neighbour and does NOT cover this: it looks for `<repo>-*` sibling directories that
git has already DEREGISTERED. The state here is the opposite one — a worktree git still
knows about, sitting in `.claude/worktrees/`, that no live batch owns.

POSTURE — WARN, never FAIL, and the ruling is explicit about it (ADR-110 §3 arms no gate;
the [#505] contract says "WARN, never FAIL"). `test_leg_is_structurally_incapable_of_failing`
pins that at the SOURCE level rather than only on today's inputs, following the
`review_artifact_coverage` precedent: an inputs-only test passes for as long as no input
happens to trip a FAIL branch that was added later.

THE THREE STATES the check distinguishes, which are this file's spine:
  * CLEAN     — the primary worktree only. Nothing to say.
  * MID-BATCH — linked worktrees whose branches carry work inside the prune horizon. These
                are live lanes, and flagging them would make the check fire during exactly
                the run it exists to close out.
  * STALE     — a linked worktree past the horizon, or one git still registers whose
                directory is gone from disk.

The horizon is the mechanized WEEKLY prune the intake keeps ("hygiene organ — WARN on stale
worktrees (mechanized weekly prune stays)"), so 7 days is that cadence and not a taste call.
"""
from __future__ import annotations

import inspect
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import audit as aud   # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_NOW = 1_754_400_000          # a fixed epoch; the check takes `now` as a parameter so the
_DAY = 86_400                 # tests never depend on the wall clock (Date.now-free by design)


def _wt(name: str, *, age_days: float = 0.0, on_disk: bool = True) -> dict:
    """One linked-worktree record in the shape `_git_linked_worktrees` returns."""
    return {
        "path": f"/repo/.claude/worktrees/{name}",
        "branch": f"worktree-{name}",
        "last_commit_epoch": _NOW - int(age_days * _DAY),
        "on_disk": on_disk,
    }


# --- the three states -------------------------------------------------------------------

def test_clean_tree_passes(monkeypatch, tmp_path):
    """CLEAN — no linked worktrees at all. The overwhelmingly common state; it stays quiet."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [])
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert len(out) == 1
    assert out[0].status == "pass"
    assert out[0].check_name == "stale_worktrees"


def test_mid_batch_worktrees_pass(monkeypatch, tmp_path):
    """MID-BATCH — three lanes, all committed inside the horizon. This is the state a batch
    is IN while it runs, so a WARN here would fire against the protocol it enforces."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [
        _wt("lane-a-505-batch-protocol", age_days=0),
        _wt("lane-b-506-grooming", age_days=1.5),
        _wt("lane-c-490-currency", age_days=6.9),
    ])
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert out[0].status == "pass"
    assert "3" in out[0].evidence


def test_worktree_past_the_horizon_warns(monkeypatch, tmp_path):
    """STALE — a lane whose last commit predates the weekly prune horizon."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [
        _wt("lane-a-505-batch-protocol", age_days=0),
        _wt("lane-z-401-forgotten", age_days=30),
    ])
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert out[0].status == "warn"
    assert "lane-z-401-forgotten" in out[0].evidence
    # the live lane is NOT named as a problem
    assert "lane-a-505-batch-protocol" not in out[0].evidence


def test_registered_but_missing_from_disk_warns_regardless_of_age(monkeypatch, tmp_path):
    """A worktree git still registers whose directory is gone is stale AT ANY AGE — that is a
    half-finished teardown (`remove` silently no-ops on a locked dir), and waiting a week to
    mention it would hide the very failure the round-trip check exists to catch."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [
        _wt("lane-a-505-batch-protocol", age_days=0, on_disk=False),
    ])
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert out[0].status == "warn"
    assert "lane-a-505-batch-protocol" in out[0].evidence
    assert "prune" in out[0].evidence.lower()


def test_horizon_boundary_is_not_stale(monkeypatch, tmp_path):
    """Exactly AT the horizon is still live — the comparison is strict, so a worktree becomes
    stale by exceeding the week rather than by reaching it."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [
        _wt("lane-a-505-batch-protocol", age_days=aud._STALE_WORKTREE_HORIZON_DAYS),
    ])
    assert aud.check_stale_worktrees(tmp_path, now=_NOW)[0].status == "pass"


# --- posture ----------------------------------------------------------------------------

def test_leg_is_structurally_incapable_of_failing():
    """WARN-tier by ruling. Pinned at the SOURCE, not only on today's inputs: an
    inputs-only assertion keeps passing right up until someone adds a `"fail"` branch."""
    src = inspect.getsource(aud.check_stale_worktrees)
    assert '"fail"' not in src and "'fail'" not in src


def test_registered_in_all_checks():
    assert aud.check_stale_worktrees in aud.ALL_CHECKS


def test_unknown_age_does_not_manufacture_staleness(monkeypatch, tmp_path):
    """A worktree whose last-commit date could not be read is reported as INDETERMINATE, not
    silently treated as fresh and not counted as stale. A detector that cannot see must not
    report clean — and equally must not invent a finding it did not measure."""
    entry = _wt("lane-a-505-batch-protocol")
    entry["last_commit_epoch"] = None
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [entry])
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert out[0].status == "warn"
    assert "age unknown" in out[0].evidence


# --- graceful degradation ---------------------------------------------------------------

def test_no_git_degrades_to_na(monkeypatch, tmp_path):
    """git absent / not a repo → n/a, the `no_sibling_orphans` contract. Classified, so the
    inert-check detector can tell 'not applicable here' from 'subject gone'."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: None)
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert out[0].status == "n/a"
    assert aud._na_reason(out[0]) == aud._NA_NOT_APPLICABLE


# --- the real reader, against the real repo ---------------------------------------------

@requires_git
def test_linked_worktrees_reader_excludes_the_primary():
    """`_git_linked_worktrees` returns LINKED worktrees only — the primary is never a candidate,
    which is the difference between this check and a plain `git worktree list` transcription.

    ON ITS OWN THIS TEST IS WEAK, and that is why the integration test below exists (terra HIGH,
    2026-08-06): a reader that always returned `[]` would satisfy this assertion and silently
    disable stale detection. Kept because it pins the primary-exclusion property specifically."""
    entries = aud._git_linked_worktrees(Path(aud._REPO_ROOT))
    assert entries is not None
    paths = {Path(e["path"]).resolve() for e in entries}
    assert Path(aud._REPO_ROOT).resolve() not in paths


def _init_repo(root: Path) -> None:
    subprocess.run(["git", "init", "-b", "main", str(root)], check=True, capture_output=True)
    for k, v in (("user.email", "t@t"), ("user.name", "t")):
        subprocess.run(["git", "-C", str(root), "config", k, v], check=True, capture_output=True)
    (root / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "f.txt"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "init", "--no-verify"],
                   check=True, capture_output=True)


@requires_git
def test_reader_actually_returns_a_real_linked_worktree(tmp_path):
    """THE TEST THAT CONSTRAINS THE READER: provision a real linked worktree against real git
    and assert every field the check consumes comes back populated. A reader returning `[]`,
    dropping the branch, or failing to read the commit date fails here — which the monkeypatched
    state tests above structurally cannot catch, since they replace the reader entirely.

    Cleans up after itself (no-leftovers): the worktree is removed and pruned, and `tmp_path`
    holds both the repo and the worktree, so nothing escapes the temp tree either way."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    wt = tmp_path / "lane-a-505-batch-protocol"
    subprocess.run(["git", "-C", str(repo), "worktree", "add", str(wt),
                    "-b", "worktree-lane-a-505-batch-protocol"], check=True, capture_output=True)
    try:
        entries = aud._git_linked_worktrees(repo)
        assert entries is not None
        assert len(entries) == 1, entries          # the primary is excluded, the linked one is not
        entry = entries[0]
        assert Path(entry["path"]).resolve() == wt.resolve()
        assert entry["branch"] == "worktree-lane-a-505-batch-protocol"
        assert entry["on_disk"] is True
        assert isinstance(entry["last_commit_epoch"], int)
        # ... and the check reads it as a live lane rather than a leftover
        assert aud.check_stale_worktrees(repo)[0].status == "pass"
    finally:
        subprocess.run(["git", "-C", str(repo), "worktree", "remove", "--force", str(wt)],
                       capture_output=True)
        subprocess.run(["git", "-C", str(repo), "worktree", "prune"], capture_output=True)


@requires_git
def test_reader_sees_a_worktree_whose_directory_was_deleted(tmp_path):
    """The half-finished teardown, end to end against real git: the registration survives, the
    directory does not, and the check reports it at any age."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    wt = tmp_path / "lane-b-505-gone"
    subprocess.run(["git", "-C", str(repo), "worktree", "add", str(wt), "-b", "worktree-lane-b-505-gone"],
                   check=True, capture_output=True)
    shutil.rmtree(wt)                              # deregistration deliberately NOT run
    try:
        entries = aud._git_linked_worktrees(repo)
        assert entries is not None and len(entries) == 1
        assert entries[0]["on_disk"] is False
        out = aud.check_stale_worktrees(repo)
        assert out[0].status == "warn"
        assert "prune" in out[0].evidence.lower()
    finally:
        subprocess.run(["git", "-C", str(repo), "worktree", "prune"], capture_output=True)


@requires_git
def test_live_repo_is_not_stale():
    """The hub's own steady state passes — a check that WARNs on a clean tree is noise."""
    out = aud.check_stale_worktrees(Path(aud._REPO_ROOT))
    assert out[0].status in ("pass", "n/a"), out[0].evidence
