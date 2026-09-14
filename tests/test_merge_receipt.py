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
from datetime import datetime, timedelta, timezone

import pytest

import actions_verdict as av
import merge_receipt as mr


# --- helpers ----------------------------------------------------------------

_OPENED = datetime(2026, 9, 12, 0, 0, 0, tzinfo=timezone.utc)


def _stamp(offset_seconds: float = 0.0) -> str:
    """An ISO timestamp `offset_seconds` after `_OPENED`, spelled the way `_now()` spells it.

    REAL TIMESTAMPS RATHER THAN `"t"` / `"t2"` PLACEHOLDERS, and the change is not cosmetic.
    Since `[#750]` the receipt's wall time is the span `opened -> closed`, so a fixture whose
    timestamps do not parse is a receipt whose duration cannot be read -- which the predicate
    now (correctly) calls incomplete. The placeholders were only ever safe while nothing read
    the fields.
    """
    return (_OPENED + timedelta(seconds=offset_seconds)).isoformat(timespec="milliseconds")


def _echo(text: str = "ok") -> list[str]:
    """A trivially fast child command, spelled portably (this repo runs on Windows)."""
    return [sys.executable, "-c", f"print({text!r})"]


def _fail() -> list[str]:
    return [sys.executable, "-c", "import sys; sys.exit(3)"]


def _receipt_with(tmp_path, steps, *, unrecorded_seconds: float = 0.0) -> mr.Receipt:
    """Build a receipt directly, so arithmetic tests do not pay for subprocesses.

    NOT A COMPLETE RECEIPT -- no suite verdict is recorded and the required steps are whatever
    the caller passes. The docstring here once said "closed-shape", which was never true and is
    what let the median tests below run on receipts that `[#744]`'s predicate correctly refuses.
    Arithmetic tests (`recorded_seconds`, `by_class`, the raced-group rules) still use this;
    tests that feed `median_report` use `_complete_merge` instead.

    `closed` IS SET, AND IT IS SET FROM THE STEPS: the span is `recorded_seconds` plus whatever
    `unrecorded_seconds` the caller wants left untimed. That keeps the class-split assertions
    below meaning what they meant before `[#750]` -- an arc with nothing untimed -- while making
    the untimed remainder a thing a test can ASK for rather than an accident of the fixture.
    """
    receipt = mr.Receipt(slug="r", batch="x", opened=_stamp(), host="test", concurrent_seats=0)
    receipt.steps.extend(steps)
    receipt.closed = _stamp(receipt.recorded_seconds() + unrecorded_seconds)
    return receipt


def _step(name, seconds, *, step_class=mr.CLASS_CEREMONY, ok=True, raced_with=(),
          verdict_state=None) -> mr.StepTiming:
    return mr.StepTiming(step=name, step_class=step_class, seconds=seconds, ok=ok,
                         returncode=0 if ok else 1, command="-", started="-",
                         raced_with=tuple(raced_with), verdict_state=verdict_state)


def _set_verdict(receipt: mr.Receipt, state) -> None:
    """Re-record the suite verdict on an existing receipt, dropping the step's own exit code
    from the picture -- which is the whole of ruling AY1-1's change and so is what a test
    varying completeness must vary."""
    receipt.steps = [s for s in receipt.steps if s.verdict_state is None]
    receipt.steps.append(_step("actions", 0.0, step_class=mr.CLASS_TESTS, verdict_state=state))


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
    receipts = [_complete_merge(m, f"r{m}") for m in (10.0, 20.0, 30.0)]

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
    rendered = mr.median_report([_complete_merge(10.0)]).render()

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
    merge = _complete_merge(40.0)
    arc = mr.Receipt(slug="a", batch="x", opened=_stamp(), host="h", concurrent_seats=0,
                     closed=_stamp(60.0), kind=mr.KIND_ARC)
    arc.steps.append(_step("commit", 60.0))

    report = mr.median_report([merge, arc])

    assert report.n == 1 and report.median_minutes == 40.0, "the cheap arc is not counted"
    assert report.excluded == 1
    assert "EXCLUDED" in report.render()
    assert mr.median_report([merge, arc], kind=mr.KIND_ARC).median_minutes == 1.0


# --- `[#744]`: A MEDIAN OVER INCOMPLETE RECEIPTS IS NOT A MEDIAN -----------
#
# RED-FIRST WITNESS (ADR-108 SB). At `dbac84b8` `median_report` filtered by `kind` and by
# nothing else. It never read `closed`, never read `failed_steps()`, never read
# `missing_required()` -- so a receipt that was opened and abandoned, or whose suite step
# exited non-zero, or that recorded one step out of four, counted at full weight in a median
# reported as "median merge minutes".
#
# AND IT WAS FULLY REALISED IN THE LIVE LEDGER, not hypothetical. `logs/MERGE-RECEIPTS.jsonl`
# held exactly two rows on 2026-09-13 and BOTH had failed steps, one of them recording a single
# failed step and 0.0 minutes of wall time. Over that data the tool printed:
#
#     arc minutes over n=2 closed receipt(s)
#       median   9.4 min   (target 3.6: under 30 -> MET)
#       per merge 0.0, 18.7
#
# "n=2 closed receipt(s)" was false -- nothing had checked `closed` -- and "target 3.6: MET"
# was a pass built from a receipt that measured nothing. That is `[#675]`'s filed failure class
# word for word: a plausible, flattering value returned because the discriminating field is
# absent from what the reader looks at.


