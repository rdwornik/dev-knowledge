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

THE STASH LEG (F4, batch-1 night audit, landed 2026-08-07). A fourth kind of leftover that
none of the three states above can see: `refs/stash` lives in the COMMON git directory, not
in any worktree's private ref space. A lane that stashes mid-work and hands its branch back
leaves that stash behind, and it survives `git worktree remove`, `git worktree prune`, the
branch delete, and every one of the four refuse-to-finish items — all of which are worktree-
or branch-shaped. The work is then invisible in the tree, invisible on the branch, and
recoverable only by someone who thinks to run `git stash list`. Hence a leg that measures
the stash directly rather than inferring it from worktree state.

The leg emits its OWN Finding rather than folding into the worktree verdict, because the two
answer different questions and the empty-worktree case is exactly where the stash matters
most — a batch that closed cleanly by every worktree measure can still be hiding a stash.
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


# --- the stash leg (F4) -----------------------------------------------------------------

def test_a_stash_entry_warns_even_with_no_worktrees(monkeypatch, tmp_path):
    """THE F4 CASE, stated exactly: teardown is complete by every worktree measure — zero
    linked worktrees, nothing to prune, no lane branch left — and a stash is still sitting in
    the common git dir holding work nobody can see. The worktree leg passes, correctly; the
    stash leg is the one that speaks."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [])
    monkeypatch.setattr(aud, "_git_stash_entries",
                        lambda _p: ["stash@{0}: WIP on worktree-lane-b-506-grooming: 1a2b3c4 wip"])
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert len(out) == 2
    assert out[0].status == "pass"                      # worktree leg: genuinely clean
    stash = out[1]
    assert stash.status == "warn"
    assert stash.check_name == "stale_worktrees"
    assert "worktree-lane-b-506-grooming" in stash.evidence
    assert "stash" in stash.evidence.lower()


def test_an_empty_stash_is_reported_rather_than_left_silent(monkeypatch, tmp_path):
    """A leg that says nothing when clean cannot be told apart from a leg that did not run.
    An empty stash reads back as an explicit pass, so the close-out evidence is positive."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [])
    monkeypatch.setattr(aud, "_git_stash_entries", lambda _p: [])
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert len(out) == 2
    assert out[1].status == "pass"
    assert "stash" in out[1].evidence.lower()


def test_several_stash_entries_are_counted_and_the_list_is_bounded(monkeypatch, tmp_path):
    """The count is the load-bearing number; the sample is a courtesy. A pathological stash
    depth stays readable instead of flooding one evidence line."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [])
    monkeypatch.setattr(aud, "_git_stash_entries",
                        lambda _p: [f"stash@{{{i}}}: WIP on lane-{i}" for i in range(9)])
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert out[1].status == "warn"
    assert "9" in out[1].evidence
    assert len(out[1].evidence) < 400


def test_stash_leg_stays_silent_when_the_stash_cannot_be_read(monkeypatch, tmp_path):
    """Unreadable is not clean and is not dirty either. The worktree leg already carries the
    n/a signal for a repo git cannot see, so the stash leg declines to invent a second one."""
    monkeypatch.setattr(aud, "_git_linked_worktrees", lambda _p: [])
    monkeypatch.setattr(aud, "_git_stash_entries", lambda _p: None)
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert len(out) == 1
    assert out[0].check_name == "stale_worktrees"


def test_a_stash_does_not_mask_or_be_masked_by_a_stale_worktree(monkeypatch, tmp_path):
    """Both leftovers at once: each is reported on its own Finding, so neither hides the
    other and an integrator reading the output sees two distinct things to close."""
    monkeypatch.setattr(aud, "_git_linked_worktrees",
                        lambda _p: [_wt("lane-z-401-forgotten", age_days=30)])
    monkeypatch.setattr(aud, "_git_stash_entries", lambda _p: ["stash@{0}: WIP on lane-z"])
    out = aud.check_stale_worktrees(tmp_path, now=_NOW)
    assert [f.status for f in out] == ["warn", "warn"]
    assert "lane-z-401-forgotten" in out[0].evidence
    assert "stash" in out[1].evidence.lower()


def test_stash_leg_is_also_structurally_incapable_of_failing():
    """Same WARN-tier posture as the organ it joins, pinned at the source for the same
    reason: an inputs-only assertion holds only until a FAIL branch is added later."""
    src = inspect.getsource(aud._stash_findings)
    assert '"fail"' not in src and "'fail'" not in src


@requires_git
def test_stash_reader_sees_a_real_stash_in_the_common_git_dir(tmp_path):
    """THE TEST THAT CONSTRAINS THE READER, against real git — the same role the linked-
    worktree integration test plays above. A reader that always returned `[]` would satisfy
    every monkeypatched assertion here and silently disable the leg.

    It also pins the property the whole finding rests on: the stash made INSIDE a linked
    worktree is visible from the PRIMARY, because `refs/stash` is common rather than
    per-worktree. That is precisely why worktree teardown cannot take it with it."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    assert aud._git_stash_entries(repo) == []          # baseline: nothing stashed yet

    wt = tmp_path / "lane-a-505-batch-protocol"
    subprocess.run(["git", "-C", str(repo), "worktree", "add", str(wt),
                    "-b", "worktree-lane-a-505-batch-protocol"], check=True, capture_output=True)
    try:
        (wt / "f.txt").write_text("lane work nobody committed", encoding="utf-8")
        subprocess.run(["git", "-C", str(wt), "stash", "push", "-m", "lane wip"],
                       check=True, capture_output=True)
        # read from the PRIMARY, not from the worktree that made it
        entries = aud._git_stash_entries(repo)
        assert entries is not None and len(entries) == 1, entries
        assert "lane wip" in entries[0]

        # ... and teardown does not take it away: this is F4 in one assertion
        subprocess.run(["git", "-C", str(repo), "worktree", "remove", "--force", str(wt)],
                       check=True, capture_output=True)
        subprocess.run(["git", "-C", str(repo), "worktree", "prune"], capture_output=True)
        subprocess.run(["git", "-C", str(repo), "branch", "-D",
                        "worktree-lane-a-505-batch-protocol"], capture_output=True)
        assert aud._git_linked_worktrees(repo) == []    # every worktree measure now clean
        survivors = aud._git_stash_entries(repo)
        assert survivors is not None and len(survivors) == 1, survivors

        out = aud.check_stale_worktrees(repo)
        assert out[0].status == "pass"                  # worktree leg sees nothing wrong
        assert out[1].status == "warn"                  # the stash leg is the only witness
    finally:
        subprocess.run(["git", "-C", str(repo), "stash", "clear"], capture_output=True)
        subprocess.run(["git", "-C", str(repo), "worktree", "prune"], capture_output=True)


@requires_git
def test_stash_reader_returns_none_outside_a_repo(tmp_path):
    """Graceful degradation, the `_git_linked_worktrees` contract: not-a-repo reads as
    unknown rather than as an empty stash, which is what keeps the leg from reporting a
    clean stash for a directory it never looked into."""
    assert aud._git_stash_entries(tmp_path) is None
