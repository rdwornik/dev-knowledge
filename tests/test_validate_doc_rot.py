"""Tests for scripts/validate_doc_rot.py — #140 doc-rot / grooming checker.

A read-only Layer-2 validator (mirrors #89 validate_doc_claims): surface history-accretion
bloat (ADR-88 FC4) across five deterministic sub-detectors — BACKLOG inline-history
accretion (ARM 1), BACKLOG row length (ARM 2), per-section Section-history accretion, file
bloat vs a declared budget, and grooming-cadence lapse. WARN-only / fail-soft; never a gate;
never mutates; one Finding PER locus (so the #147 ship-gate dispositions each independently).

The hard closure metric (per the prompt): each detector FIRES on a real bloat condition,
witnessed by a test that trips it (the *_fires_* tests below) — not "tests pass".

[#532] raises that bar for ARM 1 specifically. ARM 1 fires on ZERO live rows (the corpus is
clean of the class), and an arm that fires on nothing is indistinguishable from an arm that
is dead — so its firing behaviour is pinned by a MANDATORY SYNTHETIC FIXTURE
(`_ACCRETED_ROW`) rather than by live data, and the arm's three terms each carry a negative
control that isolates it. Without those, the amendment would be unfalsifiable.

Scope boundary (do NOT duplicate): #140 defers cross-file fidelity drift -> coherence-spine
(#179/#180/#182) and intra-file duplication -> #190; check #10 owns last_reviewed staleness;
#89 owns one doc's count/list self-accuracy.
"""
from __future__ import annotations

from datetime import date


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


# --- [#532] ARM 1: BACKLOG inline-history accretion -------------------------
# ARM 1 = >= 3 DISTINCT citation-blind history dates AND span >= 30d AND > 700 chars.
# Every test in this block passes an explicit `today` so the suite cannot drift with the
# wall clock (the future-date filter is date-relative).

_TODAY = date(2026, 8, 16)


def _dated_row(idn: int, dates: list[str], *, pad: int = 900) -> str:
    """A BACKLOG task line carrying exactly `dates` as BARE inline history dates."""
    return (f"- [#{idn}] [P3][S] task {idn} — " + "x" * pad + " "
            + " ".join(dates) + " · Done when: it is done")


# THE MANDATORY ARM-1 FIXTURE. Three distinct citation-blind history dates spanning 166
# days in a 900-char body: the ADR-65/49 shape the arm exists to name. Pinned synthetically
# because the live corpus has ZERO instances -- this row is the proof the arm is alive.
_ACCRETED_ROW = _dated_row(777, ["2026-01-05", "2026-03-10", "2026-06-20"])


def test_arm1_fires_on_the_mandatory_accretion_fixture():
    findings = vdr.scan_backlog_accretion(_backlog([_ACCRETED_ROW]), _TODAY)
    arm1 = [f for f in findings if f.category == "backlog-accretion"]
    assert len(arm1) == 1
    assert arm1[0].locus == "BACKLOG#777"
    assert "3 history dates" in arm1[0].detail
    assert "spanning 166d" in arm1[0].detail          # 2026-01-05 -> 2026-06-20


def test_arm1_no_fire_when_span_below_threshold():
    # NEGATIVE CONTROL for the SPAN term (the young-row misfire, [#523], that ARM 1 fixes):
    # 3 distinct dates and > 700 chars — the OLD predicate fired here — but 19d apart.
    row = _dated_row(778, ["2026-06-01", "2026-06-10", "2026-06-20"])
    assert [f for f in vdr.scan_backlog_accretion(_backlog([row]), _TODAY)
            if f.category == "backlog-accretion"] == []