def _complete_merge(minutes: float, slug: str = "m", *,
                    verdict: str | None = av.STATE_PASS) -> mr.Receipt:
    """A receipt complete on every leg of the predicate: closed, wall time readable, every
    required step recorded, no non-suite step failed, and a READABLE suite verdict state.

    `closed` IS DERIVED FROM `minutes`, which it was not before `[#750]`. The helper used to
    pin `closed` at one hour while varying a step's seconds, and that was harmless only while
    `wall_seconds()` summed steps: the moment the receipt's duration became the span
    `opened -> closed`, a fixed `closed` would have made every median test below a test of the
    same sixty minutes, whatever number it asked for.

    `verdict` DEFAULTS TO `PASS` AND IS A PARAMETER, because ruling AY1-1 makes the suite
    step's recorded STATE a leg of completeness -- so "a complete merge receipt" is no longer
    expressible without one, and the states that are NOT complete need the same builder.
    """
    receipt = mr.Receipt(slug=slug, batch="x", opened=_stamp(), host="test", concurrent_seats=0,
                         closed=_stamp(minutes * 60.0))
    receipt.steps.extend(
        _step(name, minutes * 60.0 if name == "merge" else 0.0)
        for name in mr.REQUIRED_STEPS)
    receipt.steps.append(_step("actions", 0.0, step_class=mr.CLASS_TESTS,
                               verdict_state=verdict))
    return receipt


def test_an_INCOMPLETE_receipt_is_EXCLUDED_from_the_median():
    """`[#744]`'s Done-when, built exactly as it specifies: complete receipts ABOVE the target
    plus incomplete ones BELOW it.

    RED at `dbac84b8`: the cheap incomplete rows dragged the median to 1.0 and the report said
    `target 3.6: MET`. The complete sample never met it.
    """
    complete = [_complete_merge(m, f"ok{m}") for m in (40.0, 45.0, 50.0)]

    never_closed = _complete_merge(1.0, "unclosed")
    never_closed.closed = None

    a_step_failed = _complete_merge(1.0, "failed")
    a_step_failed.steps.append(_step("suite", 0.0, ok=False))

    missing_steps = mr.Receipt(slug="partial", batch="x", opened=_stamp(), host="h",
                               concurrent_seats=0, closed=_stamp(60.0))
    missing_steps.steps.append(_step("merge", 60.0))

    no_steps_at_all = mr.Receipt(slug="empty", batch="x", opened=_stamp(), host="h",
                                 concurrent_seats=0, closed=_stamp(60.0))

    report = mr.median_report([*complete, never_closed, a_step_failed,
                               missing_steps, no_steps_at_all])

    assert report.n == 3, "only the complete receipts are counted"
    assert report.median_minutes == 45.0
    assert report.meets_target() is False, \
        "the incomplete rows made a NOT-MET sample read as MET -- the whole row"
    assert report.per_merge == (40.0, 45.0, 50.0)


@pytest.mark.parametrize("break_it,reason_fragment", [
    (lambda r: setattr(r, "closed", None), "closed"),
    (lambda r: r.steps.append(_step("teardown-retry", 0.0, ok=False)), "failed"),
    (lambda r: r.steps.clear(), "step"),
    # `[#750]` / AY1-1's two legs, asserted in the same list as the three that preceded them so
    # a later simplification that drops one is caught by name here rather than nowhere.
    (lambda r: _set_verdict(r, av.STATE_REGRESSED), "regressed"),
    (lambda r: _set_verdict(r, None), "verdict"),
    (lambda r: setattr(r, "closed", "not-a-timestamp"), "wall"),
])
def test_each_leg_of_the_completeness_predicate_EXCLUDES_on_its_own(break_it, reason_fragment):
    """One explicit predicate in code, not left to the reader -- the row's own words. Each leg
    is asserted alone so a later simplification that drops one is caught by name."""
    receipt = _complete_merge(40.0)
    break_it(receipt)

    assert receipt.is_complete() is False
    assert reason_fragment in receipt.incompleteness_reason().lower()
    assert mr.median_report([receipt]).n == 0


def test_a_MERGE_receipt_missing_a_REQUIRED_step_is_incomplete():
    """"Every declared step present" -- REQUIRED_STEPS is what a merge declares it will record,
    from `/lane-integrate`'s own walk. A merge receipt with no `suite` step did not record
    whether the suite ran, and an unrecorded step reads exactly like a fast one."""
    receipt = _complete_merge(40.0)
    receipt.steps = [s for s in receipt.steps if s.step != "suite"]

    assert receipt.is_complete() is False
    assert "suite" in receipt.incompleteness_reason()


