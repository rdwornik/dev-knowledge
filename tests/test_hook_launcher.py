"""The ONE shared hook launcher (`scripts/hooks/hook_launcher.py`) -- batch BW lane
`lane-bw-1001-hook-launcher`, `[#1001]` nearest.

Done-contract, as this file checks it:
  1. the declared launch shape works under bash, pwsh AND Windows PowerShell, from inside a git
     repo (root and a subdirectory), outside every git tree, and from a git tree that does not
     carry the launcher -- one subprocess per shell; a shell absent on the box SKIPS (recorded
     NOT_RUN by the lane report), it never passes;
  2. no `command` in the live `.claude/settings.json` `hooks` block holds inline code -- no `-c`
     flag, no `;` program text;
  4. every entry that has to survive a foreign shell runs through the one launcher, in exactly
     one shape (the three former inline `python -c` entries: the PreToolUse scope guard and B1's
     two Stop gates; and, since lane `lane-bw-1001-sessionstart-one`, the ONE SessionStart entry
     `scripts/hooks/session_start.py`).

The behaviour of each real hook through its declared command stays pinned where it was:
`tests/test_scope_guard_hook_command.py` (scope guard, three shells) and
`tests/test_stop_fail_closed.py` (the two Stop gates, R96).

The launch tests below run against a THROWAWAY git tree that carries a copy of the launcher and
a probe hook, so they measure the launcher's own mechanics (argv, cwd, stdin, exit code) and
never depend on any real hook's verdict.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SETTINGS = _REPO / ".claude" / "settings.json"
_LAUNCHER_REL = "scripts/hooks/hook_launcher.py"
_LAUNCHER = _REPO / _LAUNCHER_REL

#: The one declared shape. `<target>` is the hook script, repo-relative. The launcher's module
#: docstring explains each construct; this string is the pin.
_SHAPE = ('uv run --locked python ${CLAUDE_PROJECT_DIR:+"$CLAUDE_PROJECT_DIR/' + _LAUNCHER_REL
          + '"} $(git rev-parse --no-revs --no-flags -- ./$(git rev-parse --path-format=relative'
          ' --show-toplevel)' + _LAUNCHER_REL + ') -m os ')

#: The entries that must survive a shell other than Claude Code's POSIX one (Copilot CLI runs
#: `.claude/settings.json` hooks through PowerShell on Windows, with no CLAUDE_PROJECT_DIR).
_LAUNCHED = {
    "PreToolUse": ["scripts/hooks/scope_guard.py", "scripts/hooks/reuse_gate.py",
                   "scripts/hooks/subagent_model_guard.py"],
    "Stop": ["scripts/lane_end_guard.py", "scripts/lane_handback_gate.py"],
    "SessionStart": ["scripts/hooks/session_start.py"],
}


def launch_command(target: str) -> str:
    return _SHAPE + target


# --- the live settings ------------------------------------------------------------------------

def _hook_commands() -> list[tuple[str, str]]:
    hooks = json.loads(_SETTINGS.read_text(encoding="utf-8"))["hooks"]
    return [(event, h["command"]) for event, groups in hooks.items() for g in groups
            for h in g["hooks"] if isinstance(h.get("command"), str)]


_DASH_C = re.compile(r"(?<!\S)-c(?!\S)")


#: The ONE named exception: the AX15-1 prompts guard, re-armed 2026-10-15 by [#863]. Its
#: permit must be PROVEN by a stdout marker checked outside the interpreter the PATH chooses,
#: so its program lives in the command by ruling, and it cannot ride this launcher, which drops
#: every argument after the target (`sys.argv = [target]`) and so could never pass
#: `--prompts-guard`. The exception is pinned to the command's exact bytes -- the pre-disable
#: bash program of 645ec4db, unchanged, inside the bash/PowerShell polyglot wrapper (see
#: `test_the_prompts_guard_command_parses_and_allows_under_powershell`) -- so an edit to that
#: program, or any OTHER command carrying a program, is still refused.
_AX15_1_PROMPTS_GUARD_SHA256 = "7b40c5d6aafccd09f0af789663023f2161f46fccdd8544ad050a434c81678814"
#: The wrapped bash program alone: 645ec4db's command, byte for byte.
_AX15_1_BASH_PROGRAM_SHA256 = "3548dda45b4db9c1cf2f9923d411ca50e0cd8433f897d5b57a0b7886a5c4f7ec"


def _is_ax15_1_prompts_guard(event: str, cmd: str) -> bool:
    return (event == "PreToolUse"
            and hashlib.sha256(cmd.encode("utf-8")).hexdigest() == _AX15_1_PROMPTS_GUARD_SHA256)


def test_no_hook_command_holds_inline_code():
    """Done-contract 2: a `command` names programs and files; it never carries a program."""
    offenders = [(event, cmd) for event, cmd in _hook_commands()
                 if (_DASH_C.search(cmd) or ";" in cmd) and not _is_ax15_1_prompts_guard(event, cmd)]
    assert not offenders, offenders
    exempt = [cmd for event, cmd in _hook_commands() if _is_ax15_1_prompts_guard(event, cmd)]
    assert len(exempt) <= 1, "the AX15-1 exception covers exactly one prompts-guard entry"


def test_the_ax15_1_exception_admits_only_the_pinned_bytes():
    """Review finding (Codex terra, 2026-10-15): a substring match on `--prompts-guard` let any
    statement prepended to that command ride the exception. Only the exact command is exempt."""
    pinned = [cmd for event, cmd in _hook_commands() if _is_ax15_1_prompts_guard(event, cmd)]
    assert len(pinned) == 1, "the re-armed prompts guard is not the pinned command"
    assert not _is_ax15_1_prompts_guard("PreToolUse", "echo pwned; " + pinned[0])
    assert not _is_ax15_1_prompts_guard("PreToolUse", "bash -c 'echo --prompts-guard'")
    assert not _is_ax15_1_prompts_guard("SessionStart", pinned[0])
    head, program, *tail = pinned[0].split("\n")
    assert head == "echo `# <#` >/dev/null" and len(tail) == 3
    assert tail[0] == "#>" and tail[1].startswith("# ") and tail[2] == "exit 0"
    assert hashlib.sha256(program.encode("utf-8")).hexdigest() == _AX15_1_BASH_PROGRAM_SHA256


@pytest.mark.parametrize("event,target",
                         [(e, t) for e, targets in _LAUNCHED.items() for t in targets])
def test_each_shell_neutral_entry_is_the_one_launcher_shape(event, target):
    commands = [cmd for ev, cmd in _hook_commands() if ev == event and target in cmd]
    assert commands == [launch_command(target)], commands


def test_every_launched_entry_is_one_of_the_named_entries():
    """No fourth entry grows its own variant: whatever reaches the launcher uses the one shape."""
    launched = sorted(cmd for _, cmd in _hook_commands() if "hook_launcher.py" in cmd)
    expected = sorted(launch_command(t) for targets in _LAUNCHED.values() for t in targets)
    assert launched == expected


def test_the_inline_detector_catches_a_seeded_dash_c():
    assert _DASH_C.search('uv run --locked python -c "import x"')
    assert not _DASH_C.search('uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/x-c.py"')


# --- the launch shape, through each real shell ------------------------------------------------

def _works(argv: list[str]) -> bool:
    try:
        proc = subprocess.run([*argv, "echo ok"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0 and proc.stdout.strip() == "ok"


def _bash() -> list[str] | None:
    # Git Bash before PATH: on Windows `bash` on PATH can be the WSL launcher.
    candidates = [r"C:\Program Files\Git\bin\bash.exe", shutil.which("bash")]
    for exe in candidates:
        if exe and Path(exe).is_file() and _works([exe, "-c"]):
            return [exe, "-c"]
    return None


def _powershell(name: str) -> list[str] | None:
    exe = shutil.which(name)
    argv = [exe, "-NoProfile", "-NonInteractive", "-Command"] if exe else None
    return argv if argv and _works(argv) else None


_SHELLS = {"bash": _bash, "pwsh": lambda: _powershell("pwsh"),
           "powershell": lambda: _powershell("powershell")}

_PROBE = """\
import json, os, sys
print(json.dumps({"argv": sys.argv, "cwd": os.getcwd(), "path0": sys.path[0],
                  "stdin": sys.stdin.read(), "name": __name__}))
