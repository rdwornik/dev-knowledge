"""Behavioural regression guard for scripts/surface_triage.py -- the LANE-5B-5 lane-hooks-port
Python port of scripts/surface_triage.ps1.

The ps1's own regression guard (tests/test_surface_triage_ps1.py, formerly this file's name)
stays in place unchanged: the .ps1 file is retired-in-place (no longer wired in
.claude/settings.json, see tests/test_hooks_no_powershell.py) but not deleted, and its own
behaviour is unchanged, so its guard keeps guarding it. This file was renamed off
test_surface_triage_py.py to test_surface_triage.py so the [#278] impacted-tests-guard
(scripts/X.py -> tests/test_X.py) resolves it -- it guards the SAME contract -- gh resolution,
the auth gate, the [triage] surfacing, always-exit-0 -- for the module that is actually wired
now.

RED-FIRST (ADR-108 SS B): written and collected before scripts/surface_triage.py existed --
every test here failed with a collection ModuleNotFoundError.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "surface_triage.py"


# The fake `gh`: a tiny Python script driven directly by sys.executable (no shell wrapper
# needed -- surface_triage.py resolves gh via shutil.which, which finds an .exe/.cmd/.bat on
# Windows or an executable file on POSIX; a .cmd shim mirrors the ps1 suite's own fixture).
_FAKE_GH_TEMPLATE = r'''
import sys
args = sys.argv[1:]
if args[:2] == ["auth", "status"]:
    sys.exit({auth_exit})
if args[:1] == ["issue"] and "list" in args:
    sys.stdout.write({issues!r})
    sys.exit(0)
sys.exit(0)
'''


def _fake_gh(tmp_path, auth_exit=0, issues="[]"):
    (tmp_path / "fake_gh.py").write_text(
        _FAKE_GH_TEMPLATE.format(auth_exit=auth_exit, issues=issues), encoding="utf-8"
    )
    (tmp_path / "gh.cmd").write_text(
        "@echo off\r\n"
        f'"{sys.executable}" "%~dp0fake_gh.py" %*\r\n'
        "exit /b %ERRORLEVEL%\r\n",
        encoding="utf-8",
    )
    return tmp_path


def _run(gh_dir=None, on_path=True):
    env = dict(os.environ)
    if gh_dir is not None and on_path:
        env["PATH"] = str(gh_dir) + os.pathsep + env.get("PATH", "")
    elif gh_dir is None:
        # simulate gh being wholly absent: strip anything named gh* off PATH is impractical
        # cross-box, so tests that need "gh absent" instead point PATH at an empty dir only.
        pass
    return subprocess.run(
        [sys.executable, str(_SCRIPT)], capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=env,
    )


def test_gh_absent_is_silent_and_exits_0(tmp_path):
    empty = tmp_path / "empty-path"
    empty.mkdir()
    env = dict(os.environ)
    env["PATH"] = str(empty)
    env.pop("ProgramFiles", None)
    proc = subprocess.run([sys.executable, str(_SCRIPT)], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == ""


def test_gh_auth_invalid_prints_the_refresh_line_and_skips_issue_check(tmp_path):
    gh_dir = _fake_gh(tmp_path, auth_exit=1)
    proc = _run(gh_dir)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "[gh] auth invalid -- run: gh auth refresh -h github.com"


def test_zero_open_triage_issues_is_silent(tmp_path):
    gh_dir = _fake_gh(tmp_path, auth_exit=0, issues="[]")
    proc = _run(gh_dir)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == ""
    assert "[triage]" not in proc.stdout


def test_open_triage_issues_are_surfaced_with_count_and_numbers(tmp_path):
    issues = json.dumps([{"number": 12, "title": "a"}, {"number": 34, "title": "b"}])
    gh_dir = _fake_gh(tmp_path, auth_exit=0, issues=issues)
    proc = _run(gh_dir)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "[triage] 2 nightly findings await: #12, #34 -- see the Issues tab."


def test_a_single_open_triage_issue_uses_the_singular_word(tmp_path):
    issues = json.dumps([{"number": 7, "title": "a"}])
    gh_dir = _fake_gh(tmp_path, auth_exit=0, issues=issues)
    proc = _run(gh_dir)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "[triage] 1 nightly finding await: #7 -- see the Issues tab."


def test_malformed_issue_json_is_swallowed_fail_soft(tmp_path):
    gh_dir = _fake_gh(tmp_path, auth_exit=0, issues="not json")
    proc = _run(gh_dir)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == ""


def test_never_prints_the_retired_nightly_banner(tmp_path):
    """Surfacing 2 (the nightly conformance-run-health check) is retired -- carried forward
    from the .ps1 suite's own regression guard so the port cannot reintroduce it."""
    issues = json.dumps([{"number": 1, "title": "a"}])
    gh_dir = _fake_gh(tmp_path, auth_exit=0, issues=issues)
    proc = _run(gh_dir)
    assert "[nightly]" not in proc.stdout


@pytest.mark.parametrize("timeout_env", [None])
def test_always_exits_0_even_on_an_unexpected_exception(tmp_path, monkeypatch, timeout_env):
    """A gh that hangs/crashes must never take session-start down with it -- the fail-soft
    contract is the whole point of a SessionStart surfacing hook."""
    gh_dir = _fake_gh(tmp_path, auth_exit=0, issues="[")  # truncated JSON: json.loads raises
    proc = _run(gh_dir)
    assert proc.returncode == 0, proc.stderr
