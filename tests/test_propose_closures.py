"""Unit tests for scripts/propose_closures.py (ADR-70 Tier-1 closure detector).

Targets the pure detection core (no git, no I/O): STRONG/WEAK classification,
path extraction, precision guards, and the rendered artifact shape.
"""

import importlib.util
import shutil
import subprocess
from datetime import date
from pathlib import Path

import pytest

_P = Path(__file__).resolve().parent.parent / "scripts" / "propose_closures.py"


def _load():
    spec = importlib.util.spec_from_file_location("propose_closures", _P)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pc = _load()


def _commit(sha, subject, body="", files=None):
    return pc.Commit(sha, subject, body, files or [])


# --- STRONG -----------------------------------------------------------------

def test_strong_hit_when_closes_and_still_open():
    commits = [_commit("a1b2c3d4e", "chore: done, closes [#5]")]
    strong = pc.find_strong({"5", "6"}, commits)
    assert "5" in strong
    assert strong["5"] == [("a1b2c3d4e", "chore: done, closes [#5]")]


def test_strong_false_positive_avoided_when_id_not_open():
    # closes [#5] but #5 already removed from BACKLOG (not in open_ids) -> silent
    commits = [_commit("a1b2c3d4e", "chore: done, closes [#5]")]
    assert pc.find_strong({"6", "7"}, commits) == {}


def test_bare_id_without_closing_keyword_is_not_strong():
    # a reworded-task commit referencing [#5] without "closes" must not surface
    commits = [_commit("a1b2c3d4e", "docs: rework [#5] wording")]
    assert pc.find_strong({"5"}, commits) == {}


def test_closes_matches_in_body_too():
    commits = [_commit("ff00ff00f", "Merge branch", body="...\ncloses [#9]\n")]
    assert "9" in pc.find_strong({"9"}, commits)


# --- WEAK -------------------------------------------------------------------

def test_weak_hit_when_named_file_changed_without_closes():
    tasks = {"11": "Fix the thing · Done when: x · refs scripts/audit.py #11"}
    commits = [_commit("deadbeef0", "refactor audit", files=["scripts/audit.py"])]
    weak = pc.find_weak(tasks, commits, strong_ids=set())
    assert weak["11"] == [("scripts/audit.py", "deadbeef0", "refactor audit")]


def test_weak_precision_churn_file_excluded():
    # a task that names BACKLOG.md must not weak-fire on routine BACKLOG churn
    tasks = {"4": "groom · Done when: y · refs BACKLOG.md"}
    commits = [_commit("c0ffee123", "docs: groom", files=["BACKLOG.md"])]
    assert pc.find_weak(tasks, commits, strong_ids=set()) == {}


def test_weak_skipped_when_already_strong():
    tasks = {"11": "Fix · Done when: x · refs scripts/audit.py #11"}
    commits = [_commit("abc123def", "fix, closes [#11]", files=["scripts/audit.py"])]
    # commit closes #11 -> it is STRONG; must not also appear as WEAK
    assert pc.find_weak(tasks, commits, strong_ids={"11"}) == {}


def test_weak_no_match_when_unrelated_file_changed():
    tasks = {"11": "Fix · Done when: x · refs scripts/audit.py #11"}
    commits = [_commit("aaa111bbb", "edit readme", files=["docs/decisions/README.md"])]
    assert pc.find_weak(tasks, commits, strong_ids=set()) == {}


# --- path extraction --------------------------------------------------------

def test_task_paths_extracts_repo_relative_only():
    text = "do x · refs scripts/audit.py #11, ADR-35, protocols/PLAYBOOK.md"
    assert pc.task_paths(text) == {"scripts/audit.py", "protocols/PLAYBOOK.md"}


def test_task_paths_ignores_bare_ref_tokens():
    # no slash, or no file extension -> not a path token
    assert pc.task_paths("refs coherence-audit HK-1, ADR-59, durability-audit J4") == set()


# --- render -----------------------------------------------------------------

def test_render_no_candidates_is_observable():
    out = pc.render({}, {}, date(2026, 6, 2), "abc1234", None, 3, {})
    assert "No closures detected" in out
    assert "head_commit: abc1234" in out


def test_render_strong_lists_id_and_evidence():
    strong = {"5": [("a1b2c3d4e", "chore: closes [#5]")]}
    tasks = {"5": "Wire the thing · Done when: x · refs y"}
    out = pc.render(strong, {}, date(2026, 6, 2), "head999", "since111", 4, tasks)
    assert "STRONG" in out
    assert "**#5**" in out
    assert "Wire the thing" in out
    assert "a1b2c3d4" in out  # short sha in evidence


def test_render_weak_section_present_when_weak_only():
    weak = {"11": [("scripts/audit.py", "deadbeef0", "refactor")]}
    tasks = {"11": "Fix audit · Done when: x"}
    out = pc.render({}, weak, date(2026, 6, 2), "h", None, 2, tasks)
    assert "WEAK" in out
    assert "scripts/audit.py" in out
    assert "STRONG" not in out


# --- backlog adapter --------------------------------------------------------

def test_open_tasks_from_backlog_reuses_validate_backlog():
    backlog = (
        "# .dev-knowledge BACKLOG\n\n## Big picture\n\nintro\n\n"
        "## Theme\n> As a dev, I want x.\n\n### Story\nSo that y.\n"
        "- [#5] [P2][M] do a thing · Done when: done · refs z\n"
    )
    vb = pc._load_validate_backlog()
    open_tasks = pc.open_tasks_from_backlog(backlog, vb.parse)
    assert "5" in open_tasks
    assert "do a thing" in open_tasks["5"]


# --- end-to-end through the real git adapter --------------------------------

def _run(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True, encoding="utf-8")


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_integration_strong_and_weak_through_real_git(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    # base commit
    (repo / "seed.txt").write_text("x\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "chore: seed")
    base = pc.git_head(repo)
    # commit A: closing commit for #5
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "feat: do it, closes [#5]")
    # commit B: closing commit for #6 (which we will treat as already removed)
    (repo / "b.txt").write_text("b\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "feat: other, closes [#6]")
    # commit C: touches a file an open task names, no closes -> WEAK
    (repo / "pkg").mkdir()
    (repo / "pkg" / "mod.py").write_text("print(1)\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "refactor: rework pkg")

    commits = pc.git_log_commits(repo, f"{base}..HEAD")
    assert len(commits) == 3

    # only #5 is still open; #6 was removed from BACKLOG
    open_tasks = {
        "5": "do it · Done when: x · refs a.txt",
        "7": "rework · Done when: y · refs pkg/mod.py",
    }
    strong = pc.find_strong(set(open_tasks), commits)
    assert set(strong) == {"5"}            # #5 surfaced (closes + still open)
    assert "6" not in strong               # #6 closed but not open -> not surfaced

    weak = pc.find_weak(open_tasks, commits, set(strong))
    assert set(weak) == {"7"}              # pkg/mod.py changed, no closes -> WEAK
    assert weak["7"][0][0] == "pkg/mod.py"