def test_arm1_no_fire_when_dates_are_artifact_citations():
    # NEGATIVE CONTROL for CITATION-BLINDNESS: the same three wide-span dates, but each one
    # inside a `YYYY-MM-DD-slug` artifact identifier. Citing evidence is not accreting it.
    row = _dated_row(779, ["docs/audits/2026-01-05-technical-a.md",
                           "docs/audits/2026-03-10-technical-b.md",
                           "2026-06-20-dev-knowledge-architect"])
    assert [f for f in vdr.scan_backlog_accretion(_backlog([row]), _TODAY)
            if f.category == "backlog-accretion"] == []


def test_arm1_no_fire_on_short_multidate():
    # The #100 false-positive guard, unchanged by the split: 3 wide-span FACTUAL dates but a
    # SHORT line (< 700) -> no fire. The length term still suppresses it.
    row = _dated_row(100, ["2026-01-05", "2026-03-10", "2026-06-20"], pad=50)
    assert vdr.scan_backlog_accretion(_backlog([row]), _TODAY) == []


def test_arm1_no_fire_on_long_legit_low_date():
    # A legitimately detailed line (800 chars) with 1 date and under the ceiling -> no fire.
    assert vdr.scan_backlog_accretion(_backlog([_task(50, dates=1, pad=800)]), _TODAY) == []


def test_arm1_ignores_non_task_lines():
    assert vdr.scan_backlog_accretion(
        "# BACKLOG\n\nsome prose 2026-01-01 2026-03-03 2026-06-06\n", _TODAY) == []


# --- [#532] _history_dates: the three filters, in isolation -----------------

def test_history_dates_strips_artifact_identifiers():
    line = "cites docs/audits/2026-08-15-technical-x.md and 2026-07-02-ai-council-architect"
    assert vdr._history_dates(line, _TODAY) == []


def test_history_dates_keeps_a_bare_inline_date():
    assert vdr._history_dates("ruled 2026-05-01 by the architect", _TODAY) == [date(2026, 5, 1)]


def test_history_dates_collapses_duplicates():
    # The same date written twice is ONE history entry, not two.
    assert vdr._history_dates("2026-05-01 and again 2026-05-01", _TODAY) == [date(2026, 5, 1)]


def test_history_dates_drops_future_recheck_pegs():
    # A FUTURE date is a re-check peg (a plan), never accreted history ([#492]'s 2026-08-17).
    assert vdr._history_dates("done 2026-05-01, re-check 2099-01-01", _TODAY) == [date(2026, 5, 1)]


def test_history_dates_survives_a_date_shaped_non_date():
    # _DATE_RE matches on SHAPE, so a malformed token must be dropped, never raised on —
    # the scanner is fail-soft by contract and must not degrade the check to a WARN.
    assert vdr._history_dates("2026-99-99 and 2026-05-01", _TODAY) == [date(2026, 5, 1)]


# --- [#532] ARM 2: BACKLOG row length (a DECLARED ceiling) ------------------

def _row_of_length(idn: int, n: int) -> str:
    """A task line of EXACTLY `n` characters, carrying no dates."""
    stem = f"- [#{idn}] [P3][S] task {idn} — "
    return stem + "x" * (n - len(stem))


def test_arm2_fires_one_char_over_the_declared_ceiling():
    # THE ARM-2 FIXTURE, pinned AT its declared ceiling: 1321 chars fires...
    row = _row_of_length(164, vdr._BACKLOG_ROW_CEILING + 1)
    assert len(row) == 1321
    findings = vdr.scan_backlog_accretion(_backlog([row]), _TODAY)
    assert len(findings) == 1
    assert findings[0].category == "backlog-row-length"
    assert findings[0].locus == "BACKLOG#164"
    assert "1321 chars" in findings[0].detail
    assert "declared ceiling 1320" in findings[0].detail


def test_arm2_no_fire_exactly_at_the_declared_ceiling():
    # ...and 1320 does NOT. The ceiling is a DECLARED contract, so its boundary is pinned
    # in both directions — `> ceiling`, not `>=`.
    row = _row_of_length(165, vdr._BACKLOG_ROW_CEILING)
    assert len(row) == 1320
    assert vdr.scan_backlog_accretion(_backlog([row]), _TODAY) == []


