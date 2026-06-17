"""Tests for scripts/coherence_enumerator.py — the reconciliation enumerator.

The enumerator is the DETERMINISTIC half of the coherence spine: given a flagged
stale edge it extracts every candidate reference site so an LLM can verdict each.
These tests pin the contract that matters — completeness: the known walkthrough
and diagram sites in the live runbook are SURFACED, and the spec version is read
LIVE (never hardcoded).

Layer-2 read-only: the enumerator reads two in-repo docs and prints; it mutates
nothing. Tests mirror test_validate_doc_claims' sys.path import shim.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import coherence_enumerator as ce  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
_RUNBOOK = _REPO_ROOT / "docs" / "handoffs" / "README.md"
_SPEC = _REPO_ROOT / "protocols" / "HANDOFF_PROCESS.md"


def _live_sites():
    text = _RUNBOOK.read_text(encoding="utf-8")
    return ce.extract_sites(text, _SPEC.stem)


# --- Step 1: deterministic site-extraction pass ----------------------------

def test_extract_surfaces_the_mermaid_diagram():
    """The single fenced ```mermaid block must surface as a discrete diagram site."""
    diagrams = _live_sites()["diagrams"]
    assert len(diagrams) == 1, f"expected exactly one diagram, got {len(diagrams)}"
    site = diagrams[0]
    assert "mermaid" in site.anchor
    assert "flowchart" in site.text          # the block body, not just the fence
    assert site.line_end > site.line_start    # a block range, not a single line


def test_extract_surfaces_both_walkthrough_blocks():
    """Both numbered procedures — the 7-step boot walkthrough AND the 3-step
    supplement procedure — must surface as discrete step blocks."""
    steps = _live_sites()["walkthrough_steps"]
    assert len(steps) >= 2, f"expected >=2 walkthrough blocks, got {len(steps)}"
    bodies = [s.text for s in steps]
    assert any("Paste the boot payload" in b for b in bodies), "main 7-step walkthrough missing"
    assert any("SUPPLEMENT.md" in b and "ANSWERS" in b for b in bodies), "supplement procedure missing"
    # each is a multi-line block (a range), not a file-level flag
    assert all(s.line_end > s.line_start for s in steps)


def test_extract_surfaces_spec_name_mentions():
    """Mentions of the spec name / family must surface under `sections`."""
    sections = _live_sites()["sections"]
    assert sections, "no spec-name mentions surfaced"
    assert any("HANDOFF_PROCESS" in s.text for s in sections)


def test_extract_surfaces_command_invocations():
    """CLI invocations — incl. the PowerShell discovery fence — surface as commands."""
    commands = _live_sites()["commands"]
    assert commands, "no command sites surfaced"
    assert any("Get-ChildItem" in s.anchor for s in commands), "powershell fence missing"


def test_every_category_is_present_in_the_map():
    """The map always carries every category (so the checklist can state empties)."""
    sites = _live_sites()
    assert set(sites) == set(ce.CATEGORIES)


def test_read_spec_version_from_fixture():
    """The version parser reads a `Version:` frontmatter line."""
    assert ce.read_spec_version("# Spec\n\nVersion: 9.9\nStatus: stable\n") == "9.9"
    assert ce.read_spec_version("# Spec\n\nno version here\n") == ""


def test_read_spec_version_live_is_not_hardcoded():
    """The live spec parses to a real version-shaped value — asserted by SHAPE,
    never by the literal current value (which advances)."""
    v = ce.read_spec_version(_SPEC.read_text(encoding="utf-8"))
    assert v, "no version parsed from the live spec"
    assert re.match(r"^\d+(\.\d+)+$", v), f"unexpected version shape: {v!r}"
