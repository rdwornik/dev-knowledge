#!/usr/bin/env python
"""boot_frontier.py -- the deterministic library behind /boot-session's PROPOSED NEXT BATCH.

WHY A LIBRARY, NOT A SKILL (contract lane-b-2-handoff-v7, item 2). The unblocked frontier,
the scoring seam and batch selection are the HARD part of the v7 BOOT-INVERSION, and a
prompt that computes a frontier is a frontier nobody can test. This module is importable and
unit-tested; `.claude/commands/boot-session.md` only NARRATES its output.

THE GRAPH. `tasks/*.md` carries OPEN rows only (`BACKLOG.md` is a one-line VIEW of the same
tree; done items LEAVE it, ADR-65). A row's `depends-on:` clause (`derive_depends_on`,
already parsed by `gen_task_tree.py`) names another row's id. Because closed rows are absent
from the tree, a `depends-on` id that does not resolve to a currently-open row is ALREADY
satisfied -- so an edge is added only between two rows that are BOTH still open. The
UNBLOCKED FRONTIER is exactly the in-degree-0 set of that graph.

LIBRARY-FIRST -- rustworkx, reused, not re-declared. `pyproject.toml` already carries it for
FPG-1 (`scripts/file_purpose_graph.py`) on the operator's A3 mandate, hash-pinned in
`uv.lock` from a prebuilt wheel (measured 2026-08-29, `rustworkx-0.18.1-cp310-abi3-win_amd64`).
This module follows that precedent rather than adding a second graph dependency.

THE SCORING RULE IS A DECLARED SEAM, NOT INVENTED HERE (contract item 5). BOOT-R1's survey of
scoring models is still RUNNING. `default_score` wraps `gen_task_tree.rank_key` -- the
already-ruled [#566] axis (P-enum primary, constraint-contention tiebreak, id-as-age floor)
-- rather than inventing a second scoring rule to fill the gap. `ScoreFn` is a named,
swappable seam: BOOT-R1 pins the permanent rule; until then this is the documented
placeholder, and it is the one axis the repo has already ruled, not a new one.

BATCH SELECTION -- disjointness, width, ledger (contract item 6, citing AUT-R1's
self-planning axis: `docs/audits/2026-08-29-technical-aut-r1-autonomous-sdlc-orchestration.md`).

  * DISJOINTNESS -- at most one selected row per `serialize-group`. That is the group's own
    declared meaning (a shared file/resource serializes lanes), not an invented rule; two
    rows in the same group cannot run as parallel lanes.
  * WIDTH -- capped at `BATCH_WIDTH_MAX` (ADR-110's 4-6 lane batch ceiling, "bounded by
    integration capacity, which is serial").
  * LEDGER BOUND -- capped at `LEDGER_BOUND` (the night-batch protocol's ~5-proposals cap,
    PLAYBOOK Ch8, cited by AUT-R1 as the standing "never endless" precedent).
  * NEVER ONLY-EASY, by construction -- the scoring seam's primary key is the operator-set
    [P1..P3] band, never size/effort, so a trivial low-priority row can never crowd out a
    harder unblocked P1 for a batch slot.
  * HUMAN GO -- `BatchProposal` is a PROPOSAL. Nothing in this module or its CLI dispatches
    anything; AUT-R1 Phase 4: "adjudication stays a human act... nothing merges unattended."

READ-ONLY and Layer-2 (ADR-28/36): reads `tasks/` via `gen_task_tree`'s own reassembly, writes
nothing, drives no state.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import rustworkx

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
try:
    import gen_task_tree as _gtt  # the scripts/-relative form -- the SAME module object a
                                   # sibling test's bare `import gen_task_tree` resolves to,
                                   # since pytest's pythonpath already carries `scripts`
                                   # (pyproject.toml). `from scripts import gen_task_tree`
                                   # would load a SECOND module object under Python's implicit
                                   # namespace-package resolution (`scripts` has no
                                   # `__init__.py`), and a TaskRow built by one is not an
                                   # `isinstance` of the other's dataclass.
except ImportError:  # boot_frontier imported as `scripts.boot_frontier` with only the repo
                     # root on sys.path (no direct scripts/ entry) -- fall back to the
                     # package-relative form.
    from scripts import gen_task_tree as _gtt

TASKS_RELPATH = "tasks"

#: ADR-110's 4-6 lane batch ceiling -- "bounded by integration capacity, which is serial".
BATCH_WIDTH_MAX = 6
#: The night-batch protocol's ~5-proposals/night cap (PLAYBOOK Ch8), cited by AUT-R1 as the
#: standing "never endless" precedent this batch bound follows rather than re-derives.
LEDGER_BOUND = 5

_DEPENDS_ON_ID_RE = re.compile(r"#(\d+)")


class CycleError(Exception):
    """The depends-on graph is not a DAG -- the frontier's ground truth is uncomputable."""


