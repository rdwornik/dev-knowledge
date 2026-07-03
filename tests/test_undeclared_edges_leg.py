"""Tests for the audit ship-gate WARN leg `check_undeclared_edges` (Fable consult #1 ruling #2,
2026-07-03) — the audit-side wiring of the #179 undeclared-edge scan.

Distinct from tests/test_scan_undeclared_edges.py (which tests the scan LOGIC): this file tests
the LEG — registration in ALL_CHECKS, the hub-only guard, fail-soft, one-Finding-per-candidate,
the Tier<=2 filter, and — the done-contract for ruling #2 — that the WARN actually FIRES on a
crafted undeclared-edge repo (presence in ALL_CHECKS is NOT closure; demonstrated firing is).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit as aud


# --- crafted-corpus builders (mirror test_scan_undeclared_edges idiom) -------

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


def _as_hub(monkeypatch, repo: Path) -> None:
    """Make `repo` look like the hub so the hub-only guard evaluates instead of skipping."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(repo))


# --- registration ------------------------------------------------------------

def test_undeclared_edges_registered_in_all_checks() -> None:
    """Wired into ALL_CHECKS (so health / ship-gate / run / fleet_health surface it)."""
    assert aud.check_undeclared_edges in aud.ALL_CHECKS


# --- the FIRING / done-contract test (TEETH) ---------------------------------

def test_undeclared_edges_fires_on_undeclared_prose_edge(tmp_path: Path, monkeypatch) -> None:
    """TEETH: a doc that prose-references a registered spec with NO reconciled_with declaration
    MUST produce a WARN. This is ruling #2's done-proof — if this reds, the leg does not enforce.
    """
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See protocols/HANDOFF_PROCESS.md for the runbook.")
    _as_hub(monkeypatch, tmp_path)
    findings = aud.check_undeclared_edges(tmp_path)
    assert len(findings) == 1
    f = findings[0]
    assert f.status == "warn", f.evidence
    assert "GUIDE.md -> handoff-process" in f.evidence
    assert "FC2" in f.evidence


# --- the negative half: declared edge does not fire --------------------------

def test_undeclared_edges_pass_when_declared(tmp_path: Path, monkeypatch) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See protocols/HANDOFF_PROCESS.md.",
         reconciled="handoff-process@5.2")
    _as_hub(monkeypatch, tmp_path)
    findings = aud.check_undeclared_edges(tmp_path)
    assert len(findings) == 1
    assert findings[0].status == "pass", findings[0].evidence


# --- one WARN per candidate (ship-gate dispositions each independently) ------

def test_undeclared_edges_one_finding_per_candidate(tmp_path: Path, monkeypatch) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See protocols/HANDOFF_PROCESS.md.")
    _doc(tmp_path, "OTHER.md", "Follows protocols/HANDOFF_PROCESS.md too.")
    _as_hub(monkeypatch, tmp_path)
    findings = aud.check_undeclared_edges(tmp_path)
    assert len(findings) == 2
    assert all(f.status == "warn" for f in findings)
    assert {"GUIDE.md", "OTHER.md"} == {
        f.evidence.split(" -> ")[0].split(": ")[-1] for f in findings}


# --- the Tier<=2 filter: a tier-3 bare mention is NOT WARNed -----------------

def test_undeclared_edges_tier3_bare_mention_not_warned(tmp_path: Path, monkeypatch) -> None:
    """A tier-3 bare-name mention (no filename, no spec-id token) is a WEAK signal the scan
    retains but the leg does NOT WARN on — the standalone reporter still surfaces it. This
    documents the filter; it does not hide a genuine (tier<=2) undeclared edge."""
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "This follows the same HANDOFF_PROCESS pattern as elsewhere.")
    _as_hub(monkeypatch, tmp_path)
    findings = aud.check_undeclared_edges(tmp_path)
    assert len(findings) == 1
    assert findings[0].status == "pass", findings[0].evidence


# --- hub-only guard: no-op pass off the hub ----------------------------------

def test_undeclared_edges_hub_only_skip(tmp_path: Path, monkeypatch) -> None:
    _spec(tmp_path)
    _doc(tmp_path, "GUIDE.md", "See protocols/HANDOFF_PROCESS.md.")
    # _REPO_ROOT stays the real hub; tmp_path != hub -> skip
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path / "not-the-hub"))
    findings = aud.check_undeclared_edges(tmp_path)
    assert len(findings) == 1
    assert findings[0].status == "pass"
    assert "hub-only" in findings[0].evidence


# --- fail-soft: an error in the scan never wedges the gate -------------------

def test_undeclared_edges_fail_soft(tmp_path: Path, monkeypatch) -> None:
    def boom(*_a, **_k):
        raise RuntimeError("scan exploded")
    _as_hub(monkeypatch, tmp_path)
    monkeypatch.setattr(aud._sue, "scan", boom)
    findings = aud.check_undeclared_edges(tmp_path)
    assert len(findings) == 1
    assert findings[0].status == "warn"
    assert "degraded" in findings[0].evidence
