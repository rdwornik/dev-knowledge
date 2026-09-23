"""Tests for `scripts/worktree_occupancy.py` -- the four-leg occupancy predicate (RECON s5.3).

WHY FOUR LEGS AND NOT ONE: on 2026-09-20 the four instruments DISAGREED. Two empty husk
directories sat under `.claude/worktrees/` that `git worktree list` had forgotten, and a second
`--bg` job entered a tree a live session held, 70 seconds after the first. Each test below
isolates ONE leg, because a predicate that only ever fires on all four together proves nothing
about any of them -- and the husk-only case is the one no git command can see.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

import worktree_occupancy as wo   # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

SLUG = "lane-l2-dispatch-guards"


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          encoding="utf-8", check=True)
    return proc.stdout


@pytest.fixture()
def repo(tmp_path):
    r = tmp_path / "hub"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    _git(r, "config", "user.email", "t@example.invalid")
    _git(r, "config", "user.name", "t")
    (r / "f.txt").write_text("x", encoding="utf-8")
    _git(r, "add", "f.txt")
    _git(r, "commit", "-q", "-m", "init")
    return r


def _session(repo: Path, slug: str, status: str = "busy") -> dict:
    return {"id": "abcd1234", "cwd": str(repo / ".claude" / "worktrees" / slug),
            "kind": "background", "status": status, "state": "working"}


# --- a free slug passes all four legs -----------------------------------------------------------

@requires_git
def test_a_free_slug_passes_all_four_legs(repo):
    res = wo.check(SLUG, repo, sessions=[])
    assert res.fired == ()
    assert res.occupied is False
    assert set(res.legs) == {"worktree", "directory", "branch", "session"}
    assert not any(res.legs.values())


@requires_git
def test_a_free_slug_ignores_unrelated_sessions_and_slugs(repo):
    """A sibling lane, the hub root and a slug that merely SHARES A PREFIX must not fire."""
    other = [_session(repo, SLUG + "-2"), _session(repo, "lane-l3-organ-truth"),
             {"cwd": str(repo), "status": "busy"}]
    (repo / ".claude" / "worktrees" / (SLUG + "-2")).mkdir(parents=True)
    _git(repo, "branch", "worktree-" + SLUG + "-2")
    assert wo.check(SLUG, repo, sessions=other).occupied is False


# --- each leg refuses on its own ----------------------------------------------------------------

@requires_git
def test_leg_registered_worktree_alone_refuses(repo):
    wt = repo / ".claude" / "worktrees" / SLUG
    _git(repo, "worktree", "add", "-q", "--detach", str(wt))
    shutil.rmtree(wt)          # git still registers it (prunable) -- the directory is gone
    res = wo.check(SLUG, repo, sessions=[])
    assert res.fired == ("worktree",)
    assert res.occupied


@requires_git
def test_leg_directory_alone_refuses_the_husk_case(repo):
    """THE LEG THAT MATTERS: an empty directory git has forgotten. `git worktree list` is
    clean, no branch exists, no session is live -- only the directory says occupied."""
    (repo / ".claude" / "worktrees" / SLUG).mkdir(parents=True)
    assert SLUG not in _git(repo, "worktree", "list")
    res = wo.check(SLUG, repo, sessions=[])
    assert res.fired == ("directory",)
    assert res.occupied


@requires_git
def test_leg_existing_branch_alone_refuses(repo):
    _git(repo, "branch", "worktree-" + SLUG)
    res = wo.check(SLUG, repo, sessions=[])
    assert res.fired == ("branch",)
    assert res.occupied


@requires_git
def test_leg_live_session_alone_refuses(repo):
    res = wo.check(SLUG, repo, sessions=[_session(repo, SLUG)])
    assert res.fired == ("session",)
    assert res.occupied


@requires_git
def test_a_session_cwd_is_matched_across_slash_style_and_case(repo):
    cwd = str(repo / ".claude" / "worktrees" / SLUG).replace("/", "\\").upper() + "\\"
    res = wo.check(SLUG, repo, sessions=[{"cwd": cwd, "status": "busy"}])
    assert res.fired == ("session",)


@requires_git
def test_an_idle_session_does_not_hold_the_tree(repo):
    """RECON s5.3 leg 4 is `status: busy`. A finished (`idle/done`) job is not executing."""
    assert wo.check(SLUG, repo, sessions=[_session(repo, SLUG, status="idle")]).occupied is False


@requires_git
def test_every_leg_fires_together_and_all_are_named(repo):
    wt = repo / ".claude" / "worktrees" / SLUG
    _git(repo, "worktree", "add", "-q", "-b", "worktree-" + SLUG, str(wt))
    res = wo.check(SLUG, repo, sessions=[_session(repo, SLUG)])
    assert res.fired == ("worktree", "directory", "branch", "session")


@requires_git
def test_ignore_session_excludes_the_callers_own_job(repo):
    s = _session(repo, SLUG)
    assert wo.check(SLUG, repo, sessions=[s], ignore_sessions=("abcd1234",)).occupied is False


# --- read-only ----------------------------------------------------------------------------------

@requires_git
def test_the_check_is_read_only(repo):
    """It never removes, unlocks or repairs: husk, prunable registration and branch all
    survive a check, byte for byte."""
    husk = repo / ".claude" / "worktrees" / SLUG
    husk.mkdir(parents=True)
    _git(repo, "branch", "worktree-" + SLUG)
    ghost = repo / ".claude" / "worktrees" / "ghost"
    _git(repo, "worktree", "add", "-q", "--detach", str(ghost))
    shutil.rmtree(ghost)
    before = (_git(repo, "worktree", "list", "--porcelain"), _git(repo, "branch", "--list"),
              sorted(p.name for p in (repo / ".claude" / "worktrees").iterdir()))
    wo.check(SLUG, repo, sessions=[_session(repo, SLUG)])
    wo.check("ghost", repo, sessions=[])
    after = (_git(repo, "worktree", "list", "--porcelain"), _git(repo, "branch", "--list"),
             sorted(p.name for p in (repo / ".claude" / "worktrees").iterdir()))
    assert before == after
    assert husk.is_dir()


def test_the_module_has_no_destructive_verbs():
    src = Path(wo.__file__).read_text(encoding="utf-8")
    for verb in ("rmtree", "os.remove", "unlink(", "rmdir", "worktree remove", "worktree prune",
                 "worktree unlock", "worktree repair", "branch -d", "branch -D", "kill("):
        assert verb not in src, verb


# --- slug validation ----------------------------------------------------------------------------

@pytest.mark.parametrize("bad", ["", "../x", "a/b", "A-b", "-x", "x-", "a b", "worktree-lane-x"])
def test_a_malformed_slug_is_refused_before_anything_is_looked_up(bad, repo):
    with pytest.raises(wo.OccupancyError):
        wo.check(bad, repo, sessions=[])


# --- the CLI ------------------------------------------------------------------------------------

def _cli(repo, slug, sessions, capsys, *extra):
    sf = repo.parent / "sessions.json"
    sf.write_text(json.dumps(sessions), encoding="utf-8")
    code = wo.main([slug, "--repo-root", str(repo), "--sessions-file", str(sf), *extra])
    return code, capsys.readouterr().out


@requires_git
def test_cli_free_slug_exits_zero(repo, capsys):
    code, out = _cli(repo, SLUG, [], capsys)
    assert code == 0
    assert "FREE" in out


@requires_git
def test_cli_occupied_slug_exits_nonzero_and_names_the_legs(repo, capsys):
    (repo / ".claude" / "worktrees" / SLUG).mkdir(parents=True)
    code, out = _cli(repo, SLUG, [_session(repo, SLUG)], capsys)
    assert code == 1
    assert "OCCUPIED" in out
    assert "directory" in out and "session" in out


@requires_git
def test_cli_bad_slug_exits_two(repo, capsys):
    code, _ = _cli(repo, "../x", [], capsys)
    assert code == 2


@requires_git
def test_cli_json_reports_which_legs_fired(repo, capsys):
    _git(repo, "branch", "worktree-" + SLUG)
    code, out = _cli(repo, SLUG, [], capsys, "--json")
    data = json.loads(out)
    assert code == 1
    assert data["slug"] == SLUG and data["occupied"] is True
    assert data["fired"] == ["branch"]
    assert data["legs"]["branch"] is True and data["legs"]["directory"] is False


def test_cli_cannot_look_is_not_reported_as_free(tmp_path, capsys):
    """A tool that cannot look must say so (exit 2), never print FREE."""
    code = wo.main([SLUG, "--repo-root", str(tmp_path / "not-a-repo"), "--sessions-file",
                    str(tmp_path / "missing.json")])
    assert code == 2
    assert "FREE" not in capsys.readouterr().out


# --- codex terra review (2026-09-20-codex-l2-dispatch-guards): fail closed ----------------------

@requires_git
def test_an_unreadable_directory_fails_closed_rather_than_reading_free(repo, monkeypatch):
    """`Path.exists()` swallows OSError and answers False -- a husk we cannot stat would read
    FREE. Anything but 'not found' must raise."""
    real_stat = wo.os.stat

    def boom(path, *a, **k):
        if str(path).endswith(SLUG):
            raise PermissionError("denied")
        return real_stat(path, *a, **k)

    monkeypatch.setattr(wo.os, "stat", boom)
    with pytest.raises(wo.OccupancyError):
        wo.check(SLUG, repo, sessions=[])


@requires_git
@pytest.mark.parametrize("bad", [
    ["not-a-mapping"],
    [42],
    [{"status": "busy"}],                        # a busy session with no cwd: cannot be excluded
    [{"cwd": "x", "status": None}],
    [{"cwd": "x"}],                              # no status at all
])
def test_a_malformed_session_record_fails_closed(repo, bad):
    with pytest.raises(wo.OccupancyError):
        wo.check(SLUG, repo, sessions=bad)


@requires_git
def test_a_non_busy_session_without_a_cwd_is_harmless(repo):
    assert wo.check(SLUG, repo, sessions=[{"status": "idle"}]).occupied is False


# --- D23(b): a starting record carries `state`, not `status` ------------------------------------

@requires_git
def test_a_starting_record_with_state_but_no_status_does_not_fail_closed(repo):
    """D23: `worktree_occupancy` exited 2 ("could not look") on a session record still
    STARTING -- an external shape that names `state`, not `status`. A record naming either
    field is readable; only a record naming NEITHER is unreadable."""
    assert wo.check(SLUG, repo, sessions=[{"cwd": "x", "state": "starting"}]).occupied is False


@requires_git
def test_a_busy_record_named_by_state_alone_holds_the_tree(repo):
    cwd = str(repo / ".claude" / "worktrees" / SLUG)
    res = wo.check(SLUG, repo, sessions=[{"cwd": cwd, "state": "busy"}])
    assert res.fired == ("session",)
    assert res.occupied


@requires_git
def test_the_cli_applies_the_same_validation_to_a_sessions_file(repo, capsys):
    code, _ = _cli(repo, SLUG, ["oops"], capsys)
    assert code == 2


@requires_git
def test_primary_root_resolves_from_a_lane_worktree():
    """Run from wherever the suite runs (a lane worktree or the primary): the primary checkout
    resolves through `--git-common-dir`, so a lane can ask about a sibling without a flag."""
    root = wo.primary_root(Path(__file__).resolve().parent)
    assert (root / ".git").exists()
