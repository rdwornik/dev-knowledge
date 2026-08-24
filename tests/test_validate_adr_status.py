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


# --- layer 2c: terra round-1 findings (regression tests, one per failing input) --
#
# Every case below is a concrete input terra returned as a HIGH against the round-1 code.
# They are pinned here so a future edit cannot quietly reintroduce any of them.

def test_strikethrough_is_removed_not_unwrapped():
    """terra HIGH-2 / self-found. `~~X~~ Y` means "not X, now Y".

    Stripping the tildes and keeping the word turns ADR-52's real status into `Accepted` —
    inverting the ONE genuinely superseded ADR in the corpus and hiding it from the archival
    bar that exists to find it.
    """
    assert vas.normalize_value("~~Accepted~~ Superseded by ADR-53 (2026-05-19)") == "Superseded"


@pytest.mark.parametrize("value", ["A_ccepted", "Acceptedness", "Accepted-ish", "AcceptedX"])
def test_enum_match_requires_a_token_boundary(value):
    """terra HIGH-2: an unrestricted startswith (plus `_` stripping) let any word with an
    enum prefix pass the FAIL-armed enum rule."""
    assert vas.normalize_value(value) == ""


@pytest.mark.parametrize("value,expected", [
    ("Accepted", "Accepted"),
    ("Accepted - 2026-06-06", "Accepted"),
    ("Accepted — 2026-06-06", "Accepted"),
    ("Accepted (ratified by merge)", "Accepted"),
    ("Accepted, via Council", "Accepted"),
    ("Accepted 2026-05-28", "Accepted"),
])
def test_legitimate_qualifier_separators_still_match(value, expected):
    """The boundary check must not break the qualifier forms the live corpus actually uses."""
    assert vas.normalize_value(value) == expected


def test_status_line_inside_a_code_fence_is_not_a_field():
    """terra HIGH-1 / self-found. A quoted example would fire BOTH FAIL-armed legs
    (`single-field` on the count, `enum` on the quoted value), REDDING the pre-commit gate
    on a legitimate file. A false positive on a FAIL-armed leg is the worst case here."""
    body = (
        "# ADR-99 — x\n\n"
        "- **Status:** Accepted\n\n"
        "The pre-enum spelling we no longer use:\n\n"
        "```md\n"
        "- **Status:** Ratified\n"
        "```\n"
    )
    fields = _fields(body)
    assert len(fields) == 1
    assert fields[0].value == "Accepted"
    assert vas.field_defects(fields) == []


def test_tilde_fence_is_also_honoured():
    body = "# ADR-99 — x\n\n- **Status:** Accepted\n\n~~~\nStatus: Ratified\n~~~\n"
    assert len(_fields(body)) == 1


def test_utf8_bom_does_not_hide_the_status_field():
    """terra HIGH-1: a BOM makes `^-\\s+\\*\\*Status:` fail, so the field goes INVISIBLE —
    a silent miss rather than a loud one."""
    fields = _fields("﻿- **Status:** Accepted\n")
    assert len(fields) == 1
    assert fields[0].grammar == "G1"


def test_wrap_detection_does_not_depend_on_terminal_punctuation():
    """terra HIGH-3: the old heuristic missed this because the value ends in `*`."""
    body = "# ADR-99 — x\n\n- **Status:** **Accepted**\ncontinued rationale here\n"
    assert _fields(body)[0].wrapped is True


@pytest.mark.parametrize("nxt", [
    "- **Date:** 2026-01-01",
    "**Date:** 2026-01-01",
    "**Amends (does not edit):** ADR-71 §x",   # live: ADR-72:6, key contains punctuation
    "Date: 2026-01-01",
    "## Context",
    "> a blockquote",
    "| a | table |",
    "```",
    "<!-- a comment -->",
    "1. an ordered item",
])
def test_a_new_block_after_the_value_is_not_a_continuation(nxt):
    body = f"# ADR-99 — x\n\n- **Status:** Accepted\n{nxt}\n"
    assert _fields(body)[0].wrapped is False, nxt


# --- layer 2d: terra round-2 findings (regression tests) ------------------------

@pytest.mark.parametrize("value", ["Acce*pted", "Acce`pted", "Accep**ted", "Ac`cepted"])
def test_inline_markup_cannot_launder_a_bad_value(value):
    """terra R2-HIGH-1: a blanket `[*`]+` strip let inline markup inside a word normalize to
    a valid token and bypass the FAIL-armed enum rule."""
    assert vas.normalize_value(value) == ""


@pytest.mark.parametrize("value,expected", [
    ("**Accepted**", "Accepted"),
    ("*Accepted*", "Accepted"),
    ("`Accepted`", "Accepted"),
    ("**PARKED** — ruled by the operator", "PARKED"),
    ("Accepted", "Accepted"),
])
def test_balanced_emphasis_wrappers_still_match(value, expected):
    assert vas.normalize_value(value) == expected


