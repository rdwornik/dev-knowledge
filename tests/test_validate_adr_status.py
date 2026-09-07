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


# --- layer 2g: terra round-5 findings (regression tests) ------------------------

def test_tilde_fence_info_string_may_contain_backticks():
    """terra R5-HIGH-1: the info-string constraint is fence-character-specific. A single
    `[^`]*` for both wrongly rejected a tilde opener and let the block's contents parse."""
    body = ("# ADR-99 — x\n\n- **Status:** Accepted\n\n"
            "~~~python `example`\n- **Status:** Ratified\n~~~\n")
    fields = _fields(body)
    assert len(fields) == 1, [f.raw for f in fields]


def test_backtick_fence_info_string_may_NOT_contain_a_backtick():
    """The other half of the same rule — widening must not lose CommonMark's constraint."""
    body = "# ADR-99 — x\n\n```md `oops`\n- **Status:** Ratified\n```\n"
    # The opener is invalid, so the line below it IS header content and parses.
    assert len(_fields(body)) == 1


def test_fence_inside_a_blockquote_is_tracked():
    """terra R5-HIGH-1 (second case): a quoted example containing `> **Status: Ratified**`
    otherwise parses as a real G5 field."""
    body = ("# ADR-99 — x\n\n- **Status:** Accepted\n\n"
            "> ~~~\n> **Status: Ratified**\n> ~~~\n")
    fields = _fields(body)
    assert len(fields) == 1, [f.raw for f in fields]


@pytest.mark.parametrize("open_line,close_line", [
    ("> ~~~", "~~~"),      # quoted open, plain close
    ("~~~", "> ~~~"),      # plain open, quoted close
])
def test_fence_does_not_close_across_a_blockquote_boundary(open_line, close_line):
    """terra R6-HIGH-1: a fence opened inside a blockquote is NOT closed by an unquoted
    marker — that line ends the blockquote instead. Either transition leaves the fence OPEN,
    so the trailing status line is code content and must not parse."""
    body = (f"# ADR-99 — x\n\n{open_line}\nquoted example\n{close_line}\n"
            "- **Status:** Accepted\n")
    assert _fields(body) == [], [f.raw for f in _fields(body)]


def test_fence_opened_and_closed_in_the_same_container_does_close():
    """The other side of R6-HIGH-1: matched containers must still close normally."""
    body = ("# ADR-99 — x\n\n> ~~~\n> quoted example\n> ~~~\n\n- **Status:** Accepted\n")
    fields = _fields(body)
    assert len(fields) == 1 and fields[0].value == "Accepted"


@pytest.mark.parametrize("line", [
    "> **Status: Accepted**",
    "> > **Status: Accepted**",
    ">> **Status: Accepted**",
])
def test_nested_blockquote_g5_field_is_still_a_field(line):
    """terra R7-HIGH-1: G5 accepted only ONE `>`, so a nested field was invisible — and a
    file whose only field is nested then took a FALSE `single-field` FAIL."""
    fields = _fields(f"# ADR-99 — x\n\n{line}\n")
    assert len(fields) == 1, line
    assert fields[0].grammar == "G5"
    assert fields[0].value == "Accepted"


def test_live_and_archive_files_with_the_SAME_basename_are_distinct_claimants():
    """terra R7-HIGH-2: identity was `Path.name`, so `ADR-9-x.md` and `archive/ADR-9-x.md`
    collapsed into one claimant and the collision went unreported."""
    fields = [
        vas.StatusField(Path("docs/decisions/ADR-9-x.md"), "G1", 3,
                        "Accepted", "Accepted", False),
        vas.StatusField(Path("docs/decisions/archive/ADR-9-x.md"), "G1", 3,
                        "Accepted", "Accepted", False),
    ]
    defects = vas.duplicate_id_defects(fields)
    assert [d.rule for d in defects] == [vas.R_DUPLICATE]
    assert "archive/ADR-9-x.md" in defects[0].detail
    assert "ADR-9" not in vas.header_status_map(fields)


@pytest.mark.parametrize("line", [
    "  > **Status: Accepted**",
    "   > > **Status: Accepted**",
])
def test_indented_blockquote_g5_field_is_still_a_field(line):
    """terra R8-HIGH-1: CommonMark permits up to 3 leading spaces before `>`; requiring
    column zero made the field invisible and produced a FALSE `single-field` FAIL."""
    fields = _fields(f"# ADR-99 — x\n\n{line}\n")
    assert len(fields) == 1, line
    assert fields[0].value == "Accepted"


def test_status_inside_a_multiline_html_comment_is_not_a_field():
    """terra R8-HIGH-2: these ADRs really do carry `<!-- ... -->` blocks in their headers
    (`<!-- scope: meta -->`, ADR-82's `<!-- Decommission: ... -->`), so a commented-out
    historical status is a realistic shape. Untracked it fired BOTH FAIL-armed legs."""
    body = (
        "# ADR-99 — x\n\n"
        "- **Status:** Accepted\n"
        "<!-- historic example:\n"
        "> **Status: Ratified**\n"
        "-->\n"
    )
    fields = _fields(body)
    assert len(fields) == 1, [f.raw for f in fields]
    assert vas.field_defects(fields) == []


def test_single_line_html_comment_does_not_swallow_the_rest_of_the_header():
    """The common case — `<!-- scope: meta -->` — opens and closes on one line and must not
    put the parser into comment state."""
    body = "# ADR-99 — x\n\n<!-- scope: meta -->\n\n- **Status:** Accepted\n"
    fields = _fields(body)
    assert len(fields) == 1 and fields[0].value == "Accepted"


