"""The caller-side shim, run for real under pwsh against a stub `uv` executable.

Nothing here starts a real lane: `uv` is a batch stub that logs its arguments and exits with a code
the test picks. What is asserted is the SHIM's contract after LANE-W3-B: it is a thin wrapper over
`dispatch.py launch` -- exactly one `uv` call, whatever `launch` exits with comes back unchanged, and
there is no second call (no governor, no stop) after it. The parameter mapping, `-DryRun`, `-Run`
and `-Help` are covered in tests/test_dispatch_launch.py.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

SHIM = Path(__file__).resolve().parents[1] / "templates" / "dispatch-shim.ps1"
PWSH = shutil.which("pwsh")

pytestmark = pytest.mark.skipif(not PWSH or os.name != "nt",
                                reason="the shim is PowerShell and the stub is a .cmd file")

UV_STUB = "@echo off\r\necho %*>> \"%~dp0uv-args.txt\"\r\nexit /b %STUB_RC%\r\n"


def _run(tmp_path: Path, launch_rc: int) -> tuple[subprocess.CompletedProcess, list[str]]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "uv.cmd").write_text(UV_STUB, encoding="utf-8")
    hub = tmp_path / "hub"
    (hub / "scripts").mkdir(parents=True)
    (hub / "scripts" / "dispatch.py").write_text("", encoding="utf-8")
    contract = tmp_path / "LANE-wave3-witness.md"
    contract.write_text("x", encoding="utf-8")
    env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", "STUB_RC": str(launch_rc)}
    done = subprocess.run([PWSH, "-NoProfile", "-File", str(SHIM), str(contract), "-Hub", str(hub)],
                          capture_output=True, text=True, env=env, timeout=120)
    log = bin_dir / "uv-args.txt"
    return done, (log.read_text(encoding="utf-8").splitlines() if log.is_file() else [])


@pytest.mark.parametrize("code", [0, 1, 2, 5])
def test_the_exit_code_of_launch_comes_back_unchanged(tmp_path, code):
    done, calls = _run(tmp_path, code)
    assert done.returncode == code, done.stderr


def test_the_shim_makes_exactly_one_call_and_it_is_launch(tmp_path):
    """No governor after it and no recovery path: a refusal (exit 5) is just returned."""
    done, calls = _run(tmp_path, 5)
    assert len(calls) == 1 and " launch " in f" {calls[0]} "
    for later in (" govern ", " stop ", " plan "):
        assert later not in f" {calls[0]} "
