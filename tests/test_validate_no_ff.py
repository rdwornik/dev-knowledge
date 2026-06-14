"""Tests for scripts/validate_no_ff.py — #153 `--no-ff` merge guard.

The rule (core-invariants #5): every change goes branch → merge `--no-ff`; never
direct to main. A NON-merge commit on main's first-parent spine is the violation
signature — a direct commit OR a fast-forwarded feature commit. One precision
lever: an enforcement baseline (pre-guard / pre-Q9 history grandfathered). ADR-84
(Q9) REMOVED the former automation allowlist — the gate is now one rule (every
non-merge commit on main >= baseline is a violation). These tests exercise the
pure filter, the git orchestration (including the load-bearing FF-vs-`--no-ff`
distinction), and the deployed audit check (hub-only, WARN-not-FAIL,
one-finding-per-violation, fail-soft, e2e).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import validate_no_ff as vnf  # noqa: E402
import audit as aud  # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")


def _run(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True, encoding="utf-8")


def _commit(repo, msg, adate=None, fname="f.txt", content=None):
    """Stage a unique file and commit, optionally pinning the author/committer date."""
    (repo / fname).write_text(content if content is not None else msg, encoding="utf-8")
    _run(repo, "add", "-A")
    env = dict(os.environ)
    if adate:
        env["GIT_AUTHOR_DATE"] = adate
        env["GIT_COMMITTER_DATE"] = adate
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", msg],
                   check=True, capture_output=True, text=True, encoding="utf-8", env=env)


def _init_repo(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    # Root seed dated well before any test baseline -> always grandfathered.
    _commit(repo, "seed", adate="2026-06-01T00:00:00", fname="seed.txt")
    _run(repo, "branch", "-M", "main")  # deterministic default-branch name
    return repo


# --- pure filter: baseline cut, no exemptions (ADR-84 / Q9) ------------------

def test_filter_real_violation_kept():
    recs = [("a1b2c3d4e", "2026-06-12", "feat: oops direct on main", "")]
    assert vnf.filter_violations(recs, baseline="2026-06-11") == \
        [("a1b2c3d4e", "2026-06-12", "feat: oops direct on main")]


def test_filter_pre_baseline_grandfathered():
    recs = [("a1b2c3d4e", "2026-06-05", "feat: pre-rule direct commit", "")]
    assert vnf.filter_violations(recs, baseline="2026-06-11") == []


def test_filter_automation_subject_now_flagged():
    # ADR-84 (Q9) removed the exemption: a chore(routine/...) non-merge commit on
    # main at/after the baseline is NOW a violation (the writers no longer land here).
    recs = [("a1b2c3d4e", "2026-06-16", "chore(routine/fleet-audit): record baseline", "")]
    assert vnf.filter_violations(recs, baseline="2026-06-15") == \
        [("a1b2c3d4e", "2026-06-16", "chore(routine/fleet-audit): record baseline")]


def test_filter_automation_trailer_now_flagged():
    # The `Routine: <name>` body trailer is likewise no longer exempt.
    recs = [("a1b2c3d4e", "2026-06-16", "docs: nightly digest", "blah\n\nRoutine: nightly\n")]
    assert vnf.filter_violations(recs, baseline="2026-06-15") == \
        [("a1b2c3d4e", "2026-06-16", "docs: nightly digest")]


def test_filter_boundary_date_inclusive():
    # a commit AUTHORED exactly on the baseline date is in-scope (>= cut).
    recs = [("a1b2c3d4e", "2026-06-11", "feat: on the baseline day", "")]
    assert vnf.filter_violations(recs, baseline="2026-06-11") == \
        [("a1b2c3d4e", "2026-06-11", "feat: on the baseline day")]


# --- find_violations over real git ------------------------------------------

@requires_git
def test_direct_commit_after_baseline_flagged(tmp_path):
    repo = _init_repo(tmp_path)
    _commit(repo, "feat: direct on main", adate="2026-06-12T10:00:00", fname="a.txt")
    viol = vnf.find_violations(repo, baseline="2026-06-10")
    assert [v[2] for v in viol] == ["feat: direct on main"]


@requires_git
def test_no_ff_merge_not_flagged(tmp_path):
    # A proper --no-ff merge: the merge commit is excluded (--no-merges) and the
    # feature commit is off the first-parent spine -> no violation.
    repo = _init_repo(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat/x")
    _commit(repo, "feat: do x", adate="2026-06-12T10:00:00", fname="x.txt")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "--no-ff", "-q", "-m", "Merge feat/x — x arc", "feat/x")
    assert vnf.find_violations(repo, baseline="2026-06-10") == []


@requires_git
def test_fast_forward_merge_flagged(tmp_path):
    # The load-bearing case (#153a): a fast-forward merge replays the feature commit
    # ONTO main's first-parent spine with NO merge commit -> the guard must catch it.
    repo = _init_repo(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat/y")
    _commit(repo, "feat: do y (ff'd onto main)", adate="2026-06-12T10:00:00", fname="y.txt")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "--ff-only", "-q", "feat/y")  # fast-forward, no merge commit
    viol = vnf.find_violations(repo, baseline="2026-06-10")
    assert [v[2] for v in viol] == ["feat: do y (ff'd onto main)"]


@requires_git
def test_pre_baseline_grandfathered_e2e(tmp_path):
    repo = _init_repo(tmp_path)
    _commit(repo, "feat: early direct", adate="2026-06-05T10:00:00", fname="e.txt")
    assert vnf.find_violations(repo, baseline="2026-06-10") == []


@requires_git
def test_automation_now_flagged_e2e(tmp_path):
    # ADR-84 (Q9): a marker-carrying non-merge commit on main >= baseline is a real
    # violation now — the gate has no automation exemption (the writers moved off main).
    repo = _init_repo(tmp_path)
    _commit(repo, "chore(routine/fleet-audit): record baseline",
            adate="2026-06-16T10:00:00", fname="auto.txt")
    viol = vnf.find_violations(repo, baseline="2026-06-15")
    assert [v[2] for v in viol] == ["chore(routine/fleet-audit): record baseline"]


@requires_git
def test_missing_branch_failsoft(tmp_path):
    repo = _init_repo(tmp_path)
    assert vnf.find_violations(repo, branch="does-not-exist", baseline="2026-06-10") == []


# --- deployed audit check: check_no_ff_merges -------------------------------

def test_check_skips_non_hub_repo(tmp_path):
    findings = aud.check_no_ff_merges(tmp_path / "some-child")
    assert len(findings) == 1
    assert findings[0].check_name == "no_ff_merges"
    assert findings[0].status == "pass"
    assert "hub-only" in findings[0].evidence


def test_check_warns_not_fails_on_violation(monkeypatch):
    hub = Path(aud._REPO_ROOT)
    monkeypatch.setattr(aud._vnf, "find_violations",
                        lambda repo, **kw: [("a1b2c3d4e", "2026-06-12", "feat: x direct")])
    findings = aud.check_no_ff_merges(hub)
    assert len(findings) == 1
    assert findings[0].status == "warn"            # never "fail"
    assert "a1b2c3d4e" in findings[0].evidence
    assert "|" not in findings[0].evidence          # sanitized for the audit table


def test_check_passes_when_clean(monkeypatch):
    hub = Path(aud._REPO_ROOT)
    monkeypatch.setattr(aud._vnf, "find_violations", lambda repo, **kw: [])
    findings = aud.check_no_ff_merges(hub)
    assert findings[0].status == "pass"


def test_check_emits_one_finding_per_violation(monkeypatch):
    # Each violation is its own Finding so the #147 ship-gate dispositions them
    # independently (one matched token cannot suppress another). Teeth: re-aggregating
    # into one Finding makes len != 2 -> this reds.
    hub = Path(aud._REPO_ROOT)
    monkeypatch.setattr(aud._vnf, "find_violations", lambda repo, **kw: [
        ("a1b2c3d4e", "2026-06-12", "feat: x direct"),
        ("f9e8d7c6b", "2026-06-13", "fix: y ff-merged"),
    ])
    findings = aud.check_no_ff_merges(hub)
    assert len(findings) == 2
    assert all(f.status == "warn" for f in findings)
    assert {"a1b2c3d4e", "f9e8d7c6b"} <= {tok for f in findings for tok in f.evidence.split()}
    assert all("|" not in f.evidence for f in findings)


def test_check_failsoft_on_error(monkeypatch):
    # a git/parse hiccup must degrade to WARN, never raise (would wedge audit.py health).
    hub = Path(aud._REPO_ROOT)

    def _boom(repo, **kw):
        raise RuntimeError("git exploded")

    monkeypatch.setattr(aud._vnf, "find_violations", _boom)
    findings = aud.check_no_ff_merges(hub)
    assert findings[0].status == "warn"
    assert "git exploded" in findings[0].evidence or "degraded" in findings[0].evidence


@requires_git
def test_e2e_seeded_violation_fires_through_registered_check(tmp_path, monkeypatch):
    # Seed a real direct-to-main commit dated after the LIVE baseline and assert the
    # check registered in ALL_CHECKS fires WARN — deployed, not just written.
    # (Date must be >= the live BASELINE_DATE, bumped to the Q9 cutover by ADR-84.)
    repo = _init_repo(tmp_path)
    _commit(repo, "feat: oops direct on main", adate="2026-06-16T10:00:00", fname="a.txt")
    monkeypatch.setattr(aud, "_REPO_ROOT", str(repo))  # make tmp repo look like the hub
    findings = aud.check_no_ff_merges(repo)
    assert findings[0].status == "warn"
    assert "oops direct on main" in findings[0].evidence
    assert aud.check_no_ff_merges in aud.ALL_CHECKS  # actually registered