def test_index_row_inside_a_fenced_example_does_not_win():
    """terra R8-MEDIUM-1: with first-row-wins, a fenced documentation example beat the real
    index row and manufactured a coherence divergence."""
    idx = (
        "Example of the row format:\n\n"
        "```md\n"
        "| ADR-11 | 2026-01-01 | — Deprecated |\n"
        "```\n\n"
        "| ADR | Date | Title |\n|--|--|--|\n"
        "| ADR-11 | 2026-01-01 | The actual accepted title |\n"
    )
    assert vas.index_effective_status(idx)["ADR-11"] == "Accepted"


# --- layer 2h: terra round-9 findings — regressions from the round-8 comment fix ----

def test_html_comment_syntax_inside_a_fence_is_literal():
    """terra R9-HIGH-1: inside a fence `<!--` is code content. The round-8 line-level tracker
    entered comment state there and then swallowed the closing fence, so the real field that
    followed went missing. Fence state must be resolved BEFORE comment state."""
    body = (
        "# ADR-99 — x\n\n"
        "```\n"
        "<!--\n"
        "```\n"
        "- **Status:** Accepted\n"
    )
    fields = _fields(body)
    assert len(fields) == 1, [f.raw for f in fields]
    assert fields[0].value == "Accepted"


def test_trailing_inline_comment_does_not_discard_the_field():
    """terra R9-HIGH-2: a line-level tracker threw away the visible half of the line."""
    body = "# ADR-99 — x\n\n- **Status:** Accepted <!-- historical note\n-->\n"
    fields = _fields(body)
    assert len(fields) == 1, [f.raw for f in fields]
    assert fields[0].value == "Accepted"


@pytest.mark.parametrize("line,visible,state", [
    ("<!-- closed --> <!-- opens", " ", True),
    ("plain text", "plain text", False),
    ("a <!-- b --> c", "a  c", False),
    ("no opener --> here", "no opener --> here", False),
])
def test_comment_lexer_handles_sequential_and_partial_spans(line, visible, state):
    assert vas._strip_comments(line, False) == (visible, state)


def test_comment_lexer_resumes_mid_line_after_a_close():
    """A comment opened on a previous line ends mid-line; the remainder is visible."""
    assert vas._strip_comments("--> - **Status:** Accepted", True) == (
        " - **Status:** Accepted", False)


def test_quoted_indented_code_is_not_a_nested_g5_field():
    """terra R9-HIGH-3: `>     > **Status: X**` is an INDENTED CODE BLOCK inside a
    blockquote, not a field. `(?:>\\s*)+` parsed it as G5 and fired two FAIL-armed legs."""
    body = "# ADR-99 — x\n\n- **Status:** Accepted\n>     > **Status: Ratified**\n"
    fields = _fields(body)
    assert len(fields) == 1, [f.raw for f in fields]
    assert fields[0].value == "Accepted"


def test_comment_opener_in_a_fence_info_string_does_not_leak_past_the_fence():
    """terra R10: a `<!--` in a fence opener's INFO STRING is fenced content, not a comment.
    Left set, that comment state survived the whole block and then swallowed the real field
    after the closing fence."""
    body = (
        "# ADR-99 — x\n\n"
        "```html <!--\n"
        "some quoted markup\n"
        "```\n"
        "- **Status:** Accepted\n"
    )
    fields = _fields(body)
    assert len(fields) == 1, [f.raw for f in fields]
    assert fields[0].value == "Accepted"


def test_a_comment_opened_on_an_EARLIER_line_still_encloses_a_fence_marker():
    """The other side: a genuine multi-line comment really does swallow a fence marker."""
    body = (
        "# ADR-99 — x\n\n"
        "- **Status:** Accepted\n"
        "<!-- commented block:\n"
        "```\n"
        "> **Status: Ratified**\n"
        "```\n"
        "-->\n"
    )
    fields = _fields(body)
    assert len(fields) == 1, [f.raw for f in fields]
    assert fields[0].value == "Accepted"


def test_comment_closer_line_is_not_a_wrapped_value():
    """terra R12: the wrap lookahead read the RAW next line, so a standalone `-->` closer
    looked like lazy continuation text and produced a false `wrapped-value`."""
    body = (
        "# ADR-99 — x\n\n"
        "- **Status:** Accepted <!-- historical note\n"
        "-->\n"
        "- **Date:** 2026-01-01\n"
    )
    fields = _fields(body)
    assert len(fields) == 1
    assert fields[0].value == "Accepted"
    assert fields[0].wrapped is False
    assert [d for d in vas.field_defects(fields) if d.rule == vas.R_WRAP] == []


def test_index_fence_opener_comment_does_not_swallow_the_whole_index():
    """terra R11: the R10 fence-opener rule was fixed in the ADR parser and NOT mirrored in
    the index scanner, so a README documenting a fenced example with an inline annotation
    lost its ENTIRE index — every ADR then reads as `unindexed`."""
    idx = (
        "```html <!--\n"
        "example\n"
        "```\n"
        "| ADR | Date | Title |\n|--|--|--|\n"
        "| ADR-11 | 2026-01-01 | Decision |\n"
    )
    assert vas.index_effective_status(idx) == {"ADR-11": "Accepted"}


