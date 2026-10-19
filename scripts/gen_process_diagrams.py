#!/usr/bin/env python
"""gen_process_diagrams.py -- the P1 dispatch TO-BE process machine, and the diagram generated FROM it.

R131 (protocols/STANDING_RULINGS.md): the process model is code and the diagram is generated from it;
library-first. The library is python-statemachine (pinned 3.2.2, R137 Q8): it runs the machine (events,
guards) and exports the Mermaid diagram (`MermaidGraphMachine`). This module adds only what the library
cannot know: the ZONE of every state (R129: BROWSER / HARNESS / BOTH) and the check against
`ecosystem/process-binding.yaml`, the data file that binds every state and transition to today's
`file:line` or to a HOLE.

SPIKE STATUS. A draft for the morning review; never landed on its first night. The machine class lives
here only because no other new path was authorised (digest proposal: a later home `scripts/process_p1.py`).

SHAPE. ONE machine per lane (`P1DispatchLane`), 25 flat states. The batch is not a state: a one-shot
runner (R130) sends the event that arrived (handback / merge / refusal) to the lane it concerns, then
`evaluate` to every lane still queued or held. Gateways are guards (`cond=`), not states -- a state is a
place a lane can REST. Guards read the facts on the model (`LaneFacts`); nothing here starts a process.

USAGE:
    uv run --locked python scripts/gen_process_diagrams.py --check   # stored diagram == regenerated
    uv run --locked python scripts/gen_process_diagrams.py --write   # regenerate the stored diagram
    uv run --locked python scripts/gen_process_diagrams.py --print    # the Mermaid source on stdout
"""
from __future__ import annotations

import argparse
import difflib
import functools
import operator
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import yaml
from statemachine import State, StateMachine
from statemachine.contrib.diagram import MermaidGraphMachine

REPO = Path(__file__).resolve().parents[1]
BINDING_PATH = REPO / "ecosystem" / "process-binding.yaml"
DIAGRAM_KEY = "diagram_mermaid"

REFUSAL_CAP = 2  # a lane refused twice is FAILED (templates/integrator-order-template.md:97)
RESUME_CAP = 2  # continuation -resume-<n>, at most 2 (AS-IS P1-A33)
LAUNCH_CAP = 2  # launch attempts before the lane is refused
IDENTIFY_CAP = 4  # job-id identify tries (dispatch.py _identify)
IDLE_MINUTES = 30  # idle with no HANDBACK line (dispatcher-order-template.md:84)


@dataclass
class LaneFacts:
    """What the guards read. Every field is a fact the runner supplies; none is computed by the machine."""

    substrate: str = "local"  # local | codespace | cloud (R132)
    read_only: bool = False  # cloud lanes are read-only: they never build, never merge
    contract_ok: bool = True
    lint_clear: bool = True
    tier_within_role: bool = True  # R101(a): HOLE today, no code enforces it
    token_cap_set: bool = True
    no_cycle: bool = True
    merged: bool = False
    live: bool = False
    dep_failed: bool = False
    dep_waiting: bool = False
    serialize_busy: bool = False
    local_cap_full: bool = False
    ram_low: bool = False
    box_slot_free: bool = True  # HOLE today: no read of running Codespaces vs the account limit
    job_identified: bool = True
    handback_valid: bool = True
    manifest_verified: bool = True
    landed: bool = False
    worktree_exists: bool = True
    idle_minutes: int = 0
    refusals: int = 0
    resumes: int = 0
    launch_attempts: int = 0
    identify_tries: int = 0


def _each(sources: Iterable[State], target: State, **kw) -> object:
    """`source.to(target, **kw)` for every source, chained into one TransitionList."""
    return functools.reduce(operator.or_, (s.to(target, **kw) for s in sources))


