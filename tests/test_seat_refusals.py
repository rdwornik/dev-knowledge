"""The five seat refusals REFUSE.

RED-FIRST, and every test here is a removal test. `pytest.raises(SeatRefusal)` fails the moment
the refusal it names stops raising -- which is the property the contract asks for ("each with a
test that FAILS when the refusal is removed"). The passing-path tests exist so that a refusal
cannot be made to pass its own trip-test by refusing everything.

WHY REFUSALS AND NOT WARNINGS. Each of the five is a rule that ALREADY EXISTED in prose and was
broken anyway, in batches T and U, by seats that had read the prose. A warning printed after the
fact is the state being replaced: by then the lane has ended its turn on an intention, the
seventh worktree exists, the substituted reviewer's finding count is in the tally, and the
decision file is on the transport with no carrier. So these raise.
"""
from __future__ import annotations

import pytest
from click.testing import CliRunner

import boot_frontier
import seat_ch8
import seat_refusals as sr


# --- R1 -- the sleeping poll ------------------------------------------------------------------

_GOOD_WAIT = (
    "## 4 - wait for the integrator's PACKET-MERGED\n"
    "<!-- WAIT: interval=120s bound=30 "
    "predicate=to-browser/STATUS-INTEGRATOR.md names this branch as merged -->\n"
)


def test_a_wait_written_as_an_intention_is_refused():
    text = "## 4\n\nWait for the integrator to hand back, then continue.\n"
    with pytest.raises(sr.SeatRefusal, match="sleeping-poll"):
        sr.refuse_sleeping_poll(text, site="SEAT-BOOT-lane.md")


def test_a_wait_declared_as_code_passes():
    assert sr.refuse_sleeping_poll(_GOOD_WAIT, site="t") == 1


def test_a_wait_missing_its_interval_is_refused():
    text = "Wait for the packet.\n<!-- WAIT: bound=30 predicate=STATUS names it -->\n"
    with pytest.raises(sr.SeatRefusal, match="interval"):
        sr.refuse_sleeping_poll(text, site="t")


def test_a_wait_missing_its_bound_is_refused_because_unbounded_is_the_same_stall():
    text = "Wait for the packet.\n<!-- WAIT: interval=60s predicate=STATUS names it -->\n"
    with pytest.raises(sr.SeatRefusal, match="bound"):
        sr.refuse_sleeping_poll(text, site="t")


def test_a_wait_missing_its_predicate_is_refused():
    text = "Wait for the packet.\n<!-- WAIT: interval=60s bound=30 -->\n"
    with pytest.raises(sr.SeatRefusal, match="predicate"):
        sr.refuse_sleeping_poll(text, site="t")


def test_a_zero_interval_or_zero_bound_is_refused():
    for bad in ("interval=0s bound=30 predicate=x", "interval=60s bound=0 predicate=x"):
        with pytest.raises(sr.SeatRefusal):
            sr.refuse_sleeping_poll(f"Wait for x.\n<!-- WAIT: {bad} -->\n", site="t")


def test_quoted_ch8_doctrine_is_exempt_because_it_is_the_rule_not_an_instance():
    """Ch8's own text says "wait for message" -- a rendered boot quotes it and must still pass."""
    text = (
        "<!-- ch8:begin waits -->\n"
        '4. **WAITS.** Every "wait for message" has a 10-minute timeout.\n'
        "<!-- ch8:end waits -->\n"
    )
    assert sr.refuse_sleeping_poll(text, site="t") == 0


def test_a_fenced_poll_loop_is_not_read_as_an_intention():
    text = "```powershell\nwhile ($i -lt 30) { # wait for the file\n  Start-Sleep 60\n}\n```\n"
    assert sr.refuse_sleeping_poll(text, site="t") == 0


# --- R2 -- the lane ceiling, at dispatcher step 0 ---------------------------------------------

def test_a_plan_naming_seven_lanes_is_refused_and_the_excess_is_named():
    lanes = [f"lane-{i}" for i in range(7)]
    with pytest.raises(sr.SeatRefusal, match="lane-ceiling") as exc:
        sr.refuse_lane_ceiling(lanes)
    assert "lane-6" in str(exc.value)
    assert "back to the plan" in str(exc.value)


