"""[#956] lane-hooks-rearm -- WAVE4B-COMMON-2026-09-22 common rule 5: every armed hook's entry is
read from `settings.json` and its command is runnable; every still-disabled hook carries a future
date and a reason.

RED-FIRST (ADR-108 SS B). These assertions were witnessed failing against the settings.json state
before this lane's edit: the six re-armed hooks were absent from `hooks.SessionStart`, and their
`disabled_individually` entries carried the pre-lane `expiry: "2026-09-24"` with the old
bypass-rate-only `reenable_when` text.

WHAT "runnable" MEANS HERE, stated so a later reader does not read this as testing hook behaviour.
The live process-level proof (real invocation through the same POSIX shell the harness uses,
duration, exit code, orphan check) is `docs/audits/2026-09-22-technical-lane-hooks-rearm-live-measurement.md`
-- a one-off measurement, not a repeatable regression guard, and each hook's own script-level
behaviour already has its own test file (`test_fleet_health.py`, `test_conductor.py`, etc.). What
this module guards, repeatably and hermetically, is the settings.json WIRING: that an armed
command still names a script that exists and parses, and that a still-disabled entry has not gone
stale (a past expiry with nobody looking, exactly the condition this lane was filed to fix).
"""
from __future__ import annotations

import json
import py_compile
from datetime import date
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SETTINGS = _REPO / ".claude" / "settings.json"

# The six hooks this lane re-armed on live evidence (docs/audits/2026-09-22-technical-lane-hooks-rearm-live-measurement.md).
#
# UPDATED 2026-09-25 (LANE-5B-5 lane-hooks-port): the two entries that were `.ps1` at the
# 2026-09-22 rearm (surface_triage, billing_leak_sentinel) are now their ported `.py` modules --
# PowerShell was the harness's only hard break on a Linux/cloud substrate, so both were rewired
# in .claude/settings.json to run through `uv run --locked python`. The `.ps1` sources are
# retired in place (unwired, not deleted); their own regression guard
# (tests/test_surface_triage.py) still exercises the unchanged `.ps1` behaviour directly. As a
# consequence, the `.ps1` existence-and-size branch of test_rearmed_hook_script_is_runnable
# below is no longer reached by any entry in this tuple -- it stays live code for a future
# still-`.ps1` hook (see _STILL_DISABLED_HOOK_NAMES).
_REARMED_HOOK_NAMES = (
    "surface_triage.py",
    "changelog_sentinel.py",
    "conductor.py",
    "resource_lifecycle.py",
    "codespace_regime.py",
    "billing_leak_sentinel.py",
)

# fleet_health.py was ALSO left disabled by this lane (contract: "No hook is deleted"), pending
# the architectural fix (reader/trigger/isolated-producer split) [#956]'s own handback named as
# CANDIDATE. That fix landed in lane-fleet-health-split [#962] (2026-09-23), which re-armed it --
# see _LANE_962_REARMED_HOOK_NAMES below. Only surface-closures.ps1 remains still-disabled here.
_STILL_DISABLED_HOOK_NAMES = ("surface-closures.ps1",)

# [#962] lane-fleet-health-split (2026-09-23): fleet_health.py's SessionStart entry re-armed on
# fresh live evidence after the reader/trigger/isolated-producer split fixed both defects this
# lane's own FAILED 2026-09-22 entry named (the synchronous in-session audit hang, and
# audit.py::_commit_routine_outputs silently deleting untracked docs/audits/ work on restore).
# Kept separate from _REARMED_HOOK_NAMES above: that tuple is [#956]'s own six-hook set from its
# 2026-09-22 measurement and this is a distinct, later re-arm event by a different lane.
_LANE_962_REARMED_HOOK_NAMES = ("fleet_health.py",)


_TODAY = date(2026, 9, 22)  # this lane's filing date; the contract's own frame of reference


def _load_settings() -> dict:
    return json.loads(_SETTINGS.read_text(encoding="utf-8"))


