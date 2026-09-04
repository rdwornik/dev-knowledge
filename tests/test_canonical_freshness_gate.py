"""Tests for scripts/canonical_freshness_gate.py — the single-sourced freshness gate that the
enforcement-mesh carrier deploys consumer-local (#236). The hub audit leg's behaviour is covered
by test_audit.py's freshness tests (they now flow through this module's `evaluate`); this file
covers the CONSUMER surface: the pure `evaluate` contract, the `__main__` gate exit codes (FAIL
-> exit 1 blocks a commit), and git-toplevel-first root resolution.
"""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path


import canonical_freshness_gate as cfg

_GATE = Path(__file__).resolve().parent.parent / "scripts" / "canonical_freshness_gate.py"


def _doc(repo: Path, name: str, reviewed: str | None) -> None:
    fm = "---\n" + (f"last_reviewed: {reviewed}\n" if reviewed else "") + "---\n\n# body\n"
    (repo / name).parent.mkdir(parents=True, exist_ok=True)
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


def test_evaluate_absent_file_fails(tmp_path):
    """Z-G4 [#621] lane-g-621-c7 closure 3: an absent PRESENCE-REQUIRED member FAILs.

    NARROWED at integration (terra P1, 2026-09-03) from "any registry member" to "a member whose
    presence this corpus requires". The original name was a synthetic `DOES_NOT_EXIST.md`, which
    is in no corpus at all — so it exercised the branch that now belongs to presence-OPTIONAL
    entries and would have gone green against the wrong half of the split. `CLAUDE.md` is in
    `CANONICAL_MANDATORY`, so this asserts the FAIL where Z-G4 actually bites; the optional half
    is pinned separately by
    `test_an_absent_OPTIONAL_file_is_reported_not_fatal_because_this_gate_ships_to_consumers`.
    """
    fails, warns = cfg.evaluate(tmp_path, ["CLAUDE.md"])
    assert warns == []
    assert len(fails) == 1 and "CLAUDE.md" in fails[0]


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
    """Every registered file present and fresh -> exit 0 (no block).

    [#621] lane-g-621-c7 closure 3: absence now FAILs, so ALL of DEFAULT_FRESHNESS_FILES
    must be declared present here, not just the one file this test is really about
    -- otherwise every OTHER member's absence would itself FAIL the gate.
    """
    repo = _init_repo(tmp_path)
    for name in cfg.DEFAULT_FRESHNESS_FILES:
        _doc(repo, name, date.today().isoformat())
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "add all freshness-gated files, all fresh")
    r = _run_gate(repo)
    assert r.returncode == 0, r.stdout + r.stderr


# --- root resolution: git-toplevel-first (validity of the deployed gate + the fire) ----

def test_resolve_root_prefers_git_toplevel(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    # even with a MISLEADING CLAUDE_PROJECT_DIR set, git-toplevel (from cwd) wins
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "elsewhere"))
    assert cfg._resolve_repo_root().resolve() == repo.resolve()


def _stamped(p, when="2099-01-01"):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"---\nlast_reviewed: {when}\n---\n\n# doc\n", encoding="utf-8", newline="\n")


def test_an_absent_OPTIONAL_file_is_reported_not_fatal_because_this_gate_ships_to_consumers(
        tmp_path):
    """terra P1, 2026-09-03 — caught before merge, with the blast radius measured.

    This gate is BYTE-COPIED into every consumer repo as a pre-commit hook, and
    `DEFAULT_FRESHNESS_FILES` registers two documents no consumer carries. Measured against the
    three live consumers on 2026-09-03: corp-monorepo, ai-council and win-tooling each lack BOTH
    `protocols/ESSENTIALS.md` and `docs/handoffs/README.md`. An unconditional absence-FAIL blocks
    every commit in all three, permanently.

    This is not a weakening of Z-G4. `canonical_docs` puts `ESSENTIALS` in `CANONICAL_OPTIONAL`
    and states presence is required only for `CANONICAL_MANDATORY`; for an optional document
    absent IS the ground truth, not an unmeasurable one. The absence is still REPORTED — Z-G4's
    real target is silence, not non-fatality.
    """
    from datetime import date
    for name in ("ARCHITECTURE.md", "CLAUDE.md", "CONTRIBUTING.md"):
        _stamped(tmp_path / name)
    # neither optional file exists — the measured consumer shape

    fails, warns = cfg.evaluate(tmp_path, git_date_fn=lambda r, f: None,
                                today=date(2026, 9, 3))[:2]
    assert fails == [], fails
    assert any("ESSENTIALS" in w and "absent" in w for w in warns), warns
    assert any("handoffs/README" in w and "absent" in w for w in warns), warns


def test_an_absent_REQUIRED_file_still_FAILS(tmp_path):
    """The other half: Z-G4 keeps its teeth where the corpus requires the file."""
    from datetime import date
    for name in ("ARCHITECTURE.md", "CONTRIBUTING.md"):
        _stamped(tmp_path / name)
    # CLAUDE.md is presence-REQUIRED and missing
    fails, _ = cfg.evaluate(tmp_path, git_date_fn=lambda r, f: None,
                            today=date(2026, 9, 3))[:2]
    assert any(f.startswith("CLAUDE.md") and "absent" in f for f in fails), fails


def test_presence_required_is_derived_from_the_registry_not_retyped():
    """A second hand-typed list is how the two drift; the hub path derives it."""
    assert set(cfg.PRESENCE_REQUIRED) <= set(cfg.DEFAULT_FRESHNESS_FILES)
    assert "protocols/ESSENTIALS.md" not in cfg.PRESENCE_REQUIRED
    assert "CLAUDE.md" in cfg.PRESENCE_REQUIRED
