"""Tests for scripts/batch_janitor.py -- [#1014], RED-first.

THE INCIDENT: DIGEST-WAVE5A-2026-09-24.md blind spot 3, "~7 finished lane/repair `claude`
processes stayed resident (~360-400 MB each), which held a repair below the 3 GB threshold. At
each teardown the integrator stopped and removed the lane's jobs; several lane jobs' stop/rm
printed nothing." This module is the mechanical replacement for that hand walk: given a batch
name, it reads `dispatch.py`'s own launch records to find that batch's jobs, joins each to the
live `claude agents --json` listing, and stops (`claude stop <job_id>`) whichever ones the
listing already calls FINISHED.

Nothing here starts a real `claude` process: `agents` (the listing) and `run` (the stop caller)
are both injected, the same seam `dispatch.py`'s own tests use for its process boundary.
"""
from __future__ import annotations

import json
import subprocess

import pytest
from click.testing import CliRunner

import batch_janitor as bj


@pytest.fixture
def receipts(tmp_path, monkeypatch):
    target = tmp_path / "receipts"
    target.mkdir()
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(target))
    return target


def _write_job(receipts_dir, *, job_id, slug, batch, worktree=None):
    body = {"schema": 1, "job_id": job_id, "session_id": f"sid-{job_id}", "slug": slug,
           "batch": batch, "provider": "anthropic",
           "worktree": worktree or f"/repo/.claude/worktrees/{slug}",
           "contract": f"LANE-{slug}.md", "launched_at": "2026-09-24T00:00:00+00:00"}
    (receipts_dir / f"LAUNCH-JOB-{job_id}.json").write_text(json.dumps(body), encoding="utf-8")
    return body


def _entry(job_id, state):
    return {"id": job_id, "state": state}


def _listing(*entries):
    return lambda: list(entries)


# --- read_sessions: what "finished" means ------------------------------------

def test_a_terminal_listing_state_reads_as_finished(receipts):
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")
    sessions = bj.read_sessions("B1", agents=_listing(_entry("a1", "done")))
    assert sessions[0].live is False
    assert sessions[0].state == "done"


def test_a_working_listing_state_reads_as_LIVE_never_stopped(receipts):
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")
    sessions = bj.read_sessions("B1", agents=_listing(_entry("a1", "working")))
    assert sessions[0].live is True


def test_a_job_absent_from_the_listing_reads_as_finished(receipts):
    """`dispatch.py::lane_alive`'s own rule: a finished `--bg` job normally stays LISTED, so
    absence is the ended case with no state to name -- and this janitor's job records outlive
    any listing-lag window the way dispatch's own callers assume."""
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")
    sessions = bj.read_sessions("B1", agents=_listing())
    assert sessions[0].live is False
    assert sessions[0].state == "ABSENT"


def test_a_job_of_ANOTHER_batch_is_not_named_at_all(receipts):
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")
    _write_job(receipts, job_id="z9", slug="lane-z", batch="OTHER-BATCH")
    sessions = bj.read_sessions("B1", agents=_listing(_entry("a1", "done"), _entry("z9", "done")))
    assert [s.slug for s in sessions] == ["lane-a"]


def test_an_unreadable_listing_REFUSES_the_read_rather_than_guessing(receipts):
    """A batch janitor that guessed 'probably finished' on an unread listing would be the one
    mechanism in this repo where a wrong guess kills a live session -- refused instead."""
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")

    def boom():
        raise bj._ds.ListingUnreadable("gh/claude control plane hung")

    with pytest.raises(bj.BatchJanitorError):
        bj.read_sessions("B1", agents=boom)


def test_no_job_records_for_the_batch_is_an_empty_tuple_not_an_error(receipts):
    assert bj.read_sessions("NO-SUCH-BATCH", agents=_listing()) == ()


# --- the dry-run contract: lists and stops nothing ----------------------------

def test_DRY_RUN_LISTS_AND_STOPS_NOTHING(receipts):
    """The lane-merge-hygiene done-contract's own wording for the janitor clause. A hostile
    `run` that raises if ever called proves the dry-run path never reaches `stop_session`, not
    only that its return value happens to be empty."""
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")
    _write_job(receipts, job_id="b2", slug="lane-b", batch="B1")
    listing = _listing(_entry("a1", "done"), _entry("b2", "working"))

    def hostile_run(argv):
        raise AssertionError(f"dry-run must never call the stop runner; got {argv!r}")

    report = bj.run_janitor("B1", dry_run=True, agents=listing, run=hostile_run)

    assert report.dry_run is True
    assert report.stopped == ()
    assert report.after == report.before
    assert len(report.before) == 2
    rendered = report.render()
    assert "DRY RUN" in rendered
    assert "lane-a" in rendered and "would stop" in rendered
    assert "lane-b" not in rendered.split("DRY RUN")[1], \
        "the still-LIVE lane must not be listed as something the janitor would stop"


