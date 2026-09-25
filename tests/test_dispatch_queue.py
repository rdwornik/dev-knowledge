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
from pathlib import Path
from typing import Optional

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


# --- the dependency hold: an integrator receipt fixture ------------------------------------------

def test_read_lane_states_missing_file_reads_empty(tmp_path):
    assert d.read_lane_states(tmp_path / "absent.json") == {}
    assert d.read_lane_states(None) == {}


def test_read_lane_states_reads_merged_and_failed(tmp_path):
    fixture = tmp_path / "state.json"
    fixture.write_text(json.dumps({"lanes": {
        "lane-a": {"state": "MERGED", "sha": "04868005"},
        "lane-b": {"state": "failed"},
    }}), encoding="utf-8")
    assert d.read_lane_states(fixture) == {"lane-a": "MERGED", "lane-b": "FAILED"}


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


def test_repair_lane_spawns_into_the_existing_worktree_with_no_fresh_worktree_flag(tmp_path):
    tree = tmp_path / ".claude" / "worktrees" / "lane-a"
    tree.mkdir(parents=True)
    request = d.RepairRequest(slug="lane-a", attempt=2, model="claude-sonnet-5", effort="high",
                              contract=tmp_path / "LANE-a.md")
    calls = []

    def fake_spawn(argv, env, cwd, log_path=None):
        calls.append((list(argv), Path(cwd)))
        return d.Spawned(0, "backgrounded 1a2b3c4d", None)

    result = d.repair_lane(request, repo_root=tmp_path, spawn=fake_spawn, environ={})
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