def test_a_plan_at_the_ceiling_passes():
    lanes = [f"lane-{i}" for i in range(6)]
    assert sr.refuse_lane_ceiling(lanes) == lanes


def test_the_ceiling_is_read_from_the_existing_organ_not_retyped():
    """Library-first: ADR-110's number already lives in `boot_frontier.BATCH_WIDTH_MAX`."""
    assert sr.LANE_CEILING is boot_frontier.BATCH_WIDTH_MAX


def test_a_duplicate_lane_name_is_refused_because_the_plan_miscounts_its_own_width():
    with pytest.raises(sr.SeatRefusal, match="duplicate"):
        sr.refuse_lane_ceiling(["a", "b", "a"])


def test_checking_the_ceiling_after_provisioning_is_itself_refused():
    """"Run later the number is decorative" -- the placement IS the mechanism (Ch8)."""
    with pytest.raises(sr.SeatRefusal, match="checked LATE"):
        sr.refuse_lane_ceiling(["a", "b"], already_provisioned=["worktree-a"])


def test_a_step0_check_with_nothing_provisioned_is_the_sanctioned_call():
    assert sr.refuse_lane_ceiling(["a"], already_provisioned=[]) == ["a"]


# --- R3 -- the reviewer's model id in the tally ------------------------------------------------

_TALLY = "Tally: review=lane-v-000 reviewer=gpt-5.6-terra findings=3 fixed=3"


def test_a_matching_reviewer_passes_and_the_exact_id_is_returned():
    parsed = sr.refuse_tally_reviewer(_TALLY, contracted_reviewer="gpt-5.6-terra")
    assert parsed.reviewer == "gpt-5.6-terra"
    assert parsed.findings == 3 and parsed.fixed == 3


def test_a_substituted_reviewer_that_does_not_report_NONE_is_refused():
    line = "Tally: review=lane-v-000 reviewer=gpt-5.6-sol findings=3 fixed=3"
    with pytest.raises(sr.SeatRefusal, match="reviewer-mismatch"):
        sr.refuse_tally_reviewer(line, contracted_reviewer="gpt-5.6-terra")


def test_a_bare_family_id_is_a_mismatch_not_a_near_miss():
    line = "Tally: review=lane-v-000 reviewer=gpt-5.6 findings=3 fixed=3"
    with pytest.raises(sr.SeatRefusal, match="reviewer-mismatch"):
        sr.refuse_tally_reviewer(line, contracted_reviewer="gpt-5.6-terra")


def test_a_substituted_reviewer_reporting_review_NONE_is_the_honest_form_and_passes():
    line = "Tally: review=NONE reviewer=gpt-5.6-sol findings=0 fixed=0"
    assert sr.refuse_tally_reviewer(line, contracted_reviewer="gpt-5.6-terra").review == "NONE"


def test_a_tally_with_no_reviewer_field_is_refused():
    line = "Tally: review=lane-v-000 findings=3 fixed=3"
    with pytest.raises(sr.SeatRefusal, match="reviewer-absent"):
        sr.refuse_tally_reviewer(line, contracted_reviewer="gpt-5.6-terra")


def test_a_malformed_tally_line_is_refused_rather_than_partially_parsed():
    with pytest.raises(sr.SeatRefusal, match="tally-malformed"):
        sr.refuse_tally_reviewer("reviewed by terra, 3 findings",
                                 contracted_reviewer="gpt-5.6-terra")


def test_review_SELF_still_carries_the_seats_own_model_id():
    line = "Tally: review=SELF reviewer=claude-opus-5 findings=1 fixed=1"
    assert sr.refuse_tally_reviewer(line, contracted_reviewer="claude-opus-5").review == "SELF"
    with pytest.raises(sr.SeatRefusal, match="reviewer-absent"):
        sr.refuse_tally_reviewer("Tally: review=SELF findings=1 fixed=1",
                                 contracted_reviewer="claude-opus-5")


# --- R4 -- carried-by: on DECLARE- / AMEND- / BATCH- WRITES ------------------------------------

_CARRIED = "# DECLARE-X\ncarried-by: docs/audits/2026-09-08-technical-batch-v-manifest.md\n\nbody\n"


