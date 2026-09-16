"""Witnesses for `scripts/context_reclamation.py` (`[#792]`).

THE TRIP-TEST IS THE ACCEPTANCE CRITERION, and it is the one the frozen contract names:
clear at a checkpoint, then prove the seat resumes FROM FILES ALONE with no loss. A clear
that loses state is not a reclamation, it is an outage -- so the refusal path is tested at
least as hard as the happy one.

The separation tests at the bottom are not ceremony. This module and
`scripts/resource_lifecycle.py` address two quantities with two different drivers, and the
recorded failure is a single mechanism built for both. A shared constant is the first step
back to that, so it is asserted against.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import context_reclamation as cr  # noqa: E402


# ------------------------------------------------------------------- the derived trigger

def test_the_trigger_fires_on_a_sustained_rise_against_the_seats_own_median():
    costs = [0.10] * 30 + [0.20] * 6          # 2.0x the median, sustained well past 5
    verdict = cr.should_reclaim(costs)
    assert verdict.reclaim
    assert verdict.run >= cr.SUSTAINED_TURNS, verdict


def test_a_single_expensive_turn_does_not_fire_it():
    """One spike is noise. The sustained-run requirement is what makes it a signal."""
    costs = [0.10] * 30 + [0.50] + [0.10] * 5
    assert not cr.should_reclaim(costs).reclaim


def test_a_rise_shorter_than_the_sustained_run_does_not_fire_it():
    costs = [0.10] * 30 + [0.20] * (cr.SUSTAINED_TURNS - 1)
    assert not cr.should_reclaim(costs).reclaim


def test_the_trigger_is_silent_before_the_warmup():
    """A median over three turns is not a median. Nothing fires before the seat has a
    baseline of its own, or every session reclaims on turn two."""
    costs = [0.10, 0.90, 0.90, 0.90, 0.90, 0.90]
    assert not cr.should_reclaim(costs).reclaim


def test_the_trigger_reads_the_seats_OWN_median_not_a_fleet_constant():
    """Two seats with wildly different absolute costs behave identically in ratio terms.
    A fleet constant would fire on the expensive seat and never on the cheap one."""
    cheap = [0.01] * 30 + [0.02] * 6
    dear = [1.00] * 30 + [2.00] * 6
    assert cr.should_reclaim(cheap).reclaim
    assert cr.should_reclaim(dear).reclaim

    quiet_but_expensive = [1.00] * 40
    assert not cr.should_reclaim(quiet_but_expensive).reclaim


def test_the_threshold_carries_its_derivation():
    prov = cr.THRESHOLD_PROVENANCE["RECLAIM_MULTIPLE"]
    assert "52.4" in prov, "the fire-rate table that derived 1.30 is not recorded"
    assert len(prov) > 120


# ------------------------------------------------------------------- checkpoints

def test_the_three_checkpoints_are_the_contracts_three():
    assert set(cr.CHECKPOINTS) == {"dispatcher", "integrator", "lane"}


def test_every_checkpoint_declares_a_non_empty_resume_set():
    """A checkpoint whose state is in no file is not a checkpoint -- it is a hope."""
    for kind, spec in cr.CHECKPOINTS.items():
        assert spec.resume_keys, kind
        assert spec.description, kind


# ------------------------------------------------------------------- THE TRIP-TEST

def _lane_tree(tmp_path: Path, *, packet=True, commits=True) -> Path:
    root = tmp_path / "repo"
    (root / "docs" / "audits").mkdir(parents=True)
    (root / "logs").mkdir(parents=True)
    if packet:
        (root / "docs" / "audits" / "2026-09-15-technical-lane-x-packet.md").write_text(
            "# packet\n", encoding="utf-8")
    if commits:
        (root / "logs" / "LANE-COMMITS.txt").write_text("abc1234\n", encoding="utf-8")
    return root


def test_a_clear_at_a_complete_checkpoint_is_admitted(tmp_path):
    root = _lane_tree(tmp_path)
    resolved = {"handback_packet": root / "docs/audits/2026-09-15-technical-lane-x-packet.md",
                "branch_commits": root / "logs/LANE-COMMITS.txt"}
    verdict = cr.verify_resume("lane", resolved)
    assert verdict.complete, verdict
    assert verdict.missing == ()


def test_a_clear_that_would_lose_state_is_REFUSED(tmp_path):
    """The acceptance criterion, stated as its refusal. This is the whole trip-test: an
    incomplete resume set means the clear is an outage, and the organ must say so BEFORE
    the context is gone rather than after."""
    root = _lane_tree(tmp_path, packet=False)
    resolved = {"handback_packet": root / "docs/audits/nothing-here.md",
                "branch_commits": root / "logs/LANE-COMMITS.txt"}
    verdict = cr.verify_resume("lane", resolved)
    assert not verdict.complete
    assert "handback_packet" in verdict.missing, verdict


def test_an_unresolved_key_is_as_missing_as_an_absent_file(tmp_path):
    """A key nobody supplied a path for is not "fine by default". Silence is the failure
    mode this whole register exists to distinguish from enforcement."""
    root = _lane_tree(tmp_path)
    verdict = cr.verify_resume("lane", {"branch_commits": root / "logs/LANE-COMMITS.txt"})
    assert not verdict.complete
    assert "handback_packet" in verdict.missing


def test_reclaim_refuses_on_an_incomplete_checkpoint(tmp_path):
    root = _lane_tree(tmp_path, packet=False)
    decision = cr.reclaim(
        "lane",
        resolved={"handback_packet": root / "docs/audits/nope.md",
                  "branch_commits": root / "logs/LANE-COMMITS.txt"},
        costs=[0.10] * 30 + [0.20] * 6,
    )
    assert not decision.cleared
    assert "resume" in decision.reason.lower(), decision.reason


def test_reclaim_refuses_when_the_trigger_has_not_fired(tmp_path):
    """A complete checkpoint is permission to clear, not a reason to."""
    root = _lane_tree(tmp_path)
    decision = cr.reclaim(
        "lane",
        resolved={"handback_packet": root / "docs/audits/2026-09-15-technical-lane-x-packet.md",
                  "branch_commits": root / "logs/LANE-COMMITS.txt"},
        costs=[0.10] * 40,
    )
    assert not decision.cleared
    assert "trigger" in decision.reason.lower(), decision.reason


def test_reclaim_clears_when_both_legs_hold(tmp_path):
    root = _lane_tree(tmp_path)
    decision = cr.reclaim(
        "lane",
        resolved={"handback_packet": root / "docs/audits/2026-09-15-technical-lane-x-packet.md",
                  "branch_commits": root / "logs/LANE-COMMITS.txt"},
        costs=[0.10] * 30 + [0.20] * 6,
    )
    assert decision.cleared, decision.reason
    assert decision.resume_from, "a clear that names no resume set is an outage"


def test_the_round_trip_loses_nothing(tmp_path):
    """END TO END: capture the state, clear, and rebuild FROM FILES ALONE.

    The rebuild is byte-compared against the capture. This is the contract's "prove the
    seat resumes from files alone with no loss" as an executable assertion rather than a
    claim in a docstring.
    """
    root = _lane_tree(tmp_path)
    resolved = {"handback_packet": root / "docs/audits/2026-09-15-technical-lane-x-packet.md",
                "branch_commits": root / "logs/LANE-COMMITS.txt"}
    before = cr.capture_state("lane", resolved)

    decision = cr.reclaim("lane", resolved=resolved, costs=[0.10] * 30 + [0.20] * 6)
    assert decision.cleared

    # Everything that was NOT in the resume set is gone; rebuild from what is.
    after = cr.rebuild_state("lane", decision.resume_from)
    assert after == before, (
        "the rebuild from files alone did not reproduce the captured state -- that is an "
        "outage, not a reclamation")


def test_the_round_trip_detects_loss_when_a_resume_file_changes(tmp_path):
    """The round-trip check has to be able to FAIL, or it proves nothing."""
    root = _lane_tree(tmp_path)
    resolved = {"handback_packet": root / "docs/audits/2026-09-15-technical-lane-x-packet.md",
                "branch_commits": root / "logs/LANE-COMMITS.txt"}
    before = cr.capture_state("lane", resolved)
    resolved["branch_commits"].write_text("different\n", encoding="utf-8")
    after = cr.rebuild_state("lane", resolved)
    assert after != before


# ------------------------------------------------------------------- the separation

def test_this_module_declares_no_memory_threshold():
    """Context reclamation must not acquire a memory opinion. The moment it does, the two
    mechanisms have merged again and the measured distinction is lost."""
    leaked = [n for n in dir(cr)
              if n.isupper() and any(t in n for t in ("RSS", "MEMORY", "GB", "SEAT", "MB"))]
    assert leaked == [], f"a memory threshold leaked into the reclamation module: {leaked}"


def test_the_two_modules_measure_disjoint_dimensions():
    """The checkable form of "the two regimes are not one resource": no UNIT in both.

    THE FIRST VERSION OF THIS TEST COMPARED VALUES AND WAS WRONG, and the correction is
    recorded rather than quietly made. It failed on `{5}`, because
    `resource_lifecycle.MERGE_COUNT_BOUND` is 5 (the measured batch merge median) and
    `SUSTAINED_TURNS` is 5 (the run length the fire-rate table was computed with). The two
    are derived independently from different data and coincide by accident; forcing either
    off 5 to satisfy the assertion would have broken a derivation to satisfy a test, which
    is the wrong way round.

    Units are what the rule actually means. A shared VALUE across different dimensions is a
    coincidence; a shared DIMENSION is the two mechanisms measuring one resource again, and
    it would be a defect at any value -- which is why this assertion catches more than the
    one it replaced, not less.
    """
    from scripts import resource_lifecycle as rl

    shared_units = set(rl.THRESHOLD_UNITS.values()) & set(cr.THRESHOLD_UNITS.values())
    assert not shared_units, (
        f"the two regimes declare thresholds in the same dimension(s) {shared_units} -- "
        "they have merged back into one mechanism")

    shared_names = set(rl.THRESHOLD_UNITS) & set(cr.THRESHOLD_UNITS)
    assert not shared_names, f"the two regimes share the threshold name(s) {shared_names}"


def test_every_threshold_declares_a_unit_in_both_modules():
    """A threshold with no declared dimension cannot be checked for the property above, so
    an undeclared one would be a silent hole in the test that precedes this."""
    from scripts import resource_lifecycle as rl

    assert set(cr.THRESHOLD_UNITS) == set(cr.THRESHOLD_PROVENANCE)
    assert set(rl.THRESHOLD_UNITS) == set(rl.THRESHOLD_PROVENANCE)


def test_the_reclamation_module_declares_no_memory_dimension():
    """Stated as a unit rather than as a name pattern, so it survives a rename."""
    assert not [u for u in cr.THRESHOLD_UNITS.values() if "memory" in u]