def test_an_ARC_receipt_is_NOT_held_to_the_MERGE_walks_required_steps():
    """The required-steps leg is scoped to `kind == merge`, and that is a decision rather than
    an oversight. REQUIRED_STEPS is the INTEGRATOR's walk -- handback, merge, suite, teardown --
    and this module's own docstring says an arc "pays no merge and no teardown". Holding an arc
    to it would make `median --kind arc` permanently n=0 for a reason that is not incompleteness.
    The other legs -- closed, has steps, readable wall time, none failed -- still bind an arc.

    SO DOES THE SUITE-VERDICT LEG'S SCOPING, added by `[#750]`/AY1-1 for the identical reason
    and recorded here rather than in a second test: an arc reads no Actions run for a merge SHA
    (there is no merge), so requiring a verdict state of one would make `median --kind arc`
    permanently n=0 -- the same "n=0 for a reason that is not incompleteness" this test already
    exists to refuse. An arc therefore keeps the EXIT-CODE reading on a `tests` step, which is
    what the second half below asserts.
    """
    arc = mr.Receipt(slug="a", batch="x", opened=_stamp(), host="h", concurrent_seats=0,
                     closed=_stamp(600.0), kind=mr.KIND_ARC)
    arc.steps.append(_step("targeted", 600.0, step_class=mr.CLASS_TESTS))

    assert arc.is_complete() is True, "an arc is not held to a merge's walk OR to its verdict"
    assert mr.median_report([arc], kind=mr.KIND_ARC).n == 1

    arc.steps.append(_step("targeted-retry", 60.0, step_class=mr.CLASS_TESTS, ok=False))
    assert arc.is_complete() is False


def test_the_completeness_exclusion_is_REPORTED_the_way_the_kind_filter_already_is():
    """A filter nobody can see is the same defect one layer on -- this module's own rule, which
    is why `excluded` exists for `kind`. A median over a thinned sample must never render as a
    median over a full one."""
    incomplete = _complete_merge(1.0, "bad")
    incomplete.closed = None
    report = mr.median_report([_complete_merge(40.0), incomplete])

    assert report.incomplete == 1
    rendered = report.render()
    assert "INCOMPLETE" in rendered
    assert "1" in rendered


def test_an_ALL_INCOMPLETE_ledger_reports_UNDEFINED_and_says_WHY():
    """The live ledger's own shape on 2026-09-13: every row present, none of them usable. The
    honest answer is "no complete receipt", never "0.0 minutes, target MET"."""
    incomplete = _complete_merge(1.0)
    incomplete.closed = None

    report = mr.median_report([incomplete])

    assert report.n == 0
    assert report.incomplete == 1
    rendered = report.render()
    assert "NO RECEIPTS" in rendered or "no complete" in rendered.lower()
    assert "INCOMPLETE" in rendered


