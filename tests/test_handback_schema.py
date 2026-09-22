"""handback_schema.py -- the one schema for HANDBACK line, STATE line, LANE-END report and
REFUSED order (LANE-W4B-2-handback-organ Done-contract 2, RC3).

RED-first (ADR-108 s.B): authored and witnessed FAILING before `scripts/handback_schema.py`
existed. Each shape gets a render/parse round trip and a validate() boundary test; the HANDBACK
line additionally gets the agreement test the Done-contract names explicitly: "the existing
`audit.py handback` form and the organ's form agree — show both accept the same line".
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


def _mod(name: str):
    return importlib.import_module(name)


# --- 1. HandbackLine: agrees with audit.py handback ----------------------------------------------

CODE_LINE = "HANDBACK worktree-lane-x @ 1a2b3c4d code review=codex HIGH:0 MED:1 LOW:2"
DOCS_LINE = "HANDBACK worktree-lane-x @ 1a2b3c4d docs-only"
BAD_SHA_LINE = "HANDBACK worktree-lane-x @ HEAD code review=codex HIGH:0 MED:0 LOW:0"
NO_REVIEW_LINE = "HANDBACK worktree-lane-x @ 1a2b3c4d code"


def test_handback_line_parse_render_round_trips():
    hs = _mod("handback_schema")
    parsed = hs.HandbackLine.parse(CODE_LINE)
    assert parsed is not None
    assert parsed.render() == CODE_LINE


def test_handback_line_and_audit_handback_agree_on_a_mergeable_line():
    hs = _mod("handback_schema")
    audit = _mod("audit")
    schema_ok, _ = hs.validate_handback_line(CODE_LINE)
    cli_ok, _ = audit.review_handback_verdict(CODE_LINE)
    assert schema_ok is True and cli_ok is True


def test_handback_line_and_audit_handback_agree_on_a_refused_line():
    hs = _mod("handback_schema")
    audit = _mod("audit")
    for line in (BAD_SHA_LINE, NO_REVIEW_LINE, "not a handback line at all"):
        schema_ok, _ = hs.validate_handback_line(line)
        cli_ok, _ = audit.review_handback_verdict(line)
        assert schema_ok is False and cli_ok is False, line


def test_handback_line_docs_only_needs_no_reviewer():
    hs = _mod("handback_schema")
    parsed = hs.HandbackLine.parse(DOCS_LINE)
    assert parsed is not None and parsed.reviewer is None
    ok, msg = parsed.validate()
    assert ok is True, msg


def test_handback_line_parse_rejects_a_malformed_line():
    hs = _mod("handback_schema")
    assert hs.HandbackLine.parse("HANDBACK no-sha-or-class") is None
    assert hs.HandbackLine.parse("this is not a handback line") is None


def test_handback_line_parse_rejects_ambiguous_duplicate_review_tokens():
    """terra HIGH: `audit.review_handback_verdict` REFUSES >1 `review=` token outright ("a line
    that contradicts itself asserts nothing"). Collapsing that to `reviewer=None` in `parse()`
    would make `parse(line).validate()` MERGE a line `validate_handback_line(line)` refuses --
    exactly the round-trip drift this schema exists to make impossible."""
    hs = _mod("handback_schema")
    audit = _mod("audit")
    line = "HANDBACK worktree-lane-x @ 1a2b3c4d docs-only review=alice review=bob"
    assert hs.HandbackLine.parse(line) is None
    cli_ok, _ = audit.review_handback_verdict(line)
    assert cli_ok is False


# --- 2. StateLine ----------------------------------------------------------------------------

def test_state_line_round_trips_and_validates():
    hs = _mod("handback_schema")
    line = "STATE lane-x WAITING 1a2b3c4 2026-09-22T19:46:00Z"
    parsed = hs.StateLine.parse(line)
    assert parsed is not None and parsed.render() == line
    ok, _ = parsed.validate()
    assert ok is True


def test_state_line_carries_a_trailing_note():
    hs = _mod("handback_schema")
    line = "STATE lane-x REFUSED 1a2b3c4 2026-09-22T19:46:00Z repair 1 of 2 (job abc123)"
    parsed = hs.StateLine.parse(line)
    assert parsed is not None
    assert parsed.note == "repair 1 of 2 (job abc123)"
    assert parsed.render() == line


def test_state_line_rejects_an_unknown_verdict():
    hs = _mod("handback_schema")
    ok, msg = hs.validate_state_line("STATE lane-x BOGUS 1a2b3c4 2026-09-22T19:46:00Z")
    assert ok is False and "BOGUS" in msg


def test_state_line_rejects_a_bad_sha_or_timestamp():
    hs = _mod("handback_schema")
    ok, _ = hs.validate_state_line("STATE lane-x MERGED not-a-sha 2026-09-22T19:46:00Z")
    assert ok is False
    ok, _ = hs.validate_state_line("STATE lane-x MERGED 1a2b3c4 not-a-timestamp")
    assert ok is False


def test_state_line_parse_rejects_multiline_input():
    hs = _mod("handback_schema")
    assert hs.StateLine.parse("STATE a WAITING 1a2b3c4 2026-09-22T19:46:00Z\nextra") is None


# --- 3. LaneEndReport --------------------------------------------------------------------------

def test_lane_end_report_render_parse_round_trips():
    hs = _mod("handback_schema")
    text = hs.render_lane_end_report(
        "lane-x", "2026-09-22T19:46:00Z", ["feat: a"], ["scripts/a.py"],
        hs.VERDICT_CLEAN, "branch: worktree-lane-x", [("MOMENT-A.json", '{"organ": "a"}')])
    facts = hs.LaneEndReport.parse(text)
    assert facts.lane == "lane-x"
    assert facts.commits == ["feat: a"]
    assert facts.changed == ["scripts/a.py"]
    assert facts.verdict == hs.VERDICT_CLEAN
    assert facts.receipts == [{"organ": "a"}]
    ok, _ = facts.validate()
    assert ok is True


def test_lane_end_report_validate_refuses_no_heading():
    hs = _mod("handback_schema")
    facts = hs.LaneEndReport.parse("not a lane-end report at all")
    ok, msg = facts.validate()
    assert ok is False and "heading" in msg


def test_lane_end_report_validate_refuses_an_unknown_verdict():
    hs = _mod("handback_schema")
    text = "# lane-x -- lane-end report\n\n## Verdict\n\nsomething else entirely\n"
    facts = hs.LaneEndReport.parse(text)
    ok, msg = facts.validate()
    assert ok is False and "verdict" in msg.lower()


# --- 4. RefusedOrder ---------------------------------------------------------------------------

def test_refused_order_render_parse_round_trips():
    hs = _mod("handback_schema")
    checks = [hs.CheckResult("branch-purity", False, "foreign commit abc123"),
             hs.CheckResult("ratchet", True, "green")]
    order = hs.RefusedOrder(lane="lane-x", branch="worktree-lane-x", checks=checks,
                            finished_at="2026-09-22T19:46:00Z")
    ok, _ = order.validate()
    assert ok is True
    text = order.render()
    assert "branch-purity" in text and "foreign commit abc123" in text
    back = hs.RefusedOrder.parse(text)
    assert back is not None
    assert back.lane == "lane-x" and back.branch == "worktree-lane-x"
    assert back.reasons == ["branch-purity: foreign commit abc123"]


def test_refused_order_validate_refuses_with_no_failing_check():
    hs = _mod("handback_schema")
    order = hs.RefusedOrder(lane="lane-x", branch="worktree-lane-x",
                            checks=[hs.CheckResult("ratchet", True, "green")],
                            finished_at="2026-09-22T19:46:00Z")
    ok, msg = order.validate()
    assert ok is False and "no failing check" in msg
