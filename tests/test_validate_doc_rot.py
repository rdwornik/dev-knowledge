"""Tests for scripts/validate_doc_rot.py — #140 doc-rot / grooming checker.

A read-only Layer-2 validator (mirrors #89 validate_doc_claims): surface history-accretion
bloat (ADR-88 FC4) across four deterministic sub-detectors — BACKLOG inline-history
accretion, per-section Section-history accretion, file bloat vs a declared budget, and
grooming-cadence lapse. WARN-only / fail-soft; never a gate; never mutates; one Finding
PER locus (so the #147 ship-gate dispositions each independently).

The hard closure metric (per the prompt): each detector FIRES on a real bloat condition,
witnessed by a test that trips it (the *_fires_* tests below) — not "tests pass".

Scope boundary (do NOT duplicate): #140 defers cross-file fidelity drift -> coherence-spine
(#179/#180/#182) and intra-file duplication -> #190; check #10 owns last_reviewed staleness;
#89 owns one doc's count/list self-accuracy.
"""
from __future__ import annotations

import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import validate_doc_rot as vdr  # noqa: E402
import audit as aud  # noqa: E402
from pathlib import Path  # noqa: E402
import pytest


# --- fixtures ---------------------------------------------------------------

def _task(idn: int, *, dates: int = 0, pad: int = 0) -> str:
    """A BACKLOG task line with `dates` dated blocks and ~`pad` chars of filler body."""
    blocks = " ".join(f"2026-0{i % 9 + 1}-0{i % 9 + 1}" for i in range(dates))
    body = "x" * pad
    return f"- [#{idn}] [P3][S] task {idn} — {body} {blocks} · Done when: it is done"


def _history_block(n: int, *, heading: str = "## 12. Section history") -> str:
    entries = "\n".join(f"- v1.{i} — change number {i} landed and was recorded" for i in range(n))
    return f"# Doc\n\nbody\n\n{heading}\n{entries}\n"


def _backlog(tasks: list[str], *, groom_line: str = "") -> str:
    head = "# BACKLOG\n\n## Theme\n"
    body = "\n".join(tasks)
    tail = f"\n\n{groom_line}\n" if groom_line else "\n"
    return head + body + tail


# --- sub-detector: BACKLOG inline-history accretion -------------------------

def test_backlog_accretion_fires_on_dated_accretion():
    # 3 dated blocks AND > 700 chars -> the #159/#164 condensation/grooming-gate class.
    findings = vdr.scan_backlog_accretion(_backlog([_task(134, dates=3, pad=900)]))
    assert len(findings) == 1
    assert findings[0].category == "backlog-accretion"
    assert findings[0].locus == "BACKLOG#134"
    assert "3 dated block" in findings[0].detail


def test_backlog_accretion_fires_on_gross_length_no_dates():
    # > 1200 chars with ZERO dates (the live #164 shape) -> gross bloat arm.
    findings = vdr.scan_backlog_accretion(_backlog([_task(164, dates=0, pad=1300)]))
    assert len(findings) == 1
    assert findings[0].locus == "BACKLOG#164"


def test_backlog_accretion_no_fire_on_short_multidate():
    # The #100 false-positive guard: 3 FACTUAL dates but a SHORT line (< 700) -> no fire.
    # Raw date-count alone would mis-flag; the AND-length predicate suppresses it.
    assert vdr.scan_backlog_accretion(_backlog([_task(100, dates=3, pad=50)])) == []


def test_backlog_accretion_no_fire_on_long_legit_low_date():
    # A legitimately detailed line (800 chars) with < 3 dates and < 1200 chars -> no fire.
    assert vdr.scan_backlog_accretion(_backlog([_task(50, dates=1, pad=800)])) == []


def test_backlog_accretion_ignores_non_task_lines():
    assert vdr.scan_backlog_accretion("# BACKLOG\n\nsome prose 2026-01-01 2026-02-02 2026-03-03\n") == []


# --- sub-detector: Section-history accretion --------------------------------

def test_section_history_fires_at_threshold():
    findings = vdr.scan_section_history("CLAUDE.md", _history_block(vdr._SECTION_HISTORY_MAX_ENTRIES))
    assert len(findings) == 1
    assert findings[0].category == "section-history"
    assert findings[0].locus == "CLAUDE.md#section-history"
    assert f"{vdr._SECTION_HISTORY_MAX_ENTRIES} entries" in findings[0].detail


def test_section_history_no_fire_below_threshold():
    assert vdr.scan_section_history("CLAUDE.md", _history_block(vdr._SECTION_HISTORY_MAX_ENTRIES - 1)) == []


