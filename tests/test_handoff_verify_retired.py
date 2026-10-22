"""`/handoff-verify` is retired (R30; BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 3).

The browser seat boots on the ROLE PIN alone and CC runs the probe gate at the cut. No live
file may define the command or teach/wire it as a gate. Negations ("no `/handoff-verify`") and
the immutable records (ADRs, `docs/handoffs/<date>-*` bundles, audits) stay.
"""
from __future__ import annotations

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent

_LIVE = [
    ".methodology.yaml",
    ".github/workflows/conductor.yml",
    ".claude/commands/handoff.md",
    ".claude/generated/commands-repo.md",
    "CONTRIBUTING.md",
    "docs/handoffs/README.md",
    "ecosystem/harness.yaml",
    "ecosystem/parity-surfaces.yaml",
    "ecosystem/seat-ids.yaml",
    "ecosystem/transport-registry.yaml",
    "protocols/HANDOFF_PROCESS.md",
    "protocols/OPERATOR-INTERFACE.md",
    "scripts/graph_queries.py",
]
_MENTION = re.compile(r"handoff[-_ ]verify", re.IGNORECASE)
# a mention is fine only on a line that says it is gone
_NEGATION = re.compile(r"\bretired\b|\bno `?/?handoff[-_]verify|\bwithout `?/?handoff[-_]verify|"
                       r"\bnot `?/?handoff[-_]verify|\bnever `?/?handoff[-_]verify", re.IGNORECASE)


def test_the_command_file_is_gone():
    assert not (_REPO / ".claude" / "commands" / "handoff-verify.md").exists()


def test_no_live_file_teaches_or_wires_handoff_verify_as_a_gate():
    offenders = []
    for rel in _LIVE:
        text = (_REPO / rel).read_text(encoding="utf-8")
        for n, line in enumerate(text.splitlines(), 1):
            if _MENTION.search(line) and not _NEGATION.search(line):
                offenders.append(f"{rel}:{n}: {line.strip()[:110]}")
    assert not offenders, "\n".join(offenders)


def test_the_process_doc_states_the_boot_is_the_role_pin_alone():
    text = (_REPO / "protocols" / "HANDOFF_PROCESS.md").read_text(encoding="utf-8")
    assert "ROLE PIN alone" in text and "R30" in text
    assert "CC runs the probe gate at the cut" in text


# --- the Cycle hand-over launches its successor itself (LEDGER v212; witnessed 2026-10-15 16:14) ----
_TEMPLATES = ("integrator-order-template.md", "dispatcher-order-template.md")


def _cycle_section(name: str) -> str:
    text = (_REPO / "templates" / name).read_text(encoding="utf-8")
    return " ".join(text.split("## Cycle", 1)[1].split())  # prose is hard-wrapped


def test_the_cycle_handover_starts_the_successor_via_seat_cycle_and_falls_back_only_on_error():
    for name in _TEMPLATES:
        sec = _cycle_section(name)
        assert "scripts/seat_cycle.py run" in sec, name
        assert "come from the role table" in sec and "not from a typed line" in sec, name
        assert "`OPERATOR-ACTION` only if `run` exits non-zero" in sec, name


def test_no_recorded_evidence_or_system_map_node_names_the_retired_command():
    """Codex terra review (night close-out PART 3): the two recorded/generated surfaces."""
    import json

    evidence = (_REPO / "ecosystem" / "boot-retrieval-evidence.json").read_text(encoding="utf-8")
    assert not _MENTION.search(evidence)
    # the record's `diff` legitimately names what the last rebuild removed; its node list may not
    record = json.loads((_REPO / "ecosystem" / "system-map-record.json").read_text(encoding="utf-8"))
    record.pop("diff", None)
    assert not _MENTION.search(json.dumps(record))


def test_recorded_retrieval_evidence_has_no_row_for_an_item_the_probe_no_longer_has():
    import json
    import sys

    sys.path.insert(0, str(_REPO / "tests"))
    import boot_retrieval as br

    ids = {i.id for i in br.ITEMS}
    doc = json.loads((_REPO / "ecosystem" / "boot-retrieval-evidence.json").read_text(encoding="utf-8"))
    stale = {r["item"] for r in doc["rows"] if r["item"] not in ids | {"control"}}
    stale |= set(doc["pointer_text_sha256"]) - ids
    assert not stale, stale


def test_the_cycle_handover_states_the_foreground_wait_rule():
    for name in _TEMPLATES:
        sec = _cycle_section(name)
        assert "foreground of an active turn" in sec, name
        assert "memory_admission_gate.py wait" in sec, name
