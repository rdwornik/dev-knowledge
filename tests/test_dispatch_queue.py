"""`scripts/dispatch.py queue` -- the dispatcher's hand procedure becomes code (LANE-5B2-9).

RED-FIRST acceptance tests, named in the words of the contract's Done-contract and Value line.
N1's dispatcher ran the queue BY HAND: a RAM gate read by eye, a dependency hold worked out by
re-reading the integrator's prose receipts every tick, and 13 orphan watcher loops that outlived
their own usefulness. Each class of unit test below is one of those failures made mechanical:

  * the RAM gate (below the floor holds)                       -> test_decide_lane_ram_gate_*
  * the dependency hold (an integrator receipt fixture)         -> test_dependency_status_*,
                                                                    test_decide_lane_dependency_*
  * `serialize-group` (never two members live)                  -> test_serialize_group_*
  * the substrate column (`Dispatch-Codespace` routes away)      -> test_lane_substrate_*,
                                                                    test_decide_lane_routes_codespace*
  * repair relaunch into the EXISTING worktree                   -> test_build_repair_plan_*,
                                                                    test_repair_lane_*
  * every watcher carries a self-deadline                        -> test_watch_queue_*

Nothing here spawns a real process: `spawn`, `on_fire`, `sleep`/`clock`, `states_fn`,
`live_slugs_fn`, `local_live_count_fn` and `free_mb_fn` are injected throughout, the same
discipline `test_dispatch_launch.py` already applies to `launch_lane`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

import psutil
import pytest
from click.testing import CliRunner

import dispatch as d


@pytest.fixture(autouse=True)
def receipts(tmp_path, monkeypatch):
    """Isolate `launch_lane`'s receipt/lock reads from the real (shared) `logs/receipts/` --
    the same discipline `test_dispatch_launch.py` applies. Without this, the CLI-level queue
    test below collides with any real or leftover `LAUNCH-LANE-A.json` on disk."""
    target = tmp_path / "receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(target))
    return target


# --- fixtures: the minimal contract grammar `queue` reads ---------------------------------------

def _contract(tmp_path: Path, filename: str, slug: str, *, starts_after: tuple = (),
             serialize_group: Optional[str] = None, head: str = "claude",
             substrate_label: Optional[str] = None, model: str = "claude-sonnet-5") -> Path:
    """A synthetic `LANE-*.md`: the `## Dispatch` fence (read for its head, never run), the
    `**Starts after**` / `serialize-group:` clauses plan_lint's own grammar reads, and the slug
    pairing line every contract carries. `head="dispatch-codespace"` writes the real codespace
    verb's own line shape (`Dispatch-Codespace <file> -Slug <slug> ...`); any other head writes a
    `claude --bg` line naming that head's program."""
    lines = [f"# LANE {slug} -- a synthetic lane\n",
             f"| Model | Mode | Effort |\n|---|---|---|\n| {model} | execute | high |\n"]
    if substrate_label:
        lines.append(f"rendered-by: test, substrate: {substrate_label}\n")
    if head == "dispatch-codespace":
        dispatch_line = f"Dispatch-Codespace {filename} -Slug {slug} -Model {model} -Detach"
    elif head == "codex":
        dispatch_line = f'codex exec -m {model} --worktree "..."'
    else:
        dispatch_line = (f'claude --bg -n {slug} --model {model} --effort high '
                         f'--permission-mode bypassPermissions --worktree {slug} "..."')
    lines.append(f"## Dispatch\n\n```\n{dispatch_line}\n```\n")
    if starts_after:
        joined = " and ".join(f"`{dep}`" for dep in starts_after)
        verb = "is" if len(starts_after) == 1 else "are"
        lines.append(f"**Starts after {joined} {verb} merged.**\n")
    if serialize_group:
        lines.append(f"serialize-group: {serialize_group}\n")
    lines.append(f"slug `{slug}` -> branch `worktree-{slug}` -> contract `{filename}`\n")
    lines.append("**Files you own:** `scripts/nothing.py`.\n")
    path = tmp_path / filename
    path.write_text("\n\n".join(lines), encoding="utf-8")
    return path


def _lane(slug: str, *, priority: int = 0, starts_after: tuple = (),
         serialize_group: Optional[str] = None, substrate: str = "local") -> "d.QueuedLane":
    return d.QueuedLane(slug=slug, contract=Path(f"{slug}.md"), priority=priority,
                        starts_after=starts_after, serialize_group=serialize_group,
                        substrate=substrate)


# --- substrate column: a `Dispatch-Codespace` head, read without raising ------------------------

def test_dispatch_head_reads_a_codespace_head_without_raising(tmp_path):
    path = _contract(tmp_path, "LANE-cs.md", "lane-cs", head="dispatch-codespace")
    text = path.read_text(encoding="utf-8")
    assert d.dispatch_head(text) == "dispatch-codespace"
    # parse_dispatch_block, by contrast, REFUSES this head -- queue must not go through it
    with pytest.raises(d.DispatchRefused):
        d.parse_dispatch_block(text)


def test_lane_substrate_reads_dispatch_codespace_head_as_codespace(tmp_path):
    path = _contract(tmp_path, "LANE-cs.md", "lane-cs", head="dispatch-codespace")
    assert d.lane_substrate(path.read_text(encoding="utf-8")) == "codespace"


def test_lane_substrate_falls_back_to_the_contract_label_for_a_claude_head(tmp_path):
    path = _contract(tmp_path, "LANE-cloud.md", "lane-cloud", head="claude",
                     substrate_label="**codespace**")
    assert d.lane_substrate(path.read_text(encoding="utf-8")) == "codespace"


def test_lane_substrate_defaults_to_local_with_no_note(tmp_path):
    path = _contract(tmp_path, "LANE-local.md", "lane-local", head="claude")
    assert d.lane_substrate(path.read_text(encoding="utf-8")) == "local"


def test_lane_substrate_reads_the_unbolded_local_label(tmp_path):
    path = _contract(tmp_path, "LANE-local.md", "lane-local", head="claude",
                     substrate_label="local")
    assert d.lane_substrate(path.read_text(encoding="utf-8")) == "local"


# --- load_queue: priority is input order, plan_lint's own grammar is reused ---------------------

