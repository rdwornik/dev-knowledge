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

import argparse
import ast
import json
import os
import subprocess
import sys
import time
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


@pytest.fixture
def live_store():
    """The LIVE store, open for exactly as long as one test needs it.

    FUNCTION-SCOPED AND ALWAYS CLOSED, for a measured reason rather than a stylistic one. The
    six witnesses in this file's live-tree section each used to call `gs.ensure(REPO_ROOT)`
    and drop the result on the floor, which under CPython leaves the handle -- and the WAL
    sidecars -- open for the rest of the worker's life. One such test running anywhere in a
    worker turned that worker into a permanent reader of the store every OTHER worker also
    rebuilds. `tests/test_decision_coverage.py` reached the same shape from the same
    evidence; this is that fixture, applied where the leak actually was.

    It is still correct to hold nothing across tests even now that a held reader can no
    longer break a rebuild (`graph_store._write_graph`). The store fix removed the failure;
    leaking a handle per test would remain a leak.
    """
    store = gs.ensure(REPO_ROOT)
    try:
        yield store
    finally:
        store.close()


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


def test_a_stale_store_is_rebuilt_rather_than_served(tiny_repo: Path, tmp_path: Path):
    """THE TRIP for freshness: a store on disk is not, by itself, an answer.

    `ensure` must ask `is_stale` rather than `exists`. The shape this replaces served any
    readable store -- so every query after a source file changed answered from the old
    graph, and a stale graph does not fail loudly, it answers `orphan_census` and
    `task_coverage` with yesterday's edges.
    """
    db = tmp_path / "fresh" / "FPG.db"
    first = gs.ensure(tiny_repo, db)
    before = first.counts().nodes
    first.close()          # a reader holds the store open; the rebuild swaps it out
    _write(tiny_repo / "scripts" / "arrived_later.py", "def go():\n    return 2\n")
    os.utime(db, (time.time() - 3600, time.time() - 3600))   # the store predates the source

    assert gs.is_stale(tiny_repo, db), "the fixture is inert -- the store must read stale"
    assert gs.ensure(tiny_repo, db).counts().nodes > before, "a stale store was served"


def test_the_query_cli_answers_from_a_REBUILT_store_not_whatever_is_on_disk(
        tiny_repo: Path, tmp_path: Path):
    """The same trip one layer up, at the seam the three query hooks actually call.

    `_open` used to build only when the file was ABSENT, so a store that existed was served
    however old it was. This plants a new orphan after the store is built and asserts the
    census sees it -- which it can only do by rebuilding first.
    """
    db = tmp_path / "cli" / "FPG.db"
    gs.ensure(tiny_repo, db).close()
    _write(tiny_repo / "scripts" / "arrived_later.py", "def go():\n    return 2\n")
    os.utime(db, (time.time() - 3600, time.time() - 3600))

    args = argparse.Namespace(repo_root=str(tiny_repo), db=str(db))
    census = gq.orphan_census(tiny_repo, gq._open(args))
    assert "scripts/arrived_later.py" in {f.subject for f in census}


def _age(lock: Path) -> None:
    """Backdate a lock past its TTL -- i.e. make its builder look dead, without waiting."""
    stamp = time.time() - gs._LOCK_TTL_S - 5
    os.utime(lock, (stamp, stamp))


def test_a_waiter_never_removes_a_live_builders_rebuild_lock(tmp_path: Path):
    """THE TRIP, and it is a trip because the permissive direction passes either way.

    A second caller arriving on a held lock must come away with NOTHING -- no lock of its
    own, and above all the holder's lock still on disk. The shape this replaces let a waiter
    time out, rebuild without the lock, and then unlink the live builder's lock on its way
    out, which is the exact overlap the lock exists to prevent. Asserting only that the
    waiter fails to acquire would not catch that: it failed to acquire in the broken shape
    too, and then deleted the lock anyway.
    """
    lock = tmp_path / "FPG.rebuild-lock"
    held = gs.acquire_rebuild_lock(lock)
    assert held is not None

    assert gs.acquire_rebuild_lock(lock) is None
    assert lock.exists(), "a waiter removed the lock it does not hold"
    assert lock.read_text(encoding="utf-8") == held, "a waiter overwrote the live holder"


