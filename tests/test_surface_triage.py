"""Behavioural tests for scripts/surface_triage.ps1 — Surfacing 2(b), the nightly
digest side-effect check (ADR-68 / ADR-84).

The fix under test ATOMIZES two concerns the probe used to conflate into one alarm:
  (1) the automation/conformance-digest branch does NOT YET EXIST
      -> "not-yet-initialized" -> STAY SILENT (the transition-window false positive
         a probe-repoint-ahead-of-first-write produced);
  (2) the branch EXISTS but the dated digest is MISSING
      -> the real no-retry silent-skip signal -> ALARM, exactly as before.

These are BEHAVIOURAL tests: they run the REAL .ps1 end-to-end via Windows
PowerShell 5.1 (`powershell -NoProfile -File ...`, the hook's actual runtime) with
a fake `gh` first on PATH, keyed to each state by env vars. We assert on what the
script EMITS, not merely that it executes. Mirrors the subprocess "wire protocol"
half of test_block_immutable_edits.py (the repo's PowerShell-hook test pattern).
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

# The fake `gh`: a tiny dispatcher keyed on argv + two env flags. It answers the
# happy path for the auth gate / issue-list / run-list surfacings (so the ONLY
# possible output is the digest line under test), then decides branch-existence
# and digest-existence from FAKE_GH_BRANCH_PRESENT / FAKE_GH_DIGEST_PRESENT.
# Exit-code discipline mirrors real `gh api`: 0 on HTTP 200, non-zero on 404 with
# the error BODY printed to stdout (so the test also exercises the script's
# exit-code gate, not a stdout-truthiness shortcut).
_FAKE_GH_PY = r'''
import os, sys
args = sys.argv[1:]
joined = " ".join(args)

# auth gate -> valid
if args[:2] == ["auth", "status"]:
    sys.exit(0)
# open nightly-triage issues -> none
if args[:1] == ["issue"] and "list" in args:
    print("[]"); sys.exit(0)
# last Action run -> success (no failure banner)
if args[:1] == ["run"] and "list" in args:
    print('[{"conclusion":"success","status":"completed","url":"https://example/run/1"}]')
    sys.exit(0)
# branch existence probe (the NEW discriminator)
if args[:1] == ["api"] and "/branches/" in joined:
    if os.environ.get("FAKE_GH_BRANCH_PRESENT") == "1":
        print('{"name":"automation/conformance-digest"}'); sys.exit(0)
    print('{"message":"Branch not found","documentation_url":"...","status":"404"}'); sys.exit(1)
# digest existence probe (--jq .name -> bare name on success)
if args[:1] == ["api"] and "/contents/" in joined:
    if os.environ.get("FAKE_GH_DIGEST_PRESENT") == "1":
        print("2099-01-02-conformance-nightly-digest.md"); sys.exit(0)
    print('{"message":"Not Found","documentation_url":"...","status":"404"}'); sys.exit(1)
sys.exit(0)
'''


@pytest.fixture
def fake_gh_dir(tmp_path):
    """A directory holding a fake `gh` (gh.cmd -> fake_gh.py) to prepend to PATH."""
    (tmp_path / "fake_gh.py").write_text(_FAKE_GH_PY, encoding="utf-8")
    # gh.cmd shells to THIS interpreter so the test does not depend on a `python`
    # on PATH; `exit /b` propagates the exit code into PowerShell's $LASTEXITCODE.
    (tmp_path / "gh.cmd").write_text(
        "@echo off\r\n"
        f'"{sys.executable}" "%~dp0fake_gh.py" %*\r\n'
        "exit /b %ERRORLEVEL%\r\n",
        encoding="utf-8",
    )
    return tmp_path


def _run(fake_gh_dir, *, branch_present: bool, digest_present: bool) -> str:
    powershell = shutil.which("powershell")
    if not powershell:
        pytest.skip("Windows PowerShell (powershell.exe) not on PATH")
    env = dict(os.environ)
    env["PATH"] = str(fake_gh_dir) + os.pathsep + env.get("PATH", "")
    env["FAKE_GH_BRANCH_PRESENT"] = "1" if branch_present else "0"
    env["FAKE_GH_DIGEST_PRESENT"] = "1" if digest_present else "0"
    env.pop("CLAUDE_PROJECT_DIR", None)  # stay in cwd; gh is faked regardless
    proc = subprocess.run(
        [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(_SCRIPT)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    assert proc.returncode == 0, f"hook must always exit 0; stderr={proc.stderr!r}"
    return proc.stdout


# --- The two REQUIRED states (closure is on BOTH behaviours) ----------------- #

def test_branch_absent_is_silent(fake_gh_dir):
    """(1) Branch not-yet-initialized -> NO alarm. The transition-window fix."""
    out = _run(fake_gh_dir, branch_present=False, digest_present=False)
    assert _ALARM not in out
    assert "[nightly]" not in out  # no digest banner at all when the branch is absent


def test_branch_exists_digest_missing_alarms(fake_gh_dir):
    """(2) Branch exists but the dated digest is missing -> ALARM, as before."""
    out = _run(fake_gh_dir, branch_present=True, digest_present=False)
    assert _ALARM in out


# --- Regression guard: the happy path must remain silent --------------------- #

def test_branch_exists_digest_present_is_silent(fake_gh_dir):
    """Branch exists AND digest present -> silent. Proves the fix did not break
    the all-green path (the alarm must not fire when the digest is really there)."""
    out = _run(fake_gh_dir, branch_present=True, digest_present=True)
    assert _ALARM not in out