def test_median_STRICT_is_the_TARGET_axis_and_NOT_the_completeness_axis(tmp_path):
    """`[#744]`'s last clause: `--strict` "either enforces completeness or is documented as not
    being the completeness axis, with a test pinning whichever is chosen".

    CHOSEN: it is NOT the completeness axis, and completeness is enforced UNCONDITIONALLY.
    `--strict` already means "exit 1 when the median does not meet target 3.6", and a flag that
    also toggled completeness would make the false pass this row closes OPT-OUTABLE -- a median
    over incomplete receipts is not a laxer reading of the number, it is a different number. So
    the filtering happens with or without the flag, and `--strict` keeps the one meaning it had.
    """
    from click.testing import CliRunner

    ledger = tmp_path / mr.LEDGER_RELPATH
    ledger.parent.mkdir(parents=True, exist_ok=True)
    incomplete = _complete_merge(1.0, "bad")
    incomplete.closed = None
    rows = [_complete_merge(40.0, "ok"), incomplete]
    ledger.write_text("".join(json.dumps(r.to_dict()) + "\n" for r in rows), encoding="utf-8")

    runner = CliRunner()
    lax = runner.invoke(mr.cli, ["--repo-root", str(tmp_path), "median"])
    strict = runner.invoke(mr.cli, ["--repo-root", str(tmp_path), "median", "--strict"])

    # Completeness filtering is identical in both -- n=1, the 40-minute complete receipt.
    assert "n=1" in lax.output and "n=1" in strict.output
    assert "INCOMPLETE" in lax.output, "the exclusion is reported without --strict too"

    # --strict changes only the EXIT CODE, and only on the target axis (40 min > 30 min target).
    assert lax.exit_code == 0
    assert strict.exit_code == 1


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

    Summing raced steps into the RECORDED total would report a parallel run at its serial cost
    and erase the saving. Counting them once in the CLASS split would understate how much review
    or test work was actually done — and target 3.5 makes "how much review happened" the one
    quantity nobody may quietly shrink. So the recorded total groups, class does not.

    THE ASSERTION MOVED FROM `wall_seconds` TO `recorded_seconds` AT `[#750]`, and the move is
    the point rather than a rename. This arithmetic is about COVERAGE — how much of the arc was
    timed, counting a raced group once — and `[#750]` proved that reading it as the arc's
    DURATION understated a 3h01m span as 1.776 s. Wall time is now the span and has its own
    witness below; the raced-group rule keeps its own number and its own test.
    """
    receipt = _receipt_with(None, [
        _step("suite", 300.0, step_class=mr.CLASS_TESTS, raced_with=("review",)),
        _step("review", 180.0, step_class=mr.CLASS_REVIEW, raced_with=("suite",)),
        _step("merge", 60.0),
    ])

    assert receipt.recorded_seconds() == 360.0, "the raced pair costs its LONGEST member, once"
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


# --- `[#750]` / RULING AY1-1: THE MERGE RECEIPT BECOMES A REFUSAL -----------
#
# RED-FIRST WITNESSES (ADR-108 §B). Three facts were true of this module at `8a41c650`, and all
# three are recorded in the live ledger rather than reasoned about:
#
#   1. `wall_seconds()` SUMMED THE TIMED CHILDREN. Ledger row `lane-x-675-step-7` was opened at
#      19:13:21 and closed at 22:14:41 -- a span of 3h01m20s -- and recorded
#      `"wall_seconds": 1.776`, because the single child it timed ran for 1.776 s. The 72.7
#      minutes of "residual ceremony" the baseline is stated in live in exactly the gaps that
#      arithmetic could not see, so the receipt understated a three-hour arc by three orders of
#      magnitude while printing the number as the arc's wall time.
#
#   2. COMPLETENESS READ A FLATTENED `ok` BOOLEAN. `incompleteness_reason()` leg 3 refused any
#      receipt with a failed step; the suite step's `ok` comes from a verdict whose own
#      docstring says "ONLY `PASS` is ok. Every other state is non-zero, including
#      PRE-EXISTING". `main`'s Actions pytest was pre-existing red, so EVERY receipt was
#      incomplete however clean the merge, the merge median was permanently UNDEFINED, and a
#      rule worded "a merge that lands without a COMPLETE receipt is refused" would have
#      refused every merge in this repo the moment it shipped.
#
#   3. NOTHING REFUSED A MERGE THAT LANDED WITH NO RECEIPT AT ALL. The receipt was opened once
#      per BATCH, named no merge commit, and `/lane-integrate`'s own honest limit said so: "it
#      times what it is asked to time".
#
# Ruling AY1-1 (`to-cc/AMEND-BATCH-Y-ROSTER-001.md`, carried in the batch Y manifest) settles
# (2): completeness is judged on the suite step's VERDICT STATE, not its exit code. `PASS` or
# `PRE-EXISTING` -> COMPLETE with the state recorded by name; `REGRESSED`, or a verdict that
# cannot be read -> INCOMPLETE and the merge is refused. Forcing the step to exit 0 is ruled
# out BY NAME as `[#744]`'s false pass, and there is no flag here that can do it.


def _run(sha: str, *jobs: tuple[str, str], status: str = "completed") -> dict:
    """A `gh run list` row as `fetch_run` returns it, so the tests below drive the REAL state
    machine rather than asserting a state they typed themselves."""
    return {"databaseId": 1, "headSha": sha, "status": status, "conclusion": "failure",
            "displayTitle": f"run for {sha}",
            "jobs": [{"name": name, "conclusion": conclusion} for name, conclusion in jobs]}


def _fetcher(**by_sha):
    def fetch(sha, **_kwargs):
        return by_sha.get(sha)
    return fetch


# --- (1) wall time is the SPAN ----------------------------------------------

def test_WALL_TIME_is_the_ARCS_SPAN_and_not_the_sum_of_its_timed_children():
    """Ledger row `lane-x-675-step-7`, transcribed: 3h01m20s of arc, 1.776 s of child.

    The old arithmetic answered "how many seconds did the processes I wrapped run for", which
    is a COVERAGE question, and printed the answer under the name `wall_seconds`. Every gap
    between steps -- reading a diff, deciding, waiting on a reviewer, the whole of the
    baseline's 72.7 residual ceremony -- was invisible, and invisible time reads as time that
    did not happen. That is this module's founding complaint about an unrecorded STEP, arriving
    one layer up at the arc.
    """
    receipt = mr.Receipt(slug="lane-x-675-step-7", batch="x", opened=_stamp(),
                         host="h", concurrent_seats=4, kind=mr.KIND_ARC,
                         closed=_stamp(3 * 3600 + 1 * 60 + 20))
    receipt.steps.append(_step("targeted-lane", 1.776, step_class=mr.CLASS_TESTS, ok=False))

    assert receipt.wall_seconds() == pytest.approx(10880.0), \
        "the arc lasted 3h01m20s; a receipt that calls 1.776 s its wall time is not a receipt"
    assert receipt.recorded_seconds() == pytest.approx(1.776), \
        "what the stopwatch actually covered stays available, under its own name"


def test_the_time_NOBODY_TIMED_is_NAMED_rather_than_erased():
    """`wall - recorded` is the baseline's 72.7 bucket, and it is the number the old arithmetic
    destroyed. Naming it is what lets the ~90/~63 disagreement ever resolve: an itemised view
    that accounts for 11 of 84 minutes cannot adjudicate between two readings of the other 73.
    """
    receipt = _receipt_with(None, [_step("suite", 600.0, step_class=mr.CLASS_TESTS)],
                            unrecorded_seconds=3000.0)

    assert receipt.unrecorded_seconds() == pytest.approx(3000.0)
    rendered = mr.render_summary(receipt)
    assert "UNRECORDED" in rendered and "50.00" in rendered, \
        "the untimed remainder is printed where a reader looks, not only computed"


def test_the_BASELINE_SPLIT_puts_the_UNTIMED_REMAINDER_in_the_CEREMONY_bucket():
    """Commensurability with `84 = 11.3 + 72.7` is only true if the two buckets sum to the
    arc's WALL time. The baseline's 72.7 is residual ceremony -- literally "the wall figure
    minus the tests" -- so an untimed gap belongs there and nowhere else.
    """
    receipt = _receipt_with(None, [
        _step("suite", 11.3 * 60.0, step_class=mr.CLASS_TESTS),
        _step("merge", 60.0),
    ], unrecorded_seconds=72.7 * 60.0 - 60.0)

    tests_min, residual_min = receipt.baseline_split()

    assert tests_min == pytest.approx(11.3)
    assert residual_min == pytest.approx(72.7)
    assert tests_min + residual_min == pytest.approx(receipt.wall_seconds() / 60.0), \
        "the split must add up to the arc, or it is not the baseline's split"


def test_a_receipt_whose_WALL_TIME_CANNOT_BE_READ_is_INCOMPLETE_rather_than_zero_minutes():
    """Zero is still the most dangerous plausible value this module can produce.

    Deriving wall time from timestamps introduces a new way to get it: a `closed` that does not
    parse. Returning 0.0 and counting the row would meet target 3.6 spectacularly, which is the
    `[#744]` failure class arriving through the door `[#750]` opened.
    """
    receipt = _complete_merge(40.0)
    receipt.closed = "2026-09-14 whenever"

    assert receipt.wall_seconds() == 0.0, "unreadable is not a duration"
    assert receipt.is_complete() is False
    assert "wall" in receipt.incompleteness_reason().lower()
    assert mr.median_report([receipt]).n == 0


# --- (2) completeness is the VERDICT STATE, never the exit code -------------

def test_a_PRE_EXISTING_suite_verdict_is_COMPLETE_with_the_state_recorded_BY_NAME():
    """Ruling AY1-1's first half, and the leg that makes the whole refusal reachable.

    Before this, `main`'s pre-existing red Actions pytest made every receipt incomplete, so the
    merge median was UNDEFINED after however many flawless merges and a refuse-on-incomplete
    rule would have refused all of them. COMPLETE is not the same as green: the state travels
    with the receipt, by name, so nobody can read this row as a clean run.
    """
    receipt = _complete_merge(40.0, verdict=av.STATE_PRE_EXISTING)

    assert receipt.is_complete() is True
    assert receipt.suite_verdict() == av.STATE_PRE_EXISTING
    assert av.STATE_PRE_EXISTING in mr.render_summary(receipt), \
        "COMPLETE-on-a-pre-existing-red is only honest while the state is on the face of it"
    assert receipt.to_dict()["suite_verdict"] == av.STATE_PRE_EXISTING, \
        "the ledger row carries the state too -- a median a reader cannot audit is a claim"


def test_a_REGRESSED_suite_verdict_is_INCOMPLETE_and_the_STATE_is_in_the_REFUSAL():
    """AY1-1's second half. A merge that BROKE the suite is not a measurement of a merge."""
    receipt = _complete_merge(40.0, verdict=av.STATE_REGRESSED)

    assert receipt.is_complete() is False
    assert av.STATE_REGRESSED in receipt.incompleteness_reason()
    assert mr.median_report([receipt]).n == 0


