"""Per-step merge minutes, RED-first (`[#675]` target 3.1, with 3.3 and 3.6's reporting rule).

THE TARGET, verbatim from `[#675]`'s Done-when as the lane contract freezes it:

    (1) per-step minutes recorded into the receipt, so the merge stops being one opaque wall
    number and becomes an itemised one — the only way the ~90/~63 disagreement ever resolves

and, binding how target 3.6 may ever be reported:

    The parenthesis is part of the baseline and not commentary — the two itemised views
    disagree with each other and with the wall figure, and no measurement was taken on the day
    it was frozen — so every report against it NAMES THE SPREAD rather than hiding it.

WHAT THIS MODULE TESTS AND WHAT IT DOES NOT. It tests that the receipt cannot be made to LIE —
that it cannot report a bare median, cannot swallow a failing step, cannot silently omit a step
it was asked about, and cannot turn a parallel run into a fake saving. It does NOT test that any
particular merge is fast; that is target 3.6's measurement, taken in step 7 against real
receipts, not asserted here.

THE STRONGEST TESTS HERE ARE THE ONES THAT WOULD CATCH A CONVENIENT BUG. `[#675]` is the row
about a mechanism that returns a plausible answer because the discriminating field is absent
from what it looks at, and a stopwatch is a rich source of exactly that failure: an unrecorded
step reads as a fast one, a swallowed non-zero exit reads as a passing merge, and a median over
one receipt reads like a median. Each has a test whose name says which lie it refuses.
"""
from __future__ import annotations

import json
import sys

import pytest

import merge_receipt as mr


# --- helpers ----------------------------------------------------------------

def _echo(text: str = "ok") -> list[str]:
    """A trivially fast child command, spelled portably (this repo runs on Windows)."""
    return [sys.executable, "-c", f"print({text!r})"]


def _fail() -> list[str]:
    return [sys.executable, "-c", "import sys; sys.exit(3)"]


def _receipt_with(tmp_path, steps) -> mr.Receipt:
    """Build a closed-shape receipt directly, so arithmetic tests do not pay for subprocesses."""
    receipt = mr.Receipt(slug="r", batch="x", opened="2026-09-12T00:00:00+00:00",
                         host="test", concurrent_seats=0)
    receipt.steps.extend(steps)
    return receipt


def _step(name, seconds, *, step_class=mr.CLASS_CEREMONY, ok=True, raced_with=()) -> mr.StepTiming:
    return mr.StepTiming(step=name, step_class=step_class, seconds=seconds, ok=ok,
                         returncode=0 if ok else 1, command="-", started="-",
                         raced_with=tuple(raced_with))


# --- THE TARGET: per-step minutes, itemised ---------------------------------

def test_the_receipt_itemises_per_step_minutes_rather_than_one_wall_number(tmp_path):
    """Target 3.1 itself. The merge stops being one opaque number.

    The assertion is over the RENDERED summary rather than the internal list on purpose: the
    row's complaint is that a number nobody can attribute is useless, and attribution happens
    where a reader looks.
    """
    mr.open_receipt(tmp_path, slug="m", batch="x")
    receipt = mr.load_receipt(tmp_path, "m")
    receipt.steps.append(_step("suite", 120.0, step_class=mr.CLASS_TESTS))
    receipt.steps.append(_step("merge", 60.0))
    mr.save_receipt(tmp_path, receipt)

    rendered = mr.render_summary(mr.load_receipt(tmp_path, "m"))

    assert "2.00 min" in rendered and "suite" in rendered
    assert "1.00 min" in rendered and "merge" in rendered


def test_an_UNRECORDED_required_step_is_named_rather_than_read_as_a_fast_one(tmp_path):
    """The receipt's own blind spot, declared by the receipt.

    This is `[#675]`'s exact failure class one layer up: a step nobody timed contributes zero
    minutes, which is indistinguishable from a step that took no time. The discriminating field
    — "was this step even asked about?" — is absent from a plain sum, so the receipt carries it
    separately and the summary says so.
    """
    receipt = _receipt_with(tmp_path, [_step("merge", 10.0)])

    missing = receipt.missing_required()
    rendered = mr.render_summary(receipt)

    assert "suite" in missing, "a required step nobody recorded must be NAMED"
    assert "UNRECORDED" in rendered and "UNDERSTATES" in rendered