def depends_on_ids(raw: str) -> frozenset[int]:
    """Every row id named in a task line's `depends-on:` clause. Empty when the clause is
    absent. Reuses `gen_task_tree.derive_depends_on` for the clause text rather than
    re-parsing the row line."""
    clause = _gtt.derive_depends_on(raw)
    if not clause:
        return frozenset()
    return frozenset(int(m) for m in _DEPENDS_ON_ID_RE.findall(clause))


def load_open_rows(repo_root: Path | None = None) -> list[_gtt.TaskRow]:
    """The OPEN queue (DEFER-marked rows excluded), read from the `tasks/` source tree.

    Mirrors `gen_task_tree._cmd_rank`'s own read path exactly (`tasks/` is the source of
    truth post-flip; `BACKLOG.md` is its one-line projection) so this module cannot drift
    from the ranking CLI's notion of "open".
    """
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    tasks_dir = root / TASKS_RELPATH
    model = _gtt.parse_backlog(_gtt.reassemble_from_tree(tasks_dir))
    return _gtt.open_task_rows(_gtt._task_rows(model))


def build_dependency_graph(
    rows: list[_gtt.TaskRow],
) -> tuple[rustworkx.PyDiGraph, dict[int, int]]:
    """A `rustworkx.PyDiGraph` over OPEN rows, node payload = the `TaskRow`.

    An edge dependency -> dependent is added ONLY when the dependency is ITSELF one of
    `rows` (i.e. still open). A `depends-on` id absent from `rows` names an already-closed
    row (tasks/ carries OPEN rows only) and is satisfied by construction -- adding an edge
    for it would block a row on work that is already done.
    """
    graph: rustworkx.PyDiGraph = rustworkx.PyDiGraph()
    index_by_id: dict[int, int] = {}
    for row in rows:
        index_by_id[row.id] = graph.add_node(row)
    open_ids = set(index_by_id)
    for row in rows:
        for dep_id in depends_on_ids(row.raw):
            if dep_id in open_ids and dep_id != row.id:
                graph.add_edge(index_by_id[dep_id], index_by_id[row.id], None)
    return graph, index_by_id


def topological_order(graph: rustworkx.PyDiGraph) -> list[int]:
    """The graph's rustworkx topological node-index order.

    Raises `CycleError` on a cycle rather than returning a partial order: a cyclic
    depends-on graph has no well-defined frontier, and reporting one anyway would be a
    verdict drawn from an uncomputable ground truth (the Z-G4 class `funnel_lifecycle`
    already applies elsewhere in this repo).
    """
    try:
        return list(rustworkx.topological_sort(graph))
    except rustworkx.DAGHasCycle as exc:
        raise CycleError(f"depends-on graph has a cycle: {exc}") from exc


def unblocked_frontier(rows: list[_gtt.TaskRow]) -> list[_gtt.TaskRow]:
    """Every open row with no still-open `depends-on` target, in rustworkx topological order.

    The topological sort is run (and its DAGHasCycle raised as `CycleError`) even though
    the in-degree-0 set does not itself need one: proving the graph IS a DAG is part of
    this function's contract, not an optimization skipped when convenient.
    """
    graph, _index_by_id = build_dependency_graph(rows)
    order = topological_order(graph)
    return [graph[i] for i in order if graph.in_degree(i) == 0]


# --- the scoring seam (declared, swappable, pinned later -- BOOT-R1) ------------------------

ScoreFn = Callable[[_gtt.TaskRow, "dict[int, int]"], tuple]


def default_score(row: _gtt.TaskRow, contention: dict[int, int]) -> tuple:
    """The CURRENT default: `gen_task_tree.rank_key`, the already-ruled [#566] axis.

    Lower sorts first. Reused rather than reinvented -- see the module docstring's "THE
    SCORING RULE" section for why a new model is not invented here.
    """
    return _gtt.rank_key(row, contention.get(row.id, 0))


def score_frontier(
    frontier: list[_gtt.TaskRow],
    all_open_rows: list[_gtt.TaskRow],
    scorer: ScoreFn = default_score,
) -> list[_gtt.TaskRow]:
    """`frontier`, sorted by `scorer`. Contention is measured over the WHOLE open queue
    (`all_open_rows`), matching `gen_task_tree.rank_tasks`'s own semantics -- "how much
    parallel work a serialize-group is holding" is a fact about the queue, not the frontier
    subset alone.
    """
    contention = _gtt.contention_scores(all_open_rows)
    return sorted(frontier, key=lambda row: scorer(row, contention))


# --- batch selection: disjointness, width, ledger --------------------------------------------


