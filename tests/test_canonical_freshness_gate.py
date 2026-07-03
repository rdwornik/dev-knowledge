"""Tests for scripts/canonical_freshness_gate.py — the single-sourced freshness gate that the
enforcement-mesh carrier deploys consumer-local (#236). The hub audit leg's behaviour is covered
by test_audit.py's freshness tests (they now flow through this module's `evaluate`); this file
covers the CONSUMER surface: the pure `evaluate` contract, the `__main__` gate exit codes (FAIL
-> exit 1 blocks a commit), and git-toplevel-first root resolution.
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import canonical_freshness_gate as cfg

_GATE = Path(__file__).resolve().parent.parent / "scripts" / "canonical_freshness_gate.py"


def _doc(repo: Path, name: str, reviewed: str | None) -> None:
    fm = "---\n" + (f"last_reviewed: {reviewed}\n" if reviewed else "") + "---\n\n# body\n"
    (repo / name).write_text(fm, encoding="utf-8")


def _git(repo: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


# --- pure evaluate() contract (inject git_date_fn so no real git needed) -----

def test_evaluate_a2_fail_when_reviewed_predates_edit():
    reviewed_older = lambda _rp, _fn: date(2026, 7, 2)  # noqa: E731 — "last edit" newer than stamp
    fails, warns = cfg.evaluate(
        _mk_only("CLAUDE.md"), ["CLAUDE.md"],
        parse_fn=lambda _t: date(2026, 6, 2), git_date_fn=reviewed_older, today=date(2026, 7, 3))
    assert len(fails) == 1 and "predates last edit" in fails[0]
    assert warns == []


def test_evaluate_pass_when_reviewed_not_before_edit():
    fails, warns = cfg.evaluate(
        _mk_only("CLAUDE.md"), ["CLAUDE.md"],
        parse_fn=lambda _t: date(2026, 7, 2), git_date_fn=lambda _rp, _fn: date(2026, 7, 2),
        today=date(2026, 7, 3))
    assert fails == [] and warns == []


def test_evaluate_a1_warn_when_stale_by_calendar():
    fails, warns = cfg.evaluate(
        _mk_only("CLAUDE.md"), ["CLAUDE.md"],
        parse_fn=lambda _t: date(2026, 1, 1), git_date_fn=lambda _rp, _fn: None,  # no git -> no A2
        today=date(2026, 7, 3))
    assert fails == [] and len(warns) == 1 and "cadence" in warns[0]


def test_evaluate_missing_stamp_warns():
    fails, warns = cfg.evaluate(
        _mk_only("CLAUDE.md"), ["CLAUDE.md"],
        parse_fn=lambda _t: None, git_date_fn=lambda _rp, _fn: None, today=date(2026, 7, 3))
    assert fails == [] and len(warns) == 1 and "no parseable last_reviewed" in warns[0]


def test_evaluate_absent_file_skipped(tmp_path):
    fails, warns = cfg.evaluate(tmp_path, ["DOES_NOT_EXIST.md"])
    assert fails == [] and warns == []


def _mk_only(name: str, tmp=Path):  # tiny helper: a dir that "has" the named file
    import tempfile
    d = Path(tempfile.mkdtemp())
    (d / name).write_text("x", encoding="utf-8")
    return d


# --- the __main__ gate: FAIL -> exit 1 (blocks a commit), fresh -> exit 0 -----

def _run_gate(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(_GATE)], cwd=str(repo),
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    return repo


def test_gate_exits_1_on_genuine_a2_stale(tmp_path):
    """TEETH: a doc committed today with an old last_reviewed -> A2 FAIL -> exit 1 (blocks)."""
    repo = _init_repo(tmp_path)
    _doc(repo, "CLAUDE.md", "2020-01-01")  # stamp far older than the commit date (today)
    _git(repo, "add", "CLAUDE.md")
    _git(repo, "commit", "-q", "-m", "add stale CLAUDE.md")
    r = _run_gate(repo)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "FAIL" in r.stdout and "CLAUDE.md" in r.stdout


def test_gate_exits_0_when_fresh(tmp_path):
    """A doc whose last_reviewed == its commit date is fresh -> exit 0 (no block)."""
    repo = _init_repo(tmp_path)
    _doc(repo, "CLAUDE.md", date.today().isoformat())
    _git(repo, "add", "CLAUDE.md")
    _git(repo, "commit", "-q", "-m", "add fresh CLAUDE.md")
    r = _run_gate(repo)
    assert r.returncode == 0, r.stdout + r.stderr


# --- root resolution: git-toplevel-first (validity of the deployed gate + the fire) ----

def test_resolve_root_prefers_git_toplevel(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    # even with a MISLEADING CLAUDE_PROJECT_DIR set, git-toplevel (from cwd) wins
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "elsewhere"))
    assert cfg._resolve_repo_root().resolve() == repo.resolve()