def test_an_overrun_builder_does_not_release_its_SUCCESSORS_lock(tmp_path: Path):
    """THE TRIP for the release side, and it is the one an existence check cannot see.

    A rebuild that outlives the TTL has its lock BROKEN and re-taken while it is still
    running, so by the time it releases, the file under that name belongs to someone else.
    `release_rebuild_lock` must therefore remove an acquisition, never a filename -- an
    unconditional unlink here deletes the successor's lock and lets a third caller build
    concurrently with the new holder, which is the overlap the lock exists to prevent.
    """
    lock = tmp_path / "FPG.rebuild-lock"
    slow = gs.acquire_rebuild_lock(lock)
    _age(lock)
    successor = gs.acquire_rebuild_lock(lock)          # a waiter breaks and re-takes it
    assert successor is not None and successor != slow

    gs.release_rebuild_lock(lock, slow)                # the slow builder finally finishes
    assert lock.exists(), "the overrun builder released a lock it no longer held"
    assert lock.read_text(encoding="utf-8") == successor

    gs.release_rebuild_lock(lock, successor)           # the real holder still can
    assert not lock.exists()


def test_an_expired_lock_is_broken_so_a_dead_builder_never_wedges_the_store(tmp_path: Path):
    """The converse: a lock whose builder died is honoured for its TTL and then taken.

    Without this leg the two fixes above would be indistinguishable from never breaking a
    lock at all -- which trades a race for a wedge, and a wedge blocks every commit here.
    """
    lock = tmp_path / "FPG.rebuild-lock"
    dead = gs.acquire_rebuild_lock(lock)
    _age(lock)

    taken = gs.acquire_rebuild_lock(lock)
    assert taken is not None and taken != dead, "the breaker did not take the lock"
    assert lock.read_text(encoding="utf-8") == taken


def test_a_concurrent_READER_cannot_break_a_rebuild(tiny_repo: Path, tmp_path: Path):
    """THE CROSS-WORKER COLLISION, reduced to the one fact that produces it.

    Under `-n auto` the workers share one store, because the store is keyed to the TREE and
    every worker is in the same tree. So a handle held open in worker A is, from worker B's
    point of view, a reader that will not let go -- and the publication path used to be
    `os.replace` over the live file, which on Windows FAILS while any process holds the
    destination or its `-wal`. Worker B's `ensure()` then raised `StoreUnreadable` after
    ~5 s of retries, and it did so in ITS OWN tests, naming a file worker B never touched.

    MEASURED, not argued (this worktree, 2026-09-13, before the fix): one held reader,
    one `ensure()` on a store marked stale ->

        StoreUnreadable: could not swap in the rebuilt store after 20 attempts
        ([WinError 32] ... FPG.db-wal). A reader is holding it open; retry, or close
        the reader.

    The retry loop was the mitigation and it is not sufficient: a reader held for the length
    of a test -- let alone leaked for the length of a session, which six witnesses in this
    file used to do -- outlives every bounded wait. This pins the GUARANTEE rather than
    today's timing: a reader is a normal condition for this store (the module's own pragma
    comment says so -- *"readers do not block writers"*), so a rebuild that a reader can
    break is the defect, not the reader.
    """
    db = tmp_path / "store" / "FPG.db"
    reader = gs.ensure(tiny_repo, db)                  # worker A's handle
    try:
        before = reader.counts().nodes
        _write(tiny_repo / "scripts" / "planted.py", "x = 1\n")
        stale = time.time() - 3600
        os.utime(db, (stale, stale))
        assert gs.is_stale(tiny_repo, db), "the fixture is inert -- the store must read stale"

        rebuilt = gs.ensure(tiny_repo, db)             # worker B, while A still holds it
        try:
            assert rebuilt.counts().nodes > before, "a stale store was served"
        finally:
            rebuilt.close()

        # AND THE HELD READER IS STILL USABLE. A "fix" that made the rebuild succeed by
        # breaking the reader would pass the assertion above and move the failure one worker
        # over, which is the whole class of defect this witness exists to close.
        #
        # USABLE, NOT FROZEN, and the distinction was MEASURED rather than assumed. This
        # first asserted the held reader still saw `before` -- over-specified: a WAL reader
        # not inside an explicit transaction takes a fresh snapshot per statement, so after
        # the rebuild commits it legitimately sees the NEW graph. Pinning the old number
        # would have pinned the file-swap implementation (where the reader kept the replaced
        # file by its descriptor) rather than the property that matters, which is that the
        # handle still answers.
        assert reader.counts().nodes > 0, "the rebuild invalidated a live reader"
    finally:
        reader.close()


