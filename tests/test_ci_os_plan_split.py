"""LANE e2-os-split: RED-first tests for OS-specific pytest selection."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import ci_os_plan as plan

ROOT = Path(__file__).resolve().parents[1]
BASE = "b" * 40
HEAD = "a" * 40


@pytest.mark.parametrize(
    ("event", "os_name", "expected"),
    [
        ("pull_request", plan.LINUX, "not windows_only"),
        ("schedule", plan.LINUX, "not windows_only"),
        ("schedule", plan.WINDOWS, ""),
        ("pull_request", plan.WINDOWS, "windows_only or windows_smoke"),
    ],
)
def test_selection_for_linux_nightly_and_landing_legs(event, os_name, expected):
    assert plan.selection(event, os_name) == expected


def _git(changed):
    def run(args):
        if args[0] == "merge-base":
            return 0, BASE
        if args[0] == "diff":
            return 0, changed
        if args[0] == "grep":
            return 1, ""
        if args[0] == "show":
            return 0, json.dumps({"members_by_os": {}})
        return 1, ""

    return run


def test_windows_sensitive_diff_selects_both_oses_and_only_windows_marked_tests():
    oses, _reason = plan.plan(
        "pull_request", _git("scripts/hooks/x.py\n"), HEAD, None, ""
    )

    assert oses == [plan.LINUX, plan.WINDOWS]
    assert plan.selection("pull_request", plan.WINDOWS) == (
        "windows_only or windows_smoke"
    )


def test_non_matching_diff_selects_linux_only():
    assert plan.plan(
        "pull_request", _git("docs/readme.md\n"), HEAD, None, ""
    ) == (
        [plan.LINUX],
        "no Windows-sensitive path in the diff: Linux alone judges this merge",
    )


def test_cli_prints_marker_expressions_and_scheduled_plan_needs_no_git(
    monkeypatch, capsys, tmp_path
):
    calls = []

    def fake_git(_root):
        def run(args):
            calls.append(args)
            return 1, ""

        return run

    monkeypatch.setattr(plan, "run_git", fake_git)
    output_file = tmp_path / "github-output.txt"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output_file))

    assert plan.main(["--event", "schedule", "--head", HEAD]) == 0

    output = capsys.readouterr().out
    assert "m_ubuntu=not windows_only" in output
    assert "m_windows=\n" in output
    assert "m_ubuntu=not windows_only" in output_file.read_text(encoding="utf-8")
    assert "m_windows=\n" in output_file.read_text(encoding="utf-8")
    assert calls == []


@pytest.mark.parametrize(
    ("existing", "extra", "expected"),
    [
        ("not operator_host", "not windows_only",
         "(not operator_host) and (not windows_only)"),
        ("", "x", "x"),
        ("y", "", "y"),
    ],
)
def test_compose_markexpr(existing, extra, expected):
    from conftest import compose_markexpr

    assert compose_markexpr(existing, extra) == expected


def test_windows_markers_are_registered():
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--markers",
            "-p",
            "no:cacheprovider",
            "-n0",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "windows_only" in completed.stdout
    assert "windows_smoke" in completed.stdout


def test_ubuntu_marker_expression_keeps_plain_tests_and_deselects_windows_tests(
    pytester,
):
    pytester.makepyfile(
        test_sample="""
import pytest

@pytest.mark.windows_only
def test_windows_only():
    pass

def test_plain():
    pass
"""
    )

    result = pytester.runpytest("-m", "not windows_only", "-q")

    result.assert_outcomes(passed=1, deselected=1)