def test_fence_info_string_with_spaces_is_a_valid_opener():
    """terra R2-HIGH-2: ```` ```md example ```` was not recognised, so the block's contents
    were parsed as header content."""
    body = ("# ADR-99 — x\n\n- **Status:** Accepted\n\n"
            "```md example title\n- **Status:** Ratified\n```\n")
    assert len(_fields(body)) == 1


def test_a_four_char_fence_is_not_closed_by_three():
    """terra R2-HIGH-2: closing on char-class alone reopened the document early."""
    body = ("# ADR-99 — x\n\n- **Status:** Accepted\n\n"
            "````\n```\n- **Status:** Ratified\n````\n")
    fields = _fields(body)
    assert len(fields) == 1, [f.raw for f in fields]


def test_emphasis_line_is_a_continuation_not_a_bullet():
    """terra R2-MEDIUM-1: `*text*` has no space after `*`, so it is emphasis, not a list
    item — a genuine wrapped value was going undetected."""
    body = "# ADR-99 — x\n\n- **Status:** Accepted\n*continued rationale*\n"
    assert _fields(body)[0].wrapped is True


def test_duplicate_numbered_adrs_contribute_no_coherence_verdict():
    """terra R2-MEDIUM-2: `setdefault` picked a winner by filename order, so the verdict
    depended on sort order and the other file's disagreement was hidden."""
    fields = [
        vas.StatusField(Path("ADR-11-a.md"), "G1", 3, "Proposed", "Proposed", False),
        vas.StatusField(Path("ADR-11-b.md"), "G1", 3, "Accepted", "Accepted", False),
        vas.StatusField(Path("ADR-12-solo.md"), "G1", 3, "Accepted", "Accepted", False),
    ]
    mapped = vas.header_status_map(fields)
    assert "ADR-11" not in mapped        # ambiguous -> no verdict
    assert mapped["ADR-12"] == "Accepted"
    # ...and the collision is still REPORTED, not just dropped.
    assert [d.rule for d in vas.duplicate_id_defects(fields)] == [vas.R_DUPLICATE]


def test_cli_does_not_exit_green_when_the_index_is_absent(tmp_path):
    """terra R2-HIGH-3: the CLI exited 0 with the coherence leg skipped, disagreeing with
    the adapter, which WARNs for the same condition."""
    _write(tmp_path, "ADR-11-x.md", "# ADR-11 — x\n\n- **Status:** Accepted\n")
    # no README.md written
    res = CliRunner().invoke(vas.main, ["--root", str(tmp_path)])
    assert res.exit_code == 1, res.output


# --- layer 2e: terra round-3 findings (regression tests) ------------------------

@pytest.mark.parametrize("value", [
    "**Accepted",       # opened, never closed
    "Accepted**",       # closed, never opened
    "*Accepted`",       # mixed markers
    "Accepted**ness",   # emphasis run immediately after an unwrapped token
    "`Accepted*",
])
def test_emphasis_wrappers_must_be_balanced_and_same_kind(value):
    """terra R3-HIGH-1: independent optional open/close groups accepted malformed markup,
    so a value that is not cleanly an enum token still passed the FAIL-armed rule."""
    assert vas.normalize_value(value) == ""


def test_even_backslash_run_is_not_an_escaped_pipe():
    """terra R3-HIGH-2: `\\\\|` is an escaped BACKSLASH followed by a real delimiter, so this
    row has four cells and must be refused — not folded into three and mined for a status."""
    idx = ("| ADR | Date | Title |\n|--|--|--|\n"
           "| ADR-9 | 2026-01-01 | title \\\\| — Deprecated |\n")
    assert "ADR-9" not in vas.index_effective_status(idx)


def test_odd_backslash_run_is_a_genuinely_escaped_pipe():
    idx = ("| ADR | Date | Title |\n|--|--|--|\n"
           "| ADR-9 | 2026-01-01 | title \\| more — Deprecated 2026-01-01 |\n")
    assert vas.index_effective_status(idx)["ADR-9"] == "Deprecated"


def test_one_file_with_two_status_fields_contributes_no_coherence_verdict():
    """terra R3-MEDIUM-1: excluding on FILENAME count alone still let a single file with two
    fields pick its first field arbitrarily. Live on `--include-archive` via ADR-40."""
    fields = [
        vas.StatusField(Path("ADR-9-x.md"), "G1", 3, "Accepted", "Accepted", False),
        vas.StatusField(Path("ADR-9-x.md"), "G3", 9, "Proposed", "Proposed", False),
    ]
    assert "ADR-9" not in vas.header_status_map(fields)
    # ...and the structural defect is still raised.
    assert vas.R_SINGLE in {d.rule for d in vas.field_defects(fields)}


# --- layer 2f: terra round-4 findings (regression tests) ------------------------