@pytest.mark.parametrize("state", [
    None, av.STATE_NO_RUN, av.STATE_IN_PROGRESS, av.STATE_UNAVAILABLE,
    av.STATE_JOBS_UNREADABLE, av.STATE_UNATTRIBUTED,
])
def test_a_suite_verdict_THAT_CANNOT_BE_READ_is_INCOMPLETE(state):
    """"a verdict that cannot be read -> INCOMPLETE", enumerated rather than paraphrased.

    Each of these says something different about WHY the suite result is unknown -- no run, not
    finished, `gh` absent, the job list unreadable, no baseline to attribute against -- and the
    one thing none of them says is "green". `actions_verdict`'s own remedy for the fourth is
    explicit: "This merge's suite result is UNKNOWN, which is not the same as green and must
    never be recorded as it."
    """
    receipt = _complete_merge(40.0, verdict=state)

    assert receipt.is_complete() is False
    assert mr.median_report([receipt]).n == 0
    reason = receipt.incompleteness_reason()
    assert "verdict" in reason.lower()
    if state is not None:
        assert state in reason, "the refusal names the state it read, never just 'unreadable'"


def test_the_suite_steps_EXIT_CODE_no_longer_decides_completeness_and_is_still_VISIBLE():
    """The pivot itself, as one test: exit code OUT of the predicate, never out of sight.

    `[#744]`'s false pass was "force the step to exit 0", and AY1-1 rules it out by name. This
    fix does the opposite -- it stops READING the exit code for completeness -- so the failing
    step must still be printed, or the fix would have laundered a red step into silence and
    become the very thing it refuses.
    """
    receipt = _complete_merge(40.0, verdict=av.STATE_PRE_EXISTING)
    receipt.steps.append(_step("suite", 900.0, step_class=mr.CLASS_TESTS, ok=False))

    assert receipt.is_complete() is True, "a tests-class step's exit code is not the predicate"
    rendered = mr.render_summary(receipt)
    assert "FAILED" in rendered and "suite" in rendered, \
        "not read for completeness is not the same as not reported"

    receipt.steps.append(_step("teardown-retry", 1.0, ok=False))
    assert receipt.is_complete() is False, \
        "a NON-suite step that failed still means the arc did not complete"


