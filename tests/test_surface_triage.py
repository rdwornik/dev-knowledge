"""Behavioural regression guard for scripts/surface_triage.ps1.

RETIRED 2026-07-09 (#255): Surfacing 2 (the nightly conformance-run health check —
the "Nightly Conformance Triage" Action-run probe + the automation/conformance-digest
branch digest-presence probe) was removed with the conformance-digest mechanism (a
PR-triggered organ under a local-merge workflow was vacuous). This file previously
asserted that branch/digest alarm behaviour; it now GUARDS the retirement — the script
must never emit a `[nightly]` line again, regardless of what the (now-unused) branch /
digest state would have been, and must still exit 0.

BEHAVIOURAL: runs the REAL .ps1 end-to-end via Windows PowerShell 5.1
(`powershell -NoProfile -File ...`, the hook's actual runtime) with a fake `gh` first on
PATH answering the auth / issue-list / run-list surfacings on their happy path. Mirrors
the subprocess "wire protocol" half of test_block_immutable_edits.py.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "surface_triage.ps1"
_ALARM = "may have silently skipped"

# The fake `gh`: answers the auth gate (valid), issue-list (none), and run-list
# (success) happy path. The retired Surfacing 2 no longer calls /branches/ or
# /contents/ at all; a leftover 404 handler for them is harmless (never reached) and
# doubles as proof the script makes no such call.
_FAKE_GH_PY = r'''
import sys
args = sys.argv[1:]
joined = " ".join(args)
if args[:2] == ["auth", "status"]:
    sys.exit(0)
if args[:1] == ["issue"] and "list" in args:
    print("[]"); sys.exit(0)
if args[:1] == ["run"] and "list" in args:
    print('[{"conclusion":"success","status":"completed","url":"https://example/run/1"}]')
    sys.exit(0)
# Surfacing 2 retired -> these should NEVER be invoked. If they are, fail loud by
# emitting the old alarm-triggering shape so the regression test catches it.
if args[:1] == ["api"] and "/branches/" in joined:
    print('{"name":"automation/conformance-digest"}'); sys.exit(0)
if args[:1] == ["api"] and "/contents/" in joined:
    print('{"message":"Not Found","status":"404"}'); sys.exit(1)
sys.exit(0)
'''


@pytest.fixture
def fake_gh_dir(tmp_path):
    """A directory holding a fake `gh` (gh.cmd -> fake_gh.py) to prepend to PATH."""
    (tmp_path / "fake_gh.py").write_text(_FAKE_GH_PY, encoding="utf-8")
    (tmp_path / "gh.cmd").write_text(
        "@echo off\r\n"
        f'"{sys.executable}" "%~dp0fake_gh.py" %*\r\n'
        "exit /b %ERRORLEVEL%\r\n",
        encoding="utf-8",
    )
    return tmp_path


def _run(fake_gh_dir) -> "subprocess.CompletedProcess[str]":
    powershell = shutil.which("powershell")
    if not powershell:
        pytest.skip("Windows PowerShell (powershell.exe) not on PATH")
    env = dict(os.environ)
    env["PATH"] = str(fake_gh_dir) + os.pathsep + env.get("PATH", "")
    env.pop("CLAUDE_PROJECT_DIR", None)  # stay in cwd; gh is faked regardless
    return subprocess.run(
        [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(_SCRIPT)],
        capture_output=True, text=True, encoding="utf-8", env=env,
    )


def test_surfacing2_retired_no_nightly_banner(fake_gh_dir):
    """The retired conformance-run-health surfacing must never emit a `[nightly]`
    line — even though the fake `gh` would answer the old branch/digest probes if
    the script still made them. Exit code stays 0 (fail-soft surfacing contract)."""
    proc = _run(fake_gh_dir)
    assert proc.returncode == 0, f"hook must always exit 0; stderr={proc.stderr!r}"
    assert "[nightly]" not in proc.stdout, f"Surfacing 2 should be retired; got: {proc.stdout!r}"
    assert _ALARM not in proc.stdout
