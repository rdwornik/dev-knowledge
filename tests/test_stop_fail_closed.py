"""Stop gates fail closed (ratified D8 / package T5.3, operator ruling R96: "drop `|| true`").

The two lane Stop entries in `.claude/settings.json` -- `lane_end_guard.py` and
`lane_handback_gate.py` -- carried a trailing `|| true`, which turned EVERY outcome of the
command into exit 0: a gate whose interpreter could not start, or whose script was not there,
read to the host as a clean allow. R96 drops it, so the command's own exit code reaches Claude
Code. For a Stop hook, exit 2 blocks the stop and feeds stderr back to the model.

What this file pins, through the commands EXACTLY as declared and run as the harness runs them
(a POSIX shell, `$CLAUDE_PROJECT_DIR` set):
  * neither declared command swallows its exit code;
  * a bad lane report (a malformed closing HANDBACK line, on a fresh stop attempt) BLOCKS --
    exit 2 with the named reason on stderr;
  * a script that cannot be found blocks rather than silently allowing (fail-closed);
  * outside a lane, both commands still ALLOW (exit 0) even with a bad report on disk.
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
_SCRIPTS = ("lane_end_guard.py", "lane_handback_gate.py")
_FRESH = json.dumps({"stop_hook_active": False})
_BAD = "HANDBACK worktree-stop-fail-closed @ abc1234\n"   # no <kind>: malformed


def _bash() -> str:
    # Git Bash before PATH: on Windows `bash` on PATH can be the WSL launcher, not a POSIX shell
    # over this filesystem.
    exe = next((c for c in (r"C:\Program Files\Git\bin\bash.exe", shutil.which("bash"))
                if c and Path(c).exists()), None)
    if not exe:
        pytest.skip("no POSIX shell on PATH")
    return exe


def _declared(script: str) -> str:
    data = json.loads(_SETTINGS.read_text(encoding="utf-8"))
    cmds = [h["command"] for entry in data["hooks"]["Stop"] for h in entry["hooks"]
            if script in h.get("command", "")]
    assert len(cmds) == 1, cmds
    return cmds[0]


def _run(command: str, env: dict, stdin: str = _FRESH) -> subprocess.CompletedProcess:
    return subprocess.run([_bash(), "-c", command], cwd=_REPO, env={**os.environ, **env},
                          input=stdin, capture_output=True, text=True, timeout=60)


@pytest.mark.parametrize("script", _SCRIPTS)
def test_the_declared_stop_command_does_not_swallow_its_exit_code(script):
    command = _declared(script)
    assert "|| true" not in command, command
    assert "||" not in command, f"any `||` fallback can mask the exit code: {command}"


@pytest.mark.parametrize("script", _SCRIPTS)
def test_the_declared_stop_command_fails_closed_when_the_script_is_missing(script, tmp_path):
    proc = _run(_declared(script), {"CLAUDE_PROJECT_DIR": str(tmp_path / "nowhere"),
                                    "HARNESS_LANE": "stop-fail-closed"})
    assert proc.returncode != 0, "a gate that cannot run must not read as a clean allow"


def test_a_bad_lane_report_blocks_stop_through_the_declared_command(tmp_path):
    session = tmp_path / "SESSION-stop-fail-closed.md"
    session.write_text(_BAD, encoding="utf-8")
    proc = _run(_declared("lane_handback_gate.py"),
                {"CLAUDE_PROJECT_DIR": str(_REPO), "HARNESS_LANE": "stop-fail-closed",
                 "HARNESS_SESSION_FILE": str(session)})
    assert proc.returncode == 2, (proc.returncode, proc.stdout, proc.stderr)
    assert "malformed" in proc.stderr.lower(), proc.stderr


def test_a_clean_lane_report_allows_stop_through_the_declared_command(tmp_path):
    session = tmp_path / "SESSION-stop-fail-closed.md"
    session.write_text("HANDBACK worktree-stop-fail-closed @ abc1234 code\n", encoding="utf-8")
    proc = _run(_declared("lane_handback_gate.py"),
                {"CLAUDE_PROJECT_DIR": str(_REPO), "HARNESS_LANE": "stop-fail-closed",
                 "HARNESS_SESSION_FILE": str(session)})
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert proc.stdout.strip() == ""


@pytest.mark.parametrize("script", _SCRIPTS)
def test_outside_a_lane_the_declared_stop_command_still_allows(script, tmp_path):
    """A non-lane checkout: the scripts are copied into a project dir that is NOT under
    `.claude/worktrees/`, so `resolve_lane` finds no lane. A bad report on disk must not block."""
    project = tmp_path / "primary"
    (project / "scripts").mkdir(parents=True)
    for name in _SCRIPTS + ("transport_report.py",):
        shutil.copy2(_REPO / "scripts" / name, project / "scripts" / name)
    session = tmp_path / "SESSION-x.md"
    session.write_text(_BAD, encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k != "HARNESS_LANE"}
    env.update({"CLAUDE_PROJECT_DIR": str(project), "HARNESS_SESSION_FILE": str(session),
                "HARNESS_RECEIPTS_DIR": str(tmp_path / "r")})
    proc = subprocess.run([_bash(), "-c", _declared(script)], cwd=_REPO, env=env, input=_FRESH,
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert proc.stdout.strip() == ""