def test_dry_run_over_an_empty_batch_says_so_rather_than_printing_nothing(receipts):
    report = bj.run_janitor("EMPTY-BATCH", dry_run=True, agents=_listing())
    assert "NO JOB RECORDS" in report.render()


# --- the live run: stops only the finished ones, and reports before/after ----

def test_run_janitor_stops_only_FINISHED_sessions_and_reports_before_after(receipts):
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")
    _write_job(receipts, job_id="b2", slug="lane-b", batch="B1")
    calls = []

    def fake_run(argv):
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 0, "worktree retained\n", "")

    reads = [
        [_entry("a1", "done"), _entry("b2", "working")],       # before
        [_entry("a1", "stopped"), _entry("b2", "working")],    # after
    ]
    report = bj.run_janitor("B1", dry_run=False, agents=lambda: reads.pop(0), run=fake_run)

    assert calls == [["claude", "stop", "a1"]], \
        "only the FINISHED lane's job is stopped; the still-working one is left alone"
    assert len(report.stopped) == 1
    assert report.stopped[0].ok
    before_states = {s.slug: s.state for s in report.before}
    after_states = {s.slug: s.state for s in report.after}
    assert before_states == {"lane-a": "done", "lane-b": "working"}
    assert after_states == {"lane-a": "stopped", "lane-b": "working"}
    rendered = report.render()
    # "stopped" is itself a terminal state, so the lane stays counted as finished after --
    # the signal this run produced is that it is no longer a RESIDENT process, which
    # `stopped[0].ok` above is the actual proof of; the finished COUNT is unchanged by design.
    assert "1 finished before -> 1 finished after" in rendered


def test_stop_session_records_a_missing_job_id_as_SKIPPED_not_run():
    session = bj.LaneSession(slug="lane-x", job_id="", worktree="", state="ABSENT", live=False)
    outcome = bj.stop_session(
        session, run=lambda argv: (_ for _ in ()).throw(AssertionError("must not run")))
    assert outcome.ran is False
    assert not outcome.ok


def test_stop_session_records_a_nonzero_exit_as_not_ok():
    session = bj.LaneSession(slug="lane-x", job_id="j1", worktree="", state="done", live=False)
    outcome = bj.stop_session(
        session, run=lambda argv: subprocess.CompletedProcess(argv, 1, "", "no such job"))
    assert outcome.ran is True
    assert not outcome.ok
    assert outcome.returncode == 1


def test_stop_session_records_a_spawn_failure_rather_than_raising():
    session = bj.LaneSession(slug="lane-x", job_id="j1", worktree="", state="done", live=False)

    def boom(argv):
        raise OSError("claude not on PATH")

    outcome = bj.stop_session(session, run=boom)
    assert outcome.ran is True
    assert outcome.returncode is None
    assert not outcome.ok


# --- CLI -----------------------------------------------------------------------

def test_cli_dry_run_exits_0_and_prints_DRY_RUN(receipts, monkeypatch):
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")
    monkeypatch.setattr(bj._ds, "list_agents", lambda: [_entry("a1", "done")])

    result = CliRunner().invoke(bj.cli, ["run", "--batch", "B1", "--dry-run"])

    assert result.exit_code == 0, result.output
    assert "DRY RUN" in result.output


def test_cli_run_stops_the_finished_job_and_exits_0(receipts, monkeypatch):
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")
    reads = [[_entry("a1", "done")], [_entry("a1", "stopped")]]
    monkeypatch.setattr(bj._ds, "list_agents", lambda: reads.pop(0))
    monkeypatch.setattr(bj.subprocess, "run",
                        lambda *a, **k: subprocess.CompletedProcess(a, 0, "ok", ""))

    result = CliRunner().invoke(bj.cli, ["run", "--batch", "B1"])

    assert result.exit_code == 0, result.output
    assert "stopped lane-a" in result.output


def test_cli_run_exits_1_when_a_stop_fails(receipts, monkeypatch):
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")
    reads = [[_entry("a1", "done")], [_entry("a1", "done")]]
    monkeypatch.setattr(bj._ds, "list_agents", lambda: reads.pop(0))
    monkeypatch.setattr(bj.subprocess, "run",
                        lambda *a, **k: subprocess.CompletedProcess(a, 1, "", "no such job"))

    result = CliRunner().invoke(bj.cli, ["run", "--batch", "B1"])

    assert result.exit_code == 1


def test_cli_refuses_cleanly_on_an_unreadable_listing(receipts, monkeypatch):
    _write_job(receipts, job_id="a1", slug="lane-a", batch="B1")

    def boom():
        raise bj._ds.ListingUnreadable("hung")

    monkeypatch.setattr(bj._ds, "list_agents", boom)

    result = CliRunner().invoke(bj.cli, ["run", "--batch", "B1"])

    assert result.exit_code != 0
    assert "Refusing" in result.output or "could not be read" in result.output