def test_a_RETRIED_actions_read_SUPERSEDES_the_one_it_retried():
    """`JOBS-UNREADABLE`'s remedy is "RETRY it", so the retry has to be able to win.

    A predicate that took the FIRST recorded state would make the retry pointless; one that
    demanded a single state would make retrying an error. The last recorded verdict is the read
    that stands, and both stay in the itemised view so the retry is visible.
    """
    receipt = _complete_merge(40.0, verdict=av.STATE_JOBS_UNREADABLE)
    assert receipt.is_complete() is False

    receipt.steps.append(_step("actions-retry", 3.0, step_class=mr.CLASS_TESTS,
                               verdict_state=av.STATE_PASS))

    assert receipt.suite_verdict() == av.STATE_PASS
    assert receipt.is_complete() is True
    assert av.STATE_JOBS_UNREADABLE in mr.render_summary(receipt), \
        "the superseded read stays on the receipt; a retry that hides the first is a rewrite"


def test_there_is_NO_WAY_to_TYPE_a_VERDICT_STATE_onto_a_RECEIPT():
    """Enforced by absence, asserted so the absence stays deliberate -- the same shape as
    `--skip`'s absence next door, and for a stronger reason.

    A `--state PASS` flag would put `[#744]`'s false pass one flag away: the integrator whose
    `gh` is unavailable could type the green the tool refused to read. So the state arrives from
    `actions_verdict`'s own state machine or it does not arrive, and `GH-UNAVAILABLE` refuses
    the merge rather than offering a way round itself.
    """
    from click.testing import CliRunner

    runner = CliRunner()
    assert "--state" not in runner.invoke(mr.cli, ["actions", "--help"]).output
    assert "--state" not in runner.invoke(mr.cli, ["time", "--help"]).output
    assert "--verdict" not in runner.invoke(mr.cli, ["time", "--help"]).output
    assert "--state" not in runner.invoke(mr.cli, ["close", "--help"]).output


def test_the_actions_verb_RECORDS_the_state_it_READ_and_still_exits_NON_ZERO(tmp_path):
    """Recorded, not recalled -- and the exit code is untouched.

    The verb drives `actions_verdict`'s real state machine (a pytest job failing at BOTH the tip
    and the baseline is PRE-EXISTING), records the state on the receipt, and reports non-`ok`
    exactly as the standalone tool does. That last clause is `[#744]`'s false pass refused in
    the place it would have been introduced: the receipt is now COMPLETE on a pre-existing red,
    and the step still reports a failure the integrator must record.
    """
    mr.open_receipt(tmp_path, slug="m", batch="y")
    fetch = _fetcher(tip=_run("tip", ("pytest", "failure"), ("lint", "success")),
                     base=_run("base", ("pytest", "failure"), ("lint", "success")))

    receipt, verdict = mr.record_actions_verdict(tmp_path, slug="m", sha="tip",
                                                baseline="base", fetch=fetch,
                                                first_parent=_parent({"tip": "base"}))

    assert verdict.state == av.STATE_PRE_EXISTING
    assert verdict.ok is False, "PRE-EXISTING is not a pass, and this verb does not make it one"
    assert receipt.suite_verdict() == av.STATE_PRE_EXISTING
    assert mr.load_receipt(tmp_path, "m").suite_verdict() == av.STATE_PRE_EXISTING, \
        "the state is persisted, or the next command cannot read it"


def test_the_actions_verb_BINDS_the_receipt_to_the_MERGE_SHA_it_read(tmp_path):
    """Which merge this receipt is OF -- the field the refusal below needs and the receipt has
    never carried. Before `[#750]` a receipt was opened once per batch and named no commit, so
    "this merge has a receipt" was not a question the ledger could answer.
    """
    mr.open_receipt(tmp_path, slug="m", batch="y")
    fetch = _fetcher(tip=_run("tip", ("pytest", "success")),
                     base=_run("base", ("pytest", "success")))

    mr.record_actions_verdict(tmp_path, slug="m", sha="tip", fetch=fetch,
                              first_parent=_parent({"tip": "base"}))

    assert mr.load_receipt(tmp_path, "m").merge_sha == "tip"


# --- (3) a merge that lands without a receipt is REFUSED -------------------

def test_a_merge_that_LANDED_WITH_NO_RECEIPT_is_REFUSED():
    """Done-contract clause 1, and the reason the receipt had to learn the merge SHA.

    `/lane-integrate`'s honest limit -- "it times what it is asked to time" -- was the whole of
    the enforcement: a step run without the prefix was invisible, and so was a merge. The
    refusal runs over the integrator's own walk range, so an unreceipted merge is NAMED rather
    than inferred from a count that came out short.
    """
    receipt = _complete_merge(40.0, "landed")
    receipt.merge_sha = "aaa111"

    problems = dict(mr.audit_merges(["aaa111", "bbb222"], [receipt]))

    assert problems["aaa111"] is None, "the merge with a complete receipt passes"
    assert problems["bbb222"] is not None and "no receipt" in problems["bbb222"].lower()


def test_a_merge_whose_receipt_is_INCOMPLETE_is_REFUSED_TOO_and_the_reason_travels():
    """AY1-1's second half at the refusal rather than at the median: "`REGRESSED`, or a verdict
    that cannot be read -> INCOMPLETE and the merge is refused". A refusal that accepted a
    present-but-unusable receipt would be satisfied by opening and closing one.
    """
    regressed = _complete_merge(40.0, "broke", verdict=av.STATE_REGRESSED)
    regressed.merge_sha = "ccc333"

    problem = dict(mr.audit_merges(["ccc333"], [regressed]))["ccc333"]

    assert problem is not None
    assert av.STATE_REGRESSED in problem, "the refusal carries the state, not just a verdict"


