"""Tests for scripts/scan_undeclared_edges.py — the #179 undeclared-edge scan (FC2).

Covers: the RED->GREEN done-when (prose-ref-without-edge surfaced; declared-edge not),
tier classification, the gap-only / self / excluded-dir exclusions, fence-excluded
matching (the operator's verify — a fenced operational path ref is not a candidate),
tier-3 RETENTION as enumerated weak signals (never dropped), read-only-ness, registry
generality, and the report's two sections + confirm hint.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import scan_undeclared_edges as sue
import validate_reconciliation as vr

SPEC = vr._SPEC_REGISTRY["handoff-process"]          # id handoff-process, protocols/HANDOFF_PROCESS.md


# --- fixture-corpus builders (mirror test_validate_reconciliation idiom) -----

def _spec(repo: Path, version: str = "5.2") -> None:
    (repo / "protocols").mkdir(parents=True, exist_ok=True)
    (repo / "protocols" / "HANDOFF_PROCESS.md").write_text(
        f"# HANDOFF_PROCESS\n\nVersion: {version}\nStatus: stable\n", encoding="utf-8")


def _doc(repo: Path, name: str, body: str, reconciled: str | None = None) -> None:
    fm = "---\nlast_reviewed: 2026-06-17\n"
    if reconciled is not None:
        fm += f"reconciled_with: {reconciled}\n"
    fm += "---\n\n" + body + "\n"
    p = repo / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(fm, encoding="utf-8")


def _cand_paths(results, *, tier_max: int) -> set[str]:
    return {c.dependent_path for c in results if c.best_tier <= tier_max}


def _weak_paths(results) -> set[str]:
    return {c.dependent_path for c in results if c.best_tier > sue._CANDIDATE_TIER_MAX}


# --- RED -> GREEN: the #179 done-when ---------------------------------------

def test_prose_path_ref_without_edge_is_surfaced(tmp_path: Path) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See protocols/HANDOFF_PROCESS.md for the runbook.")
    results = sue.scan(tmp_path)
    cands = [c for c in results if c.dependent_path == "GUIDE.md"]
    assert len(cands) == 1
    assert cands[0].spec_id == "handoff-process" and cands[0].best_tier == 1


def test_prose_id_ref_without_edge_is_surfaced(tmp_path: Path) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "This follows the handoff-process flow.")
    cands = _cand_paths(sue.scan(tmp_path), tier_max=2)
    assert "GUIDE.md" in cands


def test_declared_edge_is_not_surfaced(tmp_path: Path) -> None:
    # the negative half of the done-when: a doc that PROPERLY declares the edge
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See protocols/HANDOFF_PROCESS.md.",
         reconciled="handoff-process@5.2")
    assert sue.scan(tmp_path) == []


def test_declared_to_older_version_still_excluded(tmp_path: Path) -> None:
    # gap-only rule: an already-declared edge (even stale) is the version checker's job
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See protocols/HANDOFF_PROCESS.md.",
         reconciled="handoff-process@5.1")
    assert sue.scan(tmp_path) == []


def test_malformed_declaration_still_excluded(tmp_path: Path) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "Uses handoff-process.", reconciled="handoff-process")
    assert sue.scan(tmp_path) == []


def test_spec_file_does_not_surface_itself(tmp_path: Path) -> None:
    _spec(tmp_path)                               # the only .md in the tree
    assert sue.scan(tmp_path) == []


def test_unrelated_doc_not_surfaced(tmp_path: Path) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "Some prose with no reference at all.")
    assert sue.scan(tmp_path) == []


def test_excluded_dir_copy_pruned(tmp_path: Path) -> None:
    _spec(tmp_path)
    (tmp_path / ".git").mkdir()
    _doc(tmp_path, ".git/COPY.md", "See protocols/HANDOFF_PROCESS.md.")
    assert sue.scan(tmp_path) == []


# --- fence-excluded MATCHING (the operator's non-blocking verify) ------------

def test_fenced_path_ref_is_not_matched(tmp_path: Path) -> None:
    _spec(tmp_path)
    body = ("Run the example:\n\n"
            "```\npy scripts/foo.py --spec protocols/HANDOFF_PROCESS.md\n```\n\n"
            "Done.")
    _doc(tmp_path, "GUIDE.md", body)
    # the only spec reference lives inside a fence -> not a content-dependency -> no candidate
    assert sue.scan(tmp_path) == []


def test_inline_code_span_ref_is_matched(tmp_path: Path) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See `protocols/HANDOFF_PROCESS.md` for the runbook.")
    # an inline span on a prose line is a genuine reference -> still surfaced (tier 1)
    assert "GUIDE.md" in _cand_paths(sue.scan(tmp_path), tier_max=2)


# --- tier classification (reference_sites, pure) -----------------------------

def test_reference_sites_tiers() -> None:
    assert reference_tier("See protocols/HANDOFF_PROCESS.md here.") == 1
    assert reference_tier("The file HANDOFF_PROCESS.md is canonical.") == 1
    assert reference_tier("Follows the handoff-process flow.") == 2
    assert reference_tier("Read HANDOFF_BOOT first.") == 3
    assert reference_tier("The handoff process is described elsewhere.") == 3
    assert sue.reference_sites("nothing relevant here.\n", SPEC) == []


def reference_tier(line: str) -> int:
    sites = sue.reference_sites(line + "\n", SPEC)
    assert len(sites) == 1, f"expected one site for {line!r}, got {sites}"
    return sites[0].tier


# --- tier-3 RETENTION: weak signals enumerated, never dropped ----------------

def test_tier3_only_doc_retained_as_weak_not_candidate(tmp_path: Path) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "WEAK.md", "Read HANDOFF_BOOT and the handoff process overview.")
    results = sue.scan(tmp_path)
    assert "WEAK.md" not in _cand_paths(results, tier_max=2)   # not a candidate
    weak = [c for c in results if c.dependent_path == "WEAK.md"]
    assert len(weak) == 1 and weak[0].best_tier == 3
    assert weak[0].sites, "weak signal must carry its evidence sites (human-promotable)"


# --- read-only contract ------------------------------------------------------

def test_scan_mutates_nothing(tmp_path: Path) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See protocols/HANDOFF_PROCESS.md.")
    before = {p: p.read_bytes() for p in tmp_path.rglob("*.md")}
    sue.scan(tmp_path)
    after = {p: p.read_bytes() for p in tmp_path.rglob("*.md")}
    assert before == after, "scan must not write or create any file (NO auto-declare)"


# --- registry generality (not hardcoded to handoff-process) ------------------

def test_custom_registry_generality(tmp_path: Path) -> None:
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "MY_SPEC.md").write_text(
        "# MY_SPEC\n\nVersion: 1.0\n", encoding="utf-8")
    _doc(tmp_path, "USES.md", "Built against specs/MY_SPEC.md.")
    registry = {"my-spec": vr.SpecSource("my-spec", "specs/MY_SPEC.md")}
    results = sue.scan(tmp_path, registry=registry)
    cands = [c for c in results if c.dependent_path == "USES.md"]
    assert len(cands) == 1 and cands[0].spec_id == "my-spec" and cands[0].best_tier == 1


# --- fixture corpus: the exact candidate set (the done-when corpus) ----------

def test_fixture_corpus_exact_candidate_set(tmp_path: Path) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "PATHREF.md", "See protocols/HANDOFF_PROCESS.md.")            # tier1 cand
    _doc(tmp_path, "IDREF.md", "Follows the handoff-process flow.")             # tier2 cand
    _doc(tmp_path, "DECLARED.md", "See protocols/HANDOFF_PROCESS.md.",
         reconciled="handoff-process@5.2")                                      # excluded
    _doc(tmp_path, "UNRELATED.md", "No reference whatsoever.")                  # excluded
    _doc(tmp_path, "FAMILY.md", "Read HANDOFF_BOOT.")                           # tier3 weak
    results = sue.scan(tmp_path)
    assert _cand_paths(results, tier_max=2) == {"PATHREF.md", "IDREF.md"}
    assert _weak_paths(results) == {"FAMILY.md"}
    all_paths = {c.dependent_path for c in results}
    assert "DECLARED.md" not in all_paths
    assert "UNRELATED.md" not in all_paths
    assert "protocols/HANDOFF_PROCESS.md" not in all_paths


# --- report rendering --------------------------------------------------------

def test_format_report_two_sections_and_confirm_hint(tmp_path: Path) -> None:
    _spec(tmp_path, "5.2")
    _doc(tmp_path, "PATHREF.md", "See protocols/HANDOFF_PROCESS.md.")
    _doc(tmp_path, "FAMILY.md", "Read HANDOFF_BOOT.")
    report = sue.format_report(tmp_path, sue.scan(tmp_path))
    assert "CANDIDATES" in report
    assert "WEAK SIGNALS" in report and "RETAINED" in report
    assert "PATHREF.md" in report and "FAMILY.md" in report      # both enumerated
    # surface-only confirm hint carries the LIVE spec version; never written to a file
    assert "reconciled_with: handoff-process@5.2" in report


def test_snippet_is_fence_safe(tmp_path: Path) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See `protocols/HANDOFF_PROCESS.md` now.")
    sites = sue.reference_sites((tmp_path / "GUIDE.md").read_text(encoding="utf-8"), SPEC)
    assert sites and all("`" not in s.snippet and "\n" not in s.snippet for s in sites)


def test_main_exits_zero() -> None:
    assert sue.main() == 0
