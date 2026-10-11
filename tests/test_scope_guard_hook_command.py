"""The PreToolUse scope-guard hook command runs the guard under bash AND PowerShell, and exits
cleanly outside a git repository.

Package T6 (to-browser/DIGEST-RATIFICATION-PACKAGE-2026-10-11.md): Copilot CLI honours
`.claude/settings.json` hooks but runs them through PowerShell on Windows and sets no
`CLAUDE_PROJECT_DIR`. The base form `"${CLAUDE_PROJECT_DIR:-.}/scripts/hooks/scope_guard.py"`
read as an empty PowerShell variable there, so the path became `/scripts/hooks/scope_guard.py`
(`C:\\scripts\\...`), python exited 2 and every Copilot tool call at the repo root was denied.
Under bash the `.` fallback is cwd-relative, so a hook fired from a subdirectory missed too.

B2-W4 lane A2 (Codex HIGH on `f9cdeb3d`): `"$(git rev-parse --show-toplevel)/scripts/..."`
fixed both, but outside a git tree git prints nothing, the path degrades to `/scripts/...`
again and python's exit 2 is read as DENY. Outside a git tree the hook must exit 0.

The test runs the DECLARED command through each shell with CLAUDE_PROJECT_DIR absent:
  * inside the repo (root and a subdirectory) a payload under an excluded root must be
    BLOCKED (non-zero exit with the guard's own block JSON) -- proof the guard itself ran;
  * outside any git tree the same payload must exit 0 with no traceback.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SETTINGS = _REPO / ".claude" / "settings.json"
_BLOCKED_PAYLOAD = json.dumps({"tool_name": "Read",
                               "tool_input": {"file_path": "C:/x/OneDrive - Blue Yonder/a.txt"}})


def _scope_guard_command() -> str:
    hooks = json.loads(_SETTINGS.read_text(encoding="utf-8"))["hooks"]["PreToolUse"]
    found = [h["command"] for g in hooks for h in g["hooks"] if "scope_guard.py" in h["command"]]
    assert len(found) == 1, found
    return found[0]


def _works(argv: list[str]) -> bool:
    try:
        proc = subprocess.run([*argv, "echo ok"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0 and proc.stdout.strip() == "ok"


def _posix_shell() -> list[str] | None:
    candidates = [shutil.which("bash")]
    git = shutil.which("git")
    if git:
        candidates.append(str(Path(git).resolve().parents[1] / "bin" / "bash.exe"))
    for exe in candidates:
        if exe and Path(exe).is_file() and _works([exe, "-c"]):
            return [exe, "-c"]
    return None


def _powershell(name: str) -> list[str] | None:
    exe = shutil.which(name)
    argv = [exe, "-NoProfile", "-NonInteractive", "-Command"] if exe else None
    return argv if argv and _works(argv) else None


_SHELLS = {"bash": _posix_shell, "pwsh": lambda: _powershell("pwsh"),
           "powershell": lambda: _powershell("powershell")}


def _env() -> dict:
    drop = {"CLAUDE_PROJECT_DIR", "GIT_DIR", "GIT_WORK_TREE", "DEV_KNOWLEDGE_SCOPE_GUARD_DISABLE"}
    return {k: v for k, v in os.environ.items() if k not in drop}


def _run(shell: str, cwd: Path) -> subprocess.CompletedProcess:
    argv = _SHELLS[shell]()
    if argv is None:
        pytest.skip(f"{shell} is not runnable here")
    return subprocess.run([*argv, _scope_guard_command()], cwd=cwd, env=_env(),
                          input=_BLOCKED_PAYLOAD, capture_output=True, text=True, timeout=180)


@pytest.mark.parametrize("cwd_rel", [".", "scripts"])
@pytest.mark.parametrize("shell", sorted(_SHELLS))
def test_inside_the_repo_the_declared_command_runs_the_guard(shell, cwd_rel):
    proc = _run(shell, _REPO / cwd_rel)
    # the guard exits 2; `pwsh -Command` reports any failed native exit as 1, so the proof the guard
    # itself ran is its own block JSON on stdout plus a non-zero exit, not the literal 2
    assert proc.returncode != 0, (shell, cwd_rel, proc.returncode, proc.stdout, proc.stderr)
    assert json.loads(proc.stdout.strip().splitlines()[-1])["decision"] == "block", proc.stdout


@pytest.mark.parametrize("shell", sorted(_SHELLS))
def test_outside_a_git_tree_the_declared_command_exits_cleanly(shell, tmp_path):
    probe = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=tmp_path, env=_env(),
                           capture_output=True, text=True)
    if probe.returncode == 0:
        pytest.skip(f"{tmp_path} is inside a git tree ({probe.stdout.strip()})")
    proc = _run(shell, tmp_path)
    assert proc.returncode == 0, (shell, proc.returncode, proc.stdout, proc.stderr)
    assert "Traceback" not in proc.stderr, proc.stderr