"""Tests for scripts/validate_doc_structure.py — prose structural linter (supplement organ #2).

A read-only Layer-2 validator (mirrors #140 validate_doc_rot): surface prose-shape rot —
section-numbering integrity, header-scheme consistency, ToC accuracy — across four
deterministic sub-detectors. WARN-only / fail-soft; never a gate; never mutates; one Finding
PER locus (so the #147 ship-gate dispositions each independently).

The hard closure metric (per the prompt): teeth verified RED->GREEN on a fixture corpus that
includes BOTH a real structural break AND the two known-intentional cases — the §18 numbering
gap (documented) and the embedded-template H2s inside fenced blocks. The linter is wrong if it
flags either; the *_oracle_* tests below (incl. two on the LIVE docs) pin that down.

Scope boundary (do NOT duplicate): this is structural shape, a different failure class from
#140 (history-accretion bloat) — follows its pattern, no overlap; ToC *regeneration* is gated
separately by the toc-freshness hook (this is the WARN-level fence-aware awareness complement).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import validate_doc_structure as vds  # noqa: E402
import audit as aud  # noqa: E402
from pathlib import Path  # noqa: E402


# --- fixtures ---------------------------------------------------------------

def _doc(*blocks: str) -> str:
    """A markdown doc: an H1 title + the given header/body blocks."""
    return "# Title\n\n" + "\n\n".join(blocks) + "\n"


def _h2(n: int) -> str:
    return f"## {n}. Section {n}"


def _toc(*anchors: str) -> str:
    """An auto-TOC marker block linking the given anchors."""
    links = "\n".join(f"- [{a}](#{a})" for a in anchors)
    return f"{vds._TOC_START}\n{links}\n{vds._TOC_END}"


# --- sub-detector A: numbering integrity ------------------------------------

def test_numbering_contiguous_no_fire():
    assert vds.scan_numbering("X.md", _doc(_h2(1), _h2(2), _h2(3)), set()) == []


def test_numbering_gap_fires_without_marker():
    findings = vds.scan_numbering("X.md", _doc(_h2(1), _h2(2), _h2(4)), set())
    assert len(findings) == 1
    assert findings[0].category == "numbering-gap"
    assert findings[0].locus == "X.md#numbering-3"
    assert "section 3 missing" in findings[0].detail


def test_numbering_gap_suppressed_by_marker():
    # The §18 oracle in miniature: a gap carrying a structure-allow marker -> PASSES.
    allow = {("numbering-gap", "3")}
    assert vds.scan_numbering("X.md", _doc(_h2(1), _h2(2), _h2(4)), allow) == []


def test_numbering_duplicate_fires():
    findings = vds.scan_numbering("X.md", _doc(_h2(1), _h2(1)), set())
    assert len(findings) == 1
    assert findings[0].category == "numbering-dup"
    assert findings[0].locus == "X.md#numbering-1"


def test_numbering_decrease_starts_new_run_no_fire():
    # A second independent numbered list (3 then 1) is NOT a gap (precision-over-recall).
    assert vds.scan_numbering("X.md", _doc(_h2(3), _h2(1), _h2(2)), set()) == []


def test_numbering_ignores_unnumbered_headers():
    # Foundations/Appendices (unnumbered) between numbered sections don't break the run.
    text = _doc(_h2(1), "## Foundations", _h2(2), "## Appendix A")
    assert vds.scan_numbering("X.md", text, set()) == []


# --- sub-detector B: header-scheme consistency ------------------------------

def test_malformed_missing_space_fires():
    findings = vds.scan_headers_scheme("X.md", _doc("##NoSpace", _h2(1)))
    assert any(f.category == "malformed-header" and "missing space" in f.detail for f in findings)


def test_malformed_empty_title_fires():
    findings = vds.scan_headers_scheme("X.md", _doc("## ", _h2(1)))
    assert any(f.category == "malformed-header" and "empty header" in f.detail for f in findings)


def test_duplicate_sibling_under_same_parent_fires():
    text = _doc("## Parent", "### Dup", "### Dup")
    findings = vds.scan_headers_scheme("X.md", text)
    dups = [f for f in findings if f.category == "dup-header"]
    assert len(dups) == 1
    assert "under the same parent 'Parent'" in dups[0].detail


def test_duplicate_under_different_parents_no_fire():
    # The live-PLAYBOOK shape: identical sub-headers under DIFFERENT parents are benign.
    text = _doc("## Parent A", "### Process", "## Parent B", "### Process")
    assert [f for f in vds.scan_headers_scheme("X.md", text) if f.category == "dup-header"] == []


def test_malformed_skips_fenced_content():
    # A `#comment` / `## header` inside a fence is not a malformed doc header.
    text = _doc(_h2(1)) + "\n```sh\n#!/bin/sh\n##notaheader\n```\n"
    assert [f for f in vds.scan_headers_scheme("X.md", text) if f.category == "malformed-header"] == []


# --- sub-detector C: ToC accuracy -------------------------------------------

def test_toc_clean_when_matched():
    text = "# T\n\n" + _toc("real") + "\n\n## Real\n"
    assert vds.scan_toc("X.md", text) == []


def test_toc_dangling_entry_fires():
    text = "# T\n\n" + _toc("real", "ghost") + "\n\n## Real\n"
    findings = vds.scan_toc("X.md", text)
    assert len(findings) == 1
    assert findings[0].category == "toc-dangling"
    assert "ghost" in findings[0].locus


def test_toc_orphan_header_fires():
    text = "# T\n\n" + _toc("real") + "\n\n## Real\n\n## Extra\n"
    findings = vds.scan_toc("X.md", text)
    assert len(findings) == 1
    assert findings[0].category == "toc-orphan"
    assert "extra" in findings[0].locus


def test_toc_oracle_fenced_template_h2_not_orphan():
    # THE embedded-template oracle: a `## H2` inside a fence must NOT read as missing-from-ToC.
    text = "# T\n\n" + _toc("real") + "\n\n## Real\n\n```markdown\n## What this project does\n```\n"
    assert vds.scan_toc("X.md", text) == []


def test_toc_skipped_when_no_markers():
    assert vds.scan_toc("X.md", _doc("## Real", "## Extra")) == []


# --- sub-detector D: dangling-allow self-policing ---------------------------

def test_dangling_allow_fires_when_gap_resolved():
    # Marker says gap 18, but the live numbering has no gap at 18 -> stale marker.
    findings = vds.scan_dangling_allow("X.md", set(), {("numbering-gap", "18")})
    assert len(findings) == 1
    assert findings[0].category == "dangling-allow"
    assert "18" in findings[0].locus


def test_dangling_allow_no_fire_when_gap_live():
    assert vds.scan_dangling_allow("X.md", {18}, {("numbering-gap", "18")}) == []


def test_parse_allow_markers_extracts_kind_and_locus():
    text = "prose <!-- structure-allow: numbering-gap 18 — deleted, git has it --> more"
    assert vds.parse_allow_markers(text) == {("numbering-gap", "18")}


# --- scan() orchestration + format ------------------------------------------

def test_scan_clean_doc_returns_empty(tmp_path):
    (tmp_path / "CLAUDE.md").write_text(_doc(_h2(1), _h2(2), _h2(3)), encoding="utf-8")
    assert vds.scan(tmp_path) == []


def test_scan_aggregates_distinct_loci(tmp_path):
    (tmp_path / "CLAUDE.md").write_text(_doc(_h2(1), _h2(3)), encoding="utf-8")  # gap 2
    (tmp_path / "VISION.md").write_text(_doc("##Broken", _h2(1)), encoding="utf-8")  # malformed
    loci = {r.locus for r in vds.scan(tmp_path)}
    assert "CLAUDE.md#numbering-2" in loci
    assert "VISION.md#malformed" in loci


def test_scan_skips_missing_docs(tmp_path):
    assert vds.scan(tmp_path) == []


def test_format_findings_no_pipe():
    out = vds.format_findings(vds.scan_numbering("X.md", _doc(_h2(1), _h2(3)), set()))
    assert "numbering-2" in out
    assert "|" not in out


# --- deployed audit check: check_doc_structure ------------------------------

def test_check_skips_non_hub_repo(tmp_path):
    findings = aud.check_doc_structure(tmp_path / "some-child")
    assert len(findings) == 1
    assert findings[0].check_name == "doc_structure"
    assert findings[0].status == "pass"
    assert "hub-only" in findings[0].evidence


def test_check_warns_one_finding_per_locus(monkeypatch):
    monkeypatch.setattr(aud._vds, "scan", lambda root: [
        vds.StructureFinding("numbering-gap", "X.md#numbering-3", "section 3 missing"),
        vds.StructureFinding("toc-orphan", "Y.md#hdr:foo", "header missing from ToC")])
    findings = aud.check_doc_structure(Path(aud._REPO_ROOT))
    assert len(findings) == 2
    assert all(f.status == "warn" for f in findings)          # never "fail"
    assert all(f.check_name == "doc_structure" for f in findings)
    assert "numbering-3" in findings[0].evidence
    assert all("|" not in f.evidence for f in findings)


def test_check_passes_when_clean(monkeypatch):
    monkeypatch.setattr(aud._vds, "scan", lambda root: [])
    assert aud.check_doc_structure(Path(aud._REPO_ROOT))[0].status == "pass"


def test_check_failsoft_on_error(monkeypatch):
    def _boom(root):
        raise RuntimeError("scan exploded")

    monkeypatch.setattr(aud._vds, "scan", _boom)
    findings = aud.check_doc_structure(Path(aud._REPO_ROOT))
    assert findings[0].status == "warn"
    assert "scan exploded" in findings[0].evidence or "degraded" in findings[0].evidence


def test_check_registered_in_all_checks():
    assert aud.check_doc_structure in aud.ALL_CHECKS


def test_registered_check_never_fails_on_live_repo():
    for f in aud.check_doc_structure(Path(aud._REPO_ROOT)):
        assert f.status in {"pass", "warn"}


def test_e2e_seeded_break_fires_through_registered_check(tmp_path, monkeypatch):
    # ADR-81 'deployed' proof: a seeded numbering gap fires WARN through the registered check.
    (tmp_path / "CLAUDE.md").write_text(_doc(_h2(1), _h2(3)), encoding="utf-8")  # gap 2
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))     # make the temp repo look like the hub
    findings = aud.check_doc_structure(tmp_path)
    assert any(f.status == "warn" and "numbering-2" in f.evidence for f in findings)
    assert aud.check_doc_structure in aud.ALL_CHECKS


# --- acceptance oracle on the LIVE docs -------------------------------------

def _live(rel: str) -> str:
    return (Path(vds._REPO_ROOT) / rel).read_text(encoding="utf-8")


def test_live_hub_scan_is_clean():
    # The headline acceptance: the live docs PASS (§18 marker + fence-awareness keep it clean).
    assert vds.scan(Path(vds._REPO_ROOT)) == []


def test_live_playbook_section18_marker_is_load_bearing():
    # The §18 oracle on REAL data: the gap is suppressed BY the marker (and is not dangling).
    pb = _live("protocols/PLAYBOOK.md")
    allow = vds.parse_allow_markers(pb)
    assert vds.scan_numbering("protocols/PLAYBOOK.md", pb, allow) == []
    assert vds.scan_numbering("protocols/PLAYBOOK.md", pb, set())  # WITHOUT the marker it WOULD flag
    assert vds.scan_dangling_allow("protocols/PLAYBOOK.md", vds.numbering_gaps(pb), allow) == []


def test_live_playbook_toc_fence_awareness():
    # The embedded-template oracle on REAL data: PLAYBOOK's fenced H2s don't read as orphans.
    assert vds.scan_toc("protocols/PLAYBOOK.md", _live("protocols/PLAYBOOK.md")) == []