def test_index_row_inside_an_html_comment_does_not_win():
    """terra R9-MEDIUM-1: the index scan gained fence-skipping but not comment-skipping."""
    idx = (
        "<!-- historical example:\n"
        "| ADR-11 | 2026-01-01 | — Deprecated |\n"
        "-->\n"
        "| ADR | Date | Title |\n|--|--|--|\n"
        "| ADR-11 | 2026-01-01 | The actual accepted title |\n"
    )
    assert vas.index_effective_status(idx)["ADR-11"] == "Accepted"


def test_duplicate_id_fires_when_the_OTHER_file_has_no_status_field():
    """terra R5-HIGH-2: only `single-field` fired, `duplicate-id` did not, and the surviving
    file was then treated as unambiguous and given a coherence verdict."""
    fields = [vas.StatusField(Path("ADR-9-a.md"), "G1", 3, "Accepted", "Accepted", False)]
    missing = ["ADR-9-b.md"]
    assert [d.rule for d in vas.duplicate_id_defects(fields, missing)] == [vas.R_DUPLICATE]
    assert "ADR-9" not in vas.header_status_map(fields, missing)
    # ...and without the collision the verdict is still produced.
    assert vas.header_status_map(fields) == {"ADR-9": "Accepted"}


def test_thematic_break_is_not_a_lazy_continuation():
    """terra R5-MEDIUM-1: `---` has no space after `-`, so the bullet alternative missed it."""
    for nxt in ("---", "***", "- - -", "___"):
        body = f"# ADR-99 — x\n\n- **Status:** Accepted\n{nxt}\n"
        assert _fields(body)[0].wrapped is False, nxt


def test_date_cell_must_BE_a_date_not_merely_start_with_one():
    """terra R5-MEDIUM-2: a prefix match let an unrelated table manufacture a verdict."""
    idx = ("| ADR | Date | Title |\n|--|--|--|\n"
           "| ADR-9 | 2026-01-01 not-a-date | — Deprecated |\n")
    assert "ADR-9" not in vas.index_effective_status(idx)


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
    # RE-MEASURED 2026-09-01 at the batch-E close: 88 -> 89. The delta is ONE ADR and it is
    # named: ADR-116 (the fuzzy-band acceptance shape) landed 2026-08-30 on `704f5a07`. No
    # other member moved. Recorded here rather than in a commit message alone, because the
    # number is the baseline and a baseline with no cause is a number nobody can re-derive.
    #
    # RE-MEASURED 2026-09-07 at batch U NIGHT-2: 89 -> 90. The delta is again ONE ADR and it
    # is named: ADR-117 (carrier split by divergence), landed by lane W2-F1 on DECLARE-F F-1.
    # No other member moved. Its status field is `Proposed`, NOT the word `DRAFT` the ruling
    # used: `DRAFT` is not an enum member, and this module's own TIER_COMMIT leg refuses it
    # as a BLOCKING defect, so the ADR could not have landed carrying it. That deviation is
    # recorded in the ADR header and its index row, not just here.
    #
    # RE-MEASURED 2026-09-07 by seat filings-N3: 90 -> 91. The delta is again ONE ADR and it
    # is named: ADR-118 (one graph — FPG-1 is the repo graph, organs are views), drafted on
    # the operator's DECLARE-GRAPH-2026-09-07 ruling. No other member moved. Its status field
    # is `Proposed` for exactly the reason ADR-117's note above records, and that deviation is
    # recorded in the ADR header and its index row rather than only here.
    assert len(fields) == 91, "live ADR count moved — re-measure the Step-1 baseline"


def test_shipped_corpus_grammar_distribution_matches_the_measured_baseline():
    fields, _, _ = vas.scan_zone(vas.LIVE_DIR)
    counts: dict[str, int] = {}
    for f in fields:
        counts[f.grammar] = counts.get(f.grammar, 0) + 1
    # RE-MEASURED 2026-09-01: G1 41 -> 42, the same single cause as the count above
    # (ADR-116 carries a G1-shaped status field). G2/G3/G4 are unchanged, which is the
    # check that the delta really is one ADR and not a grammar drift wearing its clothes.
    #
    # RE-MEASURED 2026-09-07: G1 42 -> 43, the same single cause as the count above
    # (ADR-117 carries a G1-shaped status field). G2/G3/G4 unchanged again, which is what
    # confirms the delta is one ADR rather than grammar drift wearing its clothes.
    #
    # RE-MEASURED 2026-09-07 by seat filings-N3: G1 43 -> 44, the same single cause as the
    # count above (ADR-118 carries a G1-shaped status field). G2/G3/G4 unchanged a third
    # time, which is what confirms the delta is one ADR rather than grammar drift.
    assert counts == {"G1": 44, "G2": 34, "G3": 12, "G4": 1}


def test_shipped_corpus_has_zero_enum_violations():
    """The leg armed at FAIL. If this ever goes RED the enum genuinely drifted."""
    fields, _, _ = vas.scan_zone(vas.LIVE_DIR)
    assert [d for d in vas.field_defects(fields) if d.rule == vas.R_ENUM] == []


