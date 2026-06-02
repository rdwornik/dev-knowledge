"""Unit tests for scripts/review_closures.py (ADR-70 Tier-1 reviewer-side gate).

Safety-critical: this is the first contract-driven backlog mutation. Tests cover
the re-verify gate (approved+evidenced -> close; unapproved -> untouched;
already-closed -> no-op; reverify-fail -> skip), exact-line removal, a
producer<->consumer format round-trip, and the real-git evidence check.
"""

import importlib.util
import shutil
import subprocess
from datetime import date
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rc = _load("review_closures")
pc = _load("propose_closures")

_BACKLOG = (
    "# .dev-knowledge BACKLOG\n\n## Big picture\n\nintro\n\n"
    "## Theme\n> As a dev, I want x.\n\n### Story\nSo that y.\n"
    "- [#5] [P2][M] alpha task · Done when: a · refs r1\n"
    "- [#6] [P3][S] beta task · Done when: b · refs r2\n"
    "- [#7] [P2][M] gamma task · Done when: c · refs scripts/audit.py\n"
)


def _alltrue(_sha):
    return True


def _allfalse(_sha):
    return False


# --- parse + round-trip -----------------------------------------------------

def test_parse_proposals_strong_and_weak():
    text = pc.render(
        {"5": [("a1b2c3d4e", "feat: x, closes [#5]")]},
        {"7": [("scripts/audit.py", "deadbeef0", "refactor")]},
        date(2026, 6, 2), "abcdef1234567", "fedcba9876543", 4,
        {"5": "alpha · Done when: a", "7": "gamma · Done when: c"},
    )
    p = rc.parse_proposals(text)
    assert p["head_commit"] == "abcdef1234567"
    assert p["strong"] == {"5": ["a1b2c3d4e"]}
    assert p["weak"] == {"7": [("scripts/audit.py", "deadbeef0")]}


def test_round_trip_no_candidates_parses_empty():
    text = pc.render({}, {}, date(2026, 6, 2), "abc1234", None, 3, {})
    p = rc.parse_proposals(text)
    assert p["strong"] == {} and p["weak"] == {}
    assert rc.candidate_count(p) == 0


# --- surface ----------------------------------------------------------------

def test_surface_line_present_with_candidates():
    p = {"strong": {"5": ["x"]}, "weak": {"7": [("f", "y")]}}
    line = rc.surface_line(p)
    assert "1 strong" in line and "1 weak" in line and "/review-closures" in line


def test_surface_line_silent_when_empty():
    assert rc.surface_line({"strong": {}, "weak": {}}) is None


# --- plan_closures gate -----------------------------------------------------

def _proposals(strong=None, weak=None):
    return {"head_commit": "h", "strong": strong or {}, "weak": weak or {}}


def _open_lines():
    return rc.open_task_lines(_BACKLOG)


def test_approved_strong_with_live_evidence_closes():
    prop = _proposals(strong={"5": ["a1b2c3d4e"]})
    out = rc.plan_closures(_BACKLOG, ["5"], prop, _open_lines(), _alltrue)
    assert [c["id"] for c in out["close"]] == ["5"]
    assert out["close"][0]["tier"] == "strong"
    assert out["close"][0]["line"].startswith("- [#5]")
    assert out["skip"] == []


def test_unapproved_id_is_untouched():
    # #6 is open and even proposed, but NOT in the approved list -> never closed
    prop = _proposals(strong={"5": ["a1b2c3d4e"], "6": ["b2c3d4e5f"]})
    out = rc.plan_closures(_BACKLOG, ["5"], prop, _open_lines(), _alltrue)
    assert [c["id"] for c in out["close"]] == ["5"]
    assert "6" not in [c["id"] for c in out["close"]]


def test_already_closed_id_is_skipped():
    # #99 not open in BACKLOG -> skip, never close
    prop = _proposals(strong={"99": ["a1b2c3d4e"]})
    out = rc.plan_closures(_BACKLOG, ["99"], prop, _open_lines(), _alltrue)
    assert out["close"] == []
    assert out["skip"][0]["id"] == "99"
    assert "not currently open" in out["skip"][0]["reason"]


def test_strong_reverify_fail_when_evidence_missing():
    prop = _proposals(strong={"5": ["a1b2c3d4e"]})
    out = rc.plan_closures(_BACKLOG, ["5"], prop, _open_lines(), _allfalse)
    assert out["close"] == []
    assert out["skip"][0]["id"] == "5"
    assert "no longer found" in out["skip"][0]["reason"]


