"""RED witnesses for Done-contract item 3: ratified K1 operator-act landings."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

import land_lane as ll
from test_land_lane import Env, _git, pass_verdict, stub_suite


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


def _ratification(tmp_path: Path, row: str = "| K1 | Browser landing ratified |") -> Path:
    path = tmp_path / "RATIFICATION-2026-10-22.md"
    path.write_text(f"# Ratifications\n\n| ID | Decision |\n|---|---|\n{row}\n", encoding="utf-8")
    return path


def test_resolve_ratification_returns_the_matching_table_row(tmp_path):
    """Done-contract item 3: only a ratified table row resolves the operator-act id."""
    path = _ratification(tmp_path)

    assert ll.resolve_ratification("K1", path) == "| K1 | Browser landing ratified |"


def test_resolve_ratification_rejects_absent_or_non_table_ids(tmp_path):
    """Done-contract item 3: an absent or non-table id is not ratified."""
    path = _ratification(tmp_path, "K1 — Browser landing ratified")

    assert ll.resolve_ratification("K1", path) is None
    assert ll.resolve_ratification("K2", path) is None


def test_operator_act_message_records_ratification_and_id():
    """Done-contract item 3: the landing message names the operator-act and its source."""
    message = ll.build_merge_message(
        "lane-a",
        "E1.0",
        operator_act="K1",
        ratification="to-browser/RATIFICATION-2026-10-22.md",
    )

    assert message.splitlines()[0] == "chore(land): lane-a (E1.0) operator-act K1"
    assert (
        "Ratified-by: K1 to-browser/RATIFICATION-2026-10-22.md"
        in message.splitlines()
    )


def test_cli_exposes_operator_act_and_ratification_options():
    """Done-contract item 3: the CLI exposes the required operator-act interface."""
    result = CliRunner().invoke(ll.cli, ["--help"])

    assert result.exit_code == 0
    assert "--operator-act TEXT" in result.output
    assert "--ratification PATH" in result.output


@pytest.mark.parametrize("include_file", [False, True])
def test_cli_refuses_missing_or_unresolved_ratification_before_push(
    env, tmp_path, include_file
):
    """Done-contract item 3: invalid operator-act input refuses without changing origin."""
    ratification = _ratification(tmp_path, "| K2 | Another ratified act |")
    before = env.refs()
    args = [
        "--worktree",
        str(env.worktree),
        "--slug",
        "lane-a",
        "--batch",
        "E1.0",
        "--i-am-the-integrator",
        "--operator-act",
        "K1",
    ]
    if include_file:
        args.extend(["--ratification", str(ratification)])

    result = CliRunner().invoke(ll.cli, args)

    assert result.exit_code == ll.EXIT_REFUSED == 5
    assert env.refs() == before


def test_operator_act_dry_run_prints_plan_and_resolved_row_without_pushing(env, tmp_path):
    """Done-contract item 3: dry-run prints the plan and exact resolved ratification row."""
    ratification = _ratification(tmp_path)
    before = env.refs()
    result = CliRunner().invoke(
        ll.cli,
        [
            "--worktree",
            str(env.worktree),
            "--slug",
            "lane-a",
            "--batch",
            "E1.0",
            "--lane-ref",
            "origin/worktree-lane-a",
            "--operator-act",
            "K1",
            "--ratification",
            str(ratification),
            "--dry-run",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "| K1 | Browser landing ratified |" in result.output
    assert "operator-act K1" in result.output
    assert env.refs() == before


def test_operator_act_landing_records_id_and_makes_no_model_calls(
    env, tmp_path, monkeypatch
):
    """Done-contract item 3: a valid operator-act lands without invoking any model CLI."""
    ratification = _ratification(tmp_path)
    original_run = subprocess.run
    original_popen = subprocess.Popen
    invoked: list[list[str]] = []

    def check_argv(args):
        argv = [str(arg) for arg in args]
        invoked.append(argv)
        if Path(argv[0]).stem.lower() in {"claude", "codex", "copilot"}:
            pytest.fail(f"operator-act invoked a model CLI: {argv[0]}")
        return args

    def recording_run(args, *args_rest, **kwargs):
        check_argv(args)
        return original_run(args, *args_rest, **kwargs)

    def recording_popen(args, *args_rest, **kwargs):
        check_argv(args)
        return original_popen(args, *args_rest, **kwargs)

    monkeypatch.setattr(subprocess, "run", recording_run)
    monkeypatch.setattr(subprocess, "Popen", recording_popen)
    original_land_lane = ll.land_lane

    def injected_land_lane(worktree, **kwargs):
        return original_land_lane(
            worktree,
            verdict_fn=pass_verdict,
            record_suite_fn=stub_suite,
            sleep=lambda _seconds: None,
            teardown_fn=lambda _worktree: None,
            **kwargs,
        )

    monkeypatch.setattr(ll, "land_lane", injected_land_lane)
    result = CliRunner().invoke(
        ll.cli,
        [
            "--worktree",
            str(env.worktree),
            "--slug",
            "lane-a",
            "--batch",
            "E1.0",
            "--lane-ref",
            "origin/worktree-lane-a",
            "--operator-act",
            "K1",
            "--ratification",
            str(ratification),
            "--i-am-the-integrator",
        ],
    )

    assert result.exit_code == 0, result.output
    landed = env.origin_ref("main")
    message = _git(env.origin, "show", "-s", "--format=%B", landed)
    assert "Ratified-by: K1" in message
    assert any(Path(argv[0]).name == "git" for argv in invoked)
