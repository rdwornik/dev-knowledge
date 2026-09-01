"""Coverage for scripts/boot_frontier.py -- the v7 BOOT-INVERSION frontier/scoring/batch
library (contract lane-b-2-handoff-v7, item 2: "the hard part is a library, not a skill").
"""
from __future__ import annotations

from pathlib import Path

import pytest

import boot_frontier as bootf
import gen_task_tree as gtt

REPO_ROOT = Path(__file__).resolve().parent.parent


def _row(id_, raw_tail="", priority="P2"):
    """A minimal open TaskRow: `- [#N] [P2] title <tail>`."""
    raw = f"- [#{id_}] [{priority}] row {id_}{raw_tail}"
    return gtt.TaskRow(id=id_, raw=raw, theme=None, story=None)


# --- depends_on_ids -----------------------------------------------------------------------

def test_depends_on_ids_absent():
    row = _row(1)
    assert bootf.depends_on_ids(row.raw) == frozenset()


def test_depends_on_ids_single():
    row = _row(1, " · depends-on: #2")
    assert bootf.depends_on_ids(row.raw) == frozenset({2})


def test_depends_on_ids_multiple():
    row = _row(1, " · depends-on: #2, #3")
    assert bootf.depends_on_ids(row.raw) == frozenset({2, 3})


# --- build_dependency_graph / unblocked_frontier ------------------------------------------

def test_frontier_row_with_no_dependency_is_unblocked():
    rows = [_row(1)]
    frontier = bootf.unblocked_frontier(rows)
    assert [r.id for r in frontier] == [1]


def test_frontier_excludes_row_blocked_by_open_dependency():
    # #2 depends on #1, and #1 is still open -> #2 is blocked, #1 is the frontier.
    rows = [_row(1), _row(2, " · depends-on: #1")]
    frontier = bootf.unblocked_frontier(rows)
    assert [r.id for r in frontier] == [1]


def test_frontier_includes_row_whose_dependency_already_closed():
    # #2 depends on #99, which is NOT in the open set (tasks/ carries open rows only, so an
    # absent id is already closed) -> #2 is unblocked.
    rows = [_row(2, " · depends-on: #99")]
    frontier = bootf.unblocked_frontier(rows)
    assert [r.id for r in frontier] == [2]


def test_frontier_chain_only_root_unblocked():
    # 3 -> 2 -> 1 (each depends on the previous); only #1 has no open dependency.
    rows = [_row(1), _row(2, " · depends-on: #1"), _row(3, " · depends-on: #2")]
    frontier = bootf.unblocked_frontier(rows)
    assert [r.id for r in frontier] == [1]


def test_cycle_raises_cycle_error():
    rows = [_row(1, " · depends-on: #2"), _row(2, " · depends-on: #1")]
    with pytest.raises(bootf.CycleError):
        bootf.unblocked_frontier(rows)


# --- scoring seam --------------------------------------------------------------------------

def test_default_score_orders_by_priority_band_first():
    p1 = _row(1, priority="P1")
    p3 = _row(2, priority="P3")
    scored = bootf.score_frontier([p3, p1], all_open_rows=[p3, p1])
    assert [r.id for r in scored] == [1, 2]


def test_default_score_ties_broken_by_contention_then_id():
    # Same priority band; #10 and #11 share a serialize-group (contention 1 each), #12 does
    # not (contention 0) -- higher contention sorts first as the [#566] tiebreak.
    a = _row(10, " · serialize-group: g", priority="P2")
    b = _row(11, " · serialize-group: g", priority="P2")
    c = _row(12, priority="P2")
    scored = bootf.score_frontier([c, a, b], all_open_rows=[c, a, b])
    assert [r.id for r in scored] == [10, 11, 12]


def test_scorer_is_swappable():
    """The scoring seam accepts a caller-supplied ScoreFn -- the declared, swappable
    interface BOOT-R1's survey will eventually pin (contract item 5)."""
    rows = [_row(1), _row(2)]
    reverse_by_id = lambda row, contention: -row.id  # noqa: E731 -- test-local scorer
    scored = bootf.score_frontier(rows, all_open_rows=rows, scorer=reverse_by_id)
    assert [r.id for r in scored] == [2, 1]


# --- batch selection: disjointness / width / ledger -----------------------------------------

def test_select_batch_respects_ledger_bound():
    rows = [_row(i) for i in range(1, 10)]  # 9 candidates
    batch = bootf.select_batch(rows, width=6, ledger_bound=5)
    assert len(batch.selected) == 5
    assert batch.truncated_by_ledger is True


def test_select_batch_respects_width_when_tighter_than_ledger():
    rows = [_row(i) for i in range(1, 10)]
    batch = bootf.select_batch(rows, width=3, ledger_bound=5)
    assert len(batch.selected) == 3


def test_select_batch_disjointness_holds_back_second_of_same_group():
    a = _row(1, " · serialize-group: g")
    b = _row(2, " · serialize-group: g")
    c = _row(3)
    batch = bootf.select_batch([a, b, c], width=6, ledger_bound=5)
    assert [r.id for r in batch.selected] == [1, 3]
    assert [r.id for r in batch.held_back_disjointness] == [2]


def test_select_batch_not_truncated_when_fewer_rows_than_cap():
    rows = [_row(1), _row(2)]
    batch = bootf.select_batch(rows, width=6, ledger_bound=5)
    assert batch.truncated_by_ledger is False
    assert len(batch.selected) == 2


def test_select_batch_never_only_easy():
    """An unblocked P3 must not crowd out an unblocked P1 for a ledger slot -- the primary
    sort key is the operator-set priority band, not size/effort (contract item 6)."""
    p3s = [_row(i, priority="P3") for i in range(1, 6)]
    p1 = _row(6, priority="P1")
    scored = bootf.score_frontier([*p3s, p1], all_open_rows=[*p3s, p1])
    batch = bootf.select_batch(scored, width=6, ledger_bound=1)
    assert [r.id for r in batch.selected] == [6]


def test_batch_proposal_never_executes_anything():
    """BatchProposal carries no dispatch hook -- it is data, and render_proposal states the
    GO requirement explicitly (AUT-R1 Phase 4)."""
    batch = bootf.select_batch([_row(1)])
    assert not hasattr(batch, "dispatch")
    assert "operator GO" in bootf.render_proposal(batch)


def test_render_proposal_empty_batch():
    batch = bootf.select_batch([])
    assert "no batch to propose" in bootf.render_proposal(batch)


# --- live-repo smoke tests (read-only) -------------------------------------------------------

def test_load_open_rows_reads_the_live_tree():
    rows = bootf.load_open_rows(REPO_ROOT)
    assert isinstance(rows, list)
    assert all(isinstance(r, gtt.TaskRow) for r in rows)


def test_propose_batch_on_live_repo_obeys_the_ledger_bound():
    try:
        batch = bootf.propose_batch(REPO_ROOT)
    except bootf.CycleError as exc:
        pytest.fail(f"live tasks/ depends-on graph has a cycle: {exc}")
    assert len(batch.selected) <= bootf.LEDGER_BOUND
    assert len(batch.selected) <= bootf.BATCH_WIDTH_MAX
    groups = [gtt.derive_serialize_group(r.raw) for r in batch.selected]
    groups = [g for g in groups if g is not None]
    assert len(groups) == len(set(groups))  # disjointness holds on the live proposal