# lane-bw-1001-sessionstart-one ([#1001]): the nine SessionStart entries became ONE entry,
# `scripts/hooks/session_start.py` through the shared launcher, which IMPORTS each former reader.
# A hook is "wired in SessionStart" now when it is one of that entry's READERS; the timeout that
# bounds it is the one entry's. The questions this module asks are unchanged -- is it wired
# exactly once, does it carry a positive timeout, does the script it names exist and parse.

def _session_start_entry(settings: dict) -> dict:
    entries = [h for g in settings["hooks"]["SessionStart"] for h in g["hooks"]]
    assert len(entries) == 1, entries
    return entries[0]


def _reader_scripts() -> list[str]:
    import sys
    sys.path.insert(0, str(_REPO / "scripts" / "hooks"))
    import session_start
    return [r.script for r in session_start.READERS]


def _reader_script_path(hook_name: str) -> Path:
    matching = [s for s in _reader_scripts() if Path(s).name == hook_name]
    assert len(matching) == 1, (
        f"{hook_name} should be exactly one reader of the SessionStart entry, found {matching}")
    return _REPO / matching[0]


# --- Done-contract 5a: every armed hook's command is runnable -------------------------------

def test_every_session_start_command_names_a_script_that_exists():
    # DECIDED-BY-LANE (lane-wire-quota-distiller, repair 2 of 2, LANE-5B3-2-wire-quota-distiller.md):
    # count moved 8 -> 9 with the addition of scripts/hooks/quota_daily.py, the daily
    # quota_watch.py SessionStart trigger. lane-bw-1001-sessionstart-one ([#1001]): the nine are
    # now the READERS of ONE entry, scripts/hooks/session_start.py.
    settings = _load_settings()
    entry = _session_start_entry(settings)
    assert entry["command"].endswith(" scripts/hooks/session_start.py"), entry
    assert (_REPO / "scripts" / "hooks" / "session_start.py").is_file()
    readers = _reader_scripts()
    assert len(readers) == 9, (
        f"expected arm_hooks.py, the six [#956] re-armed hooks, [#962]'s fleet_health.py, and "
        f"lane-wire-quota-distiller's scripts/hooks/quota_daily.py (9 total), found "
        f"{len(readers)}: {readers}"
    )
    for script in readers:
        path = _REPO / script
        assert path.is_file(), f"SessionStart reader names a script that does not exist: {path}"


@pytest.mark.parametrize("hook_name", _REARMED_HOOK_NAMES)
def test_rearmed_hook_is_wired_in_session_start(hook_name):
    settings = _load_settings()
    _reader_script_path(hook_name)
    entry = _session_start_entry(settings)
    assert isinstance(entry.get("timeout"), int) and entry["timeout"] > 0, (
        f"{hook_name}'s SessionStart entry has no explicit positive timeout: {entry}"
    )


@pytest.mark.parametrize("hook_name", _REARMED_HOOK_NAMES)
def test_rearmed_hook_script_is_runnable(hook_name, tmp_path):
    """Runnable, hermetically: the referenced file exists and, for a `.py` script, compiles.

    `.ps1` scripts are checked for existence and non-empty content only -- this suite runs
    without a guaranteed `powershell`/`pwsh` on every box (unlike the live audit, which measured
    real invocation on this one).
    """
    path = _reader_script_path(hook_name)
    assert path.is_file()
    if path.suffix == ".py":
        out = tmp_path / f"{path.stem}.pyc"
        py_compile.compile(str(path), cfile=str(out), doraise=True)
        assert out.exists()
    else:
        assert path.suffix == ".ps1"
        assert path.stat().st_size > 0, f"{path} is empty"


# --- Done-contract 5b: every still-disabled hook carries a future date and a reason ----------

