"""Tests for [#460]'s two legs: the mechanized push, and the replication-divergence alarm.

The defect being closed: ADR-80 promises a DURABLE record, `_commit_routine_outputs` writes it
to a local branch, and the push that made it durable was a ONE-SHOT MANUAL act owned only by
[#254] -- a row that closed on an existence-shaped Done-when ("origin/... exists and tracks")
which a single push satisfied. Nothing owned a RECURRING push, so replication died on
2026-07-16 and 51 commits accumulated on one disk, unnoticed for 16 days.

So the two legs are tested for the properties that failure mode demands:
  * the push is part of the act that creates the commit, not a separate organ that can die
    independently (which is exactly how the manual push died);
  * its failure is LOUD -- this whole class is silent success theater;
  * and the alarm is the backstop that notices when the loud failure was nonetheless missed,
    because a push can only shout at the moment it fails, while divergence PERSISTS.
"""

import logging
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest

import audit as a


def _git(*args, cwd, env=None):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, env=env)


@pytest.fixture
def repo_with_remote(tmp_path):
    """A real repo whose `automation/fleet-audit` branch tracks a bare remote.

    Real git, not a mock: the alarm reads ref topology, and a mock would assert our own
    assumptions about rev-list rather than git's behaviour.
    """
    remote = tmp_path / "remote.git"
    work = tmp_path / "work"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    subprocess.run(["git", "init", "-q", str(work)], check=True)
    _git("config", "user.email", "t@t", cwd=work)
    _git("config", "user.name", "t", cwd=work)
    _git("remote", "add", "origin", str(remote), cwd=work)

    (work / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    _git("add", "-A", cwd=work)
    _git("commit", "-q", "--no-verify", "-m", "seed", cwd=work)
    _git("branch", "-M", "automation/fleet-audit", cwd=work)
    _git("push", "-q", "origin", "automation/fleet-audit", cwd=work)
    return work


def _advance(work, n):
    """Add n commits to the local branch WITHOUT pushing -- i.e. create replication lag."""
    for i in range(n):
        (work / f"day{i}.md").write_text(f"baseline {i}\n", encoding="utf-8", newline="\n")
        _git("add", "-A", cwd=work)
        _git("commit", "-q", "--no-verify", "-m", f"record day {i}", cwd=work)


# --------------------------------------------------------------------------- pure classifier


def test_classifier_is_pure_and_graduated():
    """0 ahead is durable; a day or two is a transient push failure; more is a real outage."""
    assert a.classify_replication_lag(0)[0] == "pass"
    assert a.classify_replication_lag(1)[0] == "warn"
    assert a.classify_replication_lag(a.REPLICATION_LAG_FAIL_AFTER)[0] == "warn"
    assert a.classify_replication_lag(a.REPLICATION_LAG_FAIL_AFTER + 1)[0] == "fail"
    # the witnessed real number
    assert a.classify_replication_lag(51)[0] == "fail"


def test_classifier_evidence_is_cp1252_safe():
    """ASCII discipline: [#470] is an open row about a glyph crashing a cp1252 console."""
    for n in (0, 1, 4, 51):
        _status, evidence = a.classify_replication_lag(n)
        evidence.encode("cp1252")  # raises if a non-cp1252 glyph slipped in


# --------------------------------------------------------------------------- the alarm


def test_alarm_is_green_when_origin_is_current(repo_with_remote, monkeypatch):
    monkeypatch.setattr(a, "_REPO_ROOT", repo_with_remote)
    findings = a.check_fleet_audit_replication(repo_with_remote)
    assert [f.status for f in findings] == ["pass"], findings


def test_alarm_fires_on_the_witnessed_divergence(repo_with_remote, monkeypatch):
    """The 2026-07-16 condition: local ahead, origin stale, nothing complaining."""
    monkeypatch.setattr(a, "_REPO_ROOT", repo_with_remote)
    _advance(repo_with_remote, a.REPLICATION_LAG_FAIL_AFTER + 2)

    findings = a.check_fleet_audit_replication(repo_with_remote)
    assert [f.status for f in findings] == ["fail"], findings
    assert "ahead" in findings[0].evidence.lower()


def test_alarm_is_hub_only(tmp_path, monkeypatch):
    """Enforcement organs are not homogeneous -- the fleet-audit branch is hub machinery.

    Keying off anything else would manufacture a fleet gap on consumers that have no such
    branch and are not supposed to.
    """
    monkeypatch.setattr(a, "_REPO_ROOT", tmp_path / "hub")
    findings = a.check_fleet_audit_replication(tmp_path / "not-the-hub")
    assert [f.status for f in findings] == ["n/a"], findings


def test_alarm_degrades_gracefully_without_the_branch(tmp_path, monkeypatch):
    """No branch at all is not a failure -- it is nothing to replicate."""
    work = tmp_path / "bare-repo"
    subprocess.run(["git", "init", "-q", str(work)], check=True)
    monkeypatch.setattr(a, "_REPO_ROOT", work)
    findings = a.check_fleet_audit_replication(work)
    assert [f.status for f in findings] == ["n/a"], findings


def test_alarm_is_registered_in_all_checks():
    assert a.check_fleet_audit_replication in a.ALL_CHECKS


# --------------------------------------------------------------------------- the push leg


def test_push_succeeds_and_clears_the_lag(repo_with_remote, monkeypatch):
    monkeypatch.setattr(a, "_REPO_ROOT", repo_with_remote)
    _advance(repo_with_remote, 3)
    assert a.check_fleet_audit_replication(repo_with_remote)[0].status == "warn"

    ok, detail = a._push_routine_branch(repo_with_remote)
    assert ok, detail
    assert a.check_fleet_audit_replication(repo_with_remote)[0].status == "pass"


def test_push_failure_is_LOUD_not_silent(repo_with_remote, monkeypatch, caplog):
    """The defining property. A silent push failure is how this defect class survives.

    logger.error, not warning: the surrounding writer is deliberately fail-soft (it must never
    break the routine), so without an explicit severity bump the replication failure would be
    indistinguishable from the routine's ordinary skips.
    """
    monkeypatch.setattr(a, "_REPO_ROOT", repo_with_remote)
    _git("remote", "set-url", "origin", str(repo_with_remote / "does-not-exist.git"), cwd=repo_with_remote)
    _advance(repo_with_remote, 1)

    with caplog.at_level(logging.ERROR):
        ok, _detail = a._push_routine_branch(repo_with_remote)

    assert ok is False
    errors = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert errors, "push failure logged nothing at ERROR -- it is silent, which is the defect"
    assert any("replication" in r.getMessage().lower() for r in errors), \
        [r.getMessage() for r in errors]


def test_push_never_raises_so_the_routine_cannot_be_broken_by_it(repo_with_remote, monkeypatch):
    """Loud must not mean fatal: the writer stays crash-safe, the alarm carries persistence."""
    monkeypatch.setattr(a, "_REPO_ROOT", repo_with_remote)
    _git("remote", "remove", "origin", cwd=repo_with_remote)
    ok, detail = a._push_routine_branch(repo_with_remote)  # must not raise
    assert ok is False and detail


def test_writer_calls_the_push_leg(monkeypatch):
    """Placement contract: the push belongs to the act that CREATES the commit.

    A separate scheduler leg is a second organ that can die independently -- which is exactly
    how the manual push died. This pins the co-location so a refactor cannot quietly split
    them back apart.
    """
    import inspect

    src = inspect.getsource(a._commit_routine_outputs)
    assert "_push_routine_branch" in src, (
        "_commit_routine_outputs does not call the push leg -- replication is once again a "
        "separate organ that can die on its own, which is [#460]'s root cause"
    )