class P1DispatchLane(StateMachine):
    """P1 dispatch TO-BE, one lane. Build order = the order a lane normally walks (drafted .. merged)."""

    # --- authoring (browser) and emit / check / plan (harness)
    drafted = State(initial=True)
    emitted = State()
    checked = State()
    planned = State()
    # --- the queue: places a lane waits (R130: code fires the queue, a wait is never an error, R122)
    queued = State()
    held_dependency = State()
    held_capacity = State()
    # --- launch, per substrate (R132)
    prelaunch = State()
    launching_local = State()
    launching_codespace = State()
    launching_cloud = State()
    launch_incomplete = State()
    # --- life of a launched lane
    running = State()
    running_cloud = State()  # R132: a cloud lane is read-only, so its life is a separate, closed path
    stalled = State()
    resuming = State()
    # --- the end of a lane
    handed_back = State()
    harvesting = State()
    integrating = State()
    merged = State(final=True)
    refused = State()
    repairing = State()
    reported = State(final=True)
    blocked_failed = State(final=True)
    failed = State(final=True)

    _held = (queued, held_dependency, held_capacity)

    # ---- authoring chain
    emit = drafted.to(emitted)
    check = emitted.to(checked, cond=["contract_ok", "lint_clear", "tier_within_role"]) | emitted.to(
        drafted, cond="checks_failed"
    )
    plan = checked.to(planned, cond="token_cap_set")
    enqueue = planned.to(queued, cond="no_cycle")

    # ---- the queue pass: the runner broadcasts `evaluate` to every held lane. First match wins.
    evaluate = (
        _each(_held, merged, cond="is_merged")
        | _each(_held, running, cond="is_live")
        | _each(_held, blocked_failed, cond="dep_failed")
        | _each(_held, held_dependency, cond="blocked_by_dependency")
        | _each(_held, held_capacity, cond="blocked_by_capacity")
        | _each(_held, prelaunch, cond="clear")
    )

    # ---- pre-launch (moment:pre-launch), then the substrate's launch
    prelaunch_passed = (
        prelaunch.to(launching_local, cond="substrate_is_local")
        | prelaunch.to(launching_codespace, cond="substrate_is_codespace")
        | prelaunch.to(launching_cloud, cond="substrate_is_cloud_read_only")
    )
    prelaunch_refused = prelaunch.to(failed, cond="substrate_is_cloud_writing") | prelaunch.to(
        queued, unless="substrate_is_cloud_writing"
    )
    spawned = launching_local.to(running, cond="job_identified")
    spawn_incomplete = launching_local.to(launch_incomplete)
    box_started = launching_codespace.to(running)
    box_limit = launching_codespace.to(held_capacity)  # HTTP 400 too many codespaces is a WAIT
    cloud_started = launching_cloud.to(running_cloud)
    cloud_done = running_cloud.to(reported)
    cloud_failed = running_cloud.to(failed)
    # a cloud lane has no retry through the queue and no repair: either would let it reach `integrating`
    launch_refused = (
        _each((launching_local, launching_codespace), queued, cond="launch_attempts_left")
        | _each((launching_local, launching_codespace), refused, unless="launch_attempts_left")
        | launching_cloud.to(failed)
    )
    identified = launch_incomplete.to(running)
    give_up = (
        launch_incomplete.to(failed, unless="identify_tries_left")
        | stalled.to(failed, unless="resumes_left")
        | resuming.to(failed, unless="resumes_left")
    )

    # ---- a running lane
    idle = running.to(stalled, cond="is_idle")
    resume = stalled.to(resuming, cond="resumes_left")
    resumed = resuming.to(running)
    handback = running.to(handed_back, cond="handback_on_local")  # R130 trigger
    box_done = running.to(harvesting, cond="substrate_is_codespace")

    # ---- the end: a lane that writes code goes to the integrator; a read-only lane reports
    to_integrator = handed_back.to(integrating, unless="read_only")
    report = handed_back.to(reported, cond="read_only") | harvesting.to(reported, cond="harvest_clean_read_only")
    harvested = harvesting.to(integrating, cond="harvest_clean_writing")
    refusal = harvesting.to(refused, unless="harvest_clean") | integrating.to(refused, unless="landed")  # R130 trigger
    merge = integrating.to(merged, cond="landed")  # R130 trigger

    # ---- refusal, repair, failure
    repair = refused.to(repairing, cond="repair_allowed")
    repaired = repairing.to(running)
    fail = refused.to(failed, unless="repair_allowed") | repairing.to(failed, unless="worktree_exists")

    def __init__(self, facts: Optional[LaneFacts] = None, **kw):
        self.facts = facts if facts is not None else LaneFacts()
        super().__init__(**kw)

    # ---- guards (each reads self.facts; none has a side effect)
    def contract_ok(self):
        return self.facts.contract_ok

    def lint_clear(self):
        return self.facts.lint_clear

    def tier_within_role(self):
        return self.facts.tier_within_role

    def checks_failed(self):
        f = self.facts
        return not (f.contract_ok and f.lint_clear and f.tier_within_role)

    def token_cap_set(self):
        return self.facts.token_cap_set

    def no_cycle(self):
        return self.facts.no_cycle

    def is_merged(self):
        return self.facts.merged

    def is_live(self):
        return self.facts.live

    def dep_failed(self):
        return self.facts.dep_failed

    def blocked_by_dependency(self):
        return self.facts.dep_waiting or self.facts.serialize_busy

    def blocked_by_capacity(self):
        f = self.facts
        if f.substrate == "local":
            return f.local_cap_full or f.ram_low
        if f.substrate == "codespace":
            return not f.box_slot_free
        return False

    def clear(self):
        return not (
            self.is_merged()
            or self.is_live()
            or self.dep_failed()
            or self.blocked_by_dependency()
            or self.blocked_by_capacity()
        )

    def substrate_is_local(self):
        return self.facts.substrate == "local"

    def substrate_is_codespace(self):
        return self.facts.substrate == "codespace"

    def substrate_is_cloud_read_only(self):
        return self.facts.substrate == "cloud" and self.facts.read_only

    def substrate_is_cloud_writing(self):
        return self.facts.substrate == "cloud" and not self.facts.read_only

    def job_identified(self):
        return self.facts.job_identified

    def launch_attempts_left(self):
        return self.facts.launch_attempts < LAUNCH_CAP

    def identify_tries_left(self):
        return self.facts.identify_tries < IDENTIFY_CAP

    def is_idle(self):
        return self.facts.idle_minutes >= IDLE_MINUTES

    def resumes_left(self):
        return self.facts.resumes < RESUME_CAP

    def handback_on_local(self):
        return self.facts.handback_valid and self.facts.substrate == "local"

    def read_only(self):
        return self.facts.read_only

    def harvest_clean(self):
        return self.facts.manifest_verified and self.facts.handback_valid

    def harvest_clean_writing(self):
        return self.harvest_clean() and not self.facts.read_only

    def harvest_clean_read_only(self):
        return self.harvest_clean() and self.facts.read_only

    def landed(self):
        return self.facts.landed

    def repair_allowed(self):
        return self.facts.refusals < REFUSAL_CAP and self.facts.worktree_exists

    def worktree_exists(self):
        return self.facts.worktree_exists