def test_the_three_way_split_folds_back_into_the_BASELINES_OWN_two_buckets(tmp_path):
    """Commensurability with `84 = 11.3 + 72.7`, asserted rather than assumed.

    Review is split out of ceremony because target 3.5 forbids trading it away and a binary
    split cannot show that it was not. That extra bucket is only safe if it folds back exactly.
    """
    receipt = _receipt_with(tmp_path, [
        _step("suite", 60.0, step_class=mr.CLASS_TESTS),
        _step("review", 120.0, step_class=mr.CLASS_REVIEW),
        _step("merge", 60.0, step_class=mr.CLASS_CEREMONY),
    ])

    tests_min, residual_min = receipt.baseline_split()

    assert (tests_min, residual_min) == (1.0, 3.0)
    assert pytest.approx(sum(receipt.by_class().values())) == receipt.serial_seconds()


def test_the_baseline_is_TRANSCRIBED_including_the_disagreement_inside_it():
    """Clause 2's numbers, frozen. Transcribed, not recomputed — including the parenthesis.

    `measured_on_freeze_day is False` is the parenthesis's second half made machine-readable.
    A constant that dropped it would let a later reader treat 84 as a measurement.
    """
    assert (mr.BASELINE_WALL_MIN, mr.BASELINE_TESTS_MIN, mr.BASELINE_CEREMONY_MIN) == (
        84.0, 11.3, 72.7)
    assert mr.BASELINE_ITEMISED_VIEWS_MIN == (90.0, 63.0)
    assert mr.BASELINE_MEASURED_ON_FREEZE_DAY is False
    assert mr.TARGET_MEDIAN_MIN == 30.0


# --- THE REPORTING RULE: never a bare median --------------------------------

def test_the_median_NEVER_reports_a_number_without_its_spread():
    """The contract's own prohibition, made structural: "Do not report a median without its
    spread."

    Asserted over the RENDERED text because the prohibition is about what a reader receives.
    A `median_minutes` float exists on the report — it has to, for `--strict` — so the guarantee
    has to live at the surface that prints.
    """
    receipts = [_receipt_with(None, [_step("merge", s)]) for s in (600.0, 1200.0, 1800.0)]

    rendered = mr.median_report(receipts).render()

    assert "median" in rendered
    assert "range" in rendered, "a median with no range is the bare number the row forbids"
    assert "per merge" in rendered, "the individual merges are the spread's evidence"
    assert "n=3" in rendered


def test_the_median_carries_the_BASELINES_OWN_spread_and_that_nothing_was_measured():
    """An improvement stated against a disputed baseline inherits the dispute.

    The baseline's two itemised views (~90 and ~63) disagree with each other and with the 84
    wall figure, and nothing was measured on the day it was frozen. A report that printed only
    "84 -> 27" would be the row's own failure class: a confident number with the disagreement
    hidden inside it.
    """
    rendered = mr.median_report([_receipt_with(None, [_step("merge", 600.0)])]).render()

    assert "90" in rendered and "63" in rendered, "both itemised views travel with the median"
    assert "NOTHING WAS MEASURED" in rendered
    assert "SMALL SAMPLE" in rendered, "n=1 must say so rather than read as an estimate"


def test_a_NON_MERGE_arc_cannot_flatter_the_MERGE_median_and_its_exclusion_is_NAMED():
    """`[#675]`'s own failure class, caught inside the tool built to answer `[#675]`.

    A lane's commit arc shares most of a merge's ceremony and pays neither the merge nor the
    teardown, so mixing the two kinds under one median answers a cheaper question under target
    3.6's name — and answers it flatteringly. The discriminating field is `kind`; without it the
    read succeeds over the wrong half of the ledger and returns a plausible value, which is the
    exact shape the row is filed about. The exclusion is REPORTED, because a filter nobody can
    see is the same defect one layer on.
    """
    merge = _receipt_with(None, [_step("merge", 2400.0)])
    arc = _receipt_with(None, [_step("commit", 60.0)])
    arc.kind = mr.KIND_ARC

    report = mr.median_report([merge, arc])

    assert report.n == 1 and report.median_minutes == 40.0, "the cheap arc is not counted"
    assert report.excluded == 1
    assert "EXCLUDED" in report.render()
    assert mr.median_report([merge, arc], kind=mr.KIND_ARC).median_minutes == 1.0


def test_a_ledger_row_written_BEFORE_kind_existed_reads_as_a_MERGE():
    """The default reads the history correctly rather than conveniently: every row the ledger
    held when the field was absent was a merge receipt."""
    assert mr.Receipt.from_dict({"slug": "s", "opened": "t"}).kind == mr.KIND_MERGE