def test_no_witness_here_leaks_a_live_store_handle():
    """The ratchet behind the witness above: a LEAKED reader is a session-long one.

    Six tests in this file's live-tree section called `gs.ensure(REPO_ROOT)` and never
    closed the result, so one of them running anywhere in a worker left that worker holding
    the live store for the rest of the run -- which is how a collision that needs two
    workers became reachable from a single test file. Reading the source is the only way to
    assert this: the leak is invisible at runtime, which is exactly why it survived.

    THE RULE IS STRUCTURAL, so it is asserted structurally. A test must not open the live
    store itself; it takes the `live_store` fixture, which closes in a `finally`. Parsing
    says that in one sentence -- a `gs.ensure(REPO_ROOT)` call lexically inside a `test_`
    function -- where matching text could not: a line-based version flagged the fixture's own
    (correct, closed) call and this docstring alongside the real leaks.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    leaked = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test_"):
            continue
        for call in ast.walk(node):
            if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                    and call.func.attr == "ensure"
                    and any(isinstance(arg, ast.Name) and arg.id == "REPO_ROOT"
                            for arg in call.args)):
                leaked.append(f"{node.name} (line {call.lineno})")
    assert leaked == [], (
        "these open the live store inside the test and never close it -- take the "
        "`live_store` fixture instead:\n  " + "\n  ".join(leaked))


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


def test_task_coverage_admits_a_row_file_as_its_own_claim(tiny_repo: Path, tiny_store):
    """A ROW FILE IS ITS OWN CLAIM -- `tasks/700-wired.md` IS `[#700]`.

    Found by the gate firing on a real sync merge, which staged ten `tasks/NNN-*.md` rows
    and refused every one for not being named by an open row. Asking a row file to be named
    by a row is asking it to name itself."""
    assert not gq.task_coverage(tiny_repo, tiny_store, staged=["tasks/700-wired.md"])


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True,
                   capture_output=True, text=True)


def test_task_coverage_refuses_a_claim_that_is_in_the_TREE_but_not_in_the_COMMIT(
        tiny_repo: Path, tmp_path: Path):
    """THE TRIP for the two-tree skew -- the bypass Terra pre-merge review found.

    The subject set is the INDEX and the `implements` relation comes from a graph built off
    the WORKING TREE, so a claim that exists only in the tree would otherwise cover a staged
    change the commit does not actually claim. Here `tasks/702-late.md` is an OPEN row naming
    `scripts/lonely.py` and it is UNTRACKED: the graph carries the edge, the commit carries
    nothing, and the gate must say so.

    Both directions, because the permissive half passes either way: staging the same row --
    changing nothing about the graph, only about what the commit contains -- must admit it.
    """
    _git(tiny_repo, "init", "-q")
    _git(tiny_repo, "config", "user.email", "lane@example.invalid")
    _git(tiny_repo, "config", "user.name", "lane")
    _git(tiny_repo, "add", "-A")
    _git(tiny_repo, "commit", "-qm", "the tree as it stands")

    _write(tiny_repo / "tasks" / "702-late.md", """\
---
id: "[#702]"
title: "the row that was never committed"
status: open
---