def test_an_ARC_receipt_cannot_DISCHARGE_a_merge():
    """The `kind` filter's argument, applied to the refusal it now also guards. An arc pays no
    merge and no teardown; accepting one as a merge's receipt would let the cheapest row in the
    ledger satisfy the bar for the most expensive act."""
    arc = _complete_merge(40.0, "arc")
    arc.kind = mr.KIND_ARC
    arc.merge_sha = "ddd444"

    problem = dict(mr.audit_merges(["ddd444"], [arc]))["ddd444"]

    assert problem is not None and "no receipt" in problem.lower()


def test_the_REFUSAL_NAMES_ITS_OWN_VACUITY_when_the_range_holds_no_merge():
    """A range with no merge commit in it passes, and says why it passed.

    This module's founding complaint is a mechanism returning a plausible value because the
    discriminating field is absent from what it looks at. "0 of 0 merges unreceipted" is exactly
    that value, so the report distinguishes a clean walk from an empty one instead of printing
    OK for both.
    """
    rendered = mr.render_require([], "main..main")

    assert "no merge" in rendered.lower()
    assert "not the same as" in rendered.lower(), \
        "an empty check must not read like a passed one"


def test_an_UNREADABLE_RANGE_REFUSES_rather_than_finding_NO_MERGES(tmp_path):
    """The same failure with teeth: `git rev-list` over a bad range exits non-zero, and a reader
    that turned that into an empty list would report every merge as receipted. Fail closed --
    the identical fix `[#742]` made one organ over, where an errored `gh` call became an empty
    job list and printed PASS."""
    with pytest.raises(mr.MergeReceiptError, match="rev-list|git"):
        mr.first_parent_merges(tmp_path, "no-such-ref..also-missing")


def test_the_require_VERB_exits_NON_ZERO_on_an_UNRECEIPTED_merge(tmp_path, monkeypatch):
    """The refusal as the integrator meets it: one exit code, and the merge named in the output.

    §3's checklist is "an item is checked because its command was run", so this row has to be a
    command that fails -- `audit.py handback`'s shape, which is the one row on that list that
    was already mechanized.
    """
    from click.testing import CliRunner

    receipt = _complete_merge(40.0, "landed")
    receipt.merge_sha = "aaa111"
    ledger = tmp_path / mr.LEDGER_RELPATH
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(json.dumps(receipt.to_dict()) + "\n", encoding="utf-8")
    monkeypatch.setattr(mr, "first_parent_merges", lambda root, rng: ["aaa111", "bbb222"])

    result = CliRunner().invoke(
        mr.cli, ["--repo-root", str(tmp_path), "require", "--range", "base..HEAD"])

    assert result.exit_code == 1
    assert "bbb222" in result.output
    assert "aaa111" in result.output, \
        "the merge that PASSED is named too -- a checklist row is evidence, not a verdict"


# ---------------------------------------------------------------------------------------------
# The baseline is MEASURED, not TYPED ([#750] follow-up). Codex `gpt-5.6-terra` CRITICAL, raised
# by the integrator seat during batch Y's review and verified in the code before these witnesses
# were written. The module refuses to let a VERDICT be typed -- no `--state`, at length, with an
# absence test -- and then accepted the BASELINE as free-form text. Choosing the baseline chooses
# the verdict, so `[#744]`'s false pass was open at the side door while the front one was bolted.
# ---------------------------------------------------------------------------------------------


def _parent(mapping):
    """A `first_parent` seam, the same shape as `verdict_for`'s `fetch`: a test drives the real
    refusal rather than asserting a relationship it typed itself."""
    def first_parent(_root, sha):
        if sha not in mapping:
            raise mr.MergeReceiptError(f"git rev-parse {sha}^1 could not be read")
        return mapping[sha]
    return first_parent


def test_the_BASELINE_is_DERIVED_from_the_merges_FIRST_PARENT_rather_than_SUPPLIED(tmp_path):
    """Omitting the baseline must not mean UNATTRIBUTED; it must mean `<sha>^1`.

    The old signature defaulted to None, and None attributes nothing -- so the safe-looking
    omission produced the one state that cannot discharge a merge. Deriving it makes the correct
    reading the DEFAULT rather than something the integrator must remember at every merge of a
    six-merge walk.
    """
    mr.open_receipt(tmp_path, slug="m", batch="y")
    read: list[str] = []

    def fetch(sha, **_kwargs):
        read.append(sha)
        return _run(sha, ("pytest", "failure"))

    receipt, verdict = mr.record_actions_verdict(
        tmp_path, slug="m", sha="tip", fetch=fetch,
        first_parent=_parent({"tip": "realparent"}))

    assert "realparent" in read, \
        "the derived first parent must be the SHA actually READ, not merely computed"
    assert verdict.state == av.STATE_PRE_EXISTING
    assert receipt.steps[-1].baseline_sha == "realparent", \
        "the baseline actually attributed against is recorded, or the reading is unauditable"


