"""Witnesses for the state and cycle sections this lane owns in BOTH order templates
(LANE-5B3-10-orchestrator-cycling, Done-contract item 2): "Both order templates gain a state
section (write the file after every state change) and a cycle rule (hand over to a fresh
session of the same role every ~2 h or at a context threshold; the new session binds its seat
and re-binds from the state file); a test renders each template and asserts both."

Ownership (ruling (i)): this lane edits ONLY the two templates' state and cycle sections --
`templates/dispatcher-order-template.md`'s launch/repair/watch steps belong to `lane-wire-queue`
and `templates/integrator-order-template.md`'s close/refusal steps belong to
`lane-wire-quota-distiller`. Both sibling lanes already assert their own sections' shape
(`tests/test_dispatcher_order_adopts_queue.py`, `tests/test_integrator_order_triggers.py`); this
file additionally asserts THEIR headings survive byte-shape-unchanged, mirroring their own
ownership tests back at this lane.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
for p in (REPO_ROOT, SCRIPTS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

INTEGRATOR_TEMPLATE = REPO_ROOT / "templates" / "integrator-order-template.md"
DISPATCHER_TEMPLATE = REPO_ROOT / "templates" / "dispatcher-order-template.md"


def _section(text: str, heading: str) -> str:
    """The body of one `## <heading>` section, up to the next `## ` heading or EOF -- same
    extraction the sibling lanes' own tests use."""
    pattern = re.compile(
        rf"^##\s*{re.escape(heading)}\s*$(?P<body>.*?)(?=^##\s|\Z)", re.M | re.S)
    m = pattern.search(text)
    assert m, f"no '## {heading}' section found"
    return m.group("body")


#: The template spells this with a literal em dash; typed the same way here rather than matched
#: around, so the constant IS the heading rather than a pattern that merely tolerates it.
CYCLE_HEADING = "Cycle — hand over to a fresh session of the same role"


def _cycle_section(text: str) -> str:
    return _section(text, CYCLE_HEADING)


# --- both templates render each section --------------------------------------------------------

def test_both_templates_exist():
    assert INTEGRATOR_TEMPLATE.exists()
    assert DISPATCHER_TEMPLATE.exists()


def test_both_templates_carry_a_state_file_section():
    for path in (INTEGRATOR_TEMPLATE, DISPATCHER_TEMPLATE):
        text = path.read_text(encoding="utf-8")
        assert re.search(r"^##\s*State file\s*$", text, re.M), f"{path.name}: no State file section"


def test_both_templates_carry_a_cycle_section():
    for path in (INTEGRATOR_TEMPLATE, DISPATCHER_TEMPLATE):
        text = path.read_text(encoding="utf-8")
        assert re.search(rf"^##\s*{re.escape(CYCLE_HEADING)}\s*$", text, re.M), (
            f"{path.name}: no Cycle section")


# --- state section: names the module, the write call, the schema, the enum ----------------------

def test_integrator_state_section_writes_after_every_state_line_and_names_the_module():
    text = INTEGRATOR_TEMPLATE.read_text(encoding="utf-8")
    state = _section(text, "State file")
    assert "scripts/seat_state.py write" in state
    assert "dev-knowledge-seat-state/1" in state
    assert "--role integrator" in state
    assert "MERGED|IN-FLIGHT|QUEUED|REFUSED|FAILED|REPORTED" in state
    assert "WAITING" in state, "the receipt's own WAITING word must be reconciled with IN-FLIGHT"


def test_dispatcher_state_section_writes_after_every_state_change_and_names_the_module():
    text = DISPATCHER_TEMPLATE.read_text(encoding="utf-8")
    state = _section(text, "State file")
    assert "scripts/seat_state.py write" in state
    assert "dev-knowledge-seat-state/1" in state
    assert "--role dispatcher" in state
    assert "QUEUED" in state and "IN-FLIGHT" in state and "REPORTED" in state


# --- cycle section: the ~2h/context threshold, rebind from the state file, bind a fresh seat ------

def test_integrator_cycle_section_names_the_handover_interval_and_rebind():
    cycle = _cycle_section(INTEGRATOR_TEMPLATE.read_text(encoding="utf-8"))
    assert "at least every 3 h" in cycle
    assert "context" in cycle
    assert "seat_registry.py bind --role integrator" in cycle
    assert "scripts/seat_state.py read" in cycle


def test_dispatcher_cycle_section_names_the_handover_interval_and_rebind():
    cycle = _cycle_section(DISPATCHER_TEMPLATE.read_text(encoding="utf-8"))
    assert "2 h" in cycle
    assert "context" in cycle
    assert "seat_registry.py bind --role dispatcher" in cycle
    assert "scripts/seat_state.py read" in cycle


# --- ownership: the other lanes' sections are untouched (mirrors their own ownership tests) -------

def test_integrator_close_and_refusal_headings_untouched():
    text = INTEGRATOR_TEMPLATE.read_text(encoding="utf-8")
    for heading in (
        "Merge priority when several are waiting",
        "Per handback — the one path",
        "Refusals and repairs",
        "Close — when every lane is MERGED or FAILED, or at <time>, whichever comes first",
    ):
        assert re.search(rf"^##\s*{re.escape(heading)}\s*$", text, re.M), (
            f"heading '{heading}' is missing or reworded -- out of this lane's ownership")


def test_dispatcher_sequence_heading_untouched():
    text = DISPATCHER_TEMPLATE.read_text(encoding="utf-8")
    for heading in ("Your role", "Sequence"):
        assert re.search(rf"^##\s*{re.escape(heading)}\s*$", text, re.M), (
            f"heading '{heading}' is missing or reworded -- out of this lane's ownership")


def test_no_must_shall_or_never_added_zero_headroom_baseline():
    """Lessons of N2 (a): `templates/**` carries zero headroom on the silent-rule baseline. Scoped
    to the sections this lane owns -- the sibling lanes each guard their own sections the same
    way, and the integrator's own full-tree ratchet is the batch's actual verdict."""
    for path in (INTEGRATOR_TEMPLATE, DISPATCHER_TEMPLATE):
        text = path.read_text(encoding="utf-8")
        state, cycle = _section(text, "State file"), _cycle_section(text)
        hits = re.findall(r"\b(must|shall|never)\b", state + cycle)
        assert hits == [], f"{path.name}: forbidden normative word(s) in owned sections: {hits}"