def test_shipped_corpus_coherence_divergences_are_the_three_measured():
    """Goes through `header_status_map` — the real call path — and asserts the FULL per-rule
    distribution, not just the coherence subset.

    terra R5-MEDIUM-3: the earlier version built its own header dict, bypassing
    `header_status_map`, and asserted only the coherence divergences. An
    `index_effective_status` regression that dropped a non-divergent row would raise
    `unindexed` while leaving ADR-45/46/47 unchanged — and this test still passed.
    """
    fields, missing, extra = vas.scan_zone(vas.LIVE_DIR)
    eff = vas.index_effective_status(
        (vas.LIVE_DIR / "README.md").read_text(encoding="utf-8"))
    defects = (vas.corpus_defects(fields, missing, extra)
               + vas.duplicate_id_defects(fields, missing)
               + vas.coherence_defects(
                   vas.header_status_map(fields, missing), eff))
    counts: dict[str, int] = {}
    for d in defects:
        counts[d.rule] = counts.get(d.rule, 0) + 1
    assert counts == {
        vas.R_GRAMMAR: 47,
        vas.R_COHERENCE: 3,
        vas.R_WRAP: 1,
        vas.R_DUPLICATE: 2,
    }, counts
    # enum / single-field / unindexed are the legs measured at ZERO — assert their absence
    # explicitly rather than leaving it implied by the dict above.
    for rule in (vas.R_ENUM, vas.R_SINGLE, vas.R_UNINDEXED):
        assert counts.get(rule, 0) == 0
    assert {d.subject for d in defects if d.rule == vas.R_COHERENCE} == {
        "ADR-45", "ADR-46", "ADR-47"}


# --- the Flip-condition leg ----------------------------------------------------
#
# Same three layers as above, applied to the rule that makes an ADR name the condition under
# which its own decision reverses. Layer 1 proves the section detector has teeth (a QUOTED
# heading is not a written one); layer 2 covers the grandfather split; layer 3 pins the
# measured corpus population.

def _flip(body: str) -> str:
    return vas.flip_section_state(body)


@pytest.mark.parametrize("heading", [
    "## Flip-condition",
    "## Flip condition",
    "### flip-condition",
    "## **Flip-condition**",
    "## Flip-condition — what would reverse this",
])
def test_a_written_flip_section_is_recognised_in_its_measured_spellings(heading):
    """The heading is identified by NAME. Capitalisation, a bold wrapper, a nested level and
    a trailing subtitle are typography — failing a conforming ADR over any of them would be a
    false positive on a FAIL-armed leg, the worst failure this module has."""
    assert _flip(f"# ADR-900\n\n{heading}\n\nIf the benchmark regresses.\n") == "present"


def test_a_missing_flip_section_is_missing_not_empty():
    assert _flip("# ADR-900\n\n## Decision\n\nDo the thing.\n") == "missing"


@pytest.mark.parametrize("body", [
    "",                                        # heading, then nothing
    "\n\n",                                    # heading, then blank lines
    "\n<What would make us reverse this?>\n",  # the template placeholder, unanswered
    "\n<!-- a note -->\n",                     # comment only — lexed out, so nothing visible
    # A MULTI-LINE placeholder. Found live: the shipped template's own prompt runs to five
    # physical lines, and a line-anchored `^<...>$` test passed every one-line fixture above
    # and then read the real template as answered. The placeholder is a SPAN, not a line.
    "\n<What would make us reverse this decision?\nName the observable —\na measurement.>\n",
    # ...and two placeholder blocks with nothing else are still nothing else.
    "\n<first prompt>\n\n<second prompt>\n",
    # A NESTED prompt. Also found live: the shipped template's own says `write "none — <why>"`,
    # and a single flat subtraction pass removes the inner span while leaving the outer
    # brackets behind as residue, which then reads as an answer.
    "\n<What would reverse this? Where nothing would, write \"none — <why>\".>\n",
])
def test_an_unanswered_flip_section_is_EMPTY_not_present(body):
    """The vacuous pass this leg exists to refuse: an ADR that copied the template, kept the
    heading and never answered the question has named no flip. `empty` is a defect too."""
    assert _flip(f"# ADR-900\n\n## Flip-condition\n{body}\n## Consequences\n\nx\n") == "empty"


def test_a_flip_heading_inside_a_code_fence_does_not_satisfy_the_rule():
    """Quoting the requirement is not meeting it. Without fence tracking, any ADR could
    satisfy a FAIL-armed leg by showing the template in an example block."""
    body = ("# ADR-900\n\n```markdown\n## Flip-condition\n\nIf X.\n```\n")
    assert _flip(body) == "missing"


def test_a_flip_heading_inside_a_blockquote_does_not_satisfy_the_rule():
    """A quoted contract excerpt is someone else's document, not this ADR's section."""
    assert _flip("# ADR-900\n\n> ## Flip-condition\n>\n> If X.\n") == "missing"


def test_a_flip_heading_inside_an_html_comment_does_not_satisfy_the_rule():
    assert _flip("# ADR-900\n\n<!--\n## Flip-condition\n\nIf X.\n-->\n") == "missing"


def test_the_section_ends_at_the_next_heading_of_the_same_or_shallower_level():
    """Body collection must stop at the section boundary, or the NEXT section's prose fills an
    empty Flip-condition and the emptiness check never fires."""
    body = "# ADR-900\n\n## Flip-condition\n\n## Consequences\n\nReal prose lives here.\n"
    assert _flip(body) == "empty"


def test_prose_containing_an_angle_bracket_token_still_reads_as_FILLED():
    """The other direction of the span subtraction: this corpus writes `<name>`-shaped tokens
    in ordinary prose, and treating a body that contains one as unanswered would be a false
    positive on a FAIL-armed leg."""
    body = ("# ADR-900\n\n## Flip-condition\n\n"
            "If the `worktree-<name>` grammar stops being machine-produced.\n")
    assert _flip(body) == "present"


def test_a_deeper_subheading_stays_INSIDE_the_flip_section():
    body = ("# ADR-900\n\n## Flip-condition\n\n### The measurable\n\n"
            "If p95 latency doubles.\n\n## Consequences\n\nx\n")
    assert _flip(body) == "present"


