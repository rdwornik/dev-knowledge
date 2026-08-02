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
import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_RUNBOOK = _REPO_ROOT / "docs" / "handoffs" / "README.md"
_SPEC = _REPO_ROOT / "protocols" / "HANDOFF_PROCESS.md"


def _live_sites():
    text = _RUNBOOK.read_text(encoding="utf-8")
    return ce.extract_sites(text, _SPEC.stem)


# --- Step 1: deterministic site-extraction pass ----------------------------

@pytest.mark.live_repo
def test_extract_surfaces_the_mermaid_diagram():
    """The single fenced ```mermaid block must surface as a discrete diagram site."""
    diagrams = _live_sites()["diagrams"]
    assert len(diagrams) == 1, f"expected exactly one diagram, got {len(diagrams)}"
    site = diagrams[0]
    assert "mermaid" in site.anchor
    assert "flowchart" in site.text          # the block body, not just the fence
    assert site.line_end > site.line_start    # a block range, not a single line


@pytest.mark.live_repo
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


def test_empty_ordered_item_does_not_fragment_a_step_block():
    """An empty item ("2." on its own line) stays part of the block — the block is
    not split, so no step is dropped (the 'never miss a site' contract)."""
    text = "# Doc\n\n1. First step\n2.\n3. Third step\n\nprose after.\n"
    steps = ce.extract_sites(text, "HANDOFF_PROCESS")["walkthrough_steps"]
    assert len(steps) == 1, f"block fragmented into {len(steps)}"
    assert steps[0].line_start == 3 and steps[0].line_end == 5


@pytest.mark.live_repo
def test_extract_surfaces_spec_name_mentions():
    """Mentions of the spec name / family must surface under `sections`."""
    sections = _live_sites()["sections"]
    assert sections, "no spec-name mentions surfaced"
    assert any("HANDOFF_PROCESS" in s.text for s in sections)


@pytest.mark.live_repo
def test_extract_surfaces_command_invocations():
    """CLI invocations — incl. the PowerShell discovery fence — surface as commands.

    The pin moved off `Get-ChildItem` at [#473]. That fence used to read
    `Get-ChildItem docs/handoffs/ | Sort-Object Name | Select-Object -Last 5`, i.e. it taught
    the operator to find the current bundle by LEXICAL NAME ORDER — the exact rule [#372] and
    [#473] both proved wrong (`-arc5` sorts last but was added first; `<slug>` sorts before
    `<slug>-2` though the sibling is newer). The command was replaced by a git-add-date query,
    so the old literal is deliberately gone.

    The replacement pin is the fence's LANGUAGE MARKER, not another command string. `anchor`
    truncates at ~70 chars, so any cmdlet past the first line is unpinnable anyway — and a
    literal command is exactly what rotted here: it coupled this test to the runbook's advice
    rather than to the property the docstring claims. Asserting the ```powershell fence
    surfaces as a command site tests that property directly and survives the next rewording."""
    commands = _live_sites()["commands"]
    assert commands, "no command sites surfaced"
    assert any(s.anchor.startswith("powershell:") for s in commands), "powershell fence missing"


@pytest.mark.live_repo
def test_every_category_is_present_in_the_map():
    """The map always carries every category (so the checklist can state empties)."""
    sites = _live_sites()
    assert set(sites) == set(ce.CATEGORIES)


def test_read_spec_version_from_fixture():
    """The version parser reads a `Version:` frontmatter line."""
    assert ce.read_spec_version("# Spec\n\nVersion: 9.9\nStatus: stable\n") == "9.9"
    assert ce.read_spec_version("# Spec\n\nno version here\n") == ""


@pytest.mark.live_repo
def test_read_spec_version_live_is_not_hardcoded():
    """The live spec parses to a real version-shaped value — asserted by SHAPE,
    never by the literal current value (which advances)."""
    v = ce.read_spec_version(_SPEC.read_text(encoding="utf-8"))
    assert v, "no version parsed from the live spec"
    assert re.match(r"^\d+(\.\d+)+$", v), f"unexpected version shape: {v!r}"


def test_read_spec_version_keeps_full_text_token():
    """The enumerator surfaces the RAW version token verbatim (full-text — keeps a leading
    v), distinct from the checker's numeric-normalized form. Pins B's consumer contract
    (previously un-pinned on a v-prefix) so the shared-parser dedup (#172) preserves it."""
    assert ce.read_spec_version("# S\n\nVersion: v5.4.1\nStatus: x\n") == "v5.4.1"


# --- Step 2: the by-category checklist output contract ---------------------

_FLAG = {
    "dependent_path": "docs/handoffs/README.md",
    "spec_path": "protocols/HANDOFF_PROCESS.md",
    "old_version": "5.2",
    "new_version": "5.3",
}


def _result_from(text: str) -> dict:
    return {
        "flag": _FLAG,
        "spec_name": "HANDOFF_PROCESS",
        "spec_version_current": "5.2",
        "sites": ce.extract_sites(text, "HANDOFF_PROCESS"),
    }