# R129: every state has exactly one zone. BROWSER = judgment the browser seat owns; HARNESS = code;
# BOTH = code fires the event but a human reads or decides (a refusal's reason, a stuck launch, a
# failed lane, a read-only report). A zone that differs from the AS-IS digest is a PROPOSAL, flagged
# `diff: true` in ecosystem/process-binding.yaml, and never decided here.
ZONES: dict[str, str] = {
    "drafted": "BROWSER",
    "emitted": "HARNESS",
    "checked": "HARNESS",
    "planned": "HARNESS",
    "queued": "HARNESS",
    "held_dependency": "HARNESS",
    "held_capacity": "HARNESS",
    "prelaunch": "HARNESS",
    "launching_local": "HARNESS",
    "launching_codespace": "HARNESS",
    "launching_cloud": "HARNESS",
    "launch_incomplete": "BOTH",
    "running": "HARNESS",
    "running_cloud": "HARNESS",
    "stalled": "HARNESS",
    "resuming": "HARNESS",
    "handed_back": "HARNESS",
    "harvesting": "HARNESS",
    "integrating": "HARNESS",
    "merged": "HARNESS",
    "refused": "BOTH",
    "repairing": "HARNESS",
    "reported": "BOTH",
    "blocked_failed": "HARNESS",
    "failed": "BOTH",
}