def test_a_NEW_adr_without_a_flip_section_is_a_FAIL_armed_defect(tmp_path):
    """The teeth. An ADR numbered above the grandfather mark must name its flip."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / f"ADR-{vas.FLIP_GRANDFATHER_MAX_ADR + 1}-new.md").write_text(
        "# ADR-x\n\n- **Status:** Accepted\n", encoding="utf-8")
    defects = vas.required_section_defects(d)
    assert [d_.rule for d_ in defects] == [vas.R_FLIP, vas.R_ALTS]
    assert vas.FAIL_RULES.issuperset({vas.R_FLIP, vas.R_ALTS})


def test_a_GRANDFATHERED_adr_without_a_flip_section_WARNS_and_never_FAILS(tmp_path):
    """The lane contract's explicit bar: *existing ADRs WARN with a disposition path, not
    fail*. Failing 89 pre-existing files retroactively wedges every commit in the repo."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / f"ADR-{vas.FLIP_GRANDFATHER_MAX_ADR}-old.md").write_text(
        "# ADR-x\n\n- **Status:** Accepted\n", encoding="utf-8")
    defects = vas.required_section_defects(d)
    assert [d_.rule for d_ in defects] == [vas.R_FLIP_LEGACY, vas.R_ALTS_LEGACY]
    assert not vas.FAIL_RULES & {vas.R_FLIP_LEGACY, vas.R_ALTS_LEGACY}
    for d_ in defects:
        assert "DISPOSITION:" in d_.detail, d_.detail


