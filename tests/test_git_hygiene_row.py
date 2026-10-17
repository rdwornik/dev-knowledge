"""AMEND-1 (2026-10-17): the `git_hygiene` preflight row -- no cut on a dirty git.

RED-first: written and watched to fail before `_row_git_hygiene` existed. The row FAILs when,
local or on origin, any branch other than `main` and the allow-listed protected branches
exists, or any linked worktree exists. The allow-list is data (`ecosystem/git-hygiene-
allowlist.yaml`), each exception naming its owner.
"""
from __future__ import annotations

import subprocess

import pytest

import yaml

import gen_handoff as gh


_REAL_ROW = gh._row_git_hygiene     # captured at import, before conftest's autouse stub runs


@pytest.fixture(autouse=True)
def _real_row(monkeypatch):
    monkeypatch.setattr(gh, "_row_git_hygiene", _REAL_ROW)


def _repo(tmp_path, extra_allow=()):
    repo = tmp_path / "hyg"
    (repo / "ecosystem").mkdir(parents=True)
    entries = "".join(f"  - name: {n}\n    owner: '{o}'\n" for n, o in extra_allow)
    (repo / "ecosystem" / "git-hygiene-allowlist.yaml").write_text(
        "branches:\n" + entries if entries else "branches: []\n", encoding="utf-8")
    return repo


def _stub(monkeypatch, *, worktrees=(), local=("main",), remote=("main",)):
    monkeypatch.setattr(gh, "_linked_worktrees", lambda _r: list(worktrees))
    monkeypatch.setattr(gh, "_git_hygiene_branches",
                        lambda _r: (list(local), None if remote is None else list(remote)))


def test_git_hygiene_is_a_blocking_row_that_runs_at_batch_close():
    assert "git_hygiene" in gh.PREFLIGHT_ROW_NAMES
    assert "git_hygiene" not in gh.PREFLIGHT_NON_BLOCKING_ROWS
    assert "git_hygiene" not in gh.TRIAL_CUT_EXCLUDED_ROWS


def test_a_stray_local_branch_fails(tmp_path, monkeypatch):
    _stub(monkeypatch, local=("main", "worktree-stray"))
    row = gh._row_git_hygiene(_repo(tmp_path))
    assert row.failed, row.render()
    assert "worktree-stray" in row.detail


def test_a_stray_origin_branch_fails(tmp_path, monkeypatch):
    _stub(monkeypatch, remote=("main", "chore/old"))
    row = gh._row_git_hygiene(_repo(tmp_path))
    assert row.failed and "origin/chore/old" in row.detail


def test_a_linked_worktree_fails(tmp_path, monkeypatch):
    _stub(monkeypatch, worktrees=("/x/.claude/worktrees/w",))
    row = gh._row_git_hygiene(_repo(tmp_path))
    assert row.failed and "/x/.claude/worktrees/w" in row.detail


def test_the_worktree_running_the_preflight_is_not_a_stray(tmp_path, monkeypatch):
    repo = _repo(tmp_path)
    _stub(monkeypatch, worktrees=(str(repo), "/x/.claude/worktrees/other"))
    row = gh._row_git_hygiene(repo)
    assert row.failed and "/x/.claude/worktrees/other" in row.detail
    assert str(repo) not in row.detail
    _stub(monkeypatch, worktrees=(str(repo),))
    assert gh._row_git_hygiene(repo).status == gh.PREFLIGHT_PASS


def test_the_branch_checked_out_in_the_running_worktree_is_not_a_stray(tmp_path, monkeypatch):
    """The cut is committed on the session's own cut branch (operator, 2026-10-17: 'your own
    cut worktree until you end'), so that branch -- local and its origin twin -- is not trash."""
    repo = _repo(tmp_path)
    _stub(monkeypatch, local=("main", "worktree-cut-x"), remote=("main", "worktree-cut-x"))
    monkeypatch.setattr(gh, "_git_current_branch", lambda _r: "worktree-cut-x")
    assert gh._row_git_hygiene(repo).status == gh.PREFLIGHT_PASS
    _stub(monkeypatch, local=("main", "worktree-cut-x", "other"), remote=("main", "other"))
    row = gh._row_git_hygiene(repo)
    assert row.failed and "other" in row.detail and "worktree-cut-x" not in row.detail


def test_an_allow_listed_branch_with_an_owner_passes(tmp_path, monkeypatch):
    _stub(monkeypatch, local=("main", "automation/fleet-audit"),
          remote=("main", "automation/fleet-audit"))
    row = gh._row_git_hygiene(_repo(tmp_path, [("automation/fleet-audit", "audit.py")]))
    assert row.status == gh.PREFLIGHT_PASS, row.render()


def test_an_allow_list_entry_without_an_owner_is_not_an_exception(tmp_path, monkeypatch):
    _stub(monkeypatch, local=("main", "automation/fleet-audit"))
    assert gh._row_git_hygiene(_repo(tmp_path, [("automation/fleet-audit", "")])).failed


def test_an_unreadable_origin_fails_closed(tmp_path, monkeypatch):
    _stub(monkeypatch, remote=None)
    assert gh._row_git_hygiene(_repo(tmp_path)).failed


def test_a_clean_git_passes(tmp_path, monkeypatch):
    _stub(monkeypatch)
    assert gh._row_git_hygiene(_repo(tmp_path)).status == gh.PREFLIGHT_PASS


def test_a_fixture_repo_with_one_stray_branch_fails_end_to_end(tmp_path):
    """The real git path (no seam stubbed): a bare origin + a clone carrying one stray branch."""
    origin = tmp_path / "origin.git"
    work = tmp_path / "work"
    run = lambda *a, cwd=work: subprocess.run(  # noqa: E731
        ["git", *a], cwd=str(cwd), check=True, capture_output=True, text=True)
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(work)], check=True)
    run("config", "user.email", "t@t")
    run("config", "user.name", "t")
    (work / "ecosystem").mkdir()
    (work / "ecosystem" / "git-hygiene-allowlist.yaml").write_text("branches: []\n")
    run("add", "-A")
    run("commit", "-q", "-m", "init")
    run("remote", "add", "origin", str(origin))
    run("push", "-q", "origin", "main")
    assert gh._row_git_hygiene(work).status == gh.PREFLIGHT_PASS
    run("branch", "stray")
    row = gh._row_git_hygiene(work)
    assert row.failed and "stray" in row.detail


def test_the_committed_allow_list_names_an_owner_for_every_exception():
    data = yaml.safe_load((gh._REPO_ROOT / "ecosystem" / "git-hygiene-allowlist.yaml")
                          .read_text(encoding="utf-8"))
    names = {e["name"] for e in data["branches"]}
    assert "automation/fleet-audit" in names
    assert "main" not in names
    assert all(str(e.get("owner", "")).strip() for e in data["branches"])
