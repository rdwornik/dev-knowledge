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
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SETTINGS = _REPO / ".claude" / "settings.json"

_UV_LOCKED_PY = re.compile(r'^uv run --locked python "\$CLAUDE_PROJECT_DIR/scripts/[^"]+\.py"$')


def _settings() -> dict:
    return json.loads(_SETTINGS.read_text(encoding="utf-8"))


def _session_start_commands() -> list[str]:
    groups = _settings()["hooks"]["SessionStart"]
    return [h["command"] for g in groups for h in g["hooks"]]


def _stop_commands() -> list[str]:
    groups = _settings()["hooks"]["Stop"]
    return [h["command"] for g in groups for h in g["hooks"]]


# --- Done-contract 2: no `powershell` anywhere in the hooks section -------------------------

def test_hooks_section_carries_no_powershell_invocation():
    """A grep over the LIVE `hooks` block, not the whole file -- the surrounding comment
    prose (e.g. the ADR-77/prompts-guard essay) is allowed to keep historical mentions of
    PowerShell; only the block that actually fires may not."""
    hooks_json = json.dumps(_settings()["hooks"])
    assert "powershell" not in hooks_json.lower(), (
        "a powershell invocation survives in the live hooks{} block -- the container's hard "
        f"break was not fully removed: {hooks_json}"
    )


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


# --- sanity: the count of SessionStart commands is unchanged (2 rewired, not added/removed) --

def test_session_start_command_count_is_unchanged_at_eight():
    assert len(_session_start_commands()) == 8, _session_start_commands()