def test_checklist_states_empty_categories_explicitly():
    """A category with no hits is rendered as `[none found]`, never silently dropped."""
    # prose mentioning the spec once: sections hit, but no diagrams / steps / commands
    out = ce.format_checklist(_result_from("# Doc\n\nMentions HANDOFF_PROCESS once.\n"))
    assert "diagrams (fenced blocks) ==  [none found]" in out
    assert "walkthrough_steps (numbered / sequential procedures) ==  [none found]" in out
    # every category header is present regardless of hits
    for cat in ce.CATEGORIES:
        assert ce._CATEGORY_LABELS[cat] in out


def test_checklist_makes_fine_a_first_class_verdict():
    """`fine` / no-change-needed is an explicit, first-class verdict on every site."""
    out = ce.format_checklist(_result_from("# Doc\n\nMentions HANDOFF_PROCESS once.\n"))
    assert "'fine' (no change needed) is a first-class verdict" in out
    assert "stale | fine | not-relevant" in out


def test_checklist_carries_transclusion_candidate_label():
    """The verbatim-duplication label is offered in the skeleton (label only — v1
    does not build a transclusion engine)."""
    out = ce.format_checklist(_result_from("# Doc\n\nMentions HANDOFF_PROCESS once.\n"))
    assert "transclusion-candidate" in out


def test_checklist_has_additive_only_escape_section():
    """A final section lets the LLM ADD anchor-less sites it notices — never drop one."""
    out = ce.format_checklist(_result_from("# Doc\n\nMentions HANDOFF_PROCESS once.\n"))
    assert "additional (LLM-noticed; ADDITIVE ONLY)" in out
    assert "never drop" in out.lower()


def test_checklist_renders_a_verdict_slot_per_site():
    """Each found site gets its own location line + an empty verdict slot."""
    out = ce.format_checklist(_result_from("# Doc\n\nMentions HANDOFF_PROCESS once.\n"))
    assert "sections (spec-name / key-term mentions) ==  [1 found]" in out
    assert out.count("verdict: ___") >= 2  # >=1 per site + the additive line


# --- Step 3: isolated COMPLETENESS proof (not a drift-catch) ----------------

@pytest.mark.live_repo
def test_mutation_completeness_surfaces_the_sites_drift_would_slip_past(tmp_path):
    """COMPLETENESS proof, NOT a drift-catch.

    Inject a new required step into a COPY of the spec and leave the runbook copy
    un-updated — the partial-update scenario a version bump creates. The drift in
    the spec does NOT change what extract_sites reads from the (unchanged) runbook;
    the proof is that the enumerator SURFACES, as discrete must-verdict line items,
    the exact sites a partial update would otherwise slip past — the walkthrough
    AND the diagram — not merely a file-level "stale". The end-to-end drift CATCH
    (an LLM verdicting them `stale`) is the Integration prompt's job, not B's.
    """
    runbook_copy = tmp_path / "README.md"
    spec_copy = tmp_path / "HANDOFF_PROCESS.md"
    runbook_copy.write_text(_RUNBOOK.read_text(encoding="utf-8"), encoding="utf-8")

    # inject a NEW required step into the spec copy (runbook left un-updated)
    mutated = _SPEC.read_text(encoding="utf-8") + (
        "\n\n## Injected step (mutation)\n\n"
        "8. **New mandatory step.** Something the runbook walkthrough does not yet mention.\n"
    )
    spec_copy.write_text(mutated, encoding="utf-8")

    flag = {
        "dependent_path": str(runbook_copy),
        "spec_path": str(spec_copy),     # stem == HANDOFF_PROCESS -> spec_name resolves
        "old_version": "5.2",
        "new_version": "5.3",
    }
    result = ce.enumerate_from_flag(flag)
    sites = result["sites"]

    # the walkthrough block a partial update would skip is surfaced, as a RANGE
    walk = [s for s in sites["walkthrough_steps"] if "Paste the boot payload" in s.text]
    assert walk, "the 7-step walkthrough was not surfaced for verdict"
    assert walk[0].line_end > walk[0].line_start, "surfaced as a discrete range, not a file flag"

    # the diagram a partial update would skip is surfaced, as a RANGE
    diags = sites["diagrams"]
    assert len(diags) == 1 and "mermaid" in diags[0].anchor
    assert diags[0].line_end > diags[0].line_start

    # the rendered checklist NAMES those specific sites (not merely "stale")
    checklist = ce.format_checklist(result)
    assert "Paste the boot payload" in checklist
    assert "mermaid" in checklist
    assert "walkthrough_steps (numbered / sequential procedures) ==  [2 found]" in checklist

    # completeness, not catch: the spec mutation does not change extraction of the
    # (unchanged) runbook — extraction is identical regardless of the injected drift.
    baseline = ce.extract_sites(runbook_copy.read_text(encoding="utf-8"), "HANDOFF_PROCESS")
    assert [(s.line_start, s.line_end) for s in baseline["walkthrough_steps"]] == \
           [(s.line_start, s.line_end) for s in sites["walkthrough_steps"]]
