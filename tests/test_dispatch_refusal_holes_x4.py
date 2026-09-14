"""Two RED-first witnesses for dispatch refusals batch X4 proved are missing.

Both holes were witnessed LIVE on 2026-09-13 during batch X4 and are recorded in
`docs/audits/2026-09-13-technical-batch-x4-manifest.md`. Neither organ exists yet, so both
tests below are `xfail(strict=True)`: they FAIL today because the refusal they name is absent,
and the moment a lane implements it they XPASS -- which `strict=True` turns into a hard
failure, forcing the marker off. That is the RED-first contract of ADR-108 section B expressed
so it cannot rot: the witness cannot be satisfied by deleting it, and it cannot silently
survive the fix.

Placed in their own module rather than in `tests/test_seat_refusals.py` because that file's
four roster meta-tests assert the CURRENT refusal roster exactly; a witness for a refusal that
does not exist yet belongs beside the roster, not inside it.
"""
from __future__ import annotations

import pytest

import seat_refusals as sr


# --- [#748] -- a worktree that resolves to the primary is not isolated -------------------------

@pytest.mark.xfail(
    strict=True,
    reason="[#748] no refusal reads core.worktree; witnessed by lane-x-675-instrument-holes "
    "on 2026-09-13. Remove this marker in the lane that adds the refusal.",
)
def test_a_lane_whose_worktree_redirects_to_the_primary_is_REFUSED_before_launch():
    """A `core.worktree` redirect makes a lane's own isolation vacuous, silently.

    `git` answers every question from the redirect target, so the lane reads and WRITES the
    primary checkout while `git status`, `git log` and `git rev-parse --show-toplevel` all
    report success. Nothing fails; the lane simply is not isolated. The refusal therefore has
    to fire at DISPATCH, before the session exists -- run afterwards, the write it exists to
    prevent has already landed in the integrator's tree.

    The property: given a provisioned worktree whose resolved top level equals the primary
    checkout, the dispatcher refuses to launch, and the refusal NAMES the lane and the
    redirect target so the operator can act on it.
    """
    with pytest.raises(sr.SeatRefusal, match="worktree-isolation"):
        sr.refuse_worktree_isolation(
            {"lane-x-675-instrument-holes": "C:/repo"},
            primary_root="C:/repo",
        )


# --- [#749] -- one row, one lane, per open batch -----------------------------------------------

@pytest.mark.xfail(
    strict=True,
    reason="[#749] no organ maps a row id to its lanes; witnessed by slots 3 and 3' of batch "
    "X4 on 2026-09-13. Remove this marker in the lane that adds the refusal.",
)
def test_a_second_lane_for_a_row_that_already_has_one_is_REFUSED():
    """Two slugs, one row, one open batch -- the collision batch X4 paid for live.

    `refuse_lane_ceiling`'s DUPLICATE leg compares SLUGS, so `lane-x-675-instrument-holes` and
    `lane-x-675-instrument-fixes` are two different lanes to it and both pass. They are one row.
    The cost is not cosmetic: task ids are sequential, so two lanes filing the same finding pick
    the SAME ids in their own trees and the duplicate lands silently at integration.

    The property: a contract whose row already has a live or completed lane in the open batch is
    REFUSED, and the refusal names the row and BOTH slugs. A deliberate re-cut stays possible by
    disposing of the first lane -- the refusal is on an UNDISPOSED duplicate, not on re-cutting.
    """
    with pytest.raises(sr.SeatRefusal, match="duplicate-row-lane") as exc:
        sr.refuse_duplicate_row_lane(
            {
                "lane-x-675-instrument-holes": "[#675]",
                "lane-x-675-instrument-fixes": "[#675]",
            }
        )

    message = str(exc.value)
    assert "675" in message
    assert "lane-x-675-instrument-holes" in message
    assert "lane-x-675-instrument-fixes" in message
