"""Tests for the ADR status-grammar validator (`[#242]`, lane L3).

Three layers:

  1. **THE PARSER'S TEETH** — synthetic fixtures, one per divergent grammar measured in the
     live corpus at merge base `aeec0fd1` (docs/audits/2026-08-23-technical-lane-status-grammar.md
     Step 1). Each asserts the divergent form is **REJECTED**, not merely that the run
     completes. This is the layer that stops the validator degenerating into "accepts every
     grammar it finds", which is the failure mode the lane contract names.

  2. **THE KNOWN FALSE-POSITIVE / FALSE-NEGATIVE CASES** — the four parser hazards the Step-1
     measurement actually hit. Each is a regression test for a bug that was live in this
     lane's own first measurement pass, not a hypothetical.

  3. **THE SHIPPED CORPUS** — the validator's verdict on the real `docs/decisions/` is pinned
     to the measured baseline, so a change to the corpus (or to the validator) that moves the
     number is a test failure rather than a silent drift.

Fixtures are synthesized rather than read from the live corpus wherever teeth are being
proved, so the suite does not couple to the corpus's lifecycle. Layer 3 is the deliberate
exception and is asserted as an inequality plus a named-member check, not an exact roster.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

import validate_adr_status as vas  # noqa: E402


# --- helpers ------------------------------------------------------------------

def _write(tmp_path: Path, name: str, body: str) -> Path:
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(body, encoding="utf-8")
    return p


def _fields(body: str) -> list[vas.StatusField]:
    return vas.parse_status_fields(body, Path("ADR-99-x.md"))


# --- layer 1: one rejection case per divergent grammar -------------------------

# Each entry is (grammar_id, the header line as it appears in the live corpus).
DIVERGENT = [
    ("G2", "**Status:** Accepted"),
    ("G3", "Status: Accepted"),
    ("G4", "status: Accepted 2026-05-28"),
    ("G5", "> **Status: DEPRECATED 2026-05-23.**"),
]


@pytest.mark.parametrize("grammar,line", DIVERGENT)
def test_divergent_grammar_is_detected_as_that_grammar(grammar, line):
    body = f"# ADR-99 — x\n\n{line}\n- **Date:** 2026-01-01\n"
    fields = _fields(body)
    assert len(fields) == 1, f"{grammar}: expected exactly one status field"
    assert fields[0].grammar == grammar


@pytest.mark.parametrize("grammar,line", DIVERGENT)
def test_divergent_grammar_is_REJECTED_not_merely_parsed(grammar, line):
    """The whole point of the gate: a non-canonical grammar must produce a defect."""
    body = f"# ADR-99 — x\n\n{line}\n- **Date:** 2026-01-01\n"
    defects = vas.field_defects(_fields(body))
    rules = {d.rule for d in defects}
    assert vas.R_GRAMMAR in rules, (
        f"{grammar} was accepted by the validator — the gate rejects nothing")


def test_canonical_grammar_is_accepted():
    body = "# ADR-99 — x\n\n- **Status:** Accepted\n- **Date:** 2026-01-01\n"
    fields = _fields(body)
    assert len(fields) == 1
    assert fields[0].grammar == vas.CANONICAL_GRAMMAR
    assert [d for d in vas.field_defects(fields) if d.rule == vas.R_GRAMMAR] == []


# --- layer 1b: the enum leg ----------------------------------------------------

@pytest.mark.parametrize("value", [
    "Accepted", "Proposed", "Superseded", "Deprecated",
    "Partially superseded", "Explored, not adopted", "PARKED",
])
def test_every_declared_enum_value_is_accepted(value):
    body = f"# ADR-99 — x\n\n- **Status:** {value}\n"
    assert [d for d in vas.field_defects(_fields(body)) if d.rule == vas.R_ENUM] == []


@pytest.mark.parametrize("value", ["Ratified", "Done", "Active", "accepted", ""])
def test_off_enum_value_is_rejected(value):
    body = f"# ADR-99 — x\n\n- **Status:** {value}\n"
    rules = {d.rule for d in vas.field_defects(_fields(body))}
    assert vas.R_ENUM in rules, f"off-enum value {value!r} was accepted"


def test_enum_value_may_carry_a_qualifier():
    body = ("# ADR-99 — x\n\n- **Status:** Accepted (ratified by merge 2026-06-29)\n")
    assert [d for d in vas.field_defects(_fields(body)) if d.rule == vas.R_ENUM] == []


def test_longest_enum_match_wins():
    """`Partially superseded` must not be read as `Superseded` with junk in front."""
    body = "# ADR-99 — x\n\n- **Status:** Partially superseded — retained as convention\n"
    fields = _fields(body)
    assert fields[0].value == "Partially superseded"


# --- layer 2: the measured parser hazards (regression tests) -------------------

def test_status_update_marker_is_NOT_a_status_field():
    """ADR-82:11 hazard. `**Status update (...)` is an amendment marker, not a field.

    An optional-colon regex swallows it as a bogus SECOND status field. This bug was live in
    this lane's first measurement pass; the fix is that `Status` must be immediately
    followed by ':'.
    """
    body = (
        "# ADR-82 — x\n\n"
        "- **Status:** Accepted\n"
        "- **Date:** 2026-06-11\n\n"
        "> **Status update (in-place marker — the frozen header above is unchanged per the\n"
        "> immutability convention): canonical since 2026-06-11.**\n"
    )
    fields = _fields(body)
    assert len(fields) == 1, (
        f"amendment marker parsed as a status field: {[f.raw for f in fields]}")
    assert fields[0].lineno == 3


def test_wrapped_value_is_flagged_not_silently_truncated():
    """ADR-67:5 hazard — the value continues onto the next physical line."""
    body = (
        "# ADR-67 — x\n\n"
        "**Status:** Accepted — 2026-06-01, **Path A** (operator-chosen; no Council convene — a process\n"
        "formalization of an already-running loop, not an architectural decision).\n"
    )
    fields = _fields(body)
    assert len(fields) == 1
    assert fields[0].wrapped is True
    assert vas.R_WRAP in {d.rule for d in vas.field_defects(fields)}


def test_unwrapped_value_is_not_flagged_as_wrapped():
    body = (
        "# ADR-99 — x\n\n"
        "- **Status:** Accepted (ratified by merge 2026-06-29)\n"
        "- **Date:** 2026-06-29\n"
    )
    assert _fields(body)[0].wrapped is False


def test_markup_in_value_is_stripped_before_enum_match():
    """ADR-114 `**PARKED**` and ADR-52 `~~Accepted~~` must match the enum."""
    for raw in ("**PARKED** — ruled by the operator", "~~Accepted~~ Superseded by ADR-53"):
        body = f"# ADR-99 — x\n\n- **Status:** {raw}\n"
        assert [d for d in vas.field_defects(_fields(body)) if d.rule == vas.R_ENUM] == [], raw


def test_file_with_no_status_field_is_a_defect():
    body = "# ADR-99 — x\n\n- **Date:** 2026-01-01\n"
    rules = {d.rule for d in vas.field_defects(_fields(body))}
    assert vas.R_SINGLE in rules


def test_file_with_two_status_fields_is_a_defect():
    """ADR-40 (archive) carries a blockquote banner AND a plain field, at two casings."""
    body = (
        "# ADR-40 — x\n\n"
        "> **Status: DEPRECATED 2026-05-23.**\n\n"
        "Status: Deprecated (was: Accepted)\n"
    )
    fields = _fields(body)
    assert len(fields) == 2
    assert vas.R_SINGLE in {d.rule for d in vas.field_defects(fields)}


# --- layer 2b: header <-> README index coherence (`[#242]` Done-when leg) -------

_INDEX = (
    "## ADR Index\n\n"
    "| ADR | Date | Title |\n"
    "|-----|------|-------|\n"
    "| ADR-11 | 2026-01-01 | A plain accepted one |\n"
    "| ADR-12 | 2026-01-02 | ~~Old thing~~ Superseded by ADR-11 |\n"
    "| ADR-13 | 2026-01-03 | **PARKED (operator ruling)** — a parked one |\n"
    "| ADR-14 | 2026-01-04 | A thing — Deprecated 2026-05-23; relocated |\n"
)


def test_index_effective_status_reads_the_four_marker_forms():
    eff = vas.index_effective_status(_INDEX)
    assert eff["ADR-11"] == "Accepted"      # no marker => Accepted by convention
    assert eff["ADR-12"] == "Superseded"
    assert eff["ADR-13"] == "PARKED"
    assert eff["ADR-14"] == "Deprecated"


def test_header_vs_index_divergence_is_flagged():
    """The seeded case `[#242]`'s Done-when names explicitly."""
    eff = vas.index_effective_status(_INDEX)
    defects = vas.coherence_defects({"ADR-12": "Accepted"}, eff)
    assert [d.rule for d in defects] == [vas.R_COHERENCE]