def test_an_unnumbered_adr_filename_warns_rather_than_blocking(tmp_path):
    """A false positive on a FAIL-armed leg is this module's worst available failure, so a
    name that yields no number is treated as grandfathered."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-draft-no-number.md").write_text("# x\n", encoding="utf-8")
    assert [d_.rule for d_ in vas.required_section_defects(d)] == [
        vas.R_FLIP_LEGACY, vas.R_ALTS_LEGACY]


# --- the Alternatives-considered leg (operator, DECLARE-F-2-2026-09-07 §A) ------

@pytest.mark.parametrize("heading", [
    # Every spelling below was MEASURED in the live corpus, with its file count. Enforcing only
    # the template's wording would report 9 ADRs as having justified nothing when they plainly
    # did — and 3 more for numbering their sections.
    "## Alternatives considered",                       # 45 files — the template's spelling
    "## Rejected alternatives",                         # 6
    "## Alternatives rejected",                         # 3
    "## Alternatives considered (the #86.2 operator fork)",
    "## 10. Alternatives considered",
    "## §9 Alternatives considered",
    "## §4 — Alternatives considered and rejected, with their recorded reasons",
])
def test_every_measured_alternatives_spelling_satisfies_the_requirement(heading):
    body = f"# ADR-900\n\n{heading}\n\nThe sibling design, rejected on cost.\n"
    assert vas.alternatives_section_state(body) == "present", heading


def test_an_unanswered_alternatives_section_is_EMPTY_not_present():
    """`<Always filled…>` was in the template long before anything checked it. A copied,
    unanswered prompt is exactly what the word `Always` failed to prevent."""
    body = ("# ADR-900\n\n## Alternatives considered\n\n"
            "<Always filled. What else was evaluated, and why was it not chosen?>\n")
    assert vas.alternatives_section_state(body) == "empty"


def test_a_recorded_none_considered_SATISFIES_the_requirement():
    """The template's own escape hatch has to work, or the rule forces invention. Recording
    "none considered" plus a reason is an answer; omitting the section is not."""
    body = ("# ADR-900\n\n## Alternatives considered\n\n"
            "None considered — the operator ruled the shape directly.\n")
    assert vas.alternatives_section_state(body) == "present"


def test_the_word_alternatives_in_prose_does_not_satisfy_the_requirement():
    """Only a HEADING opens the section. A rule satisfied by mentioning the word is not a
    required section, it is a keyword search."""
    body = "# ADR-900\n\n## Decision\n\nWe weighed the alternatives and chose this one.\n"
    assert vas.alternatives_section_state(body) == "missing"


def test_the_template_carries_an_alternatives_considered_section():
    tmpl = (vas._REPO_ROOT / "templates" / "ADR-template.md").read_text(encoding="utf-8")
    assert vas.alternatives_section_state(tmpl) == "empty", (
        "the template must carry the HEADING and leave the BODY an unanswered placeholder")


def test_both_required_sections_share_one_grandfather_mark():
    """They arm in the same commit, so they grandfather the same population. Two marks would
    drift, and the second one to drift would be the one nobody re-measured."""
    assert {s.fail_rule for s in vas.REQUIRED_SECTIONS} == {vas.R_FLIP, vas.R_ALTS}
    assert {s.warn_rule for s in vas.REQUIRED_SECTIONS} == {
        vas.R_FLIP_LEGACY, vas.R_ALTS_LEGACY}
    assert vas.FAIL_RULES.issuperset({s.fail_rule for s in vas.REQUIRED_SECTIONS})
    assert not vas.FAIL_RULES & {s.warn_rule for s in vas.REQUIRED_SECTIONS}


def test_ADR_117_landed_above_the_mark_and_satisfies_BOTH_requirements():
    """The mid-lane collision, pinned. ADR-117 was written under the OLD template, in the same
    wave, and is the only live ADR ABOVE the grandfather mark — so both legs are FAIL-armed
    against it. It carries both sections on its own merits, which is why the mark was not
    raised to re-grandfather it and why this leg arms with zero FAILs.
    """
    adr = next(vas.LIVE_DIR.glob("ADR-117-*.md"), None)
    if adr is None:                       # not yet merged into this tree
        pytest.skip("ADR-117 is not in this checkout")
    text = adr.read_text(encoding="utf-8")
    assert int(vas.adr_number(adr).split("-")[1]) > vas.FLIP_GRANDFATHER_MAX_ADR
    assert vas.flip_section_state(text) == "present"
    assert vas.alternatives_section_state(text) == "present"


def test_a_section_numbered_with_an_enumerator_is_still_written():
    """`## 10. Alternatives considered` / `## §9 …` are live corpus forms. Numbering a section
    does not un-write it."""
    for heading in ("## 10. Flip-condition", "## §9 Flip-condition", "## §4 — Flip-condition"):
        body = f"# ADR-900\n\n{heading}\n\nIf the benchmark regresses.\n"
        assert vas.flip_section_state(body) == "present", heading


# --- layer 2d: the required-section reviewer round (one case per HIGH) ---------
#
# Five HIGHs, one round, `reviewer: codex`. Every case below is a concrete input the reviewer
# returned against the round-1 code and each is pinned so a later edit cannot reintroduce it.

def test_a_BLOCKQUOTED_body_is_body_not_quoted_material():
    """terra HIGH-1, and the worst class this module has: a FALSE POSITIVE on a FAIL-armed
    leg. Blockquote lines were skipped everywhere, so an ADR that answered the question in a
    blockquote — the form this corpus uses most for emphasis — was reported EMPTY."""
    body = "# ADR-900\n\n## Flip-condition\n\n> Reverse if the measured cost doubles.\n"
    assert _flip(body) == "present"


def test_a_blockquoted_heading_still_does_not_OPEN_a_section():
    """The other half of the same fix: quoted material before the section is still quoted."""
    assert _flip("# ADR-900\n\n> ## Flip-condition\n>\n> If X.\n") == "missing"


def test_a_quoted_heading_inside_the_body_does_not_END_the_section():
    """A section that quotes a later heading keeps its own body — the boundary test is matched
    against the line WITH its `>` prefix, so a quoted heading cannot terminate it."""
    body = ("# ADR-900\n\n## Flip-condition\n\n> ## Consequences\n\n"
            "If the benchmark regresses.\n")
    assert _flip(body) == "present"


def test_an_EMPTY_ATX_heading_ends_the_section():
    """terra HIGH-2: `##` alone is a valid empty ATX heading. Requiring a space after the
    hashes made it invisible as a boundary, so the NEXT section's prose filled a
    placeholder-only body and laundered it into `present`."""
    body = ("# ADR-900\n\n## Flip-condition\n\n<unanswered prompt>\n\n##\n\n"
            "Real prose that belongs to the next section.\n")
    assert _flip(body) == "empty"


def test_a_hash_run_with_no_space_is_not_a_heading_boundary():
    """The EMPTY-heading fix must not turn `###nothing` into a boundary — that is not a
    heading in CommonMark, it is text."""
    body = "# ADR-900\n\n## Flip-condition\n\n<prompt>\n\n###nothing\n"
    assert _flip(body) == "present"       # `###nothing` is body text, and it is filled


@pytest.mark.parametrize("heading", [
    "## **Flip-condition",       # opened, never closed
    "## *Flip-condition*",       # balanced
    "## __Alternatives considered",
])
def test_unbalanced_emphasis_in_a_heading_is_accepted_deliberately(heading):
    """terra HIGH-3, resolved in the LENIENT direction and pinned so the choice is visible.

    Unlike `_ENUM_AT_START_RE`, which guards a declared VALUE where unbalanced markup is how a
    bad token is laundered into a good one, this regex identifies a section by NAME — where
    the only thing sloppy emphasis can do is SATISFY the requirement. A false positive on a
    FAIL-armed leg is the worse error, so the lenient reading is the safe one.
    """
    body = f"# ADR-900\n\n{heading}\n\nAn answer.\n"
    state = (vas.alternatives_section_state(body) if "Alternatives" in heading
             else vas.flip_section_state(body))
    assert state == "present", heading


def test_an_unnumbered_adr_is_warned_AND_named_as_ungateable(tmp_path):
    """terra HIGH-4. The leniency stays — an unparseable name cannot be placed relative to the
    mark, and guessing would risk a false FAIL — but it is no longer SILENT: the evidence says
    the file is ungateable, so the hole is visible to whoever reads the WARN."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-draft-no-number.md").write_text("# x\n", encoding="utf-8")
    defects = vas.required_section_defects(d)
    assert [d_.rule for d_ in defects] == [vas.R_FLIP_LEGACY, vas.R_ALTS_LEGACY]
    for d_ in defects:
        assert "UNGATEABLE" in d_.detail, d_.detail


def test_the_grandfather_mark_is_the_measured_high_water_and_is_frozen():
    """116 is MEASURED — the highest live ADR number at the leg's arming (2026-09-07,
    `ef53b069`). It is asserted here so that RAISING it, which would re-grandfather an ADR
    written after the requirement existed, is a visible test edit and not a quiet weakening."""
    numbers = [int(vas.adr_number(p).split("-")[1])
               for p in vas.LIVE_DIR.glob("ADR-*.md") if vas.adr_number(p)]
    assert vas.FLIP_GRANDFATHER_MAX_ADR == 116
    assert max(numbers) >= vas.FLIP_GRANDFATHER_MAX_ADR, (
        "the mark is above the corpus high-water — it was raised, not measured")


