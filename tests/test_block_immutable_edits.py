"""Tests for scripts/hooks/block_immutable_edits.py — the ADR-77 immutability guard.

Covers the pure decision core (`decide`, with injectable existence) and the
stdin/stdout/exit wire protocol (`main`, via subprocess). v1 zone is transcripts
ONLY; ADRs are deliberately out of scope, which the allow-ADR-edit test pins.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "hooks" / "block_immutable_edits.py"


def _load():
    spec = importlib.util.spec_from_file_location("block_immutable_edits", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


guard = _load()

# Existence stubs for the pure core.
EXISTS = lambda _p: True  # noqa: E731
ABSENT = lambda _p: False  # noqa: E731

_TRANSCRIPT = "docs/decisions/transcripts/2026-03-29-council-browser-handoff.md"
_TRANSCRIPT_ABS = r"C:\Users\x\Dev\.dev-knowledge\docs\decisions\transcripts\foo.md"
_ADR = "docs/decisions/ADR-72-cloud-routine-hub-independence.md"


def _payload(tool, path=None, key="file_path"):
    ti = {} if path is None else {key: path}
    return {"tool_name": tool, "tool_input": ti}


# --------------------------------------------------------------------------- #
# Pure decision core
# --------------------------------------------------------------------------- #

def test_deny_existing_transcript_edit():
    decision, _ = guard.decide(_payload("Edit", _TRANSCRIPT), exists=EXISTS)
    assert decision == "block"


def test_deny_existing_transcript_multiedit():
    # "Enumerate ALL mutating tools" — MultiEdit must be caught, not just Edit.
    decision, _ = guard.decide(_payload("MultiEdit", _TRANSCRIPT), exists=EXISTS)
    assert decision == "block"


def test_deny_write_to_existing_transcript():
    decision, reason = guard.decide(_payload("Write", _TRANSCRIPT), exists=EXISTS)
    assert decision == "block"
    assert "ADR-77" in reason


def test_deny_notebookedit_existing_in_zone():
    decision, _ = guard.decide(
        _payload("NotebookEdit", _TRANSCRIPT, key="notebook_path"), exists=EXISTS
    )
    assert decision == "block"


def test_allow_new_transcript_create():
    # A brand-new transcript file is the lifecycle — Write to a non-existent path.
    decision, _ = guard.decide(_payload("Write", _TRANSCRIPT), exists=ABSENT)
    assert decision == "allow"


def test_allow_non_zone_edit():
    decision, _ = guard.decide(_payload("Edit", "protocols/PLAYBOOK.md"), exists=EXISTS)
    assert decision == "allow"


def test_allow_adr_edit_v1_scope_is_transcripts_only():
    # PINS the operator's Option-C scope ruling: ADR in-place edits are NOT
    # blocked in v1 (the sanctioned in-file Amendment flow). If this ever flips
    # to "block", the ADR zone was extended without the Option-A amend path.
    decision, _ = guard.decide(_payload("Edit", _ADR), exists=EXISTS)
    assert decision == "allow"


def test_allow_non_mutating_tool_even_in_zone():
    # A read/grep/bash referencing a transcript path must pass.
    decision, _ = guard.decide(_payload("Read", _TRANSCRIPT), exists=EXISTS)
    assert decision == "allow"


def test_absolute_windows_path_in_zone_blocked():
    decision, _ = guard.decide(_payload("Edit", _TRANSCRIPT_ABS), exists=EXISTS)
    assert decision == "block"


def test_archive_subfolder_in_zone_blocked():
    decision, _ = guard.decide(
        _payload("Edit", "docs/decisions/transcripts/archive/old.md"), exists=EXISTS
    )
    assert decision == "block"


def test_no_path_allows():
    decision, _ = guard.decide(_payload("Write", None), exists=EXISTS)
    assert decision == "allow"


# --- Codex-review hardening (2026-06-06) ----------------------------------- #

def test_dotdot_escape_not_falsely_blocked():
    # `transcripts/../ADR-77.md` resolves OUTSIDE the zone — normpath collapses
    # `..`, so the lexical substring must NOT falsely block this ADR edit.
    decision, _ = guard.decide(
        _payload("Edit", "docs/decisions/transcripts/../ADR-77-x.md"), exists=EXISTS
    )
    assert decision == "allow"


def test_notebook_path_in_zone_with_benign_file_path_blocks():
    # A benign file_path must NOT mask an in-zone notebook_path: any recognized
    # in-zone path is controlling (fail-closed).
    payload = {
        "tool_name": "NotebookEdit",
        "tool_input": {
            "file_path": "protocols/PLAYBOOK.md",
            "notebook_path": _TRANSCRIPT,
        },
    }
    decision, _ = guard.decide(payload, exists=EXISTS)
    assert decision == "block"


def test_symlink_alias_into_zone_blocked(tmp_path):
    # An out-of-zone symlink pointing AT a transcript must be caught via realpath.
    zone_dir = tmp_path / "docs" / "decisions" / "transcripts"
    zone_dir.mkdir(parents=True)
    real = zone_dir / "real-transcript.md"
    real.write_text("x", encoding="utf-8")
    link = tmp_path / "alias.md"  # outside the zone lexically
    try:
        link.symlink_to(real)
    except (OSError, NotImplementedError):
        import pytest

        pytest.skip("symlink creation not permitted on this host")
    # realpath(link) -> .../transcripts/real-transcript.md (in zone)
    decision, _ = guard.decide(_payload("Edit", str(link)), exists=EXISTS)
    assert decision == "block"


# --------------------------------------------------------------------------- #
# Wire protocol (stdin JSON -> stdout JSON + exit code), via subprocess
# --------------------------------------------------------------------------- #

def _run(payload_obj):
    raw = json.dumps(payload_obj)
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT)],
        input=raw,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return proc


def test_wire_block_existing_transcript_edit_exits_2():
    # The transcript fixture path resolves to a real existing file in the repo,
    # so even Write would block — Edit certainly does.
    proc = _run(_payload("Edit", _TRANSCRIPT))
    assert proc.returncode == 2
    out = json.loads(proc.stdout)
    assert out["decision"] == "block"
    assert "ADR-77" in out["reason"]


def test_wire_allow_non_zone_edit_exits_0():
    proc = _run(_payload("Edit", "JOURNAL.md"))
    assert proc.returncode == 0
    assert proc.stdout.strip() == ""


def test_wire_guard_error_outside_zone_passes():
    # Unparseable / garbage payload -> can't identify a zone path -> must NOT
    # block normal work (exit 0). This is the "guard-error-outside-zone-passes"
    # asymmetric-fail guarantee.
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT)],
        input="this is not json {{{",
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == ""


def test_wire_allow_new_transcript_create_exits_0():
    # Write to a transcripts-zone path that does NOT exist on disk -> allowed.
    new_path = "docs/decisions/transcripts/2099-01-01-brand-new-transcript.md"
    proc = _run(_payload("Write", new_path))
    assert proc.returncode == 0
    assert proc.stdout.strip() == ""