def test_row_ending_in_an_ESCAPED_pipe_is_refused():
    """terra R4-HIGH-1: `endswith("|")` is satisfied by a trailing ESCAPED pipe, so the
    `[1:-1]` slice dropped a real content cell and admitted a four-cell row as three."""
    idx = ("| ADR | Date | Title |\n|--|--|--|\n"
           "| ADR-9 | 2026-01-01 | — Deprecated | \\|\n")
    assert "ADR-9" not in vas.index_effective_status(idx)


@pytest.mark.parametrize("value,expected", [
    ("****Accepted****", "Accepted"),     # nested strong — valid markdown
    ("***Accepted***", "Accepted"),
    ("``Accepted``", "Accepted"),
])
def test_nested_emphasis_is_not_a_false_enum_failure(value, expected):
    """terra R4-HIGH-2: `\\*{1,3}` rejected valid nested emphasis, producing a FALSE `enum`
    FAIL — the worst failure available to a FAIL-armed leg."""
    assert vas.normalize_value(value) == expected


@pytest.mark.parametrize("value", ["****Accepted**", "**Accepted****"])
def test_mismatched_run_lengths_are_still_rejected(value):
    """Widening to `\\*+` must not cost strictness: the backreference still binds."""
    assert vas.normalize_value(value) == ""


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


def test_a_file_with_two_status_fields_does_not_collide_with_itself():
    """Self-found on the --include-archive path: ADR-40 carries two status fields, and a
    field-keyed count reported it as "2 files claim this number: ADR-40..., ADR-40..." —
    a false collision invisible on the live corpus, where no file has two fields."""
    fields = [
        vas.StatusField(Path("ADR-40-scale-tier.md"), "G5", 5, "Deprecated", "Deprecated", False),
        vas.StatusField(Path("ADR-40-scale-tier.md"), "G3", 10, "Deprecated", "Deprecated", False),
    ]
    assert vas.duplicate_id_defects(fields) == []


def test_shipped_corpus_duplicate_ids_are_the_two_measured():
    fields, _, _ = vas.scan_zone(vas.LIVE_DIR)
    assert {d.subject for d in vas.duplicate_id_defects(fields)} == {"ADR-51", "ADR-70"}


@pytest.mark.parametrize("title,expected", [
    # terra HIGH-4, one case per failing input it supplied.
    ("Pre-Deprecated API migration", "Accepted"),          # hyphen must not be the separator
    ("**Explored option** for a thing", "Accepted"),        # prefix-of-a-word is not the token
    ("~~Old~~ Partially superseded by ADR-1", "Partially superseded"),  # was truncated to
                                                                       # "Partially" -> default
    # ...and the real markers must still resolve.
    ("~~Old title~~ Superseded by ADR-53", "Superseded"),
    ("A thing — Deprecated 2026-05-23; relocated", "Deprecated"),
    ("**PARKED (operator ruling 2026-08-22)** — revisit", "PARKED"),
    ("A perfectly ordinary title", "Accepted"),
])
def test_index_markers_match_complete_tokens_only(title, expected):
    idx = ("| ADR | Date | Title |\n|--|--|--|\n"
           f"| ADR-9 | 2026-01-01 | {title} |\n")
    assert vas.index_effective_status(idx)["ADR-9"] == expected


def test_index_row_with_a_fourth_cell_is_refused():
    """terra HIGH-4: a 4-cell row folded its extra cell into Title and took a status from it."""
    idx = ("| ADR | Date | Title |\n|--|--|--|\n"
           "| ADR-9 | 2026-01-01 | Title | — Deprecated |\n")
    assert "ADR-9" not in vas.index_effective_status(idx)


def test_index_cell_split_honours_escaped_pipes():
    idx = ("| ADR | Date | Title |\n|--|--|--|\n"
           "| ADR-9 | 2026-01-01 | A \\| B — Deprecated 2026-01-01 |\n")
    assert vas.index_effective_status(idx)["ADR-9"] == "Deprecated"


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


def test_check_WARNS_when_the_index_is_missing_instead_of_passing(tmp_path):
    """terra HIGH-5: the index is HALF this check's subject. Returning `pass` while the
    coherence leg silently did not run is the vacuous pass the gate exists to prevent."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-11-x.md").write_text(
        "# ADR-11 — x\n\n- **Status:** Accepted\n", encoding="utf-8")
    # no README.md written
    findings = check_adr_status_grammar(tmp_path)
    assert findings[0].status == "warn"
    assert "DID NOT RUN" in findings[0].evidence


def test_a_missing_index_does_not_MASK_a_real_enum_failure(tmp_path):
    """Self-found while fixing terra HIGH-5: the first fix early-returned the index WARN,
    which suppressed a genuine FAIL. "Do not silently pass" must not become "swallow real
    failures" — the FAIL-armed legs are evaluated first, unconditionally."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-11-x.md").write_text(
        "# ADR-11 — x\n\n- **Status:** Ratified\n", encoding="utf-8")
    # no README.md
    findings = check_adr_status_grammar(tmp_path)
    assert findings[0].status == "fail"
    assert "enum" in findings[0].evidence


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
