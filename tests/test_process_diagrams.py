"""Coverage for scripts/gen_process_diagrams.py -- P1 dispatch-lane state machine <-> binding <-> diagram.

Pins: the 25-state machine, the zone map, ecosystem/process-binding.yaml (schema process-binding/1),
the R130/R132 invariants, file:line anchors, and regenerate-and-compare of the stored Mermaid block.
All tests use real repo files; no network.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_process_diagrams as gpd  # noqa: E402

REPO = Path(__file__).resolve().parents[1]

STATES = [
    "drafted", "emitted", "checked", "planned", "queued", "held_dependency",
    "held_capacity", "prelaunch", "launching_local", "launching_codespace",
    "launching_cloud", "launch_incomplete", "running", "running_cloud", "stalled", "resuming",
    "handed_back", "harvesting", "integrating", "merged", "refused", "repairing",
    "reported", "blocked_failed", "failed",
]
FINALS = {"merged", "reported", "blocked_failed", "failed"}
ZONE_ENUM = {"BROWSER", "HARNESS", "BOTH"}
R130_EVENTS = ("handback", "merge", "refusal")


def _machine():
    return gpd.P1DispatchLane()


def _machine_transitions() -> set[tuple[str, str, str]]:
    result: set[tuple[str, str, str]] = set()
    for state in gpd.P1DispatchLane.states:
        for t in state.transitions:
            for ev in t.events:
                result.add((str(getattr(ev, "id", ev)), t.source.id, t.target.id))
    return result


def _machine_events() -> set[str]:
    return {e for e, _, _ in _machine_transitions()}


def _p1() -> dict:
    return gpd.load_binding()["processes"]["P1"]


def test_machine_has_exactly_the_25_states_initial_and_finals():
    states = gpd.P1DispatchLane.states
    assert sorted(s.id for s in states) == sorted(STATES)
    assert len(states) == 25
    assert {s.id for s in states if s.initial} == {"drafted"}
    assert {s.id for s in states if s.final} == FINALS


def test_every_state_has_a_zone_in_the_closed_enum():
    assert set(gpd.ZONES) == {s.id for s in gpd.P1DispatchLane.states}
    assert set(gpd.ZONES.values()) <= ZONE_ENUM
    assert gpd.ZONES["drafted"] == "BROWSER"


def test_binding_state_names_match_machine():
    names = [s["name"] for s in _p1()["states"]]
    assert len(names) == len(set(names))
    assert set(names) == {s.id for s in gpd.P1DispatchLane.states}


def test_binding_transitions_match_machine():
    binding = {(t["event"], t["source"], t["target"]) for t in _p1()["transitions"]}
    assert binding == _machine_transitions()


@pytest.mark.parametrize("event", R130_EVENTS)
def test_r130_trigger_events_exist_and_are_marked(event):
    assert event in _machine_events()
    marked = [t for t in _p1()["transitions"] if t["event"] == event]
    assert marked
    assert all(t.get("r130") is True for t in marked)


def test_r132_cloud_lane_can_never_be_integrated():
    for _event, source, target in _machine_transitions():
        if source in {"launching_cloud", "reported"}:
            assert target != "integrating"
    # no path at all from launching_cloud to integrating
    edges: dict[str, set[str]] = {}
    for _e, s, t in _machine_transitions():
        edges.setdefault(s, set()).add(t)
    seen: set[str] = set()
    stack = ["launching_cloud"]
    while stack:
        cur = stack.pop()
        for nxt in edges.get(cur, ()):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    assert "integrating" not in seen


def test_cloud_path_is_closed():
    edges: dict[str, set[str]] = {}
    for _e, s, t in _machine_transitions():
        edges.setdefault(s, set()).add(t)

    def reachable(start: str) -> set[str]:
        seen: set[str] = set()
        stack = [start]
        while stack:
            for nxt in edges.get(stack.pop(), ()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    from_cloud = reachable("launching_cloud")
    assert from_cloud <= {"running_cloud", "reported", "failed"}
    assert "running_cloud" in from_cloud
    assert "reported" in reachable("running_cloud")


def _anchored_entries():
    p1 = _p1()
    entries = []
    for kind in ("states", "transitions"):
        for item in p1[kind]:
            if item.get("hole"):
                continue
            locs = []
            if item.get("file_line") and item.get("anchor"):
                locs.append((item["file_line"], item["anchor"]))
            for b in (item.get("binding") or {}).values() if isinstance(item.get("binding"), dict) else []:
                if isinstance(b, dict) and b.get("file_line") and b.get("anchor"):
                    locs.append((b["file_line"], b["anchor"]))
            if isinstance(item.get("binding"), dict) and item["binding"].get("file_line") and item["binding"].get("anchor"):
                locs.append((item["binding"]["file_line"], item["binding"]["anchor"]))
            for loc in locs:
                entries.append((kind, item.get("id") or item.get("event"), *loc))
    return entries


def test_file_line_anchors_exist_and_match():
    entries = _anchored_entries()
    assert entries, "binding has no file_line + anchor entries to verify"
    for kind, ident, file_line, anchor in entries:
        path, _, line = str(file_line).rpartition(":")
        target = REPO / path
        assert target.is_file(), f"{kind} {ident}: {path} missing"
        lines = target.read_text(encoding="utf-8").splitlines()
        n = int(line)
        assert 1 <= n <= len(lines), f"{kind} {ident}: line {n} out of range in {path}"
        assert anchor in lines[n - 1], f"{kind} {ident}: {anchor!r} not at {file_line}"


def test_every_state_has_binding_or_hole():
    for s in _p1()["states"]:
        assert s.get("binding") or s.get("hole"), f"{s['name']}: neither binding nor hole"


def test_asis_ids_are_placed_exactly_once():
    p1 = _p1()
    ids: list[str] = []
    for s in p1["states"]:
        ids.extend(s.get("asis") or [])
    ids.extend(r["asis"] for r in p1.get("retired") or [])
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"AS-IS ids placed twice: {sorted(dupes)}"


def test_render_is_deterministic_and_complete():
    first, second = gpd.render_mermaid(), gpd.render_mermaid()
    assert first == second
    assert "stateDiagram-v2" in first
    for zone in ("browser", "harness", "both"):
        assert f"classDef {zone}" in first
    for name in STATES:
        zone = gpd.ZONES[name].lower()
        assert f"class {name} {zone}" in first


def test_stored_diagram_equals_regenerated_and_check_passes():
    binding = gpd.load_binding()
    assert binding["diagram_mermaid"].strip() == gpd.render_mermaid().strip()
    assert gpd.main(["--check"]) == 0


def test_binding_zone_matches_zones_and_diff_is_bool():
    for s in _p1()["states"]:
        assert s["zone"] == gpd.ZONES[s["name"]], s["name"]
        assert isinstance(s["diff"], bool), s["name"]