def test_section_history_strips_ordinal_and_matches_plain_heading():
    # both "## 12. Section history" and "## Section history" are history blocks.
    assert vdr.scan_section_history("X.md", _history_block(15, heading="## Section history"))
    assert vdr.scan_section_history("X.md", _history_block(15, heading="## 12. Section history"))


def test_section_history_block_ends_at_next_section():
    # entries after the next same-level heading must NOT be counted into the block.
    text = (_history_block(13)  # 13 entries in the history block
            + "\n## 13. Next section\n- not a history entry\n- nor this one\n")
    findings = vdr.scan_section_history("CLAUDE.md", text)
    assert findings and "13 entries" in findings[0].detail


def test_section_history_none_when_no_block():
    assert vdr.scan_section_history("CLAUDE.md", "# Doc\n\n## Conventions\n- a\n- b\n") == []


# --- sub-detector: file bloat vs declared budget ----------------------------

def test_file_budget_fires_over():
    text = "\n".join(f"line {i}" for i in range(250))
    findings = vdr.scan_file_budget("CLAUDE.md", text, 200)
    assert len(findings) == 1
    assert findings[0].category == "file-budget"
    assert findings[0].locus == "CLAUDE.md#size"
    assert "budget 200" in findings[0].detail


def test_file_budget_no_fire_under():
    text = "\n".join(f"line {i}" for i in range(150))
    assert vdr.scan_file_budget("CLAUDE.md", text, 200) == []


# --- sub-detector: grooming-cadence lapse -----------------------------------

def test_grooming_cadence_fires_when_stale():
    log = "**Grooming log:** Recent: 2026-04-01 (pass). Next quarterly: 2026-07-01."
    findings = vdr.scan_grooming_cadence(_backlog([], groom_line=log), today=date(2026, 6, 1))
    assert len(findings) == 1
    assert findings[0].category == "grooming-cadence"
    assert findings[0].locus == "BACKLOG#grooming-cadence"
    assert "2026-04-01" in findings[0].detail


def test_grooming_cadence_no_fire_when_fresh():
    log = "**Grooming log:** Recent: 2026-06-18 (pass). Next quarterly: 2026-07-01."
    assert vdr.scan_grooming_cadence(_backlog([], groom_line=log), today=date(2026, 6, 19)) == []


def test_grooming_cadence_excludes_future_date():
    # The future "Next quarterly" date must NOT count as a recent groom (else never stale).
    log = "**Grooming log:** Recent: 2026-01-01. Next quarterly: 2099-07-01."
    findings = vdr.scan_grooming_cadence(_backlog([], groom_line=log), today=date(2026, 3, 1))
    assert findings and "2026-01-01" in findings[0].detail


def test_grooming_cadence_none_when_no_log():
    assert vdr.scan_grooming_cadence(_backlog([_task(1)]), today=date(2026, 6, 19)) == []


# --- scan() orchestration + format ------------------------------------------

