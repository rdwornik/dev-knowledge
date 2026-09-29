"""LANE-5B-5 lane-hooks-port -- Done-contract 1 & 2: every SessionStart/Stop hook this repo
declares runs through `uv run --locked python`, and no `powershell` invocation survives in
`.claude/settings.json`'s `hooks` section.

`surface_triage.ps1` and `billing_leak_sentinel.ps1` were the container's only hard break
(PowerShell does not exist on the harness's Linux/cloud substrate -- lane 14, a devcontainer,
any future Actions runner). This suite is the checkable surface for their retirement: it reads
the live `hooks` block, not a copy, so a later hand-edit that reintroduces `powershell` reds here
rather than silently reintroducing the break.

RED-FIRST (ADR-108 SS B): written and run against the pre-port `.claude/settings.json`, which
still carried two `powershell -File` commands and a bare `python` `lane_end_guard.py` Stop entry
-- every assertion below failed before the port landed.

LANE-5B5R-2-scope-guard-2 (redo, 2026-09-29): N4's scope-guard lane broadened a PreToolUse
`matcher` to include the literal tool name `"PowerShell"` (Claude Code's own first-class tool,
distinct from Bash, that this repo's guard must also gate) -- a `matcher` field NAMES a tool
class for the PreToolUse event to fire on; it never INVOKES anything. The original whole-block
substring scan could not tell that apart from a hook's `command` field actually shelling out to
the `powershell`/`pwsh` interpreter, and reddened on the matcher string alone
(`tests/test_scope_guard.py`'s own contract does not touch this file's assertions -- this is
the matcher/guard-test collision the redo's Done-contract names). The fix scans only `command`
values (recursively, whatever hook shape holds them), never `matcher` values, so naming the
tool stays allowed while invoking the interpreter stays caught --
`test_a_seeded_real_powershell_invocation_in_hooks_is_still_caught` below is the RED-first
proof that the guard is made ACCURATE, not weaker.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SETTINGS = _REPO / ".claude" / "settings.json"

_UV_LOCKED_PY = re.compile(r'^uv run --locked python "\$CLAUDE_PROJECT_DIR/scripts/[^"]+\.py"$')

#: A real interpreter invocation -- `powershell`/`powershell.exe`/`pwsh`/`pwsh.exe` as a
#: whole word (never a substring of a longer identifier, so e.g. a hypothetical
#: `my-powershell-helper.py` token is not falsely caught). Deliberately does NOT look at
#: `matcher` fields -- see the module docstring.
_POWERSHELL_INVOCATION = re.compile(r"(?<![\w-])(powershell(\.exe)?|pwsh(\.exe)?)(?![\w-])",
                                     re.IGNORECASE)


def _settings() -> dict:
    return json.loads(_SETTINGS.read_text(encoding="utf-8"))


def _all_hook_commands(hooks: dict) -> list[str]:
    """Every `command` string in a `hooks{}`-shaped structure, found recursively by KEY name
    (`"command"`), never by guessing the nesting shape -- so a `matcher` field's tool-name
    string (e.g. `"...|PowerShell|..."`) is never visited, whatever depth it sits at."""
    out: list[str] = []

    def _walk(node: object) -> None:
        if isinstance(node, dict):
            command = node.get("command")
            if isinstance(command, str):
                out.append(command)
            for value in node.values():
                _walk(value)
        elif isinstance(node, list):
            for value in node:
                _walk(value)

    _walk(hooks)
    return out


def _powershell_invocations(hooks: dict) -> list[str]:
    return [c for c in _all_hook_commands(hooks) if _POWERSHELL_INVOCATION.search(c)]


def _session_start_commands() -> list[str]:
    groups = _settings()["hooks"]["SessionStart"]
    return [h["command"] for g in groups for h in g["hooks"]]


def _stop_commands() -> list[str]:
    groups = _settings()["hooks"]["Stop"]
    return [h["command"] for g in groups for h in g["hooks"]]


# --- Done-contract 2: no `powershell` anywhere in the hooks section -------------------------

def test_hooks_section_carries_no_powershell_invocation():
    """A scan over the LIVE `hooks` block's `command` values, not the whole file -- the
    surrounding comment prose (e.g. the ADR-77/prompts-guard essay) is allowed to keep
    historical mentions of PowerShell, and so is a `matcher` field NAMING the `"PowerShell"`
    tool (Claude Code's own tool, gated the same as `"Bash"` by the scope guard); only a
    `command` that actually INVOKES the interpreter may not."""
    hooks = _settings()["hooks"]
    offenders = _powershell_invocations(hooks)
    assert not offenders, (
        "a powershell invocation survives in the live hooks{} block -- the container's hard "
        f"break was not fully removed: {offenders}"
    )


def test_a_seeded_real_powershell_invocation_in_hooks_is_still_caught():
    """RED-first proof that the matcher/command split above did not weaken the guard: a
    hook `command` that actually shells out to PowerShell -- planted here, never in the live
    file -- is still flagged, even sitting beside a `matcher` field that also says
    "PowerShell" for an unrelated reason (naming the tool class, not invoking it)."""
    seeded = {
        "PreToolUse": [{
            "matcher": "Read|Write|Edit|Bash|PowerShell|Glob|Grep",
            "hooks": [{"type": "command",
                       "command": 'powershell -File "$CLAUDE_PROJECT_DIR/scripts/x.ps1"'}],
        }],
    }
    offenders = _powershell_invocations(seeded)
    assert offenders == ['powershell -File "$CLAUDE_PROJECT_DIR/scripts/x.ps1"']


def test_a_matcher_naming_the_powershell_tool_alone_is_not_flagged():
    seeded = {
        "PreToolUse": [{
            "matcher": "Read|Write|Edit|Bash|PowerShell|Glob|Grep",
            "hooks": [{"type": "command",
                       "command": 'uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/hooks/scope_guard.py"'}],
        }],
    }
    assert _powershell_invocations(seeded) == []


# --- Done-contract 1: both former-PowerShell SessionStart hooks are uv run --locked python ---

def test_surface_triage_is_wired_as_uv_run_locked_python():
    commands = [c for c in _session_start_commands() if "surface_triage" in c]
    assert len(commands) == 1, f"expected exactly one surface_triage entry, found {commands}"
    assert _UV_LOCKED_PY.match(commands[0]), commands[0]
    assert commands[0].endswith('scripts/surface_triage.py"')


def test_billing_leak_sentinel_is_wired_as_uv_run_locked_python():
    commands = [c for c in _session_start_commands() if "billing_leak_sentinel" in c]
    assert len(commands) == 1, f"expected exactly one billing_leak_sentinel entry, found {commands}"
    assert _UV_LOCKED_PY.match(commands[0]), commands[0]
    assert commands[0].endswith('scripts/billing_leak_sentinel.py"')


def test_the_ported_scripts_exist_on_disk():
    assert (_REPO / "scripts" / "surface_triage.py").is_file()
    assert (_REPO / "scripts" / "billing_leak_sentinel.py").is_file()


# --- Done-contract 1: lane_end_guard's Stop invocation is uv run --locked python -------------

def test_lane_end_guard_stop_entry_runs_through_uv_run_locked_python():
    commands = [c for c in _stop_commands() if "lane_end_guard.py" in c]
    assert len(commands) == 1, f"expected exactly one lane_end_guard Stop entry, found {commands}"
    command = commands[0]
    assert command.startswith('uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/lane_end_guard.py"'), command
    assert command.endswith("|| true"), command


# --- sanity: the count of SessionStart commands is pinned, not just non-decreasing ----------
#
# DECIDED-BY-LANE (lane-wire-quota-distiller, repair 2 of 2): this test pinned the count at
# eight when this file's own two hooks were rewired PowerShell->python (no net change). Kept
# the same name-then-number shape rather than the original literal name
# (`..._unchanged_at_eight`) because "unchanged" stopped being true the moment a NINTH command
# (`scripts/hooks/quota_daily.py`, LANE-5B3-2-wire-quota-distiller.md) was added on top of this
# lane's own rewiring -- a name asserting "unchanged" while the file's own diff changes the
# count would be a false claim baked into the test's identity, not just its body.

def test_session_start_command_count_is_nine():
    assert len(_session_start_commands()) == 9, _session_start_commands()