# colour per zone: blue / green / amber; mid-tone fills with dark text read on both themes.
ZONE_STYLE = {
    "BROWSER": "fill:#a5d8ff,stroke:#1971c2,color:#111",
    "HARNESS": "fill:#b2f2bb,stroke:#2f9e44,color:#111",
    "BOTH": "fill:#ffd8a8,stroke:#e8590c,color:#111",
}


def today_glue(zone: str, actor_today: Optional[str]) -> bool:
    """TODAY-GLUE (R129): harness work a human or a seat does by hand today. Derived, never typed."""
    return zone == "HARNESS" and any(who in (actor_today or "") for who in ("operator", "CC-seat"))


def load_binding(path: Path = BINDING_PATH) -> dict:
    """Parse ecosystem/process-binding.yaml (schema process-binding/1)."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def machine_transitions(machine: type[StateMachine] = P1DispatchLane) -> list[tuple[str, str, str, str]]:
    """(event, source, target, guard text) for every transition, in declaration order."""
    rows: list[tuple[str, str, str, str]] = []
    for state in machine.states:
        for t in state.transitions:
            guard = ", ".join(
                (c.attr_name if c.expected_value else f"!{c.attr_name}") for c in t.cond
            )
            for ev in t.events:
                rows.append((str(ev.id), state.id, t.target.id, guard))
    return rows


def render_mermaid() -> str:
    """The library's own Mermaid export (events, guards) plus the zone classes from ZONES."""
    base = MermaidGraphMachine(P1DispatchLane).get_mermaid().rstrip("\n")
    lines = [base, ""]
    for zone, style in ZONE_STYLE.items():
        lines.append(f"    classDef {zone.lower()} {style}")
    for state in P1DispatchLane.states:
        lines.append(f"    class {state.id} {ZONES[state.id].lower()}")
    return "\n".join(lines) + "\n"


_BLOCK = re.compile(rf"^{DIAGRAM_KEY}: \|\n(?:[ ]{{2}}.*\n|\n)*", re.MULTILINE)


def _block_text(diagram: str) -> str:
    return f"{DIAGRAM_KEY}: |\n" + "".join(f"  {line}\n" if line else "\n" for line in diagram.rstrip("\n").split("\n"))


def write_diagram(path: Path = BINDING_PATH) -> bool:
    """Replace (or append) the generated `diagram_mermaid` block in place. True when the file changed."""
    text = path.read_text(encoding="utf-8")
    block = _block_text(render_mermaid())
    new = _BLOCK.sub(lambda _m: block, text) if _BLOCK.search(text) else text.rstrip("\n") + "\n" + block
    if new == text:
        return False
    path.write_text(new, encoding="utf-8", newline="\n")
    return True


def check_glue(path: Path = BINDING_PATH) -> list[str]:
    """States whose stored `today_glue` is not the derivation from zone + actor."""
    return [
        s["name"]
        for s in load_binding(path)["processes"]["P1"]["states"]
        if s["today_glue"] != today_glue(s["zone"], s.get("actor_today"))
    ]


def check_diagram(path: Path = BINDING_PATH) -> int:
    drifted = check_glue(path)
    if drifted:
        print(f"today_glue is derived and differs for: {', '.join(drifted)}")
        return 1
    stored = (load_binding(path).get(DIAGRAM_KEY) or "").strip()
    fresh = render_mermaid().strip()
    if stored == fresh:
        return 0
    sys.stdout.writelines(
        difflib.unified_diff(
            stored.splitlines(True), fresh.splitlines(True), "stored (process-binding.yaml)", "regenerated"
        )
    )
    print("\nprocess diagram is stale: run `uv run --locked python scripts/gen_process_diagrams.py --write`")
    return 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="exit 1 when the stored diagram differs from a fresh render")
    g.add_argument("--write", action="store_true", help="regenerate the stored diagram in place")
    g.add_argument("--print", dest="show", action="store_true", help="print the Mermaid source")
    args = ap.parse_args(argv)
    if args.show:
        sys.stdout.write(render_mermaid())
        return 0
    if args.write:
        print("rewrote diagram_mermaid" if write_diagram() else "diagram_mermaid already current")
        return 0
    return check_diagram()


if __name__ == "__main__":
    sys.exit(main())