def test_scan_clean_repo_returns_empty(tmp_path):
    (tmp_path / "BACKLOG.md").write_text(
        _backlog([_task(1, dates=1, pad=100)],
                 groom_line="**Grooming log:** Recent: 2026-06-18."), encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text(_history_block(5), encoding="utf-8")
    assert vdr.scan(tmp_path, today=date(2026, 6, 19)) == []


def test_scan_aggregates_multiple_loci(tmp_path):
    # a bloated backlog line + an over-threshold section-history block -> 2 distinct loci.
    (tmp_path / "BACKLOG.md").write_text(
        _backlog([_task(134, dates=3, pad=900)],
                 groom_line="**Grooming log:** Recent: 2026-06-18."), encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text(_history_block(20), encoding="utf-8")
    results = vdr.scan(tmp_path, today=date(2026, 6, 19))
    loci = {r.locus for r in results}
    assert "BACKLOG#134" in loci
    assert "CLAUDE.md#section-history" in loci


def test_scan_skips_missing_docs(tmp_path):
    # empty repo (no BACKLOG/CLAUDE) -> no crash, no findings.
    assert vdr.scan(tmp_path, today=date(2026, 6, 19)) == []


# --- #208 / GAP-7: scan() reads _FILE_SIZE_BUDGETS (the live-constant path) -------------
# scan_file_budget is unit-tested with an explicit budget arg; these exercise the
# ORCHESTRATION path where scan() itself supplies the budget from the live constant
# _FILE_SIZE_BUDGETS ({"CLAUDE.md": 200}). This exact wiring fired historically (CLAUDE.md
# §12 v2.22 — a 201-line CLAUDE.md), yet only the explicit-arg sub-detector was covered.

def _filler_lines(n):
    # n lines with NO history heading / task line, so ONLY the file-budget detector can fire.
    return "\n".join(["# CLAUDE"] + [f"filler line {i}" for i in range(n - 1)])


def test_scan_fires_file_budget_via_live_constant(tmp_path):
    # GAP-7 (1): a 201-line CLAUDE.md run through scan() with NO explicit budget must fire the
    # file-budget locus — scan() reads _FILE_SIZE_BUDGETS["CLAUDE.md"] (== 200) itself.
    text = _filler_lines(201)
    assert len(text.splitlines()) == 201
    (tmp_path / "CLAUDE.md").write_text(text, encoding="utf-8")
    results = vdr.scan(tmp_path, today=date(2026, 6, 19))
    budget = [r for r in results if r.category == "file-budget"]
    assert len(budget) == 1
    assert budget[0].locus == "CLAUDE.md#size"
    assert "201 lines" in budget[0].detail and "budget 200" in budget[0].detail


def test_scan_no_file_budget_under_via_live_constant(tmp_path):
    # GAP-7 (2) NEGATIVE CONTROL: a 199-line CLAUDE.md must NOT fire the budget locus
    # (199 <= 200), proving scan()'s live-constant wiring is discriminating at the boundary.
    text = _filler_lines(199)
    assert len(text.splitlines()) == 199
    (tmp_path / "CLAUDE.md").write_text(text, encoding="utf-8")
    results = vdr.scan(tmp_path, today=date(2026, 6, 19))
    assert [r for r in results if r.category == "file-budget"] == []


def test_format_findings_no_pipe():
    results = vdr.scan_backlog_accretion(_backlog([_task(134, dates=3, pad=900)]))
    out = vdr.format_findings(results)
    assert "BACKLOG#134" in out
    assert "|" not in out


# --- deployed audit check: check_doc_rot ------------------------------------

def test_check_skips_non_hub_repo(tmp_path):
    findings = aud.check_doc_rot(tmp_path / "some-child")
    assert len(findings) == 1
    assert findings[0].check_name == "doc_rot"
    assert findings[0].status == "pass"
    assert "hub-only" in findings[0].evidence


def test_check_warns_one_finding_per_locus(monkeypatch):
    # one Finding PER locus so the #147 ship-gate dispositions each independently.
    hub = Path(aud._REPO_ROOT)
    monkeypatch.setattr(aud._vdr, "scan", lambda root: [
        vdr.RotFinding("backlog-accretion", "BACKLOG#1", "3 dated blocks"),
        vdr.RotFinding("section-history", "CLAUDE.md#section-history", "20 entries")])
    findings = aud.check_doc_rot(hub)
    assert len(findings) == 2
    assert all(f.status == "warn" for f in findings)        # never "fail"
    assert all(f.check_name == "doc_rot" for f in findings)
    assert "BACKLOG#1" in findings[0].evidence
    assert all("|" not in f.evidence for f in findings)


def test_check_passes_when_clean(monkeypatch):
    monkeypatch.setattr(aud._vdr, "scan", lambda root: [])
    assert aud.check_doc_rot(Path(aud._REPO_ROOT))[0].status == "pass"


def test_check_failsoft_on_error(monkeypatch):
    def _boom(root):
        raise RuntimeError("scan exploded")

    monkeypatch.setattr(aud._vdr, "scan", _boom)
    findings = aud.check_doc_rot(Path(aud._REPO_ROOT))
    assert findings[0].status == "warn"
    assert "scan exploded" in findings[0].evidence or "degraded" in findings[0].evidence


def test_check_registered_in_all_checks():
    assert aud.check_doc_rot in aud.ALL_CHECKS


@pytest.mark.live_repo
def test_registered_check_never_fails_on_live_repo():
    # WARN-only contract holds in production: the live hub run must never return FAIL.
    for f in aud.check_doc_rot(Path(aud._REPO_ROOT)):
        assert f.status in {"pass", "warn"}


def test_e2e_seeded_bloat_fires_through_registered_check(tmp_path, monkeypatch):
    # ADR-81 'deployed' proof: a seeded gross-length BACKLOG line fires WARN through the
    # check registered in ALL_CHECKS (no scan mock) — deployed, not merely written.
    (tmp_path / "BACKLOG.md").write_text(
        "# BACKLOG\n\n## T\n- [#9] [P3][S] task " + "x" * 1300 + " done\n", encoding="utf-8")
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))   # make the temp repo look like the hub
    findings = aud.check_doc_rot(tmp_path)
    assert any(f.status == "warn" and "BACKLOG#9" in f.evidence for f in findings)
    assert aud.check_doc_rot in aud.ALL_CHECKS