def test_a_BASELINE_that_is_NOT_the_merges_FIRST_PARENT_is_REFUSED(tmp_path):
    """The whole of the CRITICAL. An explicitly-passed baseline is checked against `<sha>^1` and
    refused when it disagrees, because `--baseline main` instead of `sha^1` -- or one copy-pasted
    from the previous lane's block -- is an easy honest slip that silently converts a REGRESSION
    into a pre-existing red."""
    mr.open_receipt(tmp_path, slug="m", batch="y")

    with pytest.raises(mr.MergeReceiptError) as exc:
        mr.record_actions_verdict(
            tmp_path, slug="m", sha="tip", baseline="some-older-red-commit",
            fetch=_fetcher(), first_parent=_parent({"tip": "realparent"}))

    message = str(exc.value)
    assert "some-older-red-commit" in message and "realparent" in message, \
        "the refusal names BOTH commits, or the integrator cannot see which one was wrong"


def test_a_TYPED_BASELINE_cannot_convert_a_REGRESSED_merge_into_a_PRE_EXISTING_one(tmp_path):
    """The CRITICAL's scenario end-to-end, driven through the real state machine.

    `tip` broke `pytest` against its own first parent -- REGRESSED, which refuses the merge. An
    older commit where `pytest` also failed is offered as the baseline, which WOULD read
    PRE-EXISTING, complete the receipt and let `require` exit 0. The refusal is what stops it.
    """
    mr.open_receipt(tmp_path, slug="m", batch="y")
    fetch = _fetcher(tip=_run("tip", ("pytest", "failure")),
                     realparent=_run("realparent", ("pytest", "success")),
                     olderred=_run("olderred", ("pytest", "failure")))
    parent = _parent({"tip": "realparent"})

    with pytest.raises(mr.MergeReceiptError):
        mr.record_actions_verdict(tmp_path, slug="m", sha="tip", baseline="olderred",
                                  fetch=fetch, first_parent=parent)

    assert mr.load_receipt(tmp_path, "m").suite_verdict() is None, \
        "a refused read records NOTHING -- a half-recorded verdict is the false pass itself"

    receipt, verdict = mr.record_actions_verdict(tmp_path, slug="m", sha="tip", fetch=fetch,
                                                 first_parent=parent)
    assert verdict.state == av.STATE_REGRESSED
    # Closed so the VERDICT leg is the one under test: leg 1 refuses an unclosed receipt first,
    # and an assertion satisfied by the wrong leg proves nothing about this one.
    receipt.closed = receipt.opened
    assert "REGRESSED" in (receipt.incompleteness_reason() or ""), \
        "the honest baseline refuses the merge, which is why refusing the typed one matters"


def test_an_UNDERIVABLE_FIRST_PARENT_REFUSES_rather_than_reading_UNATTRIBUTED(tmp_path):
    """FAILS CLOSED, the same posture as `first_parent_merges`. A SHA whose first parent cannot
    be read must not fall back to None: None is UNATTRIBUTED, and UNATTRIBUTED arriving from a
    silent failure is indistinguishable from UNATTRIBUTED arriving from an honest unknown."""
    mr.open_receipt(tmp_path, slug="m", batch="y")

    with pytest.raises(mr.MergeReceiptError):
        mr.record_actions_verdict(tmp_path, slug="m", sha="orphan", fetch=_fetcher(),
                                  first_parent=_parent({}))


def test_a_REGRESSED_reading_is_STICKY_and_a_LATER_read_cannot_supersede_it(tmp_path):
    """The HIGH. `suite_verdict()` is last-wins so a `JOBS-UNREADABLE` retry can be superseded by
    a real read -- but a REGRESSION once observed is a fact about the merge, and a later green
    read means the run was RE-RUN, which is a different claim. So completeness refuses on ANY
    recorded REGRESSED read regardless of position, and both readings stay on the receipt."""
    mr.open_receipt(tmp_path, slug="m", batch="y")
    parent = _parent({"tip": "realparent"})

    mr.record_actions_verdict(
        tmp_path, slug="m", sha="tip", step="actions",
        fetch=_fetcher(tip=_run("tip", ("pytest", "failure")),
                       realparent=_run("realparent", ("pytest", "success"))),
        first_parent=parent)
    receipt, _verdict = mr.record_actions_verdict(
        tmp_path, slug="m", sha="tip", step="actions-rerun",
        fetch=_fetcher(tip=_run("tip", ("pytest", "success")),
                       realparent=_run("realparent", ("pytest", "success"))),
        first_parent=parent)

    assert receipt.suite_verdict() == av.STATE_PASS, "last-wins still holds for the READING"
    # Closed so the VERDICT leg is the one under test -- see the note in the typed-baseline test.
    receipt.closed = receipt.opened
    reason = receipt.incompleteness_reason()
    assert reason is not None and "REGRESSED" in reason, \
        "a re-run cannot un-regress a merge; the receipt stays INCOMPLETE and says why"
    assert "actions" in reason, "the refusal NAMES the step that read the regression"


def test_there_is_NO_WAY_to_TYPE_a_BASELINE_RELATIONSHIP_ONTO_A_RECEIPT_EITHER():
    """The MEDIUM, and it is the absence test's own gap rather than the module's. The original
    asserted `--verdict` absent for `time` ONLY -- so an `actions --verdict PASS` flag could have
    been added with every assertion still green, on the one verb where it matters most."""
    from click.testing import CliRunner

    runner = CliRunner()
    for verb in ("actions", "time", "close"):
        output = runner.invoke(mr.cli, [verb, "--help"]).output
        for flag in ("--state", "--verdict", "--ok", "--force"):
            assert flag not in output, f"{verb} must not be able to be handed a {flag}"