- [#702] names `scripts/lonely.py`.
""")
    db = tmp_path / "skew" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    store = gs.open_store(db)
    assert store.in_edges(store.key_for_path("scripts/lonely.py"), gq.COVERAGE_KINDS), \
        "the fixture is inert -- the tree must supply the edge for the trip to mean anything"

    findings = gq.task_coverage(tiny_repo, store, staged=["scripts/lonely.py"])
    assert [f.subject for f in findings] == ["scripts/lonely.py"]
    assert "tasks/702-late.md" in findings[0].evidence

    _git(tiny_repo, "add", "tasks/702-late.md")
    assert not gq.task_coverage(tiny_repo, store, staged=["scripts/lonely.py"])


def test_task_coverage_is_silent_during_a_merge(tiny_repo: Path, tiny_store, monkeypatch):
    """A MERGE IS TRANSPORT, NOT AUTHORSHIP -- the `block_commit_on_main` carve-out shape.

    The staged set of a merge is other branches' work. Refusing it would ask this branch to
    claim files it never wrote. The carve-out binds ONLY the git-derived staged set, so an
    explicit `staged=` list is still checked -- otherwise a merge would be a hole rather
    than a carve-out."""
    monkeypatch.setattr(gq, "_merge_in_progress", lambda root: True)
    assert gq.task_coverage(tiny_repo, tiny_store, staged=None) == []
    assert gq.task_coverage(tiny_repo, tiny_store, staged=["scripts/lonely.py"])


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


def test_the_live_orphan_census_reaches_zero_against_its_stated_class(live_store):
    """[#664]'s Done-when: `orphan_census` reaches 0 against its stated node class AFTER
    dispositions. The register is the mechanism; this is the assertion that it is complete."""
    findings = gq.orphan_census(REPO_ROOT, live_store)
    assert findings == [], "\n".join(f"{f.subject}: {f.evidence}" for f in findings)


def test_the_live_tree_carries_no_dangling_process_reference(live_store):
    assert gq.dangling_references(REPO_ROOT, live_store) == []


def test_the_disposition_register_names_no_file_that_is_gone():
    """A register is not allowed to rot into paper suppressions (ADR-75's decoration rule)."""
    missing = [path for path in gq.ORPHAN_DISPOSITIONS if not (REPO_ROOT / path).exists()]
    assert missing == [], f"dispositioned paths no longer on disk: {missing}"


#: The census's population-A orphan list, transcribed from
#: `docs/audits/2026-09-08-technical-process-trigger-census.md` §"A · scripts (20)". This is
#: intake #86's acceptance criterion 1 -- *"The sweep's output is the fixture. Every orphan
#: S-08…S-13 found by grep, the query finds. Seeded as test cases, not eyeballed."*
CENSUS_SCRIPT_ORPHANS = (
    # WIRED, not retired, and therefore absent for the CONVERSE of the reason the retirement
    # blocks below give. Both of `[#664]`'s ratified TRIGGER rows landed on 2026-09-13 (lane
    # `lane-x-664-delete-list-execution`), so the query no longer finds either and this fixture
    # must not claim it does. Same shape as `file_purpose_graph.py` below: named here rather
    # than dropped, because a fixture that silently shrinks is not a fixture.
    #   `scripts/archive_row_body.py`  -> the `row-archive-proof` pre-commit hook.
    #   `scripts/logs_retention.py`    -> the `SessionStart` hook in `.claude/settings.json`,
    #                                     which is `[#655]`'s missing production caller.
    "scripts/cost_usage_telemetry.py",
    "scripts/desired_state_loader.py",
    "scripts/export_backlog_view.py",
    "scripts/setup-fleet-scheduler.ps1",
    # RETIRED by lane `lane-x-664-delete-list-execution` ([#664]'s ratified DELETE list,
    # 2026-09-13), same rule as the [#734] block below and named separately so the two
    # retirements stay attributable. Each module left with its dedicated tests and its
    # `ORPHAN_DISPOSITIONS` entry. Evidence:
    # `docs/audits/2026-09-13-technical-lane-x-664-delete-list-execution-evidence.md`.
    #   `gen_trend_dashboard.py` then `gen_north_star.py` (+ `test_gen_trend_dashboard.py`,
    #   `test_trend_dashboard.py`, `test_gen_north_star.py`). The order is load-bearing rather
    #   than stylistic: the dashboard loads the north-star view through
    #   `importlib.util.spec_from_file_location`, an edge the static oracle cannot see and the
    #   FPG-1 graph can.
    #   `window_metrics.py` then `failed_set.py` (+ `test_window_metrics.py`,
    #   `test_failed_set.py`). Ordered for the same class of reason: `failed_set` was an orphan
    #   BY INHERITANCE from `window_metrics.py:359` and its own row said it is dispositioned
    #   WITH its caller and not before it.
    #   `nopack_sandbox.py` and `trace_writer.py` (+ `test_nopack_sandbox.py`,
    #   `test_trace_writer.py`). Unordered, and that is a fact rather than an omission: these
    #   two carried NO inbound edge of any kind, so neither could be the other's reason.
    # RETIRED by lane `lane-x-734-retire-stage-2` ([#734], the AX13-2 retire stage), not
    # dropped silently: `boundary_headers.py`, `boundary_report.py`, `cloud_provisioning.py`,
    # `probe_child_backlogs.py`, `seed_runbook.py`, `validate_onboarding_rulings.py` and
    # `desired_state_report.py` were
    # DELETED with their dedicated tests and their `ORPHAN_DISPOSITIONS` entries. A census
    # row leaves this fixture WITH the commit that retires its subject -- the same rule the
    # `file_purpose_graph.py` note below states for the converse (a row that acquired a
    # trigger). Evidence:
    # `docs/audits/2026-09-12-technical-lane-x-734-retire-stage-2-evidence.md`.
    # `desired_state_loader.py` was deleted in that same lane and RESTORED: the full suite
    # proved it live through an importlib load in `tests/test_membership_agreement.py`, an
    # edge the static oracle cannot see (ADR-89's declared limit). It stays a census row
    # because it stays a STATIC orphan -- being unreachable to the census and being dead are
    # different facts, and this row is now the repo's worked example of the difference.
    # `scripts/file_purpose_graph.py` is the census's twentieth and is DELIBERATELY absent:
    # `[#664]` wired it to the `graph-rebuild` hook, so it is triggered now. It is named
    # here rather than dropped, because a fixture that silently shrinks is not a fixture.
)


def test_the_query_finds_every_orphan_the_census_found(live_store):
    """intake #86 AC 1: the sweep's output is the fixture, seeded rather than eyeballed.

    Each census row must still be an orphan the query finds -- proved by it carrying a
    disposition, since an undispositioned one would already have REDDED the census test
    above. A row that acquired a real trigger since 2026-09-08 fails here and must be
    removed from the fixture WITH the commit that wired it, which is the point."""
    orphans = {f.subject for f in gq.orphan_census(REPO_ROOT, live_store, dispositions={})}
    missed = [path for path in CENSUS_SCRIPT_ORPHANS if path not in orphans]
    assert missed == [], f"the census found these and this query does not: {missed}"


def test_the_census_and_the_query_disagree_and_the_disagreement_is_REPORTED(live_store):
    """intake #86 AC 2: *"The converse is a finding, not a bug."*

    `scripts/single_flight.py` is an orphan this query finds and the 2026-09-08 census did
    not list. The criterion asks that such a disagreement be REPORTED and never silently
    reconciled, so this pins that its disposition SAYS SO -- the finding lives in the
    register where a reader meets it, not only in a lane artifact nobody reopens."""
    orphans = {f.subject for f in gq.orphan_census(REPO_ROOT, live_store, dispositions={})}
    assert "scripts/single_flight.py" in orphans
    assert "scripts/single_flight.py" not in CENSUS_SCRIPT_ORPHANS
    reason = gq.ORPHAN_DISPOSITIONS["scripts/single_flight.py"].reason
    assert "FINDING AGAINST THE CENSUS" in reason


def test_a_disposition_register_entry_cannot_manufacture_its_own_trigger(live_store):
    """The self-defeating loop this lane measured and fixed, pinned so it cannot return.

    `ORPHAN_DISPOSITIONS` is a dict whose KEYS are exact process paths. Read as call sites
    by the wiring loader, they made the register that RECORDS "this has no trigger"
    MANUFACTURE one for every row in it -- 25 dispositioned scripts came back triggered and
    the census's own 20 reported clean. The fix is `executable position`: a code string
    counts only inside a `Call` AND only when it is exactly a path."""
    reached = live_store.reachable(live_store.roots(), gq.TRIGGER_KINDS)
    laundered = [path for path in gq.ORPHAN_DISPOSITIONS
                 if (key := live_store.key_for_path(path)) and key in reached]
    assert laundered == [], (
        f"dispositioned processes reported as triggered -- the register is laundering its "
        f"own subject: {laundered}")


def test_every_disposition_carries_a_reason_and_an_owner():
    for path, disposition in gq.ORPHAN_DISPOSITIONS.items():
        assert len(disposition.reason) >= 20, f"{path}: reason is a token, not a reason"
        assert disposition.owner, f"{path}: no owner"


def test_the_persisted_live_store_answers_from_disk(live_store):
    """Clause 1 on the LIVE tree: node and edge counts read back from the artifact."""
    counts = live_store.counts()
    assert counts.nodes > 1900 and counts.edges > 12_000
    assert counts.kinds >= 12
    assert json.loads(json.dumps(counts.as_dict()))["nodes"] == counts.nodes
