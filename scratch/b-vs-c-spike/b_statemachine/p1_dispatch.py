"""P1 dispatch as ONE python-statemachine class (form B). Every gateway is a guarded transition.

Each node carries its own L1/L2 attributes beside its declaration: `actor`, `zone`, `glue`
(TODAY-GLUE), `bind` (ONE file:line, or None = a HOLE) and `test` (the test that pins it, or None).
Diagram, trace and the completeness check read those attributes; nothing is drawn by hand.

Node ORDER follows the contract, with one measured exception (substrate before cap/RAM, as
`decide_lane` does at scripts/dispatch.py:1657 -- see RESULT.md DIVERGENCES).
"""
from __future__ import annotations

from statemachine import State, StateMachine

D = "scripts/dispatch.py"
T = "tests/"


class Node(State):
    """A State that also says who does it, in which zone, and where in the code it lives."""

    def __init__(self, label, *, kind="task", actor="code", zone="HARNESS", glue=False,
                 bind=None, test=None, **kw):
        super().__init__(label, **kw)
        self.label, self.kind, self.actor, self.zone = label, kind, actor, zone
        self.glue, self.bind, self.test = glue, bind, test


class P1Dispatch(StateMachine):
    # ------------------------------------------------------------------ nodes
    start = Node("start: queue/launch entry", kind="event", actor="seat", zone="BOTH", glue=True, initial=True,
                 bind=f"{D}:3933", test=f"{T}test_dispatch_queue.py::test_launch_order_refuses_a_cycle")
    parse = Node("contract parsed (table + Dispatch block)",
                 bind=f"{D}:742", test=f"{T}test_dispatch_launch.py::test_a_dispatch_model_that_disagrees_with_the_table_is_refused")
    g_agree = Node("table = block?", kind="gateway", bind=f"{D}:765",
                   test=f"{T}test_dispatch_launch.py::test_a_dispatch_model_that_disagrees_with_the_table_is_refused")
    valid = Node("provider / model / effort valid", bind=f"{D}:213",
                 test=f"{T}test_dispatch_py.py::test_an_unknown_provider_is_refused_naming_the_known_ones")
    g_valid = Node("valid?", kind="gateway", bind=f"{D}:214",
                   test=f"{T}test_dispatch_py.py::test_effort_shorthand_is_mapped_and_an_unknown_effort_refused")
    tier = Node("R101(a) tier refusal (OWED)")                        # bound to NONE: a HOLE
    claim = Node("claim", actor="seat", glue=True, bind="scripts/claim.py:223",
                 test=f"{T}test_claim.py::test_the_cli_claims_and_the_second_call_refuses")
    g_claim = Node("claim won?", kind="gateway", bind="scripts/claim.py:233",
                   test=f"{T}test_claim.py::test_a_hand_made_marker_refuses_a_claim_too")
    g_dep = Node("Starts after MERGED?", kind="gateway", glue=True, bind=f"{D}:1601",
                 test=f"{T}test_dispatch_queue.py::test_dependency_status_blocked_when_a_dependency_failed")
    g_serial = Node("serialize-group clear?", kind="gateway", bind=f"{D}:1615",
                    test=f"{T}test_dispatch_queue.py::test_serialize_group_holds_while_another_member_is_live")
    g_substrate = Node("substrate?", kind="gateway", bind=f"{D}:1657",
                       test=f"{T}test_dispatch_queue.py::test_decide_lane_routes_codespace_before_cap_or_ram_ever_apply")
    g_capram = Node("local cap + RAM floor?", kind="gateway", bind=f"{D}:1661",
                    test=f"{T}test_dispatch_queue.py::test_decide_lane_local_cap_holds_when_full")
    route_codespace = Node("route to codespace-exec", bind=f"{D}:1978",
                           test=f"{T}test_dispatch_codespace.py::test_codespace_plan_shows_harvest_and_manifest_check_before_delete")
    prelaunch = Node("moment:pre-launch (local only)", bind=f"{D}:958",
                     test=f"{T}test_dispatch_launch.py::test_a_pre_launch_that_could_not_run_is_a_refusal_never_a_pass")
    g_prelaunch = Node("pre-launch cleared?", kind="gateway", bind=f"{D}:1148",
                       test=f"{T}test_dispatch_launch.py::test_a_pre_launch_organ_that_was_skipped_does_not_clear_the_launch")
    g_held = Node("already launched / occupied?", kind="gateway", bind=f"{D}:1140",
                  test=f"{T}test_dispatch_launch.py::test_running_launch_twice_on_one_contract_refuses_the_second")
    spawn = Node("spawn", bind=f"{D}:1169",
                 test=f"{T}test_dispatch_launch.py::test_a_free_slug_spawns_exactly_once_with_n_slug_in_its_argv")
    g_spawn = Node("provider started?", kind="gateway", bind=f"{D}:1174",
                   test=f"{T}test_dispatch_launch.py::test_a_spawn_that_failed_leaves_no_intent_receipt_behind")
    identify = Node("identify the job", bind=f"{D}:1204",
                    test=f"{T}test_dispatch_launch.py::test_a_lane_that_already_finished_is_still_identified_by_its_worktree")
    g_identify = Node("job identified?", kind="gateway", bind=f"{D}:1195",
                      test=f"{T}test_dispatch_launch.py::test_a_start_whose_job_cannot_be_identified_is_exit_8_not_a_quiet_success")
    receipt = Node("launch receipt", bind=f"{D}:1234",
                   test=f"{T}test_dispatch_launch.py::test_a_launch_writes_a_receipt_and_a_job_to_lane_record")
    running = Node("lane live: P1 watches", actor="seat", zone="BOTH", glue=True, bind=f"{D}:3787",
                   test=f"{T}test_dispatch_launch.py::test_govern_over_a_synthetic_over_cap_transcript_records_and_does_not_stop")
    # end events
    end_launched = Node("END launched", kind="end", bind=f"{D}:1201",
                        test=f"{T}test_dispatch_launch.py::test_a_free_slug_spawns_exactly_once_with_n_slug_in_its_argv", final=True)
    end_refused = Node("END REFUSED (exit 5)", kind="end", zone="BOTH", bind=f"{D}:149",
                       test=f"{T}test_dispatch_launch.py::test_the_cli_exits_non_zero_with_the_reason_and_spawns_nothing", final=True)
    end_already_launched = Node("END already-launched [#1572]", kind="end", zone="BOTH", bind=f"{D}:1141",
                                test=f"{T}test_dispatch_launch.py::test_running_launch_twice_on_one_contract_refuses_the_second", final=True)
    end_hold = Node("END HOLD (re-poll)", kind="end", bind=f"{D}:1628",
                    test=f"{T}test_dispatch_queue.py::test_decide_lane_ram_gate_holds_below_the_floor", final=True)
    end_routed_codespace = Node("END routed to codespace", kind="end", bind=f"{D}:1630",
                                test=f"{T}test_dispatch_queue.py::test_decide_lane_routes_codespace_before_cap_or_ram_ever_apply", final=True)
    end_unresolved = Node("END job unresolved (exit 8)", kind="end", zone="BOTH", bind=f"{D}:1196",
                          test=f"{T}test_dispatch_launch.py::test_a_start_whose_job_cannot_be_identified_is_exit_8_not_a_quiet_success", final=True)
    end_reaped = Node("END reaped (RAM)", kind="end", actor="operator", zone="BOTH", glue=True, final=True)     # HOLE
    end_early = Node("END-EARLY", kind="end", actor="seat", zone="BOTH", glue=True, final=True)                   # HOLE

    # ------------------------------------------------------------ transitions
    start.to(parse, event="go")
    parse.to(g_agree)
    g_agree.to(valid, cond="parse_ok")
    g_agree.to(end_refused, unless="parse_ok")
    valid.to(g_valid)
    g_valid.to(tier, cond="valid_ok")
    g_valid.to(end_refused, unless="valid_ok")
    tier.to(claim)
    claim.to(g_claim)
    g_claim.to(g_dep, cond="claim_ok")
    g_claim.to(end_refused, unless="claim_ok")
    g_dep.to(g_serial, cond="dep_ready")
    g_dep.to(end_refused, cond="dep_failed")
    g_dep.to(end_hold, cond="dep_waiting")
    g_serial.to(g_substrate, cond="serial_clear")
    g_serial.to(end_hold, unless="serial_clear")
    g_substrate.to(g_capram, cond="sub_local")
    g_substrate.to(route_codespace, cond="sub_codespace")
    g_substrate.to(end_refused, cond="sub_other")                    # 'cloud': no branch in code
    route_codespace.to(end_routed_codespace)
    g_capram.to(prelaunch, cond="capram_fire")
    g_capram.to(end_hold, unless="capram_fire")
    prelaunch.to(g_prelaunch)
    g_prelaunch.to(g_held, cond="prelaunch_ok")
    g_prelaunch.to(end_refused, unless="prelaunch_ok")
    g_held.to(spawn, cond="held_free")
    g_held.to(end_already_launched, cond="held_live")
    g_held.to(end_refused, cond="held_unreadable")
    spawn.to(g_spawn)
    g_spawn.to(identify, cond="spawn_ok")
    g_spawn.to(end_refused, unless="spawn_ok")
    identify.to(g_identify)
    g_identify.to(receipt, cond="identified")
    g_identify.to(end_unresolved, unless="identified")
    receipt.to(running)
    running.to(end_launched, event="lane_handback")
    running.to(end_reaped, event="lane_reaped")
    running.to(end_early, event="lane_ended_early")

    # ---------------------------------------------------------------- wiring
    def __init__(self, services):
        self.svc = services
        self.ctx: dict = {}
        self.trace: list[dict] = []
        super().__init__()

    def on_enter_state(self, state):
        self.trace.append({"n": len(self.trace) + 1, "node": state.id, "kind": state.kind,
                           "actor": state.actor, "zone": state.zone})

    def _do(self, node, result):
        self.ctx[node] = result
        self.trace[-1]["result"] = {k: v for k, v in result.items() if k in
                                    ("ok", "exit", "status", "clear", "substrate", "action", "held", "passed",
                                     "job_id", "returncode", "hole", "unreadable", "steps")}

    # service tasks: each calls a REAL verb in dry-run (common/services.py)
    def on_enter_start(self):
        self._do("start", self.svc.schedule())

    def on_enter_parse(self):
        self._do("parse", self.svc.parse_contract())

    def on_enter_valid(self):
        self._do("valid", self.svc.validate())

    def on_enter_tier(self):
        self._do("tier", self.svc.tier())

    def on_enter_claim(self):
        self._do("claim", self.svc.claim())

    def on_enter_g_dep(self):
        self._do("dep", self.svc.dependency())

    def on_enter_g_serial(self):
        self._do("serial", self.svc.serialize())

    def on_enter_g_substrate(self):
        self._do("substrate", self.svc.substrate())

    def on_enter_g_capram(self):
        self._do("capram", self.svc.cap_ram())

    def on_enter_route_codespace(self):
        self._do("route", self.svc.route_codespace())

    def on_enter_prelaunch(self):
        self._do("prelaunch", self.svc.prelaunch())

    def on_enter_g_held(self):
        self._do("held", self.svc.held())

    def on_enter_spawn(self):
        self._do("spawn", self.svc.spawn())

    def on_enter_identify(self):
        self._do("identify", self.svc.identify(self.ctx["spawn"]["stdout"]))

    def on_enter_receipt(self):
        i = self.ctx["identify"]
        self._do("receipt", self.svc.receipt(i["job_id"], i["session_id"], i["name"]))

    # guards (the gateways)
    def parse_ok(self): return self.ctx["parse"]["ok"]
    def valid_ok(self): return self.ctx["valid"]["ok"]
    def claim_ok(self): return self.ctx["claim"]["ok"]
    def dep_ready(self): return self.ctx["dep"]["status"] == "READY"
    def dep_failed(self): return self.ctx["dep"]["status"] == "BLOCKED-FAILED"
    def dep_waiting(self): return self.ctx["dep"]["status"] == "WAITING"
    def serial_clear(self): return self.ctx["serial"]["clear"]
    def sub_local(self): return self.ctx["substrate"]["substrate"] == "local"
    def sub_codespace(self): return self.ctx["substrate"]["substrate"] == "codespace"
    def sub_other(self): return self.ctx["substrate"]["substrate"] not in ("local", "codespace")
    def capram_fire(self): return self.ctx["capram"]["action"] == "FIRE"
    def prelaunch_ok(self): return self.ctx["prelaunch"]["passed"]
    def held_free(self): return not self.ctx["held"]["held"] and not self.ctx["held"].get("unreadable")
    def held_live(self): return bool(self.ctx["held"]["held"])
    def held_unreadable(self): return bool(self.ctx["held"].get("unreadable"))
    def spawn_ok(self): return self.ctx["spawn"]["returncode"] == 0
    def identified(self): return bool(self.ctx["identify"]["job_id"])