@dataclass(frozen=True)
class BatchProposal:
    """A PROPOSAL, never a dispatch.

    AUT-R1's self-planning axis (Phase 4): "adjudication stays a human act... nothing
    merges unattended." Every consumer of this dataclass renders an explicit GO ask before
    any lane is booted from it -- nothing here executes.
    """

    selected: list[_gtt.TaskRow]
    held_back_disjointness: list[_gtt.TaskRow]
    truncated_by_ledger: bool
    width: int
    ledger_bound: int


def select_batch(
    scored_frontier: list[_gtt.TaskRow],
    *,
    width: int = BATCH_WIDTH_MAX,
    ledger_bound: int = LEDGER_BOUND,
) -> BatchProposal:
    """Greedy pick over `scored_frontier` (assumed pre-sorted, best first) under two bounds.

    DISJOINTNESS: at most one selected row per `serialize-group` -- two rows sharing a group
    cannot run as parallel lanes, by the group's own declared meaning. A row held back this
    way is recorded, never silently dropped.

    WIDTH / LEDGER: the batch never exceeds `min(width, ledger_bound)` rows -- AUT-R1's
    "never endless" bound. `truncated_by_ledger` is True when at least one row beyond the cap
    would otherwise have been eligible, so a batch that stopped early because more work
    exists is distinguishable from one that ran out of unblocked work.
    """
    cap = min(width, ledger_bound)
    selected: list[_gtt.TaskRow] = []
    held_back: list[_gtt.TaskRow] = []
    truncated = False
    used_groups: set[str] = set()
    for row in scored_frontier:
        group = _gtt.derive_serialize_group(row.raw)
        blocked_by_group = group is not None and group in used_groups
        if len(selected) >= cap:
            if blocked_by_group:
                held_back.append(row)
            else:
                truncated = True
            continue
        if blocked_by_group:
            held_back.append(row)
            continue
        selected.append(row)
        if group is not None:
            used_groups.add(group)
    return BatchProposal(
        selected=selected,
        held_back_disjointness=held_back,
        truncated_by_ledger=truncated,
        width=width,
        ledger_bound=ledger_bound,
    )


def propose_batch(
    repo_root: Path | None = None,
    *,
    width: int = BATCH_WIDTH_MAX,
    ledger_bound: int = LEDGER_BOUND,
    scorer: ScoreFn = default_score,
) -> BatchProposal:
    """The end-to-end read: load -> frontier -> score -> select. Raises `CycleError`."""
    rows = load_open_rows(repo_root)
    frontier = unblocked_frontier(rows)
    scored = score_frontier(frontier, rows, scorer=scorer)
    return select_batch(scored, width=width, ledger_bound=ledger_bound)


def render_proposal(batch: BatchProposal) -> str:
    """Flat, un-padded report text (no column padding, per the output-formatting rule)."""
    lines = [
        f"boot_frontier: {len(batch.selected)} proposed (width<={batch.width}, "
        f"ledger<={batch.ledger_bound}) -- PROPOSAL ONLY; requires an explicit operator GO "
        f"before any lane dispatches (AUT-R1 Phase 4: adjudication stays a human act)",
    ]
    for row in batch.selected:
        lines.append(
            f"  [#{row.id}] {_gtt.derive_priority(row.raw) or 'P?'} · "
            f"{_gtt.derive_title(row.raw)}"
        )
    if batch.held_back_disjointness:
        lines.append(
            "  held back (serialize-group disjointness): "
            + ", ".join(f"#{row.id}" for row in batch.held_back_disjointness)
        )
    if batch.truncated_by_ledger:
        lines.append(
            "  more unblocked work exists beyond the ledger bound -- not endless by design"
        )
    if not batch.selected:
        lines.append("  nothing unblocked and eligible -- no batch to propose")
    return "\n".join(lines)


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="v7 BOOT-INVERSION: unblocked frontier + scoring + batch proposal "
        "(read-only, PROPOSAL ONLY -- never dispatches)."
    )
    ap.add_argument("--repo", default=str(_REPO_ROOT), help="repo root (default: this hub)")
    ap.add_argument("--frontier", action="store_true", help="print the raw unblocked frontier, unscored")
    args = ap.parse_args(argv)
    root = Path(args.repo)
    try:
        rows = load_open_rows(root)
        frontier = unblocked_frontier(rows)
    except CycleError as exc:
        print(f"boot_frontier: ground truth uncomputable: {exc}", file=sys.stderr)
        return 2
    if args.frontier:
        print(f"boot_frontier: {len(frontier)} unblocked row(s) in {len(rows)} open")
        for row in frontier:
            print(f"  [#{row.id}] {_gtt.derive_title(row.raw)}")
        return 0
    scored = score_frontier(frontier, rows)
    batch = select_batch(scored)
    print(render_proposal(batch))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
