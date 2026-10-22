"""tests/conftest.py -- the `operator_host` marker (LANE-5B4-5-host-witness, row L3).

Some reds are not code defects: they read the operator's disk directly (sibling repos
under `Dev/`, `claude` on PATH, this repo's own local `main` ref, extra worktrees) --
things a fresh CI checkout simply does not have. Before this lane they went silently red
on CI; after it they are explicit HOST WITNESSES, marked `operator_host` and REGISTERED
here, so CI can skip them by marker instead of reading them as a regression.

`OPERATOR_HOST_TESTS` is the registration list -- ground truth for which node ids this
lane confirmed CURRENTLY read the operator's disk (see the list's own comment for the
re-derivation against live CI evidence; the contract's T2 source document named 18, most
of which are PREMISE-FAILED -- STALE, not current). The marker itself is still applied at
each test with `@pytest.mark.operator_host` (Files-you-own: the environment-class test
files T2 names) -- registration and marking are two independent facts about the same
test, and `pytest_collection_modifyitems` below checks they AGREE. A registered node id
with no marker on it is exactly the failure mode Done-contract item 2 names ("an unmarked
test that reads outside the repository ... is reported"): `find_unregistered_drift` is
the pure, unit-tested half of that check (see `tests/test_test_pairing.py`); the pytest
hook is its wiring.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import pytest

# A synthetic-repo run (pytester, or any subprocess that spawns pytest against a tmp_path
# checkout) never collects tests/conftest.py; only a run rooted at THIS tests/ directory
# does. So this list is exhaustive for the real repo and inert everywhere else.
#: T2 (`to-browser/SESSION-decision-ci-verification-2026-09-26-seat-71020de7.md`) named 18
#: across five sub-categories; re-checked against CI run 36314839016 on origin/main tip
#: 316d3205 (`gh run view --job <id> --log`, both OS legs) rather than trusted as written
#: (R14/R17). PREMISE-FAILED for 12 of the 18 -- `logs/KNOWN-REDS-REGISTRY.json`'s "no
#: local main x4" entries were measured BEFORE `lane-ci-matrix` (merged 316d3205) added
#: `fetch-depth: 0` to the CI checkout, which fixed the underlying cause: 0 of those 4
#: appear in either OS leg's FAILED set in that run. "repos registered", a standalone
#: "claude not on PATH", and "no extra worktrees" do not reproduce there either. Confirmed
#: reproducing and host-witness in nature (the walk's own `claude` calls have no CLI on
#: the ubuntu runner's PATH): exactly the 6 `test_integrator_surface.py` ids below --
#: `FAILED` on ubuntu-latest, absent from windows-latest, in that same run.
OPERATOR_HOST_TESTS: frozenset[str] = frozenset({
    "tests/test_integrator_surface.py::test_the_walk_reaches_push_when_every_verification_passes",
    "tests/test_integrator_surface.py::test_a_refused_verification_never_reaches_push_or_teardown[moment:merge]",
    "tests/test_integrator_surface.py::test_a_refused_verification_never_reaches_push_or_teardown[race]",
    "tests/test_integrator_surface.py::test_the_walk_closes_the_receipt_and_commits_the_ledger_before_moment_teardown",
    "tests/test_integrator_surface.py::test_a_refusal_after_the_push_never_reaches_teardown[actions]",
    "tests/test_integrator_surface.py::test_a_refusal_after_the_push_never_reaches_teardown[close]",
})


@pytest.fixture(scope="session", autouse=True)
def _wake_home_is_not_the_operators(tmp_path_factory: pytest.TempPathFactory):
    """LANE-B2-W1-b2-integrator-liveness: `lane_end_guard.py` leaves a wake file in the operator's private state
    directory for every closing HANDBACK line. A test that runs the real guard (`test_connection_loop.py`, through
    the real Stop hook) must not wake the operator's live integrator for a fixture lane, so the whole session writes
    its wakes under pytest's own temp directory. Subprocesses inherit it; a test that wants its own home sets one."""
    prior = os.environ.get("HARNESS_WAKE_DIR")
    os.environ["HARNESS_WAKE_DIR"] = str(tmp_path_factory.mktemp("integrator-wake"))
    try:
        yield
    finally:
        if prior is None:
            os.environ.pop("HARNESS_WAKE_DIR", None)
        else:
            os.environ["HARNESS_WAKE_DIR"] = prior


