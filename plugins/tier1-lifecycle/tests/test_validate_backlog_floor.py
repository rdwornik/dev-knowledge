"""Unit tests for the PLUGIN FLOOR validate_backlog (plugins/tier1-lifecycle/scripts/).

#186 closure: the floor is the validator a child installs as its `validate-backlog` hook.
As of #186 it carries the hub's #156 task-graph checks (depends-on reference-existence +
no-cycle), VERBATIM-twinned from scripts/validate_backlog.py (carrier-doctrine, ADR-78).
These tests prove the floor REJECTS a dangling edge / cycle end-to-end on child-shaped
fixtures — not merely that the code was copied across. The hub's own #156 behaviour is
covered by tests/test_validate_backlog.py; this file guards the floor copy independently
so the two twins can't silently diverge.
"""

import importlib.util
from pathlib import Path

# plugins/tier1-lifecycle/tests/ -> plugins/tier1-lifecycle/scripts/validate_backlog.py
_FLOOR = Path(__file__).resolve().parent.parent / "scripts" / "validate_backlog.py"


def _load():
    spec = importlib.util.spec_from_file_location("floor_validate_backlog", _FLOOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


floor = _load()

# Child-shaped fixture: three tasks under one story; {dep1..dep3} inject trailing clauses.
DEP3 = """# child BACKLOG
## Big picture
A short paragraph.
**Themes (backbone):** Theme A
## Theme A
> As a persona, I want a goal.
### Story one
So that reasons hold.
- [#1] [P1][M] task one · Done when: x{dep1}
- [#2] [P1][M] task two · Done when: x{dep2}
- [#3] [P1][M] task three · Done when: x{dep3}
"""


def _run(dep1="", dep2="", dep3=""):
    text = DEP3.format(dep1=dep1, dep2=dep2, dep3=dep3)
    return floor.validate(*floor.parse(text))


def test_floor_valid_depends_on_passes():
    # edges into existing live ids, acyclic -> no hard fails
    hard, _ = _run(dep1=" · depends-on: #2", dep2=" · depends-on: #3")
    assert hard == []


def test_floor_dangling_edge_hard_fails():
    # THE #186 closure: a dangling depends-on edge is rejected by the floor
    hard, _ = _run(dep1=" · depends-on: #999")
    assert any("non-existent" in h and "999" in h for h in hard)


def test_floor_direct_cycle_hard_fails():
    hard, _ = _run(dep1=" · depends-on: #2", dep2=" · depends-on: #1")
    assert any("cycle" in h.lower() for h in hard)


def test_floor_indirect_cycle_hard_fails():
    # A -> B -> C -> A : a direct-only detector would miss this
    hard, _ = _run(dep1=" · depends-on: #2", dep2=" · depends-on: #3", dep3=" · depends-on: #1")
    assert any("cycle" in h.lower() for h in hard)


def test_floor_self_loop_hard_fails():
    hard, _ = _run(dep1=" · depends-on: #1")
    assert any("itself" in h.lower() for h in hard)


def test_floor_refs_prose_id_not_a_dependency():
    # clause-scoped parse: a #id only in refs/prose must NOT trip reference-existence
    hard, _ = _run(dep1=" · refs ADR-1, #999 (mentioned in prose, not a dependency)")
    assert not any("non-existent" in h for h in hard)


def test_floor_parse_deps_is_clause_scoped():
    deps = floor._parse_deps(
        "do x · Done when: y · refs ADR-1, #2 · depends-on: #3, #4 · note #2")
    assert deps == ["3", "4"]