def test_a_decision_file_with_no_carrier_is_refused_at_write_time():
    with pytest.raises(sr.SeatRefusal, match="carried-by-absent"):
        sr.refuse_uncarried_decision_write("DECLARE-X.md", "# DECLARE-X\n\nbody\n")


def test_a_carried_decision_file_passes():
    assert sr.refuse_uncarried_decision_write("DECLARE-X.md", _CARRIED) is True


def test_an_indented_carried_by_is_refused_because_the_probe_anchors_flush_left():
    text = "# DECLARE-X\n  carried-by: docs/x.md\n\nbody\n"
    with pytest.raises(sr.SeatRefusal, match="carried-by-absent"):
        sr.refuse_uncarried_decision_write("DECLARE-X.md", text)


def test_a_carried_by_below_the_head_window_is_refused():
    text = "# DECLARE-X\n" + "\n" * 10 + "carried-by: docs/x.md\n"
    with pytest.raises(sr.SeatRefusal, match="carried-by-absent"):
        sr.refuse_uncarried_decision_write("DECLARE-X.md", text)


def test_an_empty_carrier_value_is_refused():
    with pytest.raises(sr.SeatRefusal, match="carried-by-empty"):
        sr.refuse_uncarried_decision_write("AMEND-BATCH-V-003.md", "carried-by:   \n\nbody\n")


def test_the_literal_OPEN_is_a_lawful_value():
    text = "carried-by: OPEN -- no home written yet; named in the bundle residual\n\nbody\n"
    assert sr.refuse_uncarried_decision_write("BATCH-2026-09-09-W-CONTRACTS.md", text) is True


def test_a_value_that_is_neither_OPEN_nor_a_path_is_refused():
    text = "carried-by: the manifest, probably\n\nbody\n"
    with pytest.raises(sr.SeatRefusal, match="carried-by-unresolvable"):
        sr.refuse_uncarried_decision_write("DECLARE-X.md", text)


def test_a_file_outside_the_three_prefixes_is_not_governed():
    assert sr.refuse_uncarried_decision_write("STATUS-integrator.md", "no carrier\n") is False


def test_write_decision_file_refuses_BEFORE_it_writes(tmp_path):
    """A write-time refusal that writes first and complains after has refused nothing."""
    target = tmp_path / "DECLARE-Y.md"
    with pytest.raises(sr.SeatRefusal, match="carried-by-absent"):
        sr.write_decision_file(target, "# DECLARE-Y\n\nbody\n")
    assert not target.exists()
    sr.write_decision_file(target, _CARRIED)
    assert target.read_text(encoding="utf-8") == _CARRIED


# --- R5 -- the -DryRun line is the LAST line of dispatcher step 0 (AMEND-BATCH-V-002 s1) -------

_STEP0 = (
    "## Step 0\n\n"
    "Freeze the plan, then DryRun every generated contract -- LAST LINE of step 0:\n\n"
    "```\n"
    "dispatch LANE-a.md -DryRun\n"
    "dispatch LANE-b.md -DryRun\n"
    "```\n"
)


def test_a_step0_that_dryruns_every_contract_last_passes():
    assert sr.refuse_dispatcher_step0_without_dryrun(
        _STEP0, contracts=["LANE-a.md", "LANE-b.md"]) == 2


def test_a_step0_with_no_dryrun_at_all_is_refused():
    with pytest.raises(sr.SeatRefusal, match="dryrun-absent"):
        sr.refuse_dispatcher_step0_without_dryrun(
            "## Step 0\n\nFreeze the plan.\n", contracts=["LANE-a.md"])


def test_a_dryrun_that_is_not_the_last_line_of_step0_is_refused():
    text = _STEP0 + "\nThen provision the worktrees.\n"
    with pytest.raises(sr.SeatRefusal, match="dryrun-not-last"):
        sr.refuse_dispatcher_step0_without_dryrun(text, contracts=["LANE-a.md", "LANE-b.md"])


def test_a_contract_left_out_of_the_dryrun_is_refused_and_named():
    with pytest.raises(sr.SeatRefusal, match="dryrun-incomplete") as exc:
        sr.refuse_dispatcher_step0_without_dryrun(
            _STEP0, contracts=["LANE-a.md", "LANE-b.md", "LANE-c.md"])
    assert "LANE-c.md" in str(exc.value)