def test_weak_approved_closes_without_evidence_requirement():
    # WEAK is the operator's judgment (typed #N); re-verify is open-check only
    prop = _proposals(weak={"7": [("scripts/audit.py", "deadbeef0")]})
    out = rc.plan_closures(_BACKLOG, ["7"], prop, _open_lines(), _allfalse)
    assert [c["id"] for c in out["close"]] == ["7"]
    assert out["close"][0]["tier"] == "weak"


def test_approved_but_unproposed_id_is_refused():
    prop = _proposals(strong={"5": ["a1b2c3d4e"]})
    out = rc.plan_closures(_BACKLOG, ["6"], prop, _open_lines(), _alltrue)
    assert out["close"] == []
    assert "not a proposed candidate" in out["skip"][0]["reason"]


# --- remove_task ------------------------------------------------------------

def test_remove_task_removes_exactly_one_line_and_preserves_rest():
    new_text, ok = rc.remove_task(_BACKLOG, "6")
    assert ok is True
    assert "- [#6]" not in new_text
    assert "- [#5]" in new_text and "- [#7]" in new_text          # gaps preserved
    assert new_text.count("\n") == _BACKLOG.count("\n") - 1        # exactly one line gone


def test_remove_task_absent_id_is_noop():
    new_text, ok = rc.remove_task(_BACKLOG, "404")
    assert ok is False
    assert new_text == _BACKLOG


# --- real-git evidence check ------------------------------------------------

@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_git_commit_exists_real_repo(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()

    def run(*a):
        subprocess.run(["git", "-C", str(repo), *a], check=True,
                       capture_output=True, text=True, encoding="utf-8")

    run("init", "-q")
    run("config", "user.email", "t@t.t")
    run("config", "user.name", "t")
    (repo / "f.txt").write_text("x\n", encoding="utf-8")
    run("add", "-A")
    run("commit", "-q", "-m", "seed, closes [#5]")
    sha = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                         capture_output=True, text=True, encoding="utf-8").stdout.strip()
    assert rc.git_commit_exists(repo, sha[:9]) is True
    assert rc.git_commit_exists(repo, "0000000deadbeef") is False


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_integration_full_done_items_leave_loop(tmp_path):
    """End-to-end: approve #5 -> closed (item gone + `closes [#5]` commit);
    #6/#7 unapproved -> untouched. The full Tier-1 close mechanism in a sandbox."""
    repo = tmp_path / "r"
    repo.mkdir()

    def run(*a, msg=None):
        return subprocess.run(["git", "-C", str(repo), *a], check=True,
                              capture_output=True, text=True, encoding="utf-8")

    run("init", "-q")
    run("config", "user.email", "t@t.t")
    run("config", "user.name", "t")
    backlog = repo / "BACKLOG.md"
    backlog.write_text(_BACKLOG, encoding="utf-8")
    run("add", "-A")
    run("commit", "-q", "-m", "chore: seed backlog")
    # a real closing commit for #5
    (repo / "work.txt").write_text("done\n", encoding="utf-8")
    run("add", "-A")
    run("commit", "-q", "-m", "feat: do the alpha work, closes [#5]")
    ev = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short=9", "HEAD"],
                        capture_output=True, text=True, encoding="utf-8").stdout.strip()

    proposals = rc.parse_proposals(pc.render(
        {"5": [(ev, "feat: do the alpha work, closes [#5]")]},
        {"7": [("scripts/audit.py", "deadbeef0", "refactor")]},
        date(2026, 6, 2), ev, None, 2,
        {"5": "alpha", "7": "gamma"},
    ))

    backlog_text = backlog.read_text(encoding="utf-8")
    open_lines = rc.open_task_lines(backlog_text)
    # operator approves ONLY #5
    out = rc.plan_closures(backlog_text, ["5"], proposals, open_lines,
                           lambda s: rc.git_commit_exists(repo, s))
    assert [c["id"] for c in out["close"]] == ["5"]

    # apply done-items-leave for the approved id, then commit with `closes [#5]`
    new_text, ok = rc.remove_task(backlog_text, out["close"][0]["id"])
    assert ok is True
    backlog.write_text(new_text, encoding="utf-8")
    run("add", "BACKLOG.md")
    run("commit", "-q", "-m", f"chore: retire #5 (ev {ev}), closes [#5]")

    final = backlog.read_text(encoding="utf-8")
    assert "- [#5]" not in final                      # approved item left the file
    assert "- [#6]" in final and "- [#7]" in final     # unapproved untouched
    head_msg = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%B"],
                              capture_output=True, text=True, encoding="utf-8").stdout
    assert "closes [#5]" in head_msg                   # forward-index for the closure