def test_header_matching_index_is_not_flagged():
    eff = vas.index_effective_status(_INDEX)
    assert vas.coherence_defects({"ADR-12": "Superseded"}, eff) == []


def test_unindexed_adr_is_reported_never_silently_passed():
    """The two amendment ADRs (51, 70) carry no index row. Indeterminate != coherent."""
    eff = vas.index_effective_status(_INDEX)
    defects = vas.coherence_defects({"ADR-99": "Accepted"}, eff)
    assert [d.rule for d in defects] == [vas.R_UNINDEXED]


def test_duplicate_adr_number_is_reported_not_collapsed():
    """A first-wins dict would hide the second file AND silently disarm R_UNINDEXED for it."""
    fields = [
        vas.StatusField(Path("ADR-51-architecture-doc-convention.md"), "G1", 3,
                        "Accepted", "Accepted", False),
        vas.StatusField(Path("ADR-51-amendment-2026-07-05-llm-first.md"), "G1", 3,
                        "Accepted", "Accepted", False),
        vas.StatusField(Path("ADR-99-lonely.md"), "G1", 3, "Accepted", "Accepted", False),
    ]
    defects = vas.duplicate_id_defects(fields)
    assert [d.rule for d in defects] == [vas.R_DUPLICATE]
    assert defects[0].subject == "ADR-51"
    assert "ADR-51-amendment-2026-07-05-llm-first.md" in defects[0].detail


