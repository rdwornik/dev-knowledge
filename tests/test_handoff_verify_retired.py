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
