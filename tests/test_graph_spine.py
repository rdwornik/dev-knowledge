"""RED-first witnesses for the FPG-1 delivery spine ([#664], ADR-108 §B).

Every test in this file was written and run RED before the module it exercises existed.
The four witnesses clause 1 and clause 2 of the frozen contract name:

  1. the persistence ROUND-TRIP -- counts read back from the store on disk, never from
     an in-memory build;
  2. `orphan_census` REFUSES an untriggered process;
  3. `task_coverage` REFUSES a staged file no OPEN row claims;
  4. `process_list` REFUSES a `dangling_reference` -- prose naming a process the graph lacks.

**A test that passes on conforming input is not a trip-test** (the contract's words). Each
refusal therefore carries BOTH directions: the planted non-conforming input that must refuse,
and the conforming input that must not -- a gate that can only fail is not a gate, and one
that can only pass is not a refusal.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import file_purpose_graph as fpg  # noqa: E402
import graph_queries as gq  # noqa: E402
import graph_store as gs  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------------------- the fixture


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


@pytest.fixture
def tiny_repo(tmp_path: Path) -> Path:
    """A minimal tree carrying one of every relation the spine reads.

    `wired.py` is named by a pre-commit hook (a TRIGGER) and imports `helper.py` (so
    `helper` is triggered transitively). `lonely.py` is named by nothing -- the orphan.
    Row `[#700]` is OPEN and names `wired.py`; row `[#701]` is CLOSED and names
    `lonely.py`, so a closed row must not confer coverage.
    """
    root = tmp_path / "tiny"
    _write(root / ".pre-commit-config.yaml", """\
repos:
  - repo: local
    hooks:
      - id: wired-gate
        name: the one wired gate
        entry: uv run --locked python scripts/wired.py
        language: system
""")
    _write(root / "scripts" / "wired.py", "import helper\n\n\ndef main():\n    helper.go()\n")
    _write(root / "scripts" / "helper.py", "def go():\n    return 1\n")
    _write(root / "scripts" / "lonely.py", "def nothing():\n    return 0\n")
    _write(root / "tasks" / "700-wired.md", """\
---
id: "[#700]"
title: "the open row"
status: open
---

