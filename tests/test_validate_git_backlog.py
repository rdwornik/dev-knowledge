"""Tests for scripts/validate_git_backlog.py — #90 git↔backlog drift verifier.

Direction (a) STRONG-only (ADR-65): a `closes [#id]` commit anywhere in history
whose [#id] is still present (open) in BACKLOG.md is DRIFT — the closing commit
fired but the done item never left the file. Reuses propose_closures.find_strong
(the identical closes∩still-open core) — these tests exercise the orchestration
(full-history read + backlog parse + intersect) and the deployed audit check, not
the already-tested core.

(Direction (b) merged-arc→record is deferred to #90b — see the module docstring.)
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import validate_git_backlog as vgb  # noqa: E402
import audit as aud  # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")


def _run(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True, encoding="utf-8")


_MINI_BACKLOG = (
    "# R BACKLOG\n\n## Big picture\n\nintro\n\n"
    "## Theme\n> As a dev, I want x.\n\n### Story\nSo that y.\n"
    "- [#5] [P2][M] alpha · Done when: a · refs r1\n"
)


def _init_repo(tmp_path, backlog=_MINI_BACKLOG):
    repo = tmp_path / "r"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    (repo / "BACKLOG.md").write_text(backlog, encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "seed backlog")
    _run(repo, "branch", "-M", "main")     # deterministic default-branch name
    return repo


# --- reconcile: direction (a) orchestration over real git -------------------

@requires_git
def test_reconcile_flags_closed_but_present(tmp_path):
    # #5 is open in BACKLOG, and a commit says `closes [#5]` -> DRIFT (ADR-65).
    repo = _init_repo(tmp_path)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "feat: alpha done, closes [#5]")
    drift = vgb.reconcile(repo, repo / "BACKLOG.md")
    assert set(drift) == {"5"}
    sha, subject = drift["5"][0]          # {id: [(sha, subject), ...]}
    assert "closes [#5]" in subject


@requires_git
def test_reconcile_silent_when_closed_id_absent(tmp_path):
    # closes [#5] but #5 is NOT in BACKLOG (only #6) -> no drift (still-present guard).
    backlog = _MINI_BACKLOG.replace("[#5]", "[#6]")
    repo = _init_repo(tmp_path, backlog=backlog)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "feat: done, closes [#5]")
    assert vgb.reconcile(repo, repo / "BACKLOG.md") == {}


@requires_git
def test_reconcile_is_full_history_no_baseline(tmp_path):
    # the closing commit is EARLY; many commits follow. Full-history scan must still
    # surface it (proves no baseline window is applied to direction (a)).
    repo = _init_repo(tmp_path)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "feat: alpha done, closes [#5]")
    for i in range(5):
        (repo / f"later{i}.txt").write_text("x\n", encoding="utf-8")
        _run(repo, "add", "-A")
        _run(repo, "commit", "-q", "-m", f"chore: later {i}")
    drift = vgb.reconcile(repo, repo / "BACKLOG.md")
    assert "5" in drift


@requires_git
def test_reconcile_closes_in_merge_body_counted(tmp_path):
    # real closures often ride a merge body, not a conventional subject.
    repo = _init_repo(tmp_path)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "Merge feat/alpha — alpha arc\n\ncloses [#5]")
    drift = vgb.reconcile(repo, repo / "BACKLOG.md")
    assert "5" in drift


@requires_git
def test_reconcile_ignores_branch_internal_closes(tmp_path):
    # PRECISION (the #5 field-run false positive): a `closes [#5]` that lives only on a
    # feature branch (e.g. fixture/example text) must NOT fire — detection is --first-
    # parent (main-line only), so a closure must reach the merge spine to count.
    repo = _init_repo(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat/x")
    (repo / "fix.txt").write_text("x\n", encoding="utf-8")
    _run(repo, "add", "-A")
    # example/fixture text in a branch-internal commit body — not a real closure
    _run(repo, "commit", "-q", "-m", "test: fixture mentions closes [#5] as an example")
    _run(repo, "checkout", "-q", "main")
    # merge --no-ff with a subject that does NOT declare the close (the real shape here)
    _run(repo, "merge", "--no-ff", "-q", "-m", "Merge feat/x — fixture work", "feat/x")
    assert vgb.reconcile(repo, repo / "BACKLOG.md") == {}


@requires_git
def test_reconcile_main_line_merge_closes_still_fires(tmp_path):
    # the counterpart: a real `closes [#5]` carried on the merge commit (ship-time)
    # IS on the first-parent spine -> drift fires (proves the lever didn't over-cut).
    repo = _init_repo(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat/y")
    (repo / "y.txt").write_text("y\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "feat: do y")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "--no-ff", "-q", "-m", "Merge feat/y — y arc, closes [#5]", "feat/y")
    drift = vgb.reconcile(repo, repo / "BACKLOG.md")
    assert "5" in drift


@requires_git
def test_reconcile_bare_ref_is_not_drift(tmp_path):
    # a reworded-task commit referencing [#5] without `closes` is a touch, not a close.
    repo = _init_repo(tmp_path)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "docs: rework [#5] wording")
    assert vgb.reconcile(repo, repo / "BACKLOG.md") == {}


# --- deployed audit check: check_git_backlog_drift --------------------------

def test_check_skips_non_hub_repo(tmp_path):
    # ALL_CHECKS runs per-repo across the fleet; this check is hub-only.
    findings = aud.check_git_backlog_drift(tmp_path / "some-child")
    assert len(findings) == 1
    assert findings[0].check_name == "git_backlog_drift"
    assert findings[0].status == "pass"
    assert "hub-only" in findings[0].evidence


def test_check_warns_not_fails_on_drift(monkeypatch):
    # on the hub with drift -> WARN (informs, never blocks the audit-health gate).
    hub = Path(aud._REPO_ROOT)
    monkeypatch.setattr(aud._vgb, "reconcile",
                        lambda root, backlog: {"5": [("a1b2c3d4e", "feat: x, closes [#5]")]})
    findings = aud.check_git_backlog_drift(hub)
    assert len(findings) == 1
    assert findings[0].status == "warn"          # never "fail"
    assert "#5" in findings[0].evidence
    assert "|" not in findings[0].evidence        # sanitized for the audit table


def test_check_passes_when_clean(monkeypatch):
    hub = Path(aud._REPO_ROOT)
    monkeypatch.setattr(aud._vgb, "reconcile", lambda root, backlog: {})
    findings = aud.check_git_backlog_drift(hub)
    assert findings[0].status == "pass"


def test_check_failsoft_on_error(monkeypatch):
    # a git/parse hiccup must degrade to WARN, never raise (would wedge audit.py health).
    hub = Path(aud._REPO_ROOT)

    def _boom(root, backlog):
        raise RuntimeError("git exploded")

    monkeypatch.setattr(aud._vgb, "reconcile", _boom)
    findings = aud.check_git_backlog_drift(hub)
    assert findings[0].status == "warn"
    assert "git exploded" in findings[0].evidence or "degraded" in findings[0].evidence


# --- end-to-end: seeded drift fires through the REGISTERED check -------------

@requires_git
def test_e2e_seeded_drift_fires_through_registered_check(tmp_path, monkeypatch):
    # The #90 proof obligation: seed a closed-but-present id in a real git repo and
    # assert the check registered in ALL_CHECKS fires WARN — deployed, not just written.
    repo = _init_repo(tmp_path)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "feat: alpha done, closes [#5]")
    # make the tmp repo look like the hub so the hub-guard passes
    monkeypatch.setattr(aud, "_REPO_ROOT", str(repo))
    findings = aud.check_git_backlog_drift(repo)
    assert findings[0].status == "warn"
    assert "#5" in findings[0].evidence
    assert aud.check_git_backlog_drift in aud.ALL_CHECKS  # actually registered