def test_shipped_corpus_duplicate_ids_are_the_two_measured():
    fields, _, _ = vas.scan_zone(vas.LIVE_DIR)
    assert {d.subject for d in vas.duplicate_id_defects(fields)} == {"ADR-51", "ADR-70"}


def test_incidental_superseded_mention_is_not_a_marker():
    """A title that merely discusses supersession must not be read as a status marker."""
    idx = (
        "| ADR | Date | Title |\n"
        "|-----|------|-------|\n"
        "| ADR-98 | 2026-07-07 | Intake pipeline — superseded-in-part by intake brief #1 |\n"
    )
    assert vas.index_effective_status(idx)["ADR-98"] == "Accepted"


# --- layer 3: the shipped corpus, pinned to the measured baseline --------------

def test_shipped_corpus_parses_one_status_field_per_live_adr():
    fields, missing, extra = vas.scan_zone(vas.LIVE_DIR)
    assert missing == [], f"live ADRs with no status field: {missing}"
    assert extra == [], f"live ADRs with >1 status field: {extra}"
    assert len(fields) == 87, "live ADR count moved — re-measure the Step-1 baseline"


def test_shipped_corpus_grammar_distribution_matches_the_measured_baseline():
    fields, _, _ = vas.scan_zone(vas.LIVE_DIR)
    counts: dict[str, int] = {}
    for f in fields:
        counts[f.grammar] = counts.get(f.grammar, 0) + 1
    assert counts == {"G1": 40, "G2": 34, "G3": 12, "G4": 1}


def test_shipped_corpus_has_zero_enum_violations():
    """The leg armed at FAIL. If this ever goes RED the enum genuinely drifted."""
    fields, _, _ = vas.scan_zone(vas.LIVE_DIR)
    assert [d for d in vas.field_defects(fields) if d.rule == vas.R_ENUM] == []


def test_shipped_corpus_coherence_divergences_are_the_three_measured():
    fields, _, _ = vas.scan_zone(vas.LIVE_DIR)
    headers = {vas.adr_number(f.path): f.value for f in fields}
    eff = vas.index_effective_status(
        (vas.LIVE_DIR / "README.md").read_text(encoding="utf-8"))
    diverged = {d.subject for d in vas.coherence_defects(headers, eff)
                if d.rule == vas.R_COHERENCE}
    assert diverged == {"ADR-45", "ADR-46", "ADR-47"}