@pytest.mark.parametrize("hook_name", _STILL_DISABLED_HOOK_NAMES)
def test_still_disabled_hook_carries_a_future_expiry_and_a_reason(hook_name):
    settings = _load_settings()
    entries = settings["//hooks-RESTORED-AND-DISABLED-INDIVIDUALLY-2026-09-17"]["disabled_individually"]
    matching = [e for e in entries if e["hook"] == hook_name]
    assert len(matching) == 1, f"expected exactly one disabled_individually entry for {hook_name}"
    entry = matching[0]

    expiry = date.fromisoformat(entry["expiry"])
    assert expiry > _TODAY, (
        f"{hook_name}'s expiry {entry['expiry']} is not strictly after this lane's filing date "
        f"{_TODAY.isoformat()} -- a stale-on-arrival expiry is the exact defect this lane exists "
        f"to fix"
    )

    reason = entry.get("reenable_when", "")
    assert isinstance(reason, str) and len(reason.strip()) > 0, (
        f"{hook_name} has no reenable_when reason"
    )
    # The reason must be THIS lane's, not the stale pre-2026-09-22 bypass-rate-only boilerplate
    # every other retired entry still carries -- a copy-pasted reason would silently fail to
    # record why THIS hook specifically stayed off.
    assert "2026-09-22" in reason or "lane-hooks-rearm" in reason, (
        f"{hook_name}'s reenable_when does not cite this lane's 2026-09-22 measurement: {reason!r}"
    )


def test_no_stale_disabled_entries_remain_for_the_six_rearmed_hooks():
    """The six re-armed hooks must not ALSO still carry a disabled_individually entry -- that
    would be the settings file disagreeing with itself about whether a hook is on or off."""
    settings = _load_settings()
    entries = settings["//hooks-RESTORED-AND-DISABLED-INDIVIDUALLY-2026-09-17"]["disabled_individually"]
    disabled_names = {e["hook"] for e in entries}
    for hook_name in _REARMED_HOOK_NAMES:
        assert hook_name not in disabled_names, (
            f"{hook_name} is armed in hooks.SessionStart but still listed as disabled -- "
            f"remove the stale disabled_individually entry"
        )


# --- [#962] lane-fleet-health-split (2026-09-23): fleet_health.py re-armed --------------------

@pytest.mark.parametrize("hook_name", _LANE_962_REARMED_HOOK_NAMES)
def test_lane_962_rearmed_hook_is_wired_in_session_start(hook_name):
    settings = _load_settings()
    _reader_script_path(hook_name)
    entry = _session_start_entry(settings)
    assert isinstance(entry.get("timeout"), int) and entry["timeout"] > 0, (
        f"{hook_name}'s SessionStart entry has no explicit positive timeout: {entry}"
    )


@pytest.mark.parametrize("hook_name", _LANE_962_REARMED_HOOK_NAMES)
def test_lane_962_rearmed_hook_script_is_runnable(hook_name, tmp_path):
    path = _reader_script_path(hook_name)
    assert path.is_file()
    out = tmp_path / f"{path.stem}.pyc"
    py_compile.compile(str(path), cfile=str(out), doraise=True)
    assert out.exists()


def test_no_stale_disabled_entry_remains_for_fleet_health():
    """fleet_health.py must not ALSO still carry a disabled_individually entry now that it is
    armed in hooks.SessionStart -- the same disagreement test_no_stale_disabled_entries_remain_
    for_the_six_rearmed_hooks guards for [#956]'s six, applied to [#962]'s re-arm."""
    settings = _load_settings()
    entries = settings["//hooks-RESTORED-AND-DISABLED-INDIVIDUALLY-2026-09-17"]["disabled_individually"]
    disabled_names = {e["hook"] for e in entries}
    for hook_name in _LANE_962_REARMED_HOOK_NAMES:
        assert hook_name not in disabled_names, (
            f"{hook_name} is armed in hooks.SessionStart but still listed as disabled -- "
            f"remove the stale disabled_individually entry"
        )


def test_disable_all_hooks_is_still_false():
    """The repo-level override this lane depends on to matter at all (settings.json's own `//`
    note: disableAllHooks is FALSE here explicitly because the user-level file sets it true)."""
    settings = _load_settings()
    assert settings["disableAllHooks"] is False
