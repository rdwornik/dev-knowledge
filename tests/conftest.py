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


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "operator_host: reads the operator's disk directly (sibling repos, PATH, this "
        "repo's own local main ref, extra worktrees) -- registered in tests/conftest.py; "
        "not a code defect, skipped where the operator host is absent",
    )


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


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
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
