"""#206 / GAP-2: validate_backlog hub <-> plugin carrier-TWIN parity (stopgap).

The #156 task-graph machinery — `_DEPENDS_CLAUSE_RE` / `_DEPID_RE` / `_parse_deps` +
the two `_check_dep_*` fns — plus the done-marker + ADR-66 schema checks are mirrored
VERBATIM from `scripts/validate_backlog.py` into the plugin floor copy
`plugins/tier1-lifecycle/scripts/validate_backlog.py`. Under ADR-78 carrier doctrine the
floor is operator-generated / child-committed (not a shared module or symlink), so the two
copies are "kept in sync BY HAND" — a silent-drift edge the hub comment itself flags.

This test pins the twin: both modules, loaded independently, must produce IDENTICAL
findings on shared fixtures exercising the shared machinery (dep-cycle, dangling-dep,
serialize-group, done-marker), and the declared twin symbols must stay byte-identical.

NOTE (per the ticket): de-dup — a single shared module the floor imports — is the REAL
fix; this parity test is the STOPGAP that makes hand-mirror drift loud instead of silent.

Scope: this is the hub<->plugin TWIN parity (GAP-2), NOT the #185 architect-equilibrium
backstop — different numbering, different mechanism.
"""
from __future__ import annotations

import importlib.util
import inspect
import re
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_HUB_PATH = _REPO / "scripts" / "validate_backlog.py"
_PLUGIN_PATH = _REPO / "plugins" / "tier1-lifecycle" / "scripts" / "validate_backlog.py"

# The declared carrier-twin (the hub comment scopes it to exactly these symbols).
_TWIN_REGEXES = ("_DEPENDS_CLAUSE_RE", "_DEPID_RE")
_TWIN_FUNCS = ("_parse_deps", "_check_dep_references", "_check_dep_cycles")


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # so inspect.getsource / linecache resolve cleanly
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def hub():
    return _load(_HUB_PATH, "vb_hub")


@pytest.fixture
def plugin():
    return _load(_PLUGIN_PATH, "vb_plugin")


# --- shared corpus fixtures (dup-title-free so the hub-only #187 WARN never fires) ------
# `_DUP_MIN_TOKENS == 4`: keeping every task action <= 2 meaningful tokens means the hub's
# `_check_duplicate_titles` skips them entirely, so full-`validate` output is comparable.

_PREAMBLE = (
    "# .dev-knowledge BACKLOG\n\n"
    "## Big picture\n\n"
    "The backbone paragraph.\n\n"
)


def _backlog(task_lines: str, *, theme: str = "Theme A", story: str = "A user story") -> str:
    # story carries a stable [S<n>] id (#286) so the governance-backlog-story-id rule
    # (present in BOTH twins) does not fire and mask the machinery under test.
    return (_PREAMBLE
            + f"## {theme}\n\n### [S1] {story}\n\nSo that we have a goal.\n\n"
            + task_lines)


_FIXTURES = {
    "dep-cycle": _backlog(
        "- [#10] [P1][M] alpha step · Done when: ok · depends-on: #11\n"
        "- [#11] [P1][M] beta step · Done when: ok · depends-on: #10\n"),
    "dangling-dep": _backlog(
        "- [#10] [P1][M] alpha step · Done when: ok · depends-on: #999\n"),
    "serialize-group": _backlog(
        "- [#10] [P1][M] alpha step · Done when: ok · serialize-group: codeedge\n"
        "- [#11] [P1][M] beta step · Done when: ok · serialize-group: codeedge\n"),
    "done-marker": _backlog(
        "- [#10] [P1][M] alpha step · Done when: ok · status: done\n"),
}


def _findings(mod, corpus: str):
    """(hard, warn) from a module's own parse+validate over `corpus`."""
    return mod.validate(*mod.parse(corpus))


# --- (1) behavioral parity: identical findings on the shared fixtures -------------------

@pytest.mark.parametrize("name", sorted(_FIXTURES))
def test_hub_and_plugin_produce_identical_findings(hub, plugin, name):
    corpus = _FIXTURES[name]
    hub_out = _findings(hub, corpus)
    plugin_out = _findings(plugin, corpus)
    assert hub_out == plugin_out, f"carrier-twin drift on the {name} fixture"


def test_shared_fixtures_actually_exercise_the_machinery(hub):
    # Anti-vacuous guard: a parity test over fixtures that produce NO findings would pass
    # trivially even under total drift. Assert the defect fixtures really fire (and the
    # clean serialize-group one really stays empty), so the parity above has something to
    # compare. (Mirrors the audit's #141 skip-pass / non-empty-scope discipline.)
    assert any("cycle" in h for h in _findings(hub, _FIXTURES["dep-cycle"])[0])
    assert any("non-existent id #999" in h for h in _findings(hub, _FIXTURES["dangling-dep"])[0])
    assert any("done task present" in h for h in _findings(hub, _FIXTURES["done-marker"])[0])
    assert _findings(hub, _FIXTURES["serialize-group"]) == ([], [])


# --- (2) negative control: weakened plugin regex MUST break parity ----------------------

def test_parity_catches_depends_clause_regex_drift(hub, plugin, monkeypatch):
    # Weaken the plugin's `_DEPENDS_CLAUSE_RE` exactly as a careless "simplification" would:
    # drop the clause-boundary capture `[^·]*` -> `.*`, so the depends-on clause bleeds past
    # the next `·` into a trailing `· refs #N`. That id (#777, not a live task) then registers
    # as a phantom dependency -> the plugin invents a dangling finding the hub does not.
    corpus = _backlog(
        "- [#10] [P1][M] alpha step · Done when: ok · depends-on: #11 · refs #777\n"
        "- [#11] [P1][M] beta step · Done when: ok\n")
    # the unweakened twin agrees (clause-scoped: only #11 is a dependency, which exists)
    assert _findings(hub, corpus) == _findings(plugin, corpus)
    monkeypatch.setattr(plugin, "_DEPENDS_CLAUSE_RE",
                        re.compile(r"·\s*depends-on\s*:\s*(.*)"))
    # now they diverge -> the parity test has teeth (it would catch real hand-mirror drift)
    assert _findings(hub, corpus) != _findings(plugin, corpus)
    assert any("non-existent id #777" in h
               for h in _findings(plugin, corpus)[0])  # the drift the hub never sees


# --- source-identity drift guard on the declared twin (complements the behavioral pair) -

def test_declared_twin_symbols_are_byte_identical(hub, plugin):
    # The behavioral fixtures can only exercise the paths they hit; this guard catches drift
    # in ANY twin logic (e.g. a tweak to the cycle DFS no fixture covers) by asserting the
    # declared twin's regex patterns + function sources are character-for-character equal.
    for name in _TWIN_REGEXES:
        assert getattr(hub, name).pattern == getattr(plugin, name).pattern, \
            f"twin regex {name} drifted between hub and plugin"
    for name in _TWIN_FUNCS:
        assert inspect.getsource(getattr(hub, name)) == inspect.getsource(getattr(plugin, name)), \
            f"twin function {name} drifted between hub and plugin"