def test_an_EMPTY_ledger_reports_UNDEFINED_rather_than_zero_minutes():
    """Zero is the most dangerous plausible value available to this module.

    An empty ledger with a `0.0` median meets target 3.6 spectacularly and means nothing. Same
    shape as the defaulting read `[#675]` is filed about: not an error, not a miss, a plausible
    value.
    """
    report = mr.median_report([])

    assert report.n == 0
    assert "NO RECEIPTS" in report.render()
    assert "undefined, not zero" in report.render()


# --- TARGET 3.3: parallel is a SCHEDULING change, never a coverage one ------

def test_a_RACED_group_counts_ONCE_in_wall_time_and_IN_FULL_in_the_class_split():
    """Target 3.3's arithmetic, and the reason it is two numbers rather than one.

    Summing raced steps into wall time would report a parallel run at its serial cost and erase
    the saving. Counting them once in the CLASS split would understate how much review or test
    work was actually done — and target 3.5 makes "how much review happened" the one quantity
    nobody may quietly shrink. So wall groups, class does not.
    """
    receipt = _receipt_with(None, [
        _step("suite", 300.0, step_class=mr.CLASS_TESTS, raced_with=("review",)),
        _step("review", 180.0, step_class=mr.CLASS_REVIEW, raced_with=("suite",)),
        _step("merge", 60.0),
    ])

    assert receipt.wall_seconds() == 360.0, "the raced pair costs its LONGEST member, once"
    assert receipt.serial_seconds() == 540.0, "the counterfactual stays available"
    assert receipt.by_class()[mr.CLASS_REVIEW] == 180.0, "review work is not discounted"


def test_racing_records_EVERY_jobs_verdict_and_FAILS_when_any_job_failed(tmp_path):
    """The guarantee that keeps target 3.3 from becoming a coverage cut.

    Running two checks concurrently is a scheduling change. Reporting only the winner, or
    exiting 0 because the fast one passed, would be a coverage change wearing one — exactly the
    "median reached by cutting review" that target 3.5 calls a false pass.
    """
    from click.testing import CliRunner

    mr.open_receipt(tmp_path, slug="m", batch="x")
    result = CliRunner().invoke(mr.cli, [
        "--repo-root", str(tmp_path), "race", "--slug", "m",
        "--job", f"good:tests={sys.executable} -c \"pass\"",
        "--job", f"bad:review={sys.executable} -c \"import sys; sys.exit(3)\"",
    ])

    receipt = mr.load_receipt(tmp_path, "m")
    recorded = {s.step: s for s in receipt.steps}
    assert set(recorded) == {"good", "bad"}, "a raced job's verdict is never dropped"
    assert recorded["bad"].ok is False and recorded["bad"].returncode == 3
    assert result.exit_code != 0, "one failing job fails the race"


def test_a_raced_job_KNOWS_what_it_ran_against(tmp_path):
    """`raced_with` is what makes the wall-time grouping honest rather than a guess."""
    from click.testing import CliRunner

    mr.open_receipt(tmp_path, slug="m", batch="x")
    CliRunner().invoke(mr.cli, [
        "--repo-root", str(tmp_path), "race", "--slug", "m",
        "--job", f"a:tests={sys.executable} -c \"pass\"",
        "--job", f"b:review={sys.executable} -c \"pass\"",
    ])

    recorded = {s.step: s.raced_with for s in mr.load_receipt(tmp_path, "m").steps}

    assert recorded == {"a": ("b",), "b": ("a",)}


# --- TARGET 3.5: the saving may never come from removing a step -------------

def test_the_module_offers_NO_WAY_to_mark_a_step_skipped():
    """Target 3.5, enforced by absence and asserted so the absence stays deliberate.

    "The saving comes from removing assembly, never from removing the judgement step, and a
    median reached by cutting either is a false pass on this row." A `--skip` flag, or a step
    class meaning "not run", would make that false pass one flag away. This test is what makes
    adding one a visible act rather than a convenience.
    """
    from click.testing import CliRunner

    help_text = CliRunner().invoke(mr.cli, ["time", "--help"]).output

    assert "--skip" not in help_text
    assert "skip" not in {c.lower() for c in mr.STEP_CLASSES}


