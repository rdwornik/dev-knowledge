"""The caller-side shim, run for real under pwsh against stub `uv` and `claude` executables.

Nothing here starts a real lane: `claude` is a batch stub that prints what `claude --bg` prints, and
`uv` is a stub that answers `plan` from a fixture and fails or succeeds `govern` / `stop` on demand.
What is asserted is the SHIM's contract: whatever the governor does, the shim exits with a code from
the documented set, and a lane it could not govern is never reported as if it were fine.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

SHIM = Path(__file__).resolve().parents[1] / "templates" / "dispatch-shim.ps1"
PWSH = shutil.which("pwsh")

pytestmark = pytest.mark.skipif(not PWSH or os.name != "nt",
                                reason="the shim is PowerShell and the stubs are .cmd files")

PLAN = {"schema": 1, "slug": "wave3-witness", "provider": "anthropic", "model": "haiku",
        "effort": "low", "token_cap": 100, "substrate": "local", "metering": "transcript",
        "argv": ["claude", "--bg", "--model", "haiku"], "prompt": "p", "contract": "c",
        "env_set": {}, "env_unset": [], "steps": []}

UV_STUB = r"""@echo off
echo %* | findstr /C:" plan " >nul && (type "%~dp0plan.json" & exit /b 0)
echo %* | findstr /C:" govern " >nul && exit /b %STUB_GOVERN_RC%
echo %* | findstr /C:" stop " >nul && exit /b %STUB_STOP_RC%
exit /b 99
"""
CLAUDE_STUB = "@echo off\r\necho backgrounded abcd1234\r\nexit /b 0\r\n"


def _run(tmp_path: Path, govern_rc: int, stop_rc: int) -> subprocess.CompletedProcess:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "uv.cmd").write_text(UV_STUB, encoding="utf-8")
    (bin_dir / "claude.cmd").write_text(CLAUDE_STUB, encoding="utf-8")
    (bin_dir / "plan.json").write_text(json.dumps(PLAN), encoding="utf-8")
    hub = tmp_path / "hub"
    (hub / "scripts").mkdir(parents=True)
    (hub / "scripts" / "dispatch.py").write_text("", encoding="utf-8")
    contract = tmp_path / "LANE-wave3-witness.md"
    contract.write_text("x", encoding="utf-8")
    env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
           "STUB_GOVERN_RC": str(govern_rc), "STUB_STOP_RC": str(stop_rc)}
    return subprocess.run([PWSH, "-NoProfile", "-File", str(SHIM), str(contract), "-TokenCap", "100",
                           "-Hub", str(hub)], capture_output=True, text=True, env=env, timeout=120)


@pytest.mark.parametrize("code", [0, 3, 4, 5, 6, 7])
def test_a_documented_governor_exit_code_passes_through_unchanged(tmp_path, code):
    assert _run(tmp_path, govern_rc=code, stop_rc=99).returncode == code


def test_an_abnormal_governor_failure_is_recovered_by_stopping_the_lane_by_worktree(tmp_path):
    """CRITICAL (shim:139): `uv` / Python failing before `govern` reached its own recovery left the
    started lane uncapped and the shim exiting with an arbitrary code. The shim now asks the hub to
    STOP the lane by its worktree, and exits 5 when that stopped it."""
    done = _run(tmp_path, govern_rc=1, stop_rc=5)
    assert done.returncode == 5, done.stdout + done.stderr


def test_an_abnormal_governor_failure_that_cannot_be_recovered_is_exit_4_may_be_running(tmp_path):
    done = _run(tmp_path, govern_rc=1, stop_rc=1)
    assert done.returncode == 4, done.stdout + done.stderr
    assert "may be running" in (done.stdout + done.stderr).lower()