@pytest.fixture(scope="session", autouse=True)
def _git_hygiene_row_reads_no_live_git():
    """AMEND-1-BATCH-CUT-2026-10-17: the `git_hygiene` preflight row reads the LIVE branch list,
    origin and worktree list -- state no test owns, and which differs on every clone (CI's origin
    carries the integration branch `land` just pushed). Every test that runs the real preflight
    (a dry cut, a bundle fixture) would otherwise pass or fail on the box's git, not on its own
    subject. SESSION-scoped, because the bundle fixtures are module-scoped and cut before any
    function-scoped patch runs. The row has its own tests (`tests/test_git_hygiene_row.py`),
    which restore the real one. Patched on every module object the repo's three-root pythonpath
    may hold."""
    import sys
    mp = pytest.MonkeyPatch()
    for name in ("gen_handoff", "scripts.gen_handoff"):
        mod = sys.modules.get(name)
        if mod is not None and hasattr(mod, "_row_git_hygiene"):
            mp.setattr(
                mod, "_row_git_hygiene",
                lambda _root, _m=mod: _m.PreflightRow(
                    "git_hygiene", _m.PREFLIGHT_PASS, "tests/conftest.py",
                    "stubbed: a test reads no live git state"))
    try:
        yield
    finally:
        mp.undo()


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "operator_host: reads the operator's disk directly (sibling repos, PATH, this "
        "repo's own local main ref, extra worktrees) -- registered in tests/conftest.py; "
        "not a code defect, skipped where the operator host is absent",
    )
    config.addinivalue_line(
        "markers",
        "windows_only: skips on Ubuntu by a platform condition (registered in "
        "WINDOWS_ONLY_TESTS, applied at collection) -- Ubuntu deselects it, Windows runs it",
    )
    config.addinivalue_line(
        "markers",
        "windows_smoke: a cheap Windows-leg canary that runs on a Windows-sensitive landing "
        "alongside the windows_only tests",
    )
    extra = os.environ.get("CI_OS_MARKEXPR", "").strip()
    if extra:
        config.option.markexpr = compose_markexpr(config.option.markexpr, extra)


def compose_markexpr(existing: str, extra: str) -> str:
    """AND two `-m` expressions; an empty side contributes nothing."""
    existing, extra = (existing or "").strip(), (extra or "").strip()
    if existing and extra:
        return f"({existing}) and ({extra})"
    return existing or extra


# e2-os-split (ADR-127 AMENDMENT 2): the tests that skip on Ubuntu by a PLATFORM condition
# (os.name / sys.platform / winreg / platform.system), plus Windows-only shell availability.
# Derivation: 17 found statically by the gate's own detector (`ubuntu_skipping_tests` over
# tests/**/*.py: os.name/sys.platform/winreg skips, one helper-mediated -- tests/test_scope_guard.py's
# 8.3 short-name test), plus 13 added from the measured CI junit of run 39673029519 (ubuntu skipped,
# windows passed). Those 13 are all `[powershell]`-parametrised: the Windows PowerShell 5.1 binary
# `powershell` does not exist on Linux (only `pwsh`). The static gate CANNOT see that skip (a runtime
# shell lookup), so those 13 are registry data only, found by measurement.
# Posix-only skips (sys.platform == "win32") and tool-absence skips (git/bash/uv/claude/pwsh via
# shutil.which) are not here: ubuntu-latest has pwsh, so those still run on Ubuntu.
# Entries: 25 (24 exact node ids + 1 module, tests/test_dispatch_shim.py) expanding to
# 30 collected tests (the module entry = 6 of them); matches
# to-browser/DIGEST-TEST-EXECUTION-EVAL-2026-10-20-ANNEX.md Q4 (ubuntu 45 skipped vs windows 15
# => ~30 Windows-only).
# Entry grammar (the gate's `_covered`): exact node id, or a module path covering every test in it.
WINDOWS_ONLY_TESTS: frozenset[str] = frozenset({
    "tests/test_dispatch_launch.py::test_the_shim_needs_no_cap_and_passes_only_launch_and_the_contract",
    "tests/test_dispatch_launch.py::test_the_shim_keeps_dry_run_and_run",
    "tests/test_dispatch_launch.py::test_the_shim_passes_a_cap_through_only_when_given_and_returns_launchs_exit_code",
    "tests/test_dispatch_launch.py::test_the_shims_help_switch_prints_dispatchs_own_help",
    "tests/test_dispatch_py.py::test_an_unmounted_prompts_authority_is_a_different_refusal_from_a_missing_file",
    "tests/test_dispatch_shim.py",
    "tests/test_fleet_health.py::test_read_user_scope_returns_none_when_the_value_is_absent",
    "tests/test_fleet_health.py::test_read_user_scope_returns_none_when_the_key_cannot_be_opened",
    "tests/test_fleet_health.py::test_read_user_scope_returns_a_plain_string_value",
    "tests/test_fleet_health.py::test_read_user_scope_expands_a_reg_expand_sz_value",
    "tests/test_fleet_health.py::test_read_user_scope_treats_an_empty_value_as_absent",
    "tests/test_scope_guard.py::test_windows_8dot3_short_form_is_refused",
    "tests/test_hook_launcher.py::test_a_git_tree_without_the_launcher_fails_closed[powershell]",
    "tests/test_hook_launcher.py::test_inside_a_git_tree_the_hook_runs_as_if_invoked_directly[powershell-.]",
    "tests/test_hook_launcher.py::test_inside_a_git_tree_the_hook_runs_as_if_invoked_directly[powershell-sub/deeper]",
    "tests/test_hook_launcher.py::test_outside_every_git_tree_the_command_allows_silently[powershell]",
    "tests/test_hook_launcher.py::test_the_adr77_guard_runs_on_the_system_interpreter_and_blocks_in_zone_in_every_shell[powershell]",
    "tests/test_hook_launcher.py::test_the_hooks_exit_code_is_the_commands_exit_code[powershell]",
    "tests/test_hook_launcher.py::test_the_prompts_guard_command_parses_and_allows_under_powershell[powershell]",
    "tests/test_reuse_gate.py::test_in_a_lane_the_declared_command_allows_an_existing_file[powershell]",
    "tests/test_reuse_gate.py::test_in_a_lane_the_declared_command_denies_an_unnamed_new_file[powershell]",
    "tests/test_reuse_gate.py::test_outside_a_git_tree_the_declared_command_exits_cleanly[powershell]",
    "tests/test_scope_guard_hook_command.py::test_inside_the_repo_the_declared_command_runs_the_guard[powershell-.]",
    "tests/test_scope_guard_hook_command.py::test_inside_the_repo_the_declared_command_runs_the_guard[powershell-scripts]",
    "tests/test_scope_guard_hook_command.py::test_outside_a_git_tree_the_declared_command_exits_cleanly[powershell]",
})


