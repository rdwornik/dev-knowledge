"""Witnesses for `lane-claim-marker`'s own Done-contract item 2: "Templates call it: each of the
four templates' step 0 runs `claim`; teardown removes the markers (`no_leftovers.py`); a test
renders each template and asserts both." Follows the same read-the-template-text style as the
sibling ownership tests (`tests/test_order_cycle_rule.py`, `tests/test_dispatcher_order_adopts_
queue.py`, `tests/test_integrator_order_triggers.py`) rather than a template-filling engine.

Ownership (ruling (i)): this lane edits ONLY the step-0 claim line and the teardown removal line
of each of the four templates -- everything else in them (state/cycle sections, close/refusal/
verification steps) belongs to `lane-orchestrator-cycling` and `lane-arm-ci`, so these tests pin
only the added lines, never the templates' other content.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = REPO_ROOT / "templates"

LANE_TEMPLATE = TEMPLATES / "lane-contract-template.md"
INTEGRATOR_TEMPLATE = TEMPLATES / "integrator-order-template.md"
DISPATCHER_TEMPLATE = TEMPLATES / "dispatcher-order-template.md"
COMMON_TEMPLATE = TEMPLATES / "batch-common-rules-template.md"

ALL_FOUR = (LANE_TEMPLATE, INTEGRATOR_TEMPLATE, DISPATCHER_TEMPLATE, COMMON_TEMPLATE)


def _text(path: Path) -> str:
    assert path.exists(), f"{path} does not exist"
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Prose in these templates wraps at ~100 chars, so a phrase this test cares about can span a
    line break the author is free to move. Collapse all whitespace runs to one space before
    substring checks, so wrapping is not part of what is pinned."""
    return re.sub(r"\s+", " ", text)


def test_all_four_templates_exist():
    for path in ALL_FOUR:
        assert path.exists()


def test_every_template_has_a_step_0_line_that_runs_claim():
    for path in ALL_FOUR:
        text = _flat(_text(path))
        assert "scripts/claim.py claim" in text, f"{path.name}: no step-0 `claim.py claim` line"
        assert "step 0" in text.lower(), f"{path.name}: the claim line is not marked as step 0"


def test_every_template_has_a_teardown_line_that_removes_the_marker():
    for path in ALL_FOUR:
        text = _flat(_text(path))
        assert "claim.py release" in text, f"{path.name}: no `claim.py release` teardown line"
        assert "no_leftovers.py" in text, (
            f"{path.name}: teardown removal is not tied to the no_leftovers.py verifier")


def test_the_claim_line_names_a_refusal_exit_code():
    """A step-0 line that does not say what refusal looks like is not actionable by a lane
    following the contract at 2am -- pin that every one names exit 3."""
    for path in ALL_FOUR:
        text = _flat(_text(path))
        assert "exit 3" in text, f"{path.name}: the claim step does not name the refusal exit code"


def test_the_lane_template_claim_names_are_scoped_to_the_lane_contract_placeholder():
    text = _flat(_text(LANE_TEMPLATE))
    assert "claim.py claim LANE-<id>-<slug>" in text
    assert "claim.py release LANE-<id>-<slug>" in text
    assert "no_leftovers.py verify --contract LANE-<id>-<slug>" in text
    # A resume/repair session claims a DIFFERENT name -- pin the convention is stated here too.
    assert "LANE-<id>-<slug>-resume-<n>" in text and "-repair-<n>" in text


def test_the_integrator_template_claims_its_own_order_and_releases_the_merged_lanes_marker():
    text = _flat(_text(INTEGRATOR_TEMPLATE))
    assert "claim.py claim INTEGRATOR-<BATCH>" in text
    assert "claim.py release <lane-contract-name>" in text
    assert "no_leftovers.py verify --lane <slug> --contract <lane-contract-name>" in text


def test_the_dispatcher_template_claims_its_own_order():
    text = _flat(_text(DISPATCHER_TEMPLATE))
    assert "claim.py claim DISPATCHER-<BATCH>" in text
    assert "claim.py release DISPATCHER-<BATCH>" in text
    assert "no_leftovers.py verify --contract DISPATCHER-<BATCH>" in text


def test_the_common_rules_template_states_the_universal_claim_and_teardown_rules():
    text = _flat(_text(COMMON_TEMPLATE))
    assert "claim.py claim <name>" in text
    assert "claim.py release <name>" in text
    assert "no_leftovers.py verify --contract <name>" in text
    assert "<name>-resume-<n>" in text and "<name>-repair-<n>" in text


def test_the_claim_step_0_line_sits_before_the_worktree_pairing_section_in_the_lane_template():
    """The step-0 line must actually be step 0 -- before any other numbered work, not appended
    somewhere it would be read only after the lane has already started building."""
    text = _flat(_text(LANE_TEMPLATE))
    claim_idx = text.index("scripts/claim.py claim LANE-<id>-<slug>")
    pairing_idx = text.index("## Worktree pairing")
    assert claim_idx < pairing_idx


def test_do_not_edit_the_forbidden_sections_of_the_order_templates():
    """Do-not: this lane does not touch the close/refusal/arming/cycle sections owned by
    lane-arm-ci and lane-orchestrator-cycling. Pins their headings are untouched rather than
    asserting a byte-diff (which a concurrent, later-merging sibling lane would legitimately
    change) -- the same reconciliation posture `test_order_cycle_rule.py` uses for the reverse
    direction.
    """
    integrator_text = _text(INTEGRATOR_TEMPLATE)
    for heading in ("## Refusals and repairs", "## Close — when every lane is MERGED or FAILED",
                    "## Cycle — hand over to a fresh session of the same role"):
        assert heading in integrator_text, f"integrator template: missing {heading!r}"

    dispatcher_text = _text(DISPATCHER_TEMPLATE)
    for heading in ("## Cycle — hand over to a fresh session of the same role",):
        assert heading in dispatcher_text, f"dispatcher template: missing {heading!r}"
    # The Close step (owned by lane-arm-ci) still exists, unrenamed, in the Sequence section.
    assert "4. **Close**" in dispatcher_text
