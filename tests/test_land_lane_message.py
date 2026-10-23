"""RED witnesses for Done-contract item 1: landing commit messages pass commit-msg hooks."""
from __future__ import annotations

import check_backlog_commit_msg
import check_backlog_filing
import check_commit_message_type
import pytest
from click.testing import CliRunner

import land_lane as ll
from test_land_lane import Env, _commit_file, _git, do_land


@pytest.fixture(autouse=True)
def _git_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "safe.bareRepository")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", "all")
    monkeypatch.setenv("GIT_CONFIG_KEY_1", "core.autocrlf")
    monkeypatch.setenv("GIT_CONFIG_VALUE_1", "false")
    monkeypatch.setenv("GIT_CONFIG_COUNT", "2")


@pytest.fixture
def env(tmp_path, monkeypatch):
    e = Env(tmp_path / "env")
    monkeypatch.chdir(e.worktree)
    return e


def test_default_merge_message_closes_ids_from_diff():
    """Done-contract item 1: the default message cites every closed backlog id."""
    diff = "@@ -1 +1 @@\n-- [#101] Old row\n+- [#102] New row\n"
    message = ll.build_merge_message("lane-a", "E1.0", diff=diff)

    assert message.splitlines()[0] == "chore(land): lane-a (E1.0)"
    assert "[#101]" in message
    assert check_commit_message_type.check(message)
    assert check_backlog_commit_msg.check(message, diff) == []


def test_added_rows_use_lane_log_kill_candidates_and_pass_hook():
    """Done-contract item 1: additions carry the lane's kill-candidates line."""
    diff = "@@ -0,0 +1 @@\n+- [#202] [P2][M] New row\n"
    lane_log = "chore: file row\n\nkill-candidates: #303 -- obsolete row\n"
    message = ll.build_merge_message("lane-a", "E1.0", diff=diff, lane_log=lane_log)

    assert "kill-candidates: #303 -- obsolete row" in message.splitlines()
    block, _warnings = check_backlog_filing.check(message, diff)
    assert block == []


def test_added_rows_without_lane_candidate_get_a_reasoned_fallback():
    """Done-contract item 1: an addition always gets a valid fallback candidate line."""
    diff = "@@ -0,0 +1 @@\n+- [#203] [P2][M] New row\n"
    message = ll.build_merge_message("lane-a", "E1.0", diff=diff)

    assert any(
        line.startswith("kill-candidates: none -- ") for line in message.splitlines()
    )
    assert check_backlog_filing.check(message, diff)[0] == []


def test_message_override_replaces_the_whole_default_message():
    """Done-contract item 1: --message is an exact whole-message override."""
    override = "docs(land): operator wording\n\n[#404] details"
    assert ll.build_merge_message("lane-a", "E1.0", override=override) == override


def test_pushed_merge_message_passes_all_commit_msg_hooks_for_lane_diff(env):
    """Done-contract item 1: the actual pushed merge message satisfies all relevant hooks."""
    base = env.origin_ref("main")
    _commit_file(
        env.seed,
        "BACKLOG.md",
        "- [#100] Old row\n",
        "seed backlog",
    )
    _git(env.seed, "push", "origin", "main")
    env.make_lane("lane-a", "lane_a.txt")
    _commit_file(
        env.lane,
        "BACKLOG.md",
        "- [#101] [P2][M] New row\n",
        "add backlog row\n\nkill-candidates: none -- test fixture",
    )
    _git(env.lane, "push", "-f", "origin", "worktree-lane-a")

    report = do_land(env)
    assert report.ok, report.message
    message = _git(env.origin, "show", "-s", "--format=%B", report.sha)
    diff = _git(env.worktree, "diff", "-U0", f"{base}..{report.sha}", "--", "BACKLOG.md")

    block, _warnings = check_backlog_filing.check(message, diff)
    assert check_commit_message_type.check(message)
    assert check_backlog_commit_msg.check(message, diff) == []
    assert block == []


def test_cli_exposes_message_override():
    """Done-contract item 1: the CLI accepts and documents --message."""
    result = CliRunner().invoke(ll.cli, ["--help"])

    assert result.exit_code == 0
    assert "--message TEXT" in result.output