def test_arm2_fires_with_zero_dates():
    # ARM 2 is a SIZE contract: it is entirely independent of the date terms.
    row = _row_of_length(166, 2000)
    findings = vdr.scan_backlog_accretion(_backlog([row]), _TODAY)
    assert [f.category for f in findings] == ["backlog-row-length"]


# --- [#532] the split itself: two arms, two names, one locus ----------------

def test_both_arms_fire_independently_on_one_row():
    # A row that is BOTH accreted and over-long yields TWO findings on the SAME locus, with
    # DIFFERENT categories — which is the whole point of the split: the output says which
    # contract was breached, and the #147 ship-gate dispositions each independently.
    row = _dated_row(780, ["2026-01-05", "2026-03-10", "2026-06-20"], pad=1500)
    findings = vdr.scan_backlog_accretion(_backlog([row]), _TODAY)
    assert {f.category for f in findings} == {"backlog-accretion", "backlog-row-length"}
    assert {f.locus for f in findings} == {"BACKLOG#780"}


def test_the_two_arm_names_are_distinct_and_registered():
    # Both arms must be reachable under their OWN name — a rename that silently collapsed
    # one into the other would still pass every per-arm test above.
    both = vdr.scan_backlog_accretion(
        _backlog([_ACCRETED_ROW, _row_of_length(781, 1400)]), _TODAY)
    assert {f.category for f in both} == {"backlog-accretion", "backlog-row-length"}


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


# --- #312: comment-only lines are EXCLUDED from the prose budget -------------

def test_is_comment_only_boundary():
    # A fully render-invisible comment line (any surrounding whitespace) -> excluded.
    assert vdr._is_comment_only("<!-- methodology:start id=x owner=hub -->")
    assert vdr._is_comment_only("  <!-- scope: meta -->  ")
    assert vdr._is_comment_only("<!-- version: 2.35 -->")
    # A line that MIXES prose with a comment still counts (narrow loophole).
    assert not vdr._is_comment_only("prose <!-- trailing note -->")
    assert not vdr._is_comment_only("<!-- leading --> then prose")
    assert not vdr._is_comment_only("- **Naming:** UPPERCASE living docs")


def test_file_budget_excludes_comment_only_lines():
    # 190 prose lines (< 200) plus 40 comment-only marker lines: raw count 230 would fire,
    # but the prose budget must NOT — the markers are render-invisible metadata (#312).
    prose = [f"line {i}" for i in range(190)]
    markers = ["<!-- methodology:start id=r owner=hub -->",
               "<!-- methodology:end id=r -->"] * 20
    text = "\n".join(prose + markers)
    assert len(text.splitlines()) == 230  # raw line count is over budget
    assert vdr.scan_file_budget("CLAUDE.md", text, 200) == []  # prose count (190) is not


def test_file_budget_counts_mixed_prose_comment_lines():
    # 201 lines each mixing prose with a trailing comment -> NOT comment-only -> all count.
    text = "\n".join(f"line {i} <!-- note -->" for i in range(201))
    findings = vdr.scan_file_budget("CLAUDE.md", text, 200)
    assert len(findings) == 1
    assert findings[0].category == "file-budget"
    assert "201 lines" in findings[0].detail


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