def _windows_only_covered(nodeid: str, registry: frozenset[str]) -> bool:
    nodeid = nodeid.replace("\\", "/")
    module = nodeid.split("::", 1)[0]
    return (nodeid in registry or module in registry
            or f"{module}::<module>" in registry)


@dataclass(frozen=True)
class _CollectedMarker:
    nodeid: str
    marked: bool


def find_unregistered_drift(collected: list[_CollectedMarker],
                            registry: frozenset[str]) -> list[str]:
    """Registered <-> marked must agree in both directions. Returns registered node ids
    that WERE COLLECTED this run but carry no `operator_host` marker -- the unmarked-but-
    registered drift Done-contract item 2 requires this mechanism to report. Scoped to
    what was actually collected: a registered id absent from `collected` (a narrowed run,
    `-k`, a single node id) is not evidence of anything and must not be reported as drift.
    (Marked-but-unregistered is a *different* drift -- a new host witness the registry has
    not caught up to yet -- and is reported separately so the two failure modes are never
    conflated in one message.)
    """
    seen = {c.nodeid: c.marked for c in collected}
    return sorted(nodeid for nodeid in registry if nodeid in seen and not seen[nodeid])


def find_unregistered_markers(collected: list[_CollectedMarker],
                              registry: frozenset[str]) -> list[str]:
    """The mirror check: a test carries `operator_host` but is absent from the registration
    list -- the registry has drifted behind the marker, silently (a marker with no listing
    is invisible to anything that reads the registry rather than every test's own source)."""
    return sorted({c.nodeid for c in collected if c.marked} - registry)


@pytest.hookimpl(tryfirst=True)   # mark before the `-m` deselection runs
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    for item in items:
        if _windows_only_covered(item.nodeid, WINDOWS_ONLY_TESTS):
            item.add_marker(pytest.mark.windows_only)
    collected = [
        _CollectedMarker(item.nodeid.replace("\\", "/"),
                         item.get_closest_marker("operator_host") is not None)
        for item in items
    ]
    unmarked = find_unregistered_drift(collected, OPERATOR_HOST_TESTS)
    unregistered = find_unregistered_markers(collected, OPERATOR_HOST_TESTS)
    if not unmarked and not unregistered:
        return
    lines = ["operator_host registry/marker drift (tests/conftest.py):"]
    if unmarked:
        lines.append(f"  registered but unmarked ({len(unmarked)}):")
        lines += [f"    - {n}" for n in unmarked]
    if unregistered:
        lines.append(f"  marked but unregistered ({len(unregistered)}):")
        lines += [f"    - {n}" for n in unregistered]
    raise pytest.UsageError("\n".join(lines))


pytest_plugins = ["pytester"]