def test_the_template_carries_a_flip_condition_section():
    """`templates/ADR-template.md` is the requirement's declaration site: an author meets the
    rule by copying the template. If the section leaves the template, every new ADR fails a
    FAIL-armed leg with nothing to copy from."""
    tmpl = (vas._REPO_ROOT / "templates" / "ADR-template.md").read_text(encoding="utf-8")
    assert vas.flip_section_state(tmpl) == "empty", (
        "the template must carry the HEADING and leave the BODY an unanswered placeholder — "
        "a filled template body would let a copied-but-unanswered section read as compliant")


def test_shipped_corpus_required_section_baseline_is_the_measured_population():
    """Layer 3, both required sections. MEASURED 2026-09-07 on `ec0d7912`, after ADR-117
    landed mid-lane: 90 live ADRs; 89 name no flip (ADR-117 is the only one that does) and 32
    record no alternatives. Every one of them is at or below the mark, so the two legs add 121
    WARNs and exactly **0 FAILs** on the day they arm.

    A FAIL appearing here means a NEW ADR landed carrying neither section — which is the
    requirement working, not this baseline being wrong.

    The alternatives figure is re-measured against the operator's 57/88 (65%) in
    DECLARE-F-2-2026-09-07 §A and does NOT reproduce it: this predicate counts 58 of 90 (64%).
    The denominator moved (two ADRs landed since), and the numerator agrees only because the
    predicate accepts the corpus's three measured spellings; a grep for the template's exact
    words counts 46, not 57.
    """
    defects = vas.required_section_defects(vas.LIVE_DIR)
    counts: dict[str, int] = {}
    for d in defects:
        counts[d.rule] = counts.get(d.rule, 0) + 1
    assert counts == {vas.R_FLIP_LEGACY: 89, vas.R_ALTS_LEGACY: 32}, counts


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
    """Proof the check is not warn-by-construction — a clean corpus really does pass.

    UPDATED when the `Flip-condition` leg landed: "fully conforming" now includes naming the
    flip, so this fixture gained the section. That is the requirement arriving, not the test
    being relaxed — the assertion is still `pass`, and dropping the new section from the
    fixture puts it back to `warn`.
    """
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-11-x.md").write_text(
        "# ADR-11 — x\n\n- **Status:** Accepted\n"
        "\n## Flip-condition\n\nIf the measured cost crosses 2x.\n"
        "\n## Alternatives considered\n\nNone considered — the sibling measured slower.\n",
        encoding="utf-8")
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


def test_FAIL_evidence_still_reports_the_warn_defects_it_computed(tmp_path):
    """terra R7-HIGH-3: when any FAIL-rule defect existed, the adapter returned evidence
    listing ONLY the blocking defects — silently discarding every grammar/coherence/duplicate
    defect the same run had already found. A FAIL must not make the rest invisible."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-11-x.md").write_text(          # G3 -> a grammar WARN
        "# ADR-11 — x\n\nStatus: Accepted\n", encoding="utf-8")
    (d / "ADR-12-y.md").write_text(          # no status -> a single-field FAIL
        "# ADR-12 — y\n\n(nothing)\n", encoding="utf-8")
    (d / "README.md").write_text(
        "| ADR | Date | Title |\n|--|--|--|\n"
        "| ADR-11 | 2026-01-01 | x |\n| ADR-12 | 2026-01-02 | y |\n", encoding="utf-8")

    f = check_adr_status_grammar(tmp_path)[0]
    assert f.status == "fail"
    assert "single-field" in f.evidence          # the blocking one
    assert "grammar=1" in f.evidence, f.evidence  # ...and the one it used to drop


@pytest.mark.parametrize("seed,expect", [
    ("Status: Accepted\n", "warn"),      # G3 -> grammar WARN only
    ("(nothing)\n", "fail"),             # no field -> single-field FAIL
    # The `pass` seed carries a Flip-condition section: since that leg landed, a status line
    # alone is conforming on the status rules but WARNs on the flip one, and this test is
    # about evidence sanitation on all three branches — it needs a genuine `pass` branch.
    ("- **Status:** Accepted\n\n## Flip-condition\n\nIf the cost crosses 2x.\n"
     "\n## Alternatives considered\n\nNone considered — measured.\n", "pass"),
])
def test_evidence_never_contains_a_literal_pipe(tmp_path, seed, expect):
    """`Finding.evidence` is markdown-table-safe by contract (`_common.Finding` docstring):
    emitters replace `|` with `/`. The R7-HIGH-3 fix introduced `||` separators, so the
    sanitation has to cover them — on every branch, not just the one that was edited."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-11-x.md").write_text(f"# ADR-11 — x\n\n{seed}", encoding="utf-8")
    (d / "README.md").write_text(
        "| ADR | Date | Title |\n|--|--|--|\n| ADR-11 | 2026-01-01 | x |\n", encoding="utf-8")
    f = check_adr_status_grammar(tmp_path)[0]
    assert f.status == expect, f.evidence
    assert "|" not in f.evidence, f.evidence