sys.exit(int(os.environ.get("PROBE_EXIT", "0")))
"""
_PAYLOAD = json.dumps({"hook_event_name": "Probe", "stop_hook_active": False})


def _git_tree(path: Path, *, with_launcher: bool) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(path)], check=True, capture_output=True)
    (path / "sub" / "deeper").mkdir(parents=True)
    if with_launcher:
        (path / "scripts" / "hooks").mkdir(parents=True)
        shutil.copy2(_LAUNCHER, path / _LAUNCHER_REL)
        (path / "scripts" / "probe.py").write_text(_PROBE, encoding="utf-8")
    return path


def _env(**extra: str) -> dict:
    drop = {"CLAUDE_PROJECT_DIR", "GIT_DIR", "GIT_WORK_TREE", "PROBE_EXIT"}
    env = {k: v for k, v in os.environ.items() if k not in drop}
    env["UV_PROJECT"] = str(_REPO)   # the locked interpreter, whatever the cwd; cwd is untouched
    env.update(extra)
    return env


def _launch(shell: str, cwd: Path, env: dict, target: str = "scripts/probe.py",
            command: str | None = None, stdin: str = _PAYLOAD):
    argv = _SHELLS[shell]()
    if argv is None:
        pytest.skip(f"{shell} is not runnable on this box -- NOT_RUN, not a pass")
    return subprocess.run([*argv, command or launch_command(target)], cwd=cwd, env=env,
                          input=stdin, capture_output=True, text=True, timeout=180)


@pytest.mark.parametrize("shell", ["pwsh", "powershell"])
def test_the_prompts_guard_command_parses_and_allows_under_powershell(shell):
    """[#863] (4), measured 2026-10-15 (lane-bu-863 QA): Copilot CLI 1.0.98 runs this file's
    PreToolUse hooks through PowerShell and fails CLOSED on a hook error, and the bash-only
    prompts-guard program is a PowerShell ParserError -- every Copilot shell call in this repo
    was refused. Claude Code runs a hook through PowerShell only when its entry declares
    `"shell": "powershell"` (claude.exe 2.1.300) -- asserted absent below, since it would turn
    this ALLOW branch into a disarmed guard -- so PowerShell is reached only by a non-Claude
    client, whose calls the Claude prompts-dir guard does not govern: it must parse, print
    nothing on stderr and ALLOW."""
    hooks = json.loads(_SETTINGS.read_text(encoding="utf-8"))["hooks"]["PreToolUse"]
    entries = [h for g in hooks for h in g["hooks"] if "--prompts-guard" in h.get("command", "")]
    assert len(entries) == 1 and entries[0].get("shell", "bash") == "bash", entries
    commands = [entries[0]["command"]]
    proc = _launch(shell, _REPO, _env(), command=commands[0])
    assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
    assert proc.stderr.strip() == "", proc.stderr
    # Line 1's literal `#` is the one byte PowerShell prints; Copilot CLI 1.0.98 ALLOWS on it
    # (measured 2026-10-15: `echo PROBE-OK-7c41` ran with this command wired).
    assert proc.stdout.strip() == "#", proc.stdout


#: [#863] (4) round 2: the ADR-77 guard stays on the SYSTEM interpreter (settings.json `//`
#: ruling: stdlib-only, a stale lockfile must never block every Edit/Write), so it does not take
#: the uv launcher shape; it uses the launcher's two shell-neutral locators on the guard itself.
_ADR77 = "scripts/hooks/block_immutable_edits.py"
_ADR77_SHAPE = ('python ${CLAUDE_PROJECT_DIR:+"$CLAUDE_PROJECT_DIR/' + _ADR77 + '"} $(git rev-parse'
                ' --no-revs --no-flags -- ./$(git rev-parse --path-format=relative --show-toplevel)'
                + _ADR77 + ') -m os')


@pytest.mark.parametrize("shell", sorted(_SHELLS))
def test_the_adr77_guard_runs_on_the_system_interpreter_and_blocks_in_zone_in_every_shell(shell):
    """Copilot CLI 1.0.98 runs this file's hooks through PowerShell, fail-closed, with no
    CLAUDE_PROJECT_DIR: the pre-disable `python "$CLAUDE_PROJECT_DIR/..."` would have refused
    every Copilot edit. Under every shell the guard must still block an in-zone Edit and allow
    an out-of-zone one."""
    commands = [cmd for ev, cmd in _hook_commands() if ev == "PreToolUse" and _ADR77 in cmd]
    assert commands == [_ADR77_SHAPE], commands
    zone = json.dumps({"tool_name": "Edit", "tool_input": {
        "file_path": "docs/decisions/transcripts/2026-03-29-council-browser-handoff.md"}})
    blocked = _launch(shell, _REPO, _env(), command=commands[0], stdin=zone)
    # bash relays 2 exactly; `pwsh -Command` reports any failed native exit as 1, which Copilot
    # CLI fails closed on -- either way the edit is refused, and the JSON verdict is printed
    expected = {2} if shell == "bash" else {1, 2}
    assert blocked.returncode in expected, (blocked.returncode, blocked.stdout, blocked.stderr)
    assert json.loads(blocked.stdout.strip().splitlines()[-1])["decision"] == "block"
    outside = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": "README.md"}})
    allowed = _launch(shell, _REPO, _env(), command=commands[0], stdin=outside)
    assert allowed.returncode == 0, (allowed.returncode, allowed.stdout, allowed.stderr)


def _probe_report(proc: subprocess.CompletedProcess) -> dict:
    lines = proc.stdout.strip().splitlines()
    assert lines, (proc.returncode, proc.stdout, proc.stderr)
    return json.loads(lines[-1])


def _same(a: str, b: Path) -> bool:
    return Path(a).resolve() == b.resolve()


@pytest.mark.parametrize("cwd_rel", [".", "sub/deeper"])
@pytest.mark.parametrize("shell", sorted(_SHELLS))
def test_inside_a_git_tree_the_hook_runs_as_if_invoked_directly(shell, cwd_rel, tmp_path):
    tree = _git_tree(tmp_path / "tree", with_launcher=True)
    proc = _launch(shell, tree / cwd_rel, _env())
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    report = _probe_report(proc)
    assert report["name"] == "__main__"
    assert len(report["argv"]) == 1 and _same(report["argv"][0], tree / "scripts" / "probe.py")
    assert _same(report["path0"], tree / "scripts"), "the hook's own directory leads sys.path"
    assert _same(report["cwd"], tree / cwd_rel), "the launcher never moves the cwd"
    assert json.loads(report["stdin"]) == json.loads(_PAYLOAD), "the payload reaches the hook"


@pytest.mark.parametrize("shell", sorted(_SHELLS))
def test_the_hooks_exit_code_is_the_commands_exit_code(shell, tmp_path):
    tree = _git_tree(tmp_path / "tree", with_launcher=True)
    proc = _launch(shell, tree / "sub", _env(PROBE_EXIT="2"))
    # bash relays 2 exactly; `pwsh -Command` reports any failed native exit as 1
    expected = {2} if shell == "bash" else {1, 2}
    assert proc.returncode in expected, (proc.returncode, proc.stdout, proc.stderr)
    _probe_report(proc)


@pytest.mark.parametrize("shell", sorted(_SHELLS))
def test_outside_every_git_tree_the_command_allows_silently(shell, tmp_path):
    loose = tmp_path / "loose"
    loose.mkdir()
    probe = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=loose,
                           capture_output=True, text=True)
    if probe.returncode == 0:
        pytest.skip(f"{loose} sits inside a git tree on this box")
    proc = _launch(shell, loose, _env())
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert proc.stdout.strip() == ""
    assert "Traceback" not in proc.stderr, proc.stderr


@pytest.mark.parametrize("shell", sorted(_SHELLS))
def test_a_git_tree_without_the_launcher_fails_closed(shell, tmp_path):
    """A root resolves but the launcher is not in it: never a clean allow (R96)."""
    tree = _git_tree(tmp_path / "bare", with_launcher=False)
    proc = _launch(shell, tree, _env())
    assert proc.returncode != 0, (proc.stdout, proc.stderr)
    assert proc.stdout.strip() == ""


def test_bash_prefers_the_claude_project_dir_over_the_cwds_tree(tmp_path):
    """Claude Code (POSIX shell, CLAUDE_PROJECT_DIR set) whose cwd wandered into another checkout
    still runs ITS project's hook -- never the other tree's, and never a fail-closed exit because
    the other tree lacks the launcher."""
    project = _git_tree(tmp_path / "project", with_launcher=True)
    elsewhere = _git_tree(tmp_path / "elsewhere", with_launcher=False)
    proc = _launch("bash", elsewhere, _env(CLAUDE_PROJECT_DIR=str(project)))
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    report = _probe_report(proc)
    assert _same(report["argv"][0], project / "scripts" / "probe.py")
    assert _same(report["cwd"], elsewhere)


def test_bash_with_a_project_dir_that_lacks_the_launcher_fails_closed(tmp_path):
    """DECIDED (Codex r1 HIGH, disputed -- see the launcher docstring, "A CLAUDE_PROJECT_DIR
    WITHOUT THE LAUNCHER"): when the variable is set it is trusted, exactly as every other
    `"$CLAUDE_PROJECT_DIR/scripts/..."` entry in the file trusts it and as the pre-A2 scope-guard
    entry did. A project dir that lacks the launcher is never a silent allow; it does not fall
    back to the cwd's tree either, because no shell construct can test a file's existence
    without spawning a process on every tool call."""
    stale = tmp_path / "stale"
    stale.mkdir()
    tree = _git_tree(tmp_path / "tree", with_launcher=True)
    proc = _launch("bash", tree, _env(CLAUDE_PROJECT_DIR=str(stale)))
    assert proc.returncode != 0, (proc.stdout, proc.stderr)
    assert proc.stdout.strip() == ""


def test_bash_with_the_project_dir_outside_every_git_tree_still_runs_the_hook(tmp_path):
    project = _git_tree(tmp_path / "project", with_launcher=True)
    loose = tmp_path / "loose"
    loose.mkdir()
    proc = _launch("bash", loose, _env(CLAUDE_PROJECT_DIR=str(project)))
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert _same(_probe_report(proc)["argv"][0], project / "scripts" / "probe.py")


# --- the launcher's own refusals --------------------------------------------------------------

def _direct(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["uv", "run", "--locked", "python", str(_LAUNCHER), *args],
                          cwd=_REPO, env=_env(), input="", capture_output=True, text=True,
                          timeout=120)


@pytest.mark.parametrize("target", ["scripts/no_such_hook.py", "../outside.py", "scripts", ""])
def test_a_target_that_is_not_a_file_under_the_root_is_refused_closed(target):
    proc = _direct("-m", "os", target)
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    assert "hook_launcher: no hook script" in proc.stderr and proc.stdout == ""


def test_no_target_at_all_is_refused_closed():
    proc = _direct()
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    assert "hook_launcher: no hook script" in proc.stderr
