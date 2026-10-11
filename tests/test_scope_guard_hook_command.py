"""The PreToolUse scope-guard hook command resolves its script under bash AND PowerShell.

Package T6 (to-browser/DIGEST-RATIFICATION-PACKAGE-2026-10-11.md): Copilot CLI honours
`.claude/settings.json` hooks but runs them through PowerShell on Windows and sets no
`CLAUDE_PROJECT_DIR`. The base form `"${CLAUDE_PROJECT_DIR:-.}/scripts/hooks/scope_guard.py"`
reads as an empty PowerShell variable there, so the path became `/scripts/hooks/scope_guard.py`
(`C:\\scripts\\...`), python exited 2 and every Copilot tool call at the repo root was denied.
Under bash the `.` fallback is cwd-relative, so a hook fired from a subdirectory missed too.

RED-first: against the base command every PowerShell case and the bash-from-a-subdirectory
case resolve to a path that is not the guard. The test runs the declared command itself,
with only its `uv run --locked python` launcher swapped for `echo`, so the shell's own
expansion is what is measured.
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
_GUARD = _REPO / "scripts" / "hooks" / "scope_guard.py"
_LAUNCHER = "uv run --locked python "


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


@pytest.mark.parametrize("cwd_rel", [".", "scripts"])
@pytest.mark.parametrize("shell", sorted(_SHELLS))
def test_scope_guard_command_resolves_the_guard_without_claude_project_dir(shell, cwd_rel):
    argv = _SHELLS[shell]()
    if argv is None:
        pytest.skip(f"{shell} is not runnable here")
    command = _scope_guard_command()
    assert command.startswith(_LAUNCHER), command
    probe = "echo " + command[len(_LAUNCHER):]
    cwd = _REPO / cwd_rel
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
    proc = subprocess.run([*argv, probe], cwd=cwd, env=env, capture_output=True, text=True,
                          timeout=60)
    assert proc.returncode == 0, proc.stderr
    printed = proc.stdout.strip().splitlines()[0]
    resolved = (cwd / printed).resolve() if not Path(printed).is_absolute() else Path(printed).resolve()
    assert resolved == _GUARD.resolve(), (
        f"{shell} from {cwd_rel!r} with CLAUDE_PROJECT_DIR absent resolved the guard to "
        f"{printed!r}, not {_GUARD}")
