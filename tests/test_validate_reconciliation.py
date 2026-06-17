"""Tests for scripts/validate_reconciliation.py + the audit adapter.

Covers the pure parsing/version helpers, the discovery + reconcile classifier, the
Prompt-B enumerate_edges contract, and the audit.check_reconciled_versions mapping
(match -> no FAIL; mismatch -> FAIL; malformed -> WARN; fail-open on own error).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit as aud
import validate_reconciliation as vr

SPEC_V52 = """\
# HANDOFF_PROCESS v5

Version: 5.2
Status: stable
"""


def _spec(repo: Path, version_line: str = "Version: 5.2") -> None:
    (repo / "protocols").mkdir(parents=True, exist_ok=True)
    (repo / "protocols" / "HANDOFF_PROCESS.md").write_text(
        f"# HANDOFF_PROCESS\n\n{version_line}\nStatus: stable\n", encoding="utf-8")


def _dependent(repo: Path, name: str, reconciled: str | None) -> None:
    fm = "---\nlast_reviewed: 2026-06-17\n"
    if reconciled is not None:
        fm += f"reconciled_with: {reconciled}\n"
    fm += "---\n\n# Doc\n"
    (repo / name).write_text(fm, encoding="utf-8")


# --- pure helpers -----------------------------------------------------------

def test_parse_reconciled_with_present() -> None:
    text = "---\nreconciled_with: handoff-process@5.2\n---\n# x\n"
    assert vr.parse_reconciled_with(text) == "handoff-process@5.2"


def test_parse_reconciled_with_absent() -> None:
    assert vr.parse_reconciled_with("---\nlast_reviewed: 2026-06-17\n---\n# x\n") is None
    assert vr.parse_reconciled_with("# no frontmatter\n") is None


def test_split_edge_wellformed_and_malformed() -> None:
    assert vr.split_edge("handoff-process@5.2") == ("handoff-process", "5.2")
    assert vr.split_edge("handoff-process") is None
    assert vr.split_edge("handoff-process@v5") is None  # no leading-v, numeric only


def test_norm_version_trailing_zero() -> None:
    assert vr.norm_version("5.2") == vr.norm_version("5.2.0")
    assert vr.norm_version("5.2") != vr.norm_version("5.3")


def test_spec_current_version_live(tmp_path: Path) -> None:
    _spec(tmp_path, "Version: v5.4.1")
    spec = vr._SPEC_REGISTRY["handoff-process"]
    assert vr.spec_current_version(tmp_path, spec) == "5.4.1"


# --- the one shared spec-version parser (#172 dedup) -------------------------
# Two consumer contracts diverge by CAPTURE SCOPE, so they are pinned separately and the
# dedup preserves both: the checker numeric-normalizes (v stripped, above), the enumerator
# surfaces the raw token full-text (test_coherence_enumerator). One regex, two behaviors.

def test_parse_spec_version_tolerant_keeps_full_token() -> None:
    # the shared extractor returns the raw token VERBATIM (full-text — keeps a leading v)
    assert vr.parse_spec_version("# S\n\nVersion: v5.4.1\nStatus: x\n") == "v5.4.1"
    assert vr.parse_spec_version("# S\n\nVersion: 9.9\n") == "9.9"
    assert vr.parse_spec_version("# S\n\nno version here\n") == ""


def test_spec_current_version_numeric_normalizes_the_shared_token(tmp_path: Path) -> None:
    # A's CONSUMER layer strips the v and keeps dotted-numeric (for version comparison),
    # distinct from the raw token the shared parser returns — NOT a second parser.
    _spec(tmp_path, "Version: v5.4.1")
    assert vr.parse_spec_version("Version: v5.4.1\n") == "v5.4.1"
    assert vr.spec_current_version(tmp_path, vr._SPEC_REGISTRY["handoff-process"]) == "5.4.1"


def test_spec_version_numeric_is_the_shared_comparison_form() -> None:
    # the comparison form both equality consumers (checker + nudge) share: numeric, v stripped
    assert vr.spec_version_numeric("Version: v5.4.1\n") == "5.4.1"
    assert vr.spec_version_numeric("Version: 9.9\n") == "9.9"
    assert vr.spec_version_numeric("no version here\n") == ""


# --- reconcile classifier ---------------------------------------------------

def test_reconcile_match(tmp_path: Path) -> None:
    _spec(tmp_path)
    _dependent(tmp_path, "README.md", "handoff-process@5.2")
    results = vr.reconcile(tmp_path)
    assert len(results) == 1 and results[0].status == "match"


def test_reconcile_match_normalizes_trailing_zero(tmp_path: Path) -> None:
    _spec(tmp_path, "Version: 5.2")
    _dependent(tmp_path, "README.md", "handoff-process@5.2.0")
    assert vr.reconcile(tmp_path)[0].status == "match"


def test_reconcile_mismatch(tmp_path: Path) -> None:
    _spec(tmp_path, "Version: 5.2")
    _dependent(tmp_path, "README.md", "handoff-process@5.1")
    r = vr.reconcile(tmp_path)[0]
    assert r.status == "mismatch" and r.declared == "5.1" and r.current == "5.2"


def test_reconcile_malformed(tmp_path: Path) -> None:
    _spec(tmp_path)
    _dependent(tmp_path, "README.md", "handoff-process")  # no @version
    assert vr.reconcile(tmp_path)[0].status == "malformed"


def test_reconcile_unknown_spec(tmp_path: Path) -> None:
    _spec(tmp_path)
    _dependent(tmp_path, "README.md", "nonesuch@1.0")
    assert vr.reconcile(tmp_path)[0].status == "unknown-spec"


def test_reconcile_spec_absent_is_unknown(tmp_path: Path) -> None:
    _dependent(tmp_path, "README.md", "handoff-process@5.2")  # no spec file written
    assert vr.reconcile(tmp_path)[0].status == "unknown-spec"


def test_reconcile_no_edges(tmp_path: Path) -> None:
    _spec(tmp_path)
    _dependent(tmp_path, "README.md", None)
    assert vr.reconcile(tmp_path) == []


def test_discover_prunes_excluded_dirs(tmp_path: Path) -> None:
    _spec(tmp_path)
    (tmp_path / ".git").mkdir()
    _dependent(tmp_path, ".git/COPY.md", "handoff-process@5.1")
    _dependent(tmp_path, "README.md", "handoff-process@5.2")
    paths = [p for p, _ in vr.discover_dependents(tmp_path)]
    assert paths == ["README.md"]


# --- enumerate_edges (Prompt-B contract) ------------------------------------

def test_enumerate_edges_contract(tmp_path: Path) -> None:
    _spec(tmp_path, "Version: 5.2")
    _dependent(tmp_path, "README.md", "handoff-process@5.1")
    edges = vr.enumerate_edges(tmp_path)
    assert len(edges) == 1
    e = edges[0]
    assert e.dependent_path == "README.md"
    assert e.spec_path == "protocols/HANDOFF_PROCESS.md"
    assert e.old_version == "5.1" and e.new_version == "5.2"


def test_enumerate_edges_excludes_malformed(tmp_path: Path) -> None:
    _spec(tmp_path)
    _dependent(tmp_path, "README.md", "handoff-process")  # malformed
    assert vr.enumerate_edges(tmp_path) == []


# --- audit adapter ----------------------------------------------------------

def test_adapter_match_no_finding(tmp_path: Path) -> None:
    _spec(tmp_path, "Version: 5.2")
    _dependent(tmp_path, "README.md", "handoff-process@5.2")
    findings = aud.check_reconciled_versions(tmp_path)
    assert len(findings) == 1 and findings[0].status == "pass"


def test_adapter_mismatch_fails(tmp_path: Path) -> None:
    _spec(tmp_path, "Version: 5.2")
    _dependent(tmp_path, "README.md", "handoff-process@5.1")
    findings = aud.check_reconciled_versions(tmp_path)
    assert [f.status for f in findings] == ["fail"]


def test_adapter_malformed_warns(tmp_path: Path) -> None:
    _spec(tmp_path)
    _dependent(tmp_path, "README.md", "handoff-process")
    findings = aud.check_reconciled_versions(tmp_path)
    assert [f.status for f in findings] == ["warn"]


def test_adapter_no_edges_passes(tmp_path: Path) -> None:
    findings = aud.check_reconciled_versions(tmp_path)
    assert len(findings) == 1 and findings[0].status == "pass"


def test_adapter_registered_in_all_checks() -> None:
    assert aud.check_reconciled_versions in aud.ALL_CHECKS