def test_check_FAILS_a_new_adr_that_names_no_flip_condition(tmp_path):
    """The adapter half of the teeth: the FAIL-armed flip leg has to reach the audit finding,
    not just the library function. This check is tiered at TIER_COMMIT, so this is what
    actually blocks a commit."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    n = vas.FLIP_GRANDFATHER_MAX_ADR + 1
    (d / f"ADR-{n}-new.md").write_text(
        f"# ADR-{n} — new\n\n- **Status:** Accepted\n", encoding="utf-8")
    (d / "README.md").write_text(
        f"| ADR | Date | Title |\n|--|--|--|\n| ADR-{n} | 2026-01-01 | new |\n",
        encoding="utf-8")
    f = check_adr_status_grammar(tmp_path)[0]
    assert f.status == "fail", f.evidence
    assert "flip-condition" in f.evidence


def test_check_WARNS_rather_than_FAILS_on_the_grandfathered_population(tmp_path):
    """The other half of the contract bar, at the adapter: a pre-existing ADR with no flip
    section must not block a commit."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-11-x.md").write_text(
        "# ADR-11 — x\n\n- **Status:** Accepted\n", encoding="utf-8")
    (d / "README.md").write_text(
        "| ADR | Date | Title |\n|--|--|--|\n| ADR-11 | 2026-01-01 | x |\n", encoding="utf-8")
    f = check_adr_status_grammar(tmp_path)[0]
    assert f.status == "warn", f.evidence
    assert "flip-condition-legacy=1" in f.evidence, f.evidence


def test_hub_evidence_separates_this_legs_warns_from_the_inherited_baseline():
    """The dispatcher pin: *say what YOUR leg adds*, so the next reader can tell the new WARNs
    from the four inherited populations. They are separate keys in one tally, never a merged
    total."""
    ev = check_adr_status_grammar(vas._REPO_ROOT)[0].evidence
    for inherited in ("grammar=47", "coherence=3", "duplicate-id=2", "wrapped-value=1"):
        assert inherited in ev, ev
    assert "flip-condition-legacy=89" in ev, ev
    assert "alternatives-considered-legacy=32" in ev, ev


def test_a_required_section_read_error_does_not_MASK_a_real_enum_failure(tmp_path,
                                                                        monkeypatch):
    """terra HIGH-5: the adapter early-returned a WARN when the required-section pass raised,
    discarding every defect the same run had already computed — so a race could downgrade a
    genuine commit-blocking FAIL, and the adapter then disagreed with the CLI, which takes no
    such path. Exactly the failure `test_a_missing_index_does_not_MASK_a_real_enum_failure`
    pins for the index leg."""
    d = tmp_path / "docs" / "decisions"
    d.mkdir(parents=True)
    (d / "ADR-11-x.md").write_text(
        "# ADR-11 — x\n\n- **Status:** Ratified\n", encoding="utf-8")   # enum FAIL
    (d / "README.md").write_text(
        "| ADR | Date | Title |\n|--|--|--|\n| ADR-11 | 2026-01-01 | x |\n", encoding="utf-8")

    # Patch the module object the ADAPTER holds, not the one this test imported. The adapter
    # resolves `scripts.validate_adr_status` or bare `validate_adr_status` depending on how it
    # was imported, and those can be two distinct module objects — patching the wrong one makes
    # the test pass by never firing.
    import audit_checks.check_adr_status_grammar as _mod

    def _boom(_directory):
        raise _mod._vas.CorpusUnusable("simulated race")

    monkeypatch.setattr(_mod._vas, "required_section_defects", _boom)
    f = check_adr_status_grammar(tmp_path)[0]
    assert f.status == "fail", f.evidence          # the FAIL survives the read error
    assert "enum" in f.evidence
    assert "DID NOT RUN" in f.evidence, f.evidence  # ...and the error is still reported


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
    # Carries a Flip-condition section for the same reason the adapter's `pass` fixture does:
    # "clean" now includes naming the flip, and the CLI must agree with the adapter about it.
    _write(tmp_path, "ADR-11-x.md",
           "# ADR-11 — x\n\n- **Status:** Accepted\n"
           "\n## Flip-condition\n\nIf the cost crosses 2x.\n"
           "\n## Alternatives considered\n\nNone considered — measured.\n")
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


def test_cli_include_archive_folds_archive_missing_into_duplicate_detection(tmp_path):
    """terra R6-HIGH-2, and a genuine TEST HOLE the mutation run found: fixing the CLI to
    combine `a_missing` into `missing` was not covered by anything, so a mutation reverting
    it survived. A live ADR and a status-less ARCHIVE file sharing a number must produce
    `duplicate-id`, and the live file must NOT then receive a coherence verdict."""
    d = tmp_path / "docs" / "decisions"
    (d / "archive").mkdir(parents=True)
    (d / "ADR-9-main.md").write_text(
        "# ADR-9 — x\n\n- **Status:** Accepted\n", encoding="utf-8")
    (d / "archive" / "ADR-9-amendment.md").write_text(
        "# ADR-9 — amendment\n\n(no status field)\n", encoding="utf-8")
    (d / "README.md").write_text(
        "| ADR | Date | Title |\n|--|--|--|\n| ADR-9 | 2026-01-01 | x |\n", encoding="utf-8")

    res = CliRunner().invoke(vas.main, ["--root", str(tmp_path), "--include-archive"])
    assert res.exit_code == 1, res.output
    assert "duplicate-id: ADR-9" in res.output, res.output
    assert "coherence: ADR-9" not in res.output, res.output


def test_cli_exit_2_when_the_corpus_dir_is_absent(tmp_path):
    """An unreadable subject must never render as a green pass."""
    res = CliRunner().invoke(vas.main, ["--root", str(tmp_path / "nope")])
    assert res.exit_code == 2, res.output