def test_zero_contracts_is_refused_because_a_batch_with_no_contract_dryruns_nothing():
    with pytest.raises(sr.SeatRefusal, match="dryrun-no-contracts"):
        sr.refuse_dispatcher_step0_without_dryrun(_STEP0, contracts=[])


# --- the refusal type itself -------------------------------------------------------------------

def test_every_refusal_names_itself_and_carries_a_remedy():
    with pytest.raises(sr.SeatRefusal) as exc:
        sr.refuse_lane_ceiling([f"l{i}" for i in range(9)])
    message = str(exc.value)
    assert message.startswith("REFUSED [lane-ceiling]")
    assert "->" in message or "--" in message


def test_the_refusal_registry_lists_all_five():
    assert sr.REFUSALS == (
        "sleeping-poll", "lane-ceiling", "reviewer-mismatch", "carried-by", "dryrun-step0",
    )


def test_every_seat_runs_at_least_one_refusal_and_names_only_real_ones():
    assert set(sr.SEAT_REFUSALS) == set(seat_ch8.SEATS)
    for seat, names in sr.SEAT_REFUSALS.items():
        assert names, f"seat {seat!r} runs no refusal"
        assert set(names) <= set(sr.REFUSALS), f"seat {seat!r} names an unknown refusal"


def test_every_refusal_has_at_least_one_seat_that_runs_it():
    """A refusal nobody runs is a module nobody imports wearing an enforcement label."""
    run = {name for names in sr.SEAT_REFUSALS.values() for name in names}
    assert set(sr.REFUSALS) - run == set()


# --- the CLI: the refusals are RUNNABLE, which is what a seat template can carry ---------------

def _run(*args: str):
    return CliRunner().invoke(sr.cli, list(args))


def test_cli_lists_the_roster():
    result = _run("list")
    assert result.exit_code == 0
    assert result.output.split() == list(sr.REFUSALS)


def test_cli_exits_1_on_a_refusal_and_0_on_a_pass():
    over = [arg for lane in range(9) for arg in ("--lane", f"l{lane}")]
    refused = _run("lane-ceiling", *over)
    assert refused.exit_code == 1
    assert "REFUSED [lane-ceiling]" in refused.output

    ok = _run("lane-ceiling", "--lane", "a", "--lane", "b")
    assert ok.exit_code == 0 and "PASS" in ok.output


def test_cli_late_check_is_refused_through_the_provisioned_flag():
    result = _run("lane-ceiling", "--lane", "a", "--provisioned", ".claude/worktrees/a")
    assert result.exit_code == 1 and "checked LATE" in result.output


def test_cli_carried_by_reads_files(tmp_path):
    good = tmp_path / "DECLARE-Ok.md"
    good.write_text(_CARRIED, encoding="utf-8")
    bad = tmp_path / "AMEND-Bad.md"
    bad.write_text("# AMEND-Bad\n\nbody\n", encoding="utf-8")
    assert _run("carried-by", str(good)).exit_code == 0
    assert _run("carried-by", str(bad)).exit_code == 1


def test_cli_reviewer_reads_the_tally_out_of_an_artifact(tmp_path):
    art = tmp_path / "REVIEW.md"
    art.write_text(f"# review\n\n{_TALLY}\n", encoding="utf-8")
    assert _run("reviewer", "--contracted", "gpt-5.6-terra", str(art)).exit_code == 0
    assert _run("reviewer", "--contracted", "gpt-5.6-sol", str(art)).exit_code == 1


def test_cli_sleeping_poll_and_dryrun_read_files(tmp_path):
    waiting = tmp_path / "boot.md"
    waiting.write_text("Wait for the integrator, then continue.\n", encoding="utf-8")
    assert _run("sleeping-poll", str(waiting)).exit_code == 1

    step0 = tmp_path / "step0.md"
    step0.write_text(_STEP0, encoding="utf-8")
    assert _run("dryrun-step0", "--step0", str(step0),
                "--contract", "LANE-a.md", "--contract", "LANE-b.md").exit_code == 0
    assert _run("dryrun-step0", "--step0", str(step0), "--contract", "LANE-z.md").exit_code == 1