def test_grooming_cadence_past_next_quarterly_does_not_mask():
    # F2 (2026-07-09) frozen contract: once the "Next quarterly:" TARGET date is itself in
    # the past, it must NOT be counted as a completed groom — the cadence clock stays pinned
    # to the real past groom date so an overdue escalation still fires.
    log = "**Grooming log:** Recent: 2026-07-08 (pass). Next quarterly: 2026-10-08."
    findings = vdr.scan_grooming_cadence(_backlog([], groom_line=log), today=date(2026, 10, 20))
    assert len(findings) == 1                       # escalation NOT masked
    assert "2026-07-08" in findings[0].detail       # clock pinned to the real groom...
    assert "2026-10-08" not in findings[0].detail   # ...not the past target date


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
    # an accreted backlog line + an over-threshold section-history block -> 2 distinct loci.
    (tmp_path / "BACKLOG.md").write_text(
        _backlog([_ACCRETED_ROW],
                 groom_line="**Grooming log:** Recent: 2026-08-15."), encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text(_history_block(20), encoding="utf-8")
    results = vdr.scan(tmp_path, today=_TODAY)
    loci = {r.locus for r in results}
    assert "BACKLOG#777" in loci
    assert "CLAUDE.md#section-history" in loci


def test_scan_threads_today_into_the_backlog_arms(tmp_path):
    # [#532] wiring proof: scan() must pass its `today` down to the BACKLOG scanner, or the
    # future-date filter silently uses the wall clock. Same row, two `today` values: with
    # today BEFORE the newest date that date is a future peg (2 dates, no ARM 1); after it,
    # the row is accreted (3 dates, span 166d).
    (tmp_path / "BACKLOG.md").write_text(_backlog([_ACCRETED_ROW]), encoding="utf-8")
    before = vdr.scan(tmp_path, today=date(2026, 6, 19))
    after = vdr.scan(tmp_path, today=_TODAY)
    assert [r for r in before if r.category == "backlog-accretion"] == []
    assert [r.locus for r in after if r.category == "backlog-accretion"] == ["BACKLOG#777"]


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
    results = vdr.scan_backlog_accretion(_backlog([_ACCRETED_ROW]), _TODAY)
    out = vdr.format_findings(results)
    assert "BACKLOG#777" in out
    assert "|" not in out


# --- [#532] the citation regex vs THE LIVE CORPUS IT WAS MEASURED ON ---------
# NB3-C §2.4 measured the citation-stripping regex on the live BACKLOG and reported a
# 0-false-strip rate. That claim is re-measured here against the tree rather than trusted,
# and it is denominator-free: it asserts a PROPERTY of every token stripped, so it cannot
# rot as the corpus grows. `live_repo` because it reads the hub's real BACKLOG.md.

@pytest.mark.live_repo
def test_citation_regex_strips_only_real_dated_artifact_identifiers():
    root = Path(aud._REPO_ROOT)
    backlog = (root / "BACKLOG.md").read_text(encoding="utf-8")
    stripped = set()
    for line in backlog.splitlines():
        if vdr._TASK_RE.match(line):
            stripped.update(vdr._ARTIFACT_DATE_RE.findall(line))
    assert stripped, "no citations found — the corpus or the regex has changed shape"

    # Every stripped token must be a GENUINE dated-artifact identifier. Two admissible
    # shapes, and the second is checked against the filesystem, not asserted:
    false_strips = []
    for tok in sorted(stripped):
        if "/" in tok:
            continue                                   # a path-qualified citation
        if (root / "docs" / "handoffs" / tok).is_dir():
            continue                                   # a REAL handoff bundle directory
        false_strips.append(tok)
    assert false_strips == [], f"citation regex false-stripped: {false_strips}"


@pytest.mark.live_repo
def test_live_corpus_has_no_accretion_arm_findings_only_length_findings():
    # The amendment's measured live effect ([#532]): every live locus is a LENGTH finding.
    # This is the assertion that would break first if ARM 1 ever started mislabelling
    # again — and it is safe to pin because ARM 1's firing behaviour is proved separately
    # by the synthetic fixture above, not by this zero.
    results = vdr.scan(Path(aud._REPO_ROOT))
    assert [r for r in results if r.category == "backlog-accretion"] == []


# --- deployed audit check: check_doc_rot ------------------------------------

def test_check_skips_non_hub_repo(tmp_path):
    findings = aud.check_doc_rot(tmp_path / "some-child")
    assert len(findings) == 1
    assert findings[0].check_name == "doc_rot"
    assert findings[0].status == "n/a"  # [#465] leg 1
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