def test_a_failing_step_passes_the_childs_exit_code_through_rather_than_swallowing_it(tmp_path):
    """A stopwatch that made a failing merge step look successful would be worse than no
    stopwatch: it would convert a gate into a gate that lets things through."""
    from click.testing import CliRunner

    mr.open_receipt(tmp_path, slug="m", batch="x")
    result = CliRunner().invoke(mr.cli, [
        "--repo-root", str(tmp_path), "time", "--slug", "m", "--step", "suite",
        "--class", "tests", "--", *_fail(),
    ])

    step = mr.load_receipt(tmp_path, "m").steps[-1]
    assert step.ok is False and step.returncode == 3
    assert result.exit_code == 3, "the CHILD's code, not a wrapper's"


def test_a_step_whose_command_could_not_be_RUN_is_recorded_as_failed_not_as_fast(tmp_path):
    """An OSError is the same lie as an unrecorded step, arriving by a different door."""
    timing = mr.run_timed(["a-command-that-does-not-exist-anywhere"], step="x",
                          step_class=mr.CLASS_CEREMONY)

    assert timing.ok is False and timing.returncode is None


# --- the ledger -------------------------------------------------------------

def test_closing_APPENDS_to_the_ledger_and_never_rewrites_an_earlier_line(tmp_path):
    """ADR-29/ADR-39's append-only posture, in the `logs/TOKEN-LOG.md` class.

    A median over "a real run of merges" needs receipts that survive, so this file is committed
    and never rewritten in place.
    """
    for slug in ("first", "second"):
        mr.open_receipt(tmp_path, slug=slug, batch="x")
        receipt = mr.load_receipt(tmp_path, slug)
        receipt.steps.append(_step("merge", 30.0))
        mr.save_receipt(tmp_path, receipt)
        mr.close_receipt(tmp_path, slug)

    lines = (tmp_path / mr.LEDGER_RELPATH).read_text(encoding="utf-8").strip().splitlines()

    assert len(lines) == 2
    assert json.loads(lines[0])["slug"] == "first", "the earlier line is untouched"
    assert [r.slug for r in mr.read_ledger(tmp_path)] == ["first", "second"]


def test_closing_REMOVES_the_scratch_so_a_receipt_is_counted_exactly_once(tmp_path):
    mr.open_receipt(tmp_path, slug="m", batch="x")
    mr.close_receipt(tmp_path, "m")

    assert not mr.scratch_path(tmp_path, "m").exists()
    assert len(mr.read_ledger(tmp_path)) == 1


def test_opening_over_an_IN_FLIGHT_receipt_is_REFUSED(tmp_path):
    """An abandoned scratch file is the record of a merge that died half-way.

    Overwriting it silently would destroy the only evidence that a merge was abandoned — and an
    abandoned merge is precisely the kind of cost this lane exists to make visible.
    """
    mr.open_receipt(tmp_path, slug="m", batch="x")

    with pytest.raises(mr.MergeReceiptError, match="already open"):
        mr.open_receipt(tmp_path, slug="m", batch="x")


def test_timing_against_NO_open_receipt_REFUSES_rather_than_starting_one(tmp_path):
    """A step timed against a receipt nobody opened is a measurement nothing keeps, and a
    module that helpfully created one would hide the operator's missing `open`."""
    with pytest.raises(mr.MergeReceiptError, match="no open receipt"):
        mr.load_receipt(tmp_path, "never-opened")


def test_ONE_unreadable_ledger_line_does_not_make_every_good_one_unreadable(tmp_path, caplog):
    """The ledger is append-only, so a malformed line cannot be repaired in place.

    Refusing the whole file would make one bad append permanently destroy the history the
    median is computed over.
    """
    mr.open_receipt(tmp_path, slug="m", batch="x")
    mr.close_receipt(tmp_path, "m")
    with (tmp_path / mr.LEDGER_RELPATH).open("a", encoding="utf-8") as handle:
        handle.write("{not json\n")

    receipts = mr.read_ledger(tmp_path)

    assert len(receipts) == 1
    assert "unreadable" in caplog.text.lower()


def test_the_receipt_records_HOW_MANY_SEATS_were_in_flight_beside_it(tmp_path):
    """Wall time here is shared-machine time, and the receipt says so.

    Three lanes committing at once stretch every duration in this file. A number recorded
    without that context invites comparing a quiet merge with a busy one as though the
    difference were the process — the honest limit, carried in the data rather than only in
    prose.
    """
    receipt = mr.open_receipt(tmp_path, slug="m", batch="x")

    assert isinstance(receipt.concurrent_seats, int)
    assert "concurrent_seats" in json.loads(
        mr.scratch_path(tmp_path, "m").read_text(encoding="utf-8"))