def test_load_queue_priority_is_input_order(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a")
    b = _contract(tmp_path, "LANE-b.md", "lane-b")
    lanes = d.load_queue([b, a])   # b passed FIRST
    assert [(lane.slug, lane.priority) for lane in lanes] == [("lane-b", 0), ("lane-a", 1)]


def test_load_queue_reads_starts_after_and_serialize_group(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", starts_after=("lane-a",),
                 serialize_group="grp")
    lanes = {lane.slug: lane for lane in d.load_queue([a, b])}
    assert lanes["lane-b"].starts_after == ("lane-a",)
    assert lanes["lane-b"].serialize_group == "grp"


def test_load_queue_refuses_a_duplicate_slug(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-dup")
    b = _contract(tmp_path, "LANE-b.md", "lane-dup")
    # `dispatch.py` imports plan_lint through its own `scripts.`-prefixed try/except shim (the
    # same dual-import pattern `lane_cost` already uses); catching via `d.pl` rather than this
    # test's own top-level `import plan_lint as pl` is what actually matches the raised class --
    # the two import paths otherwise produce two DIFFERENT module objects for the same file.
    with pytest.raises(d.pl.PlanLintError):
        d.load_queue([a, b])


# --- launch_order: the static schedule, layered so a late dependency never jumps a wave ---------

#: The WAVE5B-N2 batch's own 16-lane shape (`BATCH-WAVE5B-N2-2026-09-25.md` §3): priority = table
#: row, substrate and `Starts after` exactly as the real contracts declare them, `serialize-group:
#: order-templates` on rows 5/6/7. Kept as data so the acceptance test and the real dry-run this
#: lane's Done-contract item 1 runs are checking the SAME graph shape.
_BATCH_SHAPE = [
    ("lane-codespace-proof", "codespace", ()),
    ("lane-rows-owed", "codespace", ("lane-codespace-proof",)),
    ("lane-adr122-accept", "codespace", ("lane-codespace-proof",)),
    ("lane-copilot-codespace", "codespace", ("lane-rows-owed",)),
    ("lane-teardown-visible", "local", ()),
    ("lane-quota-watch", "local", ()),
    ("lane-done-when-gate", "local", ()),
    ("lane-codespace-roundtrip-ci", "local", ()),
    ("lane-launch-queue", "local", ()),
    ("lane-organ-wirings", "local", ("lane-launch-queue",)),
    ("lane-adr-drafts", "local", ()),
    ("lane-boot-contract", "local", ()),
    ("lane-learning-distiller", "local", ()),
    ("lane-python-standard-1", "local", ()),
    ("lane-aj-scan", "local", ()),
    ("lane-transport-strays", "local", ()),
]
_ORDER_TEMPLATES_GROUP = {"lane-teardown-visible", "lane-quota-watch", "lane-done-when-gate"}


def _batch_contracts(tmp_path: Path) -> list[Path]:
    return [
        _contract(tmp_path, f"LANE-{slug}.md", slug, starts_after=starts_after,
                 serialize_group="order-templates" if slug in _ORDER_TEMPLATES_GROUP else None,
                 head="dispatch-codespace" if substrate == "codespace" else "claude",
                 substrate_label=substrate)
        for slug, substrate, starts_after in _BATCH_SHAPE]


def test_launch_order_reproduces_the_batch_sequence_wave_alpha_beta(tmp_path):
    """Wave alpha + beta (`DISPATCHER-WAVE5B-N2-2026-09-25.md` §Sequence steps 1-2): every lane
    with no dependency, codespace first, then local in table order -- exactly the written
    `1, 5, 8, 9, 11, 12, 13, 14, 15, 16` (here by slug)."""
    lanes = d.load_queue(_batch_contracts(tmp_path))
    order = d.launch_order(lanes)
    assert order[:10] == [
        "lane-codespace-proof", "lane-teardown-visible", "lane-codespace-roundtrip-ci",
        "lane-launch-queue", "lane-adr-drafts", "lane-boot-contract", "lane-learning-distiller",
        "lane-python-standard-1", "lane-aj-scan", "lane-transport-strays"]


def test_launch_order_reproduces_the_batch_sequence_wave_gamma(tmp_path):
    """Wave gamma: every lane released only once its dependency's whole ROUND has placed --
    `lane-copilot-codespace` (depends on `lane-rows-owed`) and `lane-done-when-gate` (depends,
    via `serialize-group`, on `lane-quota-watch`) land in the FINAL round, never earlier."""
    lanes = d.load_queue(_batch_contracts(tmp_path))
    order = d.launch_order(lanes)
    assert order[10:] == ["lane-rows-owed", "lane-adr122-accept", "lane-quota-watch",
                          "lane-organ-wirings", "lane-copilot-codespace", "lane-done-when-gate"]
    # the two-parent dependency lands strictly after BOTH: teardown-visible (round 1) and
    # quota-watch (round 2, itself gated by teardown-visible's serialize-group)
    assert order.index("lane-done-when-gate") > order.index("lane-quota-watch")
    assert order.index("lane-done-when-gate") > order.index("lane-teardown-visible")


def test_launch_order_never_lets_a_later_round_preempt_an_earlier_one(tmp_path):
    """The bug this lane's own development caught: a flat pop-lowest priority queue lets a
    freshly-freed codespace lane jump an entire still-pending local wave. `a` is local and ready
    immediately; `cs` is codespace but depends on `a` -- `cs` must never precede `a`."""
    a = _contract(tmp_path, "LANE-a.md", "lane-a", head="claude")
    cs = _contract(tmp_path, "LANE-cs.md", "lane-cs", starts_after=("lane-a",),
                  head="dispatch-codespace")
    lanes = d.load_queue([a, cs])
    assert d.launch_order(lanes) == ["lane-a", "lane-cs"]


def test_launch_order_refuses_a_cycle(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", starts_after=("lane-b",))
    b = _contract(tmp_path, "LANE-b.md", "lane-b", starts_after=("lane-a",))
    lanes = d.load_queue([a, b])
    with pytest.raises(d.DispatchRefused, match="cycle"):
        d.launch_order(lanes)


# --- the dependency hold: the integrator's REAL receipt, not an invented fixture -----------------
#
# N2 lane 9 (`LANE-5B2-9-launch-queue`) invented a `{"lanes": {"<slug>": {"state": ...}}}` JSON
# shape with no writer anywhere in the harness -- carried into this lane's own ROWS-OWED
# ("reconcile if a real format exists elsewhere", `to-browser/SESSION-lane-launch-queue.md`
# Repair item 5). The real format is the free-text `STATE <lane> ...` line the integrator writes
# into its own session receipt. `_STATE_TEXT` below is a VERBATIM copy of eight such lines from
# `to-browser/SESSION-integrator-wave5b-n2-2026-09-25.md` (lines 37, 99, 122, 200, 269, 325, 375,
# 376) -- unedited, in the file's own order, including the mid-batch WAITING->REFUSED->MERGED
# transitions two of the slugs actually go through as repairs land.

_STATE_TEXT = """\
STATE lane-codespace-proof REFUSED - 2026-09-25T17:02 -
STATE lane-teardown-visible REFUSED - 2026-09-25T17:56 -
STATE lane-launch-queue REFUSED - 2026-09-25T18:15 -
STATE lane-codespace-proof-repair-1 WAITING - 2026-09-25T18:57 -
STATE lane-codespace-proof-repair-1 MERGED 3d13a2d2 2026-09-25T19:42 47
STATE lane-teardown-visible FAILED - 20:42 -
STATE lane-codespace-roundtrip-ci MERGED 32791ac3 22:20 96
STATE lane-launch-queue MERGED bc969abc 22:20 108
"""


def test_read_lane_states_missing_file_reads_empty(tmp_path):
    assert d.read_lane_states(tmp_path / "absent.md") == {}
    assert d.read_lane_states(None) == {}


def test_parse_state_lines_reads_the_real_integrator_grammar():
    assert d.parse_state_lines(_STATE_TEXT) == {
        "lane-codespace-proof": "REFUSED",
        "lane-teardown-visible": "FAILED",
        "lane-codespace-proof-repair-1": "MERGED",
        "lane-launch-queue": "MERGED",
        "lane-codespace-roundtrip-ci": "MERGED",
    }


def test_parse_state_lines_last_occurrence_wins_across_a_transition():
    """`lane-launch-queue` appears twice in `_STATE_TEXT`: REFUSED (line 122), then MERGED (line
    376) once its repair landed. The append-only receipt's LAST line for a slug is its current
    state -- a dependent waiting on it must read MERGED, not the earlier REFUSED."""
    assert d.parse_state_lines(_STATE_TEXT)["lane-launch-queue"] == "MERGED"


def test_parse_state_lines_ignores_a_state_word_outside_the_five():
    """The integrator's transcript also carries `STATE integrator BOUND - ... -` and
    `STATE <lane> HANDBACK-SEEN - ... -` -- neither is one of the five states
    `dependency_status` ever reads, so the pattern must not match them."""
    text = ("STATE integrator BOUND - 2026-09-25T15:51 -\n"
           "STATE lane-handoff-system-design HANDBACK-SEEN - 22:1x -\n")
    assert d.parse_state_lines(text) == {}


def test_read_lane_states_reads_the_real_receipt_from_disk(tmp_path):
    receipt = tmp_path / "SESSION-integrator-wave5b-n2-2026-09-25.md"
    receipt.write_text(_STATE_TEXT, encoding="utf-8")
    assert d.read_lane_states(receipt) == {
        "lane-codespace-proof": "REFUSED",
        "lane-teardown-visible": "FAILED",
        "lane-codespace-proof-repair-1": "MERGED",
        "lane-launch-queue": "MERGED",
        "lane-codespace-roundtrip-ci": "MERGED",
    }


def test_dependency_status_ready_with_no_dependency():
    lane = _lane("lane-a")
    assert d.dependency_status(lane, {}) == d.DEP_READY


def test_dependency_status_waiting_when_dependency_absent_from_the_fixture():
    lane = _lane("lane-b", starts_after=("lane-a",))
    assert d.dependency_status(lane, {}) == d.DEP_WAITING


def test_dependency_status_ready_once_every_dependency_reads_merged():
    lane = _lane("lane-c", starts_after=("lane-a", "lane-b"))
    states = {"lane-a": "MERGED", "lane-b": "MERGED"}
    assert d.dependency_status(lane, states) == d.DEP_READY


def test_dependency_status_waiting_when_only_some_dependencies_are_merged():
    lane = _lane("lane-c", starts_after=("lane-a", "lane-b"))
    states = {"lane-a": "MERGED"}
    assert d.dependency_status(lane, states) == d.DEP_WAITING


def test_dependency_status_blocked_when_a_dependency_failed():
    lane = _lane("lane-b", starts_after=("lane-a",))
    assert d.dependency_status(lane, {"lane-a": "FAILED"}) == d.DEP_BLOCKED_FAILED


# --- serialize-group: never two members live -----------------------------------------------------

def test_serialize_group_clear_with_no_group():
    lane = _lane("lane-a")
    assert d.serialize_group_clear(lane, [lane], live_slugs=["lane-a"])


def test_serialize_group_clear_when_no_member_is_live():
    a = _lane("lane-a", serialize_group="g")
    b = _lane("lane-b", serialize_group="g")
    assert d.serialize_group_clear(a, [a, b], live_slugs=[])


def test_serialize_group_holds_while_another_member_is_live():
    a = _lane("lane-a", serialize_group="g")
    b = _lane("lane-b", serialize_group="g")
    assert not d.serialize_group_clear(b, [a, b], live_slugs=["lane-a"])


def test_serialize_group_ignores_the_lanes_own_liveness():
    """A lane checking itself in `live_slugs` (already fired) must not hold on ITS OWN entry --
    only an OTHER member counts."""
    a = _lane("lane-a", serialize_group="g")
    b = _lane("lane-b", serialize_group="g")
    assert d.serialize_group_clear(a, [a, b], live_slugs=["lane-a"])


# --- decide_lane: the gates, in order --------------------------------------------------------

def _decide(lane, **overrides):
    kwargs = dict(states={}, live_slugs=(), all_lanes=[lane], local_cap=4, local_live_count=0,
                 free_mb=8000.0, floor_mb=3072.0)
    kwargs.update(overrides)
    return d.decide_lane(lane, **kwargs)


def test_decide_lane_fires_when_every_gate_clears():
    lane = _lane("lane-a")
    decision = _decide(lane)
    assert decision.action == d.ACTION_FIRE


def test_decide_lane_dependency_hold_outranks_every_other_gate():
    lane = _lane("lane-b", starts_after=("lane-a",))
    decision = _decide(lane, free_mb=1.0, local_live_count=99, local_cap=1)  # every other gate would hold too
    assert decision.action == d.ACTION_HOLD
    assert "lane-a" in decision.reason


def test_decide_lane_hold_reason_names_only_the_unmet_dependency():
    """One dependency MERGED, one not: the HOLD reason names the unmet one only (dispatcher,
    2026-10-02 20:05Z -- the reason listed a lane that had already merged)."""
    lane = _lane("lane-c", starts_after=("lane-a", "lane-b"))
    decision = _decide(lane, states={"lane-a": "MERGED", "lane-b": "IN-FLIGHT"})
    assert decision.action == d.ACTION_HOLD
    assert "lane-b" in decision.reason
    assert "lane-a" not in decision.reason


def test_decide_lane_hold_reason_names_every_unmet_dependency():
    lane = _lane("lane-d", starts_after=("lane-a", "lane-b", "lane-c"))
    decision = _decide(lane, states={"lane-a": "MERGED", "lane-c": "REFUSED"})
    assert decision.action == d.ACTION_HOLD
    assert "lane-b" in decision.reason and "lane-c" in decision.reason   # b absent, c not MERGED
    assert "lane-a" not in decision.reason


def test_decide_lane_hold_decision_is_unchanged_by_the_reason_fix():
    lane = _lane("lane-c", starts_after=("lane-a", "lane-b"))
    assert _decide(lane, states={"lane-a": "MERGED", "lane-b": "MERGED"}).action == d.ACTION_FIRE
    assert _decide(lane, states={"lane-a": "MERGED", "lane-b": "FAILED"}).action \
        == d.ACTION_HELD_FAILED


def test_decide_lane_held_failed_when_dependency_failed():
    lane = _lane("lane-b", starts_after=("lane-a",))
    decision = _decide(lane, states={"lane-a": "FAILED"})
    assert decision.action == d.ACTION_HELD_FAILED


def test_decide_lane_ram_gate_holds_below_the_floor():
    lane = _lane("lane-a")
    decision = _decide(lane, free_mb=1000.0, floor_mb=3072.0)
    assert decision.action == d.ACTION_HOLD
    assert "floor" in decision.reason


def test_decide_lane_ram_gate_clears_at_or_above_the_floor():
    lane = _lane("lane-a")
    decision = _decide(lane, free_mb=3072.0, floor_mb=3072.0)
    assert decision.action == d.ACTION_FIRE


def test_decide_lane_local_cap_holds_when_full():
    lane = _lane("lane-a")
    decision = _decide(lane, local_cap=4, local_live_count=4)
    assert decision.action == d.ACTION_HOLD
    assert "cap" in decision.reason


def test_decide_lane_routes_codespace_before_cap_or_ram_ever_apply():
    """A codespace lane is never gated on the local cap or the RAM floor -- it does not use
    either -- and it is never spawned as a local process (Done-contract item 2)."""
    lane = _lane("lane-a", substrate="codespace")
    decision = _decide(lane, local_cap=0, local_live_count=99, free_mb=0.0, floor_mb=3072.0)
    assert decision.action == d.ACTION_ROUTE_CODESPACE


def test_decide_lane_serialize_group_hold_before_substrate_routing():
    a = _lane("lane-a", substrate="codespace", serialize_group="g")
    b = _lane("lane-b", substrate="codespace", serialize_group="g")
    decision = _decide(b, all_lanes=[a, b], live_slugs=["lane-a"])
    assert decision.action == d.ACTION_HOLD
    assert "serialize-group" in decision.reason


def test_plan_pass_skips_already_fired_slugs():
    a = _lane("lane-a", priority=0)
    b = _lane("lane-b", priority=1)
    decisions = d.plan_pass([a, b], ["lane-a", "lane-b"], fired=["lane-a"], states={},
                            live_slugs=(), local_cap=4, local_live_count=0, free_mb=8000.0,
                            floor_mb=3072.0)
    assert [dec.slug for dec in decisions] == ["lane-b"]


def test_plan_pass_reserves_the_local_cap_within_the_same_pass():
    """Codex terra review, HIGH (`docs/audits/2026-09-25-codex-lane-launch-queue.md`): every
    decision in ONE `plan_pass` call used to read the SAME `local_live_count` snapshot, so several
    ready local lanes could all clear a cap of four at once. With cap=1 and TWO ready local lanes,
    only the FIRST may FIRE; the second must see the first's reservation and HOLD."""
    a = _lane("lane-a", priority=0)
    b = _lane("lane-b", priority=1)
    decisions = d.plan_pass([a, b], ["lane-a", "lane-b"], fired=(), states={}, live_slugs=(),
                            local_cap=1, local_live_count=0, free_mb=8000.0, floor_mb=3072.0)
    assert [(dec.slug, dec.action) for dec in decisions] == [
        ("lane-a", d.ACTION_FIRE), ("lane-b", d.ACTION_HOLD)]


def test_plan_pass_reserves_a_serialize_group_within_the_same_pass():
    """The same race for `serialize-group`: two ready members of ONE group must not both read
    `FIRE` out of a single pass -- "never two members live" (Done-contract item 2) has to hold
    WITHIN a pass, not only across polls."""
    a = _lane("lane-a", priority=0, serialize_group="g")
    b = _lane("lane-b", priority=1, serialize_group="g")
    decisions = d.plan_pass([a, b], ["lane-a", "lane-b"], fired=(), states={}, live_slugs=(),
                            local_cap=4, local_live_count=0, free_mb=8000.0, floor_mb=3072.0)
    assert [(dec.slug, dec.action) for dec in decisions] == [
        ("lane-a", d.ACTION_FIRE), ("lane-b", d.ACTION_HOLD)]
    assert "serialize-group" in decisions[1].reason


def test_plan_pass_a_held_failed_or_routed_codespace_lane_reserves_nothing():
    """A `HELD-FAILED` or `ROUTE-CODESPACE` decision is not a real local occupant, so it must not
    consume the cap or block a `serialize-group` sibling within the same pass."""
    failed_dep = _lane("lane-a", priority=0, starts_after=("lane-x",))
    sibling = _lane("lane-b", priority=1, serialize_group="g")
    other = _lane("lane-c", priority=2, serialize_group="g")
    decisions = d.plan_pass([failed_dep, sibling, other],
                            ["lane-a", "lane-b", "lane-c"], fired=(),
                            states={"lane-x": "FAILED"}, live_slugs=(), local_cap=1,
                            local_live_count=0, free_mb=8000.0, floor_mb=3072.0)
    assert [(dec.slug, dec.action) for dec in decisions] == [
        ("lane-a", d.ACTION_HELD_FAILED), ("lane-b", d.ACTION_FIRE), ("lane-c", d.ACTION_HOLD)]


# --- repair: relaunch into the EXISTING worktree, never a fresh one ------------------------------

def test_build_repair_plan_carries_no_worktree_flag():
    plan = d.build_repair_plan("claude-sonnet-5", "lane-a", 1, "high", "do the repair")
    assert "--worktree" not in plan.argv
    assert plan.argv[:4] == ["claude", "--bg", "-n", "lane-a-repair-1"]


def test_build_repair_plan_refuses_an_unknown_effort():
    with pytest.raises(d.DispatchRefused):
        d.build_repair_plan("claude-sonnet-5", "lane-a", 1, "not-an-effort", "x")


def test_repair_lane_refuses_when_the_worktree_is_missing(tmp_path):
    request = d.RepairRequest(slug="lane-ghost", attempt=1, model="claude-sonnet-5",
                              effort="high", contract=tmp_path / "LANE-ghost.md")
    with pytest.raises(d.DispatchRefused, match="existing worktree"):
        d.repair_lane(request, repo_root=tmp_path)


def test_repair_lane_spawns_into_the_existing_worktree_with_no_fresh_worktree_flag(tmp_path, monkeypatch):
    tree = tmp_path / ".claude" / "worktrees" / "lane-a"
    tree.mkdir(parents=True)
    request = d.RepairRequest(slug="lane-a", attempt=2, model="claude-sonnet-5", effort="high",
                              contract=tmp_path / "LANE-a.md")
    calls = []

    def fake_spawn(argv, env, cwd, log_path=None):
        calls.append((list(argv), Path(cwd)))
        return d.Spawned(0, "backgrounded 1a2b3c4d", None)

    # `repair` runs `moment:pre-launch` and writes a LAUNCH receipt now (`e2-subst-gate`, item 2b):
    # both are stubbed here (cleared pre-launch, private receipts dir); their witnesses are in
    # `tests/test_dispatch_repair_prelaunch.py`.
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(tmp_path / "receipts"))
    result = d.repair_lane(request, repo_root=tmp_path, spawn=fake_spawn, environ={},
                           prelaunch=lambda r, repair=False: d.PreLaunch(True))
    assert result.returncode == 0
    [(argv, cwd)] = calls
    assert cwd == tree
    assert "--worktree" not in argv
    assert "-n" in argv and argv[argv.index("-n") + 1] == "lane-a-repair-2"


# --- watch_queue: one bounded loop, never an orphan -----------------------------------------------

class _FakeClock:
    """A monotonic clock that advances by exactly the amount every injected `sleep()` call asks
    for -- so a test can assert `watch_queue` polls a KNOWN, FINITE number of times and returns,
    rather than trusting a real wall clock (or, worse, a real `time.sleep`) in a unit test."""

    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def clock(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def test_watch_queue_expires_at_its_deadline_and_never_loops_past_it():
    """A lane whose dependency never shows up in the fixture stays WAITING forever -- this is
    N1's orphan-watcher shape. `watch_queue` must still RETURN, at `deadline_s`, not hang."""
    lane = _lane("lane-b", starts_after=("lane-a",))
    clock = _FakeClock()
    result = d.watch_queue([lane], ["lane-b"], deadline_s=300.0, poll_interval_s=60.0,
                           sleep=clock.sleep, clock=clock.clock)
    assert result.expired is True
    assert result.fired == ()
    # bounded: the clock never advances past what the deadline allows, and sleep was called a
    # small, finite number of times, not an unbounded one
    assert clock.now >= 300.0
    assert len(clock.sleeps) == 5  # 60s steps to cross a 300s deadline


def test_watch_queue_fires_every_lane_and_ends_before_the_deadline():
    a = _lane("lane-a", priority=0)
    b = _lane("lane-b", priority=1, starts_after=("lane-a",))
    clock = _FakeClock()
    fired_order: list[str] = []
    states = {"lane-a": ""}   # becomes MERGED only once lane-a's on_fire records it

    def on_fire(slug: str) -> None:
        fired_order.append(slug)
        if slug == "lane-a":
            states["lane-a"] = "MERGED"

    result = d.watch_queue([a, b], ["lane-a", "lane-b"], deadline_s=300.0, poll_interval_s=10.0,
                           sleep=clock.sleep, clock=clock.clock, on_fire=on_fire,
                           states_fn=lambda: dict(states))
    assert result.expired is False
    assert fired_order == ["lane-a", "lane-b"]
    assert set(result.fired) == {"lane-a", "lane-b"}


def test_watch_queue_routes_a_codespace_lane_without_ever_spawning_it():
    """`fired` names only a real launch (Codex terra review, HIGH,
    `docs/audits/2026-09-25-codex-lane-launch-queue.md`): a routed codespace lane is terminal
    (nothing left to wait for) but must NEVER read as `fired`, or `queue --watch`'s own "fired
    N/N" summary would claim a launch that never happened."""
    lane = _lane("lane-cs", substrate="codespace")
    on_fire_calls = []
    result = d.watch_queue([lane], ["lane-cs"], deadline_s=60.0, poll_interval_s=10.0,
                           sleep=lambda s: None, clock=iter([0.0, 100.0]).__next__,
                           on_fire=on_fire_calls.append)
    assert on_fire_calls == []   # never spawned
    assert result.fired == ()
    assert result.routed_codespace == ("lane-cs",)
    assert result.terminal == {"lane-cs"}   # not left pending either


def test_watch_queue_marks_a_failed_dependency_terminal_without_spawning():
    lane = _lane("lane-b", starts_after=("lane-a",))
    on_fire_calls = []
    result = d.watch_queue([lane], ["lane-b"], deadline_s=60.0, poll_interval_s=10.0,
                           sleep=lambda s: None, clock=iter([0.0, 100.0]).__next__,
                           on_fire=on_fire_calls.append, states_fn=lambda: {"lane-a": "FAILED"})
    assert on_fire_calls == []
    assert result.fired == ()
    assert result.held_failed == ("lane-b",)
    assert result.terminal == {"lane-b"}


def test_watch_queue_never_sleeps_past_a_non_divisible_deadline():
    """A 125s deadline with a 60s poll interval: the THIRD sleep must be clamped to the 5s
    remaining, not the full 60s -- Codex terra review, HIGH: an un-clamped sleep with little time
    left overshoots `deadline_s` by up to a whole interval before the next check catches it."""
    lane = _lane("lane-b", starts_after=("lane-a",))   # never clears: proves the loop still ends
    clock = _FakeClock()
    result = d.watch_queue([lane], ["lane-b"], deadline_s=125.0, poll_interval_s=60.0,
                           sleep=clock.sleep, clock=clock.clock)
    assert result.expired is True
    assert clock.now == 125.0            # exact -- no overshoot past the deadline
    assert clock.sleeps == [60.0, 60.0, 5.0]


def test_watch_queue_respects_max_polls_independent_of_the_deadline():
    lane = _lane("lane-b", starts_after=("lane-a",))
    clock = _FakeClock()
    result = d.watch_queue([lane], ["lane-b"], deadline_s=99999.0, poll_interval_s=1.0,
                           sleep=clock.sleep, clock=clock.clock, max_polls=3)
    assert result.expired is True
    assert result.polls == 3


# --- `queue`'s CLI: --repo-root actually reaches the local launch it fires ----------------------

def test_queue_cli_passes_repo_root_to_the_local_launch(tmp_path, monkeypatch):
    """Codex terra review, HIGH (`docs/audits/2026-09-25-codex-lane-launch-queue.md`): `queue_cmd`
    accepted `--repo-root` but never threaded it into `launch_lane`'s `cwd`, so a queued launch
    silently used the CALLER's cwd instead of the repository root the operator named."""
    contract = _contract(tmp_path, "LANE-a.md", "lane-a", head="claude")
    other_root = tmp_path / "elsewhere"
    other_root.mkdir()
    calls = []
    spawned = {"yet": False}

    def fake_spawn(argv, env, cwd, log_path=None):
        calls.append(Path(cwd))
        spawned["yet"] = True
        return d.Spawned(returncode=0, stdout="backgrounded abcd1234\n", pid=4321)

    def fake_agents():
        # empty until AFTER the spawn (the pre-launch collision check must see nothing live yet);
        # a matching LIVE entry afterward lets `_identify` resolve on its first read instead of
        # polling (its own retry loop sleeps a real second between attempts otherwise).
        if not spawned["yet"]:
            return []
        return [{"id": "abcd1234", "sessionId": "sid-1", "name": "lane-a",
                 "cwd": str(other_root / ".claude" / "worktrees" / "lane-a"),
                 "state": "working", "status": "busy"}]

    monkeypatch.setattr(d, "run_prelaunch", lambda request: d.PreLaunch(passed=True))
    monkeypatch.setattr(d, "spawn_process", fake_spawn)
    monkeypatch.setattr(d, "list_agents", fake_agents)

    out = CliRunner().invoke(d.cli, ["queue", str(contract), "--repo-root", str(other_root),
                                     "--floor-mb", "0"])
    assert out.exit_code == 0, out.output
    assert calls == [other_root]


# --- [#1572]: a re-run of `queue` is idempotent ---------------------------------------------------

class _Fleet:
    """A fake `claude agents` listing plus a fake spawn that adds a live record per launched slug,
    so a three-lane `queue` run exercises the real `launch_lane` collision check end to end."""

    def __init__(self, tmp_path: Path) -> None:
        self.root = tmp_path / "repo"
        self.root.mkdir()
        self.records: list[dict] = []
        self.spawned: list[str] = []

    def add_live(self, slug: str, job: str) -> None:
        self.records.append({"id": job, "sessionId": f"sid-{job}", "name": slug, "state": "working",
                             "status": "busy",
                             "cwd": str(self.root / ".claude" / "worktrees" / slug)})

    def agents(self) -> list[dict]:
        return list(self.records)

    def spawn(self, argv, env, cwd, log_path=None):
        slug = argv[argv.index("-n") + 1]
        job = f"{len(self.spawned) + 1:08x}"
        self.spawned.append(slug)
        self.add_live(slug, job)
        return d.Spawned(returncode=0, stdout=f"backgrounded {job}\n", pid=4000 + len(self.spawned))

    def install(self, monkeypatch) -> None:
        monkeypatch.setattr(d, "run_prelaunch", lambda request: d.PreLaunch(passed=True))
        monkeypatch.setattr(d, "spawn_process", self.spawn)
        monkeypatch.setattr(d, "list_agents", self.agents)


def _three_contracts(tmp_path: Path) -> list[Path]:
    return [_contract(tmp_path, f"LANE-{n}.md", f"lane-{n}") for n in ("a", "b", "c")]


def test_queue_reports_an_already_launched_lane_and_fires_the_rest(tmp_path, monkeypatch, receipts):
    """[#1572] RED first: lane-a is already launched (a live job and its launch receipt). One
    re-run of `queue` used to exit 5 at lane-a and never reach lane-b or lane-c."""
    fleet = _Fleet(tmp_path)
    fleet.add_live("lane-a", "aaaa1111")
    d._write_json(d._receipt_path("lane-a"), {
        "schema": 1, "organ": "launch", "launched_at": d._stamp(), "exit_code": 0,
        "job_id": "aaaa1111", "slug": "lane-a", "provider": "claude"})
    fleet.install(monkeypatch)
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0"])

    assert out.exit_code == 0, out.output
    assert fleet.spawned == ["lane-b", "lane-c"]
    assert "already-launched lane-a" in out.output


def test_queue_watch_reports_an_already_launched_lane_and_fires_the_rest(tmp_path, monkeypatch, receipts):
    fleet = _Fleet(tmp_path)
    fleet.add_live("lane-a", "aaaa1111")
    d._write_json(d._receipt_path("lane-a"), {
        "schema": 1, "organ": "launch", "launched_at": d._stamp(), "exit_code": 0,
        "job_id": "aaaa1111", "slug": "lane-a", "provider": "claude"})
    fleet.install(monkeypatch)
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0", "--watch", "--deadline-s", "5",
                                     "--poll-interval", "0.01"])

    assert out.exit_code == 0, out.output
    assert fleet.spawned == ["lane-b", "lane-c"]
    assert "already-launched lane-a" in out.output


def test_queue_never_refires_a_lane_whose_receipt_reads_merged(tmp_path, monkeypatch, receipts):
    """[#1572] sibling: the integrator's `STATE lane-a MERGED ...` line is the lane's end. A lane
    that finished (no live job, so `launch_lane` sees nothing holding it) was fired again."""
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    state = tmp_path / "SESSION-integrator-x.md"
    state.write_text("STATE lane-a MERGED abc1234 2026-10-18T10:00 5\n", encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0", "--state-file", str(state)])

    assert out.exit_code == 0, out.output
    assert fleet.spawned == ["lane-b", "lane-c"]
    assert "lane-a" in out.output and "MERGED" in out.output


def test_queue_watch_never_refires_a_lane_whose_receipt_reads_merged(tmp_path, monkeypatch, receipts):
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    state = tmp_path / "SESSION-integrator-x.md"
    state.write_text("STATE lane-a MERGED abc1234 2026-10-18T10:00 5\n", encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0", "--state-file", str(state), "--watch",
                                     "--deadline-s", "5", "--poll-interval", "0.01"])

    assert out.exit_code == 0, out.output
    assert fleet.spawned == ["lane-b", "lane-c"]
    assert "all clear" in out.output


def test_decide_lane_reports_a_live_lane_as_already_launched_before_the_cap_or_ram_gate():
    """Codex review P2 on [#1572]: a lane already live holds a slot of the very cap it would be
    held by, so with the cap full (or RAM low) a re-run said HOLD and `--watch` waited out its
    deadline for a lane that was running. Liveness decides it before any new-launch gate."""
    lane = _lane("lane-a")
    full = d.decide_lane(lane, states={}, live_slugs={"lane-a"}, all_lanes=[lane], local_cap=1,
                         local_live_count=1, free_mb=10_000, floor_mb=0)
    low = d.decide_lane(lane, states={}, live_slugs={"lane-a"}, all_lanes=[lane], local_cap=4,
                        local_live_count=1, free_mb=1, floor_mb=3072)
    assert full.action == low.action == d.ACTION_ALREADY_LAUNCHED


def test_queue_watch_with_the_cap_full_of_launched_lanes_ends_without_waiting(tmp_path, monkeypatch, receipts):
    fleet = _Fleet(tmp_path)
    fleet.add_live("lane-a", "aaaa1111")
    fleet.install(monkeypatch)
    contracts = [_contract(tmp_path, "LANE-a.md", "lane-a")]

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0", "--cap", "1", "--watch", "--deadline-s", "5",
                                     "--poll-interval", "0.01"])

    assert out.exit_code == 0, out.output
    assert fleet.spawned == []
    assert "already-launched lane-a" in out.output and "all clear" in out.output