# --- the audit-check adapter ---------------------------------------------------

from audit_checks.check_adr_status_grammar import (  # noqa: E402
    check_adr_status_grammar,
)


def test_check_returns_warn_with_the_measured_baseline_on_the_hub():
    """The arming level the lane contract requires: WARN against a recorded baseline,
    never a day-one RED block."""
    findings = check_adr_status_grammar(vas._REPO_ROOT)
    assert len(findings) == 1
    f = findings[0]
    assert f.check_name == "adr_status_grammar"
    assert f.status == "warn"
    assert "grammar=47" in f.evidence
    assert "coherence=3" in f.evidence


def test_check_is_child_repo_safe(tmp_path):
    """A repo with no docs/decisions/ is n/a subject-absent, never a FAIL."""
    findings = check_adr_status_grammar(tmp_path)
    assert findings[0].status == "n/a"
    assert "SUBJECT-ABSENT" in findings[0].evidence


def test_check_FAILS_on_an_off_enum_value(tmp_path):
    """The FAIL-armed leg has teeth: seed an off-enum status, get a blocking finding."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-11-x.md").write_text(
        "# ADR-11 — x\n\n- **Status:** Ratified\n", encoding="utf-8")
    findings = check_adr_status_grammar(tmp_path)
    assert findings[0].status == "fail"
    assert "enum" in findings[0].evidence


def test_check_PASSES_on_a_fully_conforming_corpus(tmp_path):
    """Proof the check is not warn-by-construction — a clean corpus really does pass."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-11-x.md").write_text(
        "# ADR-11 — x\n\n- **Status:** Accepted\n", encoding="utf-8")
    (d / "README.md").write_text(
        "| ADR | Date | Title |\n|--|--|--|\n| ADR-11 | 2026-01-01 | x |\n",
        encoding="utf-8")
    findings = check_adr_status_grammar(tmp_path)
    assert findings[0].status == "pass", findings[0].evidence


def test_check_carries_the_rule_annotation_for_the_doc_code_edge():
    """`_markers_for_check` walks back from the def through the contiguous comment block;
    losing `# rule: governance-adr-status` silently drops the doc->code edge."""
    src = (vas._REPO_ROOT / "scripts" / "audit_checks"
           / "check_adr_status_grammar.py").read_text(encoding="utf-8")
    lines = src.splitlines()
    def_idx = next(i for i, ln in enumerate(lines)
                   if ln.startswith("def check_adr_status_grammar("))
    assert lines[def_idx - 1].strip() == "# rule: governance-adr-status"


# --- the CLI exit contract -----------------------------------------------------

def test_cli_exit_0_on_a_clean_synthetic_corpus(tmp_path):
    _write(tmp_path, "ADR-11-x.md", "# ADR-11 — x\n\n- **Status:** Accepted\n")
    (tmp_path / "docs" / "decisions" / "README.md").write_text(
        "| ADR | Date | Title |\n|--|--|--|\n| ADR-11 | 2026-01-01 | x |\n",
        encoding="utf-8")
    res = CliRunner().invoke(vas.main, ["--root", str(tmp_path)])
    assert res.exit_code == 0, res.output


def test_cli_exit_1_on_a_divergent_corpus(tmp_path):
    _write(tmp_path, "ADR-11-x.md", "# ADR-11 — x\n\nStatus: Accepted\n")
    (tmp_path / "docs" / "decisions" / "README.md").write_text(
        "| ADR | Date | Title |\n|--|--|--|\n| ADR-11 | 2026-01-01 | x |\n",
        encoding="utf-8")
    res = CliRunner().invoke(vas.main, ["--root", str(tmp_path)])
    assert res.exit_code == 1, res.output
    assert "G3" in res.output


def test_cli_exit_2_when_the_corpus_dir_is_absent(tmp_path):
    """An unreadable subject must never render as a green pass."""
    res = CliRunner().invoke(vas.main, ["--root", str(tmp_path / "nope")])
    assert res.exit_code == 2, res.output