- [#700] names `scripts/wired.py` and nothing else.
""")
    _write(root / "tasks" / "701-done.md", """\
---
id: "[#701]"
title: "the closed row"
status: done
---

- [#701] names `scripts/lonely.py`, but it is CLOSED.
""")
    _write(root / "ARCHITECTURE.md", "# Architecture\n\nThe gate is `scripts/wired.py`.\n")
    return root


@pytest.fixture
def tiny_store(tiny_repo: Path, tmp_path: Path):
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    return gs.open_store(db)


# ------------------------------------------------------- witness 1: the persistence round-trip


def test_store_round_trip_reads_counts_back_from_disk(tiny_repo: Path, tmp_path: Path):
    """Clause 1: counts come from the PERSISTED artifact, never from an in-memory build."""
    db = tmp_path / "store" / "FPG.db"
    written = gs.rebuild(tiny_repo, db)
    assert db.exists(), "rebuild must leave a queryable artifact on disk"

    # A SECOND process's worth of isolation: open the file fresh, with no build in scope.
    read_back = gs.open_store(db).counts()
    assert read_back.nodes == written.nodes
    assert read_back.edges == written.edges
    assert read_back.kinds == written.kinds
    assert read_back.nodes > 0 and read_back.edges > 0


def test_store_reports_the_wiring_roots_it_was_built_from(tiny_repo: Path, tmp_path: Path):
    """The store is self-describing: a reader never has to re-derive the roots."""
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    roots = gs.open_store(db).roots()
    assert fpg._file_key(".pre-commit-config.yaml") in roots


def test_store_path_resolves_outside_the_working_tree():
    """The store may never dirty `git status` -- it lives under the resolved git dir."""
    path = gs.store_path(REPO_ROOT)
    assert ".git" in path.parts, f"store must live under the git dir, got {path}"
    assert not path.is_relative_to(REPO_ROOT / "logs")


# ----------------------------------------------------- witness 2: orphan_census REFUSES


def test_orphan_census_refuses_an_untriggered_process(tiny_repo: Path, tiny_store):
    """THE TRIP. `scripts/lonely.py` is named by no wiring surface and by no triggered
    module, so the census must REFUSE -- not report."""
    findings = gq.orphan_census(tiny_repo, tiny_store)
    assert [f for f in findings if f.subject == "scripts/lonely.py"], (
        f"an untriggered script must be refused; got {findings}")


def test_orphan_census_admits_a_triggered_process(tiny_repo: Path, tiny_store):
    """THE OTHER DIRECTION. `wired.py` is named by a hook; `helper.py` is reached from it.
    A gate that can only fail is not a gate."""
    subjects = {f.subject for f in gq.orphan_census(tiny_repo, tiny_store)}
    assert "scripts/wired.py" not in subjects
    assert "scripts/helper.py" not in subjects, "transitive reach must count as triggered"


def test_orphan_census_admits_a_dispositioned_orphan(tiny_repo: Path, tiny_store):
    """A disposition with a reason clears the refusal -- intake #86's cadence, and the
    mechanism by which the census reaches 0 against its stated class."""
    register = {"scripts/lonely.py": gq.Disposition(
        reason="fixture", owner="the test")}
    findings = gq.orphan_census(tiny_repo, tiny_store, dispositions=register)
    assert not [f for f in findings if f.subject == "scripts/lonely.py"]


def test_orphan_census_cli_exits_non_zero_on_a_refusal(tiny_repo: Path, tmp_path: Path,
                                                       capsys):
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    code = gq.main(["orphan-census", "--repo-root", str(tiny_repo), "--db", str(db)])
    assert code != 0, "a query that reports without refusing does not discharge clause 2"
    assert "lonely" in capsys.readouterr().out


# ---------------------------------------------------- witness 3: task_coverage REFUSES


def test_task_coverage_refuses_a_staged_file_no_open_row_claims(tiny_repo: Path, tiny_store):
    """THE TRIP. `lonely.py` is claimed only by a CLOSED row -- at OPEN, not only at CLOSE."""
    findings = gq.task_coverage(tiny_repo, tiny_store, staged=["scripts/lonely.py"])
    assert [f for f in findings if f.subject == "scripts/lonely.py"]


def test_task_coverage_admits_a_file_an_open_row_names(tiny_repo: Path, tiny_store):
    assert not gq.task_coverage(tiny_repo, tiny_store, staged=["scripts/wired.py"])


def test_task_coverage_admits_a_file_that_names_its_own_open_row(tiny_repo: Path,
                                                                 tmp_path: Path):
    """The other direction of `implements`: a module whose own text names an OPEN row is
    claimed by it. This repo's every script already carries that convention."""
    _write(tiny_repo / "scripts" / "claims_back.py", '"""Built for [#700]."""\n')
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    store = gs.open_store(db)
    assert not gq.task_coverage(tiny_repo, store, staged=["scripts/claims_back.py"])


def test_task_coverage_cli_exits_non_zero_on_a_refusal(tiny_repo: Path, tmp_path: Path):
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    code = gq.main(["task-coverage", "--repo-root", str(tiny_repo), "--db", str(db),
                    "--staged", "scripts/lonely.py"])
    assert code != 0


# ---------------------------------------------------- witness 4: process_list REFUSES


def test_process_list_refuses_a_dangling_process_reference(tiny_repo: Path, tmp_path: Path):
    """THE TRIP. Prose naming a process the graph lacks is a `dangling_reference`."""
    (tiny_repo / "ARCHITECTURE.md").write_text(
        "# Architecture\n\nThe gate is `scripts/ghost.py`.\n", encoding="utf-8", newline="\n")
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    findings = gq.dangling_references(tiny_repo, gs.open_store(db))
    assert [f for f in findings if "ghost" in f.subject]


def test_process_list_admits_prose_naming_a_real_process(tiny_repo: Path, tiny_store):
    assert not gq.dangling_references(tiny_repo, tiny_store)


def test_process_list_enumerates_every_process_with_its_trigger(tiny_repo: Path, tiny_store):
    """The traversal that answers "all processes" -- the surface ARCHITECTURE.md Ch2 is
    RENDERED from. Rendering Ch2 is a different lane; producing the answer is this one."""
    rows = {row.path: row for row in gq.process_list(tiny_repo, tiny_store)}
    assert rows["scripts/wired.py"].triggered is True
    assert rows["scripts/lonely.py"].triggered is False
    assert ".pre-commit-config.yaml" in rows["scripts/wired.py"].trigger


def test_process_list_cli_exits_non_zero_on_a_dangling_reference(tiny_repo: Path,
                                                                 tmp_path: Path):
    (tiny_repo / "ARCHITECTURE.md").write_text(
        "# Architecture\n\nThe gate is `scripts/ghost.py`.\n", encoding="utf-8", newline="\n")
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    code = gq.main(["process-list", "--repo-root", str(tiny_repo), "--db", str(db)])
    assert code != 0


# --------------------------------------------------- the graph half: new inputs on FPG-1


def test_wiring_input_contributes_trigger_edges(tiny_repo: Path):
    graph = fpg.build(tiny_repo)
    kinds = {edge.kind for edge in graph.all_edges()}
    assert fpg.EDGE_TRIGGERS in kinds
    assert fpg.EDGE_IMPORTS in kinds


def test_task_implements_input_runs_from_an_OPEN_row_only(tiny_repo: Path):
    graph = fpg.build(tiny_repo)
    implements = [e for e in graph.all_edges() if e.kind == fpg.EDGE_IMPLEMENTS]
    assert (fpg._task_key("700"), fpg._file_key("scripts/wired.py")) in {
        (e.src, e.dst) for e in implements}
    assert fpg._task_key("701") not in {e.src for e in implements}, (
        "a CLOSED row confers no coverage -- at OPEN and not only at CLOSE")


def test_process_class_is_DERIVED_from_path_never_a_rival_node_kind():
    """intake #40 §1: layer is derived from kind and path, never hand-declared. A second
    vertex for one file is the defect `node_for_path` exists to prevent."""
    assert fpg.process_class("scripts/audit.py") == "script"
    assert fpg.process_class(".claude/commands/preflight.md") == "command"
    assert fpg.process_class(".claude/skills/verify/SKILL.md") == "skill"
    assert fpg.process_class("docs/decisions/ADR-118-one-graph-organs-are-views.md") is None
    assert fpg.NODE_FILE in {n.kind for n in
                             [fpg._file_node("scripts/audit.py")]}


def test_every_new_edge_kind_is_registered_with_both_render_phrases():
    """FPG-1's direction-invariant contract: an unregistered kind renders as a bare token."""
    for kind in (fpg.EDGE_TRIGGERS, fpg.EDGE_IMPORTS, fpg.EDGE_IMPLEMENTS):
        assert kind in fpg.EDGE_KINDS
        assert len(fpg.EDGE_KINDS[kind]) == 2


# ------------------------------------------------------------------- the live tree, measured


def test_the_live_orphan_census_reaches_zero_against_its_stated_class():
    """[#664]'s Done-when: `orphan_census` reaches 0 against its stated node class AFTER
    dispositions. The register is the mechanism; this is the assertion that it is complete."""
    store = gs.ensure(REPO_ROOT)
    findings = gq.orphan_census(REPO_ROOT, store)
    assert findings == [], "\n".join(f"{f.subject}: {f.evidence}" for f in findings)


def test_the_live_tree_carries_no_dangling_process_reference():
    store = gs.ensure(REPO_ROOT)
    assert gq.dangling_references(REPO_ROOT, store) == []


def test_the_disposition_register_names_no_file_that_is_gone():
    """A register is not allowed to rot into paper suppressions (ADR-75's decoration rule)."""
    missing = [path for path in gq.ORPHAN_DISPOSITIONS if not (REPO_ROOT / path).exists()]
    assert missing == [], f"dispositioned paths no longer on disk: {missing}"


def test_every_disposition_carries_a_reason_and_an_owner():
    for path, disposition in gq.ORPHAN_DISPOSITIONS.items():
        assert len(disposition.reason) >= 20, f"{path}: reason is a token, not a reason"
        assert disposition.owner, f"{path}: no owner"


def test_the_persisted_live_store_answers_from_disk():
    """Clause 1 on the LIVE tree: node and edge counts read back from the artifact."""
    store = gs.ensure(REPO_ROOT)
    counts = store.counts()
    assert counts.nodes > 1900 and counts.edges > 12_000
    assert counts.kinds >= 12
    assert json.loads(json.dumps(counts.as_dict()))["nodes"] == counts.nodes