def test_queue_reports_a_lane_whose_launch_lock_is_held_and_fires_the_rest(tmp_path, monkeypatch, receipts):
    """Codex review P1 on [#1572]: a second `queue` run racing the first finds the slug's launch
    lock held before any receipt or listing entry exists. That is already-launched too, not a halt."""
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    lock = d.receipts_dir() / "LAUNCH-LOCK-LANE-A"
    lock.parent.mkdir(parents=True, exist_ok=True)
    contents = f"pid {os.getpid()} at {d._stamp()}\n"
    lock.write_text(contents, encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0"])

    assert out.exit_code == 0, out.output
    assert fleet.spawned == ["lane-b", "lane-c"]
    assert "already-launched lane-a" in out.output
    assert lock.exists()
    assert lock.read_text(encoding="utf-8") == contents
    assert not (receipts / "LAUNCH-RECLAIM-LANE-A.jsonl").exists()


# --- [#1572] D6: a held launch lock is judged by its holder --------------------------------------

_UNPARSEABLE_LOCKS = [
    ("empty", ""),
    ("garbage", "garbage"),
    ("missing-stamp-pid-1", "pid 1"),
    ("non-numeric-pid", "pid abc at x"),
    ("zero-pid", "pid 0 at 2026-10-18T12:00:00+00:00"),
    ("negative-pid", "pid -5 at 2026-10-18T12:00:00+00:00"),
    ("missing-stamp-current-pid", f"pid {os.getpid()}"),
]


def _dead_holder_pid() -> int:
    process = subprocess.Popen([sys.executable, "-c", "pass"])
    process.wait()
    return process.pid


def test_queue_reclaims_a_dead_holder_lock_and_fires_every_lane(tmp_path, monkeypatch, receipts):
    """[#1572] D6(a): a lock held by a dead process is journaled, removed, and relaunched."""
    dead_pid = _dead_holder_pid()
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    lock = receipts / "LAUNCH-LOCK-LANE-A"
    lock.parent.mkdir(parents=True, exist_ok=True)
    stamp = d._stamp()
    lock.write_text(f"pid {dead_pid} at {stamp}\n", encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0"])

    assert out.exit_code == 0, out.output
    assert fleet.spawned == ["lane-a", "lane-b", "lane-c"]
    assert "already-launched lane-a" not in out.output
    reclaim = receipts / "LAUNCH-RECLAIM-LANE-A.jsonl"
    lines = reclaim.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert set(record) == {"event", "slug", "lock", "dead_pid", "at"}
    assert record["event"] == "lock-reclaimed"
    assert record["slug"] == "lane-a"
    assert record["lock"] == str(lock)
    assert record["dead_pid"] == dead_pid
    assert datetime.fromisoformat(record["at"]) >= datetime.fromisoformat(stamp)   # when it was reclaimed
    assert not lock.exists()


def test_queue_reclaims_a_recycled_pid_lock_and_fires_every_lane(tmp_path, monkeypatch, receipts):
    """[#1572] D6(a2): a live pid whose start postdates the lock stamp is treated as recycled."""
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    lock = receipts / "LAUNCH-LOCK-LANE-A"
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text(f"pid {os.getpid()} at 1970-01-02T00:00:00+00:00\n", encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0"])

    assert out.exit_code == 0, out.output
    assert fleet.spawned == ["lane-a", "lane-b", "lane-c"]
    assert "already-launched lane-a" not in out.output
    reclaim = receipts / "LAUNCH-RECLAIM-LANE-A.jsonl"
    lines = reclaim.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert set(record) == {"event", "slug", "lock", "dead_pid", "at"}
    assert record["event"] == "lock-reclaimed"
    assert record["slug"] == "lane-a"
    assert record["lock"] == str(lock)
    assert record["dead_pid"] == os.getpid()
    assert datetime.fromisoformat(record["at"]).year >= 2026   # when it was reclaimed, not the lock's stamp
    assert not lock.exists()


def test_live_holder_lock_stays_already_launched_for_queue_and_direct_launch(tmp_path, monkeypatch,
                                                                             receipts):
    """[#1572] D6(b): a live holder remains protected and is never recorded as reclaimed."""
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    lock = receipts / "LAUNCH-LOCK-LANE-A"
    lock.parent.mkdir(parents=True, exist_ok=True)
    contents = f"pid {os.getpid()} at {d._stamp()}\n"
    lock.write_text(contents, encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0"])

    assert out.exit_code == 0, out.output
    assert "already-launched lane-a" in out.output
    assert fleet.spawned == ["lane-b", "lane-c"]
    assert lock.exists()
    assert lock.read_text(encoding="utf-8") == contents
    assert not (receipts / "LAUNCH-RECLAIM-LANE-A.jsonl").exists()
    with pytest.raises(d.AlreadyLaunched) as refused:
        d.launch_lane(d.request_from_contract(contracts[0]), prelaunch=lambda request: d.PreLaunch(
            passed=True), spawn=lambda *args: pytest.fail("live lock must not spawn"),
                     agents=lambda: [], cwd=fleet.root)
    assert "in progress" in refused.value.message


@pytest.mark.parametrize(("case", "contents"), _UNPARSEABLE_LOCKS,
                         ids=[case for case, _ in _UNPARSEABLE_LOCKS])
def test_unparseable_lock_refuses_queue_and_direct_launch(tmp_path, monkeypatch, receipts, case,
                                                          contents):
    """[#1572] D6(c): malformed lock contents fail closed without changing or reclaiming the lock."""
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    lock = receipts / "LAUNCH-LOCK-LANE-A"
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text(contents, encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0"])

    assert out.exit_code != 0, out.output
    assert out.exit_code == 5, out.output
    assert fleet.spawned == []
    assert lock.exists()
    assert lock.read_text(encoding="utf-8") == contents
    assert not (receipts / "LAUNCH-RECLAIM-LANE-A.jsonl").exists()
    assert "already-launched lane-a" not in out.output
    with pytest.raises(d.LaunchRefused) as refused:
        d.launch_lane(d.request_from_contract(contracts[0]), prelaunch=lambda request: d.PreLaunch(
            passed=True), spawn=lambda *args: pytest.fail("unparseable lock must not spawn"),
                     agents=lambda: [], cwd=fleet.root)
    assert not isinstance(refused.value, d.AlreadyLaunched)
    assert "in progress" in refused.value.message


def test_undeterminable_lock_holder_refuses_queue_and_direct_launch(tmp_path, monkeypatch, receipts):
    """[#1572] D6(c): inability to check a well-formed holder's liveness fails closed."""
    def boom(pid):
        raise psutil.Error("boom")

    monkeypatch.setattr("psutil.Process", boom)
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    lock = receipts / "LAUNCH-LOCK-LANE-A"
    lock.parent.mkdir(parents=True, exist_ok=True)
    contents = f"pid {os.getpid()} at {d._stamp()}\n"
    lock.write_text(contents, encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0"])

    assert out.exit_code != 0, out.output
    assert out.exit_code == 5, out.output
    assert fleet.spawned == []
    assert lock.exists()
    assert lock.read_text(encoding="utf-8") == contents
    assert not (receipts / "LAUNCH-RECLAIM-LANE-A.jsonl").exists()
    assert "already-launched lane-a" not in out.output
    with pytest.raises(d.LaunchRefused) as refused:
        d.launch_lane(d.request_from_contract(contracts[0]), prelaunch=lambda request: d.PreLaunch(
            passed=True), spawn=lambda *args: pytest.fail("undeterminable lock must not spawn"),
                     agents=lambda: [], cwd=fleet.root)
    assert not isinstance(refused.value, d.AlreadyLaunched)
    assert "in progress" in refused.value.message


@pytest.mark.parametrize(
    ("case", "malformed_contents"),
    [("dead", None), ("recycled", None),
     *((f"unparseable-{case}", contents) for case, contents in _UNPARSEABLE_LOCKS),
     ("undeterminable", None)],
    ids=["dead", "recycled", *(f"unparseable-{case}" for case, _ in _UNPARSEABLE_LOCKS),
         "undeterminable"],
)
def test_no_stale_lock_path_exits_zero_without_a_launch_and_a_reclaim_line(
        tmp_path, monkeypatch, receipts, case, malformed_contents):
    """[#1572] D6(d): any stale or indeterminate lock either launches after reclaim or fails closed."""
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    lock = receipts / "LAUNCH-LOCK-LANE-A"
    lock.parent.mkdir(parents=True, exist_ok=True)
    if case == "dead":
        contents = f"pid {_dead_holder_pid()} at {d._stamp()}\n"
    elif case == "recycled":
        contents = f"pid {os.getpid()} at 1970-01-02T00:00:00+00:00\n"
    elif case == "undeterminable":
        def boom(pid):
            raise psutil.Error("boom")

        monkeypatch.setattr("psutil.Process", boom)
        contents = f"pid {os.getpid()} at {d._stamp()}\n"
    else:
        contents = malformed_contents
    lock.write_text(contents, encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0"])

    if out.exit_code == 0:
        assert "lane-a" in fleet.spawned
        assert (receipts / "LAUNCH-RECLAIM-LANE-A.jsonl").exists()
    assert "already-launched lane-a" not in out.output


def test_racing_launches_reclaim_a_dead_holder_once_and_spawn_once(tmp_path, receipts):
    """[#1572] D6(e): concurrent attempts serialize dead-lock reclamation and exactly one spawn."""
    contract = _contract(tmp_path, "LANE-a.md", "lane-a")
    lock = receipts / "LAUNCH-LOCK-LANE-A"
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text(f"pid {_dead_holder_pid()} at {d._stamp()}\n", encoding="utf-8")
    request = d.request_from_contract(contract)
    start = threading.Barrier(2)
    release_spawn = threading.Event()
    already_finished = threading.Event()
    spawned = []
    results = []
    refused = []
    unexpected = []

    def spawn(*args):
        spawned.append(args)
        if not release_spawn.wait(10):
            raise TimeoutError("test did not release the blocked spawn")
        return d.Spawned(returncode=0, stdout="backgrounded abcdef12\n", pid=os.getpid())

    def launch():
        start.wait(timeout=10)
        try:
            results.append(d.launch_lane(request, prelaunch=lambda req: d.PreLaunch(passed=True),
                                         spawn=spawn, agents=lambda: [], cwd=tmp_path,
                                         sleep=lambda seconds: None))
        except d.AlreadyLaunched as exc:
            refused.append(exc)
            already_finished.set()
        except Exception as exc:
            unexpected.append(exc)

    threads = [threading.Thread(target=launch) for _ in range(2)]
    try:
        for thread in threads:
            thread.start()
        assert already_finished.wait(10), "the competing launch did not refuse while spawn was blocked"
    finally:
        release_spawn.set()
        for thread in threads:
            if thread.ident is not None:
                thread.join(timeout=10)

    assert all(not thread.is_alive() for thread in threads), "launch thread hung"
    assert not unexpected
    assert len(spawned) == 1
    assert len(refused) == 1
    assert len(results) == 1
    reclaim_lines = (receipts / "LAUNCH-RECLAIM-LANE-A.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(reclaim_lines) == 1


def test_a_lock_removed_between_the_create_and_the_read_is_gone_not_unreadable(receipts):
    """[#1572] D6: a holder that finishes between our failed create and our read leaves nothing to
    judge -- the launcher tries the create again, it does not refuse."""
    verdict, pid, _why = d._judge_lock(receipts / "LAUNCH-LOCK-LANE-A")
    assert verdict == "GONE" and pid is None


def test_a_holder_whose_start_time_is_denied_refuses_rather_than_reading_as_alive(tmp_path, monkeypatch, receipts):
    """[#1572] Codex terra review P1: a pid that exists but whose start time cannot be read might be a
    recycled pid -- it cannot be told from the holder, so the lock is refused (not AlreadyLaunched,
    which `queue` would report with exit 0)."""
    class Denied:
        def __init__(self, pid):
            pass

        def create_time(self):
            raise psutil.AccessDenied()

    monkeypatch.setattr("psutil.Process", Denied)
    fleet = _Fleet(tmp_path)
    fleet.install(monkeypatch)
    lock = receipts / "LAUNCH-LOCK-LANE-A"
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text(f"pid {os.getpid()} at {d._stamp()}\n", encoding="utf-8")
    contracts = _three_contracts(tmp_path)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(fleet.root),
                                     "--floor-mb", "0"])

    assert out.exit_code == 5, out.output
    assert fleet.spawned == [] and lock.exists()
    assert "already-launched lane-a" not in out.output


def test_a_stamp_the_platform_cannot_convert_is_unreadable_not_a_crash(receipts, monkeypatch):
    """[#1572] Codex terra review P2: `fromisoformat` accepts dates `.timestamp()` cannot convert on some
    platforms; that is an unreadable lock (a refusal), never an uncaught OverflowError."""
    class Unconvertible:
        tzinfo = object()

        def timestamp(self):
            raise OverflowError("year out of range")

    class FakeDatetime:
        @staticmethod
        def fromisoformat(text):
            return Unconvertible()

    monkeypatch.setattr(d, "datetime", FakeDatetime)
    assert d._lock_stamp_epoch("9999-12-31T23:59:59+00:00") is None
