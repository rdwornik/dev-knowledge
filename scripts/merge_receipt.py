#!/usr/bin/env python
"""merge_receipt.py — per-step merge minutes, recorded rather than recalled (`[#675]` 3.1/3.3/3.6).

THE NUMBER THIS EXISTS TO REPLACE. `[#675]`'s baseline, frozen by the operator 2026-09-12 and
transcribed here rather than recomputed:

    84 min wall = 11.3 targeted tests + 72.7 residual ceremony
    (itemised views ~90 and ~63, nothing measured today)

**The parenthesis is part of the baseline, not commentary.** Two itemised views disagree with
each other AND with the wall figure, and no measurement was taken on the day it was frozen. A
merge that reports one opaque wall number can never resolve that disagreement — there is
nothing in it to attribute. So target 3.1 is *per-step minutes recorded into the receipt*, and
this module is that receipt.

IT IS A STOPWATCH, NOT A RUNNER, and that boundary is load-bearing twice over. Layer 2 never
executes (Critical Rule #4; ADR-28/36): a module that drove the merge would be the orchestration
script this repo forbids. And an integrator will not adopt a tool that takes the merge away from
them. So the integrator issues exactly the commands `/lane-integrate` already names, each behind
one prefix:

    merge_receipt.py time --step suite --class tests -- uv run --locked pytest -q …

The wrapper runs the child, times it, records it, and exits with the CHILD'S code. Remove every
prefix and the merge is unchanged.

TARGET 3.3 IS THE `race` VERB, and it is why this is a wrapper rather than a log. *"Codex reviews
in parallel — not serially behind the suite."* Serial, the merge pays `suite + review`; raced, it
pays `max(suite, review)` and the receipt records both durations AND the saving, so the claim is
a measurement rather than an assertion. **`race` never drops a job's verdict**: every job's exit
code is recorded and the verb exits non-zero if ANY failed. Running two checks concurrently is a
scheduling change; reporting only the winner would be a coverage change wearing one.

TARGET 3.5 IS WHY THERE IS NO `--skip`. *"Review and triage are handed pre-assembled inputs and
are NOT cut — the saving comes from removing assembly, never from removing the judgement step."*
This module can make a step CONCURRENT and it can make a step's input PRE-ASSEMBLED. It offers no
way to make a step disappear, because a median reached that way is a false pass on the row.

THE CLASS FIELD IS THE BASELINE'S OWN SPLIT, widened by exactly one. The baseline is binary —
tests vs residual ceremony — and a binary split cannot say whether review time grew or shrank,
which target 3.5 makes the one thing nobody may quietly trade away. So steps carry one of three
classes and the summary reports BOTH: the three-way split, and the two-way split the baseline is
stated in (`tests` vs everything else). Commensurability is preserved rather than assumed.

WHERE RECEIPTS LIVE, and why they are COMMITTED. `logs/MERGE-RECEIPTS.jsonl` — the `[#395]`
naming (UPPERCASE-KEBAB, extension honest to the format) and the `logs/TOKEN-LOG.md` class: an
append-only record of cost that outlives the run that produced it. A median over "a real run of
merges" (target 3.6) needs receipts that survive, so the gitignored-digest pattern the rest of
`logs/` uses would defeat the row. **Append-only in the ADR-29/ADR-39 sense**: `close` appends
one line and never rewrites an earlier one.

`[#750]` MADE IT A REFUSAL, AND FIXED THE NUMBER IT WAS REFUSING ON. Three changes, one row,
ruled by AY1-1 (2026-09-14):

  * **ONE RECEIPT PER MERGE, each naming its merge SHA.** It used to be one per BATCH, which made
    `REQUIRED_STEPS` satisfiable by whichever lane recorded a step id first, left target 3.1's
    itemised view of *a merge* nowhere to live, and turned `median` into a median over batches
    printed as "median merge minutes" — the `kind`-field failure with the discriminator moved one
    level out. `require --range <base>..<tip>` then REFUSES a merge in the integrator's own walk
    range that no complete receipt names.

  * **COMPLETENESS IS THE SUITE'S VERDICT STATE, NOT ITS EXIT CODE.** `PASS` or `PRE-EXISTING` is
    COMPLETE with the state recorded by name; `REGRESSED`, or a verdict that cannot be read, is
    INCOMPLETE and refuses the merge. The old predicate read `ok`, and `Verdict.ok` is
    `state == PASS` — so while `main`'s Actions `pytest` job is pre-existing red it refused EVERY
    receipt however clean the merge, and the median stayed UNDEFINED rather than low. Forcing the
    step to exit 0 is ruled out BY NAME as `[#744]`'s false pass, and no flag here can do it:
    there is no way to TYPE a state onto a receipt, only to read one.

  * **WALL TIME IS THE ARC'S SPAN.** It used to sum the timed children. Ledger row
    `lane-x-675-step-7` spans 3h01m20s and recorded `wall_seconds: 1.776` — the duration of its
    one child — and the baseline's 72.7 minutes of residual ceremony live precisely in the gaps
    that sum could not see. The summed figure keeps its own name (`recorded_seconds`), the
    difference is reported as `unrecorded_seconds`, and the baseline's two buckets now add up to
    the arc rather than to the part of it that happened to be wrapped.

HONEST LIMITS, stated so a number from here is not over-read:

  * **It times what it is asked to time.** A merge step run without the prefix is invisible, and
    an unrecorded step reads exactly like a fast one. `summary --strict` refuses a receipt whose
    recorded steps do not cover `REQUIRED_STEPS`; nothing forces `--strict`. Since `[#750]` the
    UNTIMED part of the arc is at least visible as a number — `unrecorded_seconds` — so an
    unprefixed step now shows up as ceremony nobody attributed rather than as no time at all.
  * **The refusal is scoped to a range, and is wired into no hook.** `require` judges the merges
    in the range the integrator hands it. Armed tree-wide it would refuse every merge that
    predates the receipt; run at commit time it would query an Actions run that cannot exist yet.
    It is a checklist row with an exit code, which is what makes it a refusal rather than a memo.
  * **Wall time is not work.** These runs share a machine with concurrent lanes; three seats
    committing at once stretch every duration. `concurrent_seats` is recorded per receipt for
    exactly that reason, and it is a COUNT of sibling worktrees, not a load measurement.
  * **A median over few merges is a median over few merges.** `median` always prints n, the
    spread and the range; there is no call that returns a bare number, because `[#675]` is the
    row about a confident figure with a hidden disagreement inside it.
"""
from __future__ import annotations

import json
import logging
import platform
import statistics
import subprocess
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, UTC
from pathlib import Path
from collections.abc import Sequence

import click

# THE SUITE VERDICT'S STATE MACHINE, imported rather than restated -- ruling AY1-1's whole point
# is that this module stopped reading it and read a flattened boolean instead. Same module-import
# shape as `audit.py`'s adapters; the `except` leg is the `scripts/`-on-sys.path entrypoint.
#
# IMPORTING A READER IS NOT EXECUTING. Critical Rule #4 forbids a script that drives state in a
# child repo; `verdict_for` reads a GitHub Actions run's conclusion and writes nothing anywhere.
# This module already spawns arbitrary child processes through `time` and `race`, so reaching a
# sibling READER directly is strictly less than what it already does -- and it is the only way to
# get the STATE rather than an exit code, which is what AY1-1 requires.
try:
    from scripts import actions_verdict as _av
except ImportError:  # pragma: no cover -- exercised by the scripts/-on-sys.path entrypoint
    import actions_verdict as _av

# THE ORDERED/RAN COMPARISON, imported rather than restated -- `[#752]`. Same shape and the same
# argument as the `actions_verdict` shim directly above: the question "does this model id
# discharge that ordered tier" has ONE home, and a receipt judged by a second copy of the
# tier->family table would drift from the organ that reads the transcript -- which is the defect
# one layer down, where five modules each restated the launch vocabulary.
#
# `compare_order` IS PURE. It takes two strings and returns a verdict, so this import reaches no
# filesystem, starts no session and reads no transcript. That is what lets a receipt be judged
# long after the transcript that produced it is gone, and identically on every host.
try:
    from scripts import routing_agreement as _ra
except ImportError:  # pragma: no cover -- exercised by the scripts/-on-sys.path entrypoint
    import routing_agreement as _ra

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("merge-receipt")

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent

#: The durable ledger. Committed, append-only, one JSON object per CLOSED receipt.
LEDGER_RELPATH = "logs/MERGE-RECEIPTS.jsonl"
#: The in-flight receipt, keyed by slug. It exists only between `open` and `close`.
#:
#: DELIBERATELY NOT GITIGNORED, and the reason is the same one that makes `open` refuse to
#: clobber it: a merge that dies half-way leaves this file behind, and that file is the only
#: record that a merge was abandoned. An ignore rule would hide exactly the case worth seeing
#: -- an integrator's tree would read clean while an abandoned receipt sat in it. On the normal
#: path `close` removes it, so it never reaches a commit; on the abandoned path it shows as
#: untracked, which is the signal, not a defect.
#:
#: (An ignore rule was written and then withdrawn on that reasoning. It also could not have
#: landed: `graph-task-coverage` refuses a staged file with no `implements` edge from an open
#: row, and `file_purpose_graph._REL_PATH_RE` requires at least one `/` in a path, so a
#: root-level dotfile can never carry that edge in EITHER direction -- the refusal's own remedy
#: ("name this file in the row's body, or name the row in this file") is unsatisfiable for
#: `.gitignore`. Recorded because it is a live gate defect, not this module's business to fix.)
SCRATCH_TEMPLATE = "logs/.merge-receipt-{slug}.json"

#: THE BASELINE, TRANSCRIBED — operator, 2026-09-12. Not recomputed here, and every field of it
#: is carried including the disagreement: `views` are the two itemised readings that disagree
#: with each other and with `wall`, and `measured_on_freeze_day` is False because nothing was.
BASELINE_WALL_MIN = 84.0
BASELINE_TESTS_MIN = 11.3
BASELINE_CEREMONY_MIN = 72.7
BASELINE_ITEMISED_VIEWS_MIN: tuple[float, ...] = (90.0, 63.0)
BASELINE_MEASURED_ON_FREEZE_DAY = False
BASELINE_FROZEN = "2026-09-12"
#: Target 3.6's bar.
TARGET_MEDIAN_MIN = 30.0

#: Step classes. `tests` and `ceremony` are the baseline's own two; `review` is split out of
#: ceremony because target 3.5 forbids trading it away and a binary split cannot show that it
#: was not. `summary` folds `review` back into ceremony for the baseline-commensurable view.
CLASS_TESTS = "tests"
CLASS_REVIEW = "review"
CLASS_CEREMONY = "ceremony"
STEP_CLASSES: tuple[str, ...] = (CLASS_TESTS, CLASS_REVIEW, CLASS_CEREMONY)

#: The steps a merge is EXPECTED to record, from `/lane-integrate`'s own walk. `--strict` reads
#: this; it is a completeness bar for a receipt, never a schedule the merge must follow.
REQUIRED_STEPS: tuple[str, ...] = ("handback", "merge", "suite", "teardown")

#: WHAT KIND OF ARC THIS RECEIPT TIMED, and the reason the field exists at all.
#:
#: Target 3.6 is "median MERGE minutes". The moment this ledger can also hold a lane's own commit
#: arc — which is useful, shares most of the same ceremony, and is the only thing a lane seat can
#: actually measure — a median over every row silently answers a different question than the one
#: `[#675]` asked, and answers it FLATTERINGLY, because a commit arc pays no merge and no
#: teardown. That is `[#675]`'s own filed failure class exactly: a reader that returns a
#: plausible value because the discriminating field is absent from what it looks at. So the field
#: is present, `median` filters on it, and the report NAMES what it excluded rather than quietly
#: dropping rows.
KIND_MERGE = "merge"
KIND_ARC = "arc"
RECEIPT_KINDS: tuple[str, ...] = (KIND_MERGE, KIND_ARC)

#: THE SUITE VERDICT STATES THAT MAKE A MERGE RECEIPT COMPLETE -- operator ruling AY1-1,
#: 2026-09-14 (`to-cc/AMEND-BATCH-Y-ROSTER-001.md`, carried in the batch Y manifest):
#:
#:     "completeness is judged on the suite step's VERDICT STATE, not its exit code. `PASS` or
#:      `PRE-EXISTING` -> COMPLETE with the state recorded by name; `REGRESSED`, or a verdict
#:      that cannot be read -> INCOMPLETE and the merge is refused. Forcing the step to exit 0
#:      is ruled out by name (`[#744]`'s false pass)."
#:
#: WHY IT HAD TO BE RULED. `actions_verdict.Verdict.ok` is `state == STATE_PASS`, under a
#: docstring that says so in capitals -- "ONLY `PASS` is ok. Every other state is non-zero,
#: including PRE-EXISTING". `main`'s Actions `pytest` job is pre-existing red, so a completeness
#: predicate reading that boolean refused EVERY receipt however clean the merge, and target 3.6's
#: median was permanently UNDEFINED rather than low. A rule worded "a merge that lands without a
#: COMPLETE receipt is refused" would then have refused every merge in this repo on its first day.
#:
#: PRE-EXISTING IS COMPLETE AND IS NOT GREEN, and both halves are load-bearing. The state is
#: recorded BY NAME on the receipt, in the ledger row and in the rendered summary, so a reader
#: meets "this merge ran against an already-red suite" rather than a clean row. What is ruled out
#: is making the STEP exit 0 -- that is the false pass, and no flag here can do it.
COMPLETE_SUITE_STATES: tuple[str, ...] = (_av.STATE_PASS, _av.STATE_PRE_EXISTING)

#: The step id the `actions` verb records under, unless told otherwise.
ACTIONS_STEP = "actions"


class MergeReceiptError(RuntimeError):
    """A receipt that cannot be opened, read or closed. Raised rather than degraded: a missing
    receipt is not an empty one, and an empty one times out at zero minutes."""


@dataclass(frozen=True)
class StepTiming:
    """One timed step. `seconds` is wall time; `ok` is the child's verdict, never inferred."""
    step: str
    step_class: str
    seconds: float
    ok: bool
    returncode: int | None
    command: str
    started: str
    #: Set when this step ran concurrently with others, naming the `race` group it belonged to.
    raced_with: tuple[str, ...] = ()
    #: THE SUITE RESULT'S STATE, in `actions_verdict`'s own vocabulary, when this step read one.
    #: `None` on every step that read no verdict -- which is most of them, and is not a defect.
    #:
    #: IT LIVES ON THE STEP RATHER THAN ON THE RECEIPT because ruling AY1-1 judges "the suite
    #: STEP's verdict state", and because a RETRY has to be expressible: `JOBS-UNREADABLE`'s own
    #: remedy is "RETRY it", so a second read must be able to supersede the first with both still
    #: visible. `Receipt.suite_verdict()` takes the last one recorded.
    verdict_state: str | None = None
    #: THE COMMIT THIS READING WAS ATTRIBUTED AGAINST -- the merge's first parent, derived rather
    #: than supplied. Recorded because a differential is only meaningful relative to its
    #: baseline: a `PRE-EXISTING` whose baseline nobody can name is not an auditable reading, it
    #: is a claim. `None` on a step that read no verdict, and on a ledger row written before the
    #: baseline was derived -- which is honest, because those readings took a baseline that was
    #: typed and is no longer recoverable.
    baseline_sha: str | None = None

    @property
    def minutes(self) -> float:
        return self.seconds / 60.0

    @property
    def ended(self) -> str | None:
        """`started` + `seconds`, as an ISO timestamp -- the step's END.

        UNTIL THIS FIELD, THE RECEIPT KNEW A STEP'S END AND NEVER SAID SO. `started` and
        `seconds` were both recorded, so the end was always arithmetic a reader could do by
        hand; `render_summary` did it for nobody. The lane-merge-hygiene done-contract asks
        for "each step's start, end and minutes" as three things shown, not one shown and one
        implied.

        None WHEN `started` DOES NOT PARSE -- the same honest-absence rule
        `Receipt._span_seconds` uses for the arc as a whole. This suite's own placeholder
        (`started="-"`, in `_step`) and every ledger row written before `[#750]` gave `started`
        a real clock reading; a receipt that never had one reports an unknown end, not a
        fabricated one at `seconds` past the epoch.
        """
        try:
            start = datetime.fromisoformat(self.started)
        except (TypeError, ValueError):
            return None
        return (start + timedelta(seconds=self.seconds)).isoformat(timespec="seconds")


@dataclass
class Receipt:
    """One merge, itemised. Serialised to the scratch file between steps."""
    slug: str
    batch: str
    opened: str
    host: str
    concurrent_seats: int
    kind: str = KIND_MERGE
    #: THE MERGE COMMIT THIS RECEIPT IS OF -- set by the `actions` verb from the SHA whose
    #: Actions run it read, and the field `require` matches on.
    #:
    #: IT DID NOT EXIST BEFORE `[#750]`, and its absence was the whole of the missing refusal:
    #: `/lane-integrate` opened ONE receipt per BATCH, so "does this merge have a receipt" was
    #: not a question the ledger could answer, and `median` was a median over batches printed as
    #: "median merge minutes" -- the `kind`-field failure with the discriminator moved one level
    #: out. One receipt per merge, each naming its merge.
    merge_sha: str | None = None
    #: THE TIER THE CONTRACT ORDERED, and THE MODEL THE LANE ACTUALLY RAN (`[#752]`).
    #:
    #: THE SPLIT IS AY1-1's, REUSED. `ordered_model` is an INPUT -- it is what the contract's
    #: routing row says, and it is typed, because an order IS a declaration. `ran_model` is READ
    #: off the lane's own transcript by `routing_agreement.model_reading`, and there is no flag
    #: anywhere in this module that can hand one in: a seat able to type what it wished had run
    #: would produce a receipt that agrees with itself, which is `[#744]`'s false pass reached by
    #: the cheapest route in the module.
    #:
    #: THE FACT NO RECEIPT COULD HOLD BEFORE THEM. `lane-x-689-conductor-e-proof` was ordered at
    #: `opusplan` and ran 84 of 84 assistant messages on `claude-sonnet-5`; its receipt recorded
    #: the merge SHA, the suite verdict, the baseline and per-step minutes, and not one field
    #: named the model the work was DONE at -- so an arc run at a tier nobody ordered was
    #: indistinguishable from the arc that was, and fed a median printed as the cost of the order.
    #:
    #: BOTH DEFAULT TO None AND THAT PAIR IS NOT A FAILURE. A ledger row written before these
    #: fields existed knows neither value, and leg 4 does not fire on it -- the same decision
    #: `merge_sha` forced for the same reason: refusing a corpus of clean merges to arm a new
    #: field is `Verdict.ok`'s trap with a new field in it. A receipt carrying exactly ONE of them
    #: is a different case and IS refused, because asking a question and failing to answer it is
    #: not the answer being yes.
    ordered_model: str | None = None
    ran_model: str | None = None
    steps: list[StepTiming] = field(default_factory=list)
    closed: str | None = None

    # -- arithmetic ---------------------------------------------------------------------------

    def _span_seconds(self) -> float | None:
        """`opened` -> `closed` in seconds, or **None when that cannot be read**.

        None rather than 0.0, and the distinction is the same one `[#742]` drew one organ over
        between "there were no failing jobs" and "the job list could not be read": zero is a
        plausible, flattering value and unreadable is an absence. `incompleteness_reason` reads
        the None; `wall_seconds` renders it as 0.0 for arithmetic, having already been refused.

        An open receipt is measured to NOW, which is honest for an in-flight summary -- and it
        never reaches the median, because leg 1 refuses a receipt that was never closed.
        """
        try:
            start = datetime.fromisoformat(self.opened)
            end = (datetime.fromisoformat(self.closed) if self.closed
                   else datetime.now(UTC))
            span = (end - start).total_seconds()
        except (TypeError, ValueError):
            return None
        # A receipt closed before it opened is not a short arc; it is an unreadable one.
        return span if span >= 0 else None

    def wall_seconds(self) -> float:
        """THE ARC'S DURATION -- `opened` to `closed`, from the timestamps.

        IT USED TO SUM THE TIMED CHILDREN, and that is the defect `[#750]` was filed on. Ledger
        row `lane-x-675-step-7` opened 2026-09-12T19:13:21 and closed 22:14:41 -- a span of
        3h01m20s -- and recorded `"wall_seconds": 1.776`, the duration of the one child it
        wrapped. The sibling row `lane-x-675-step-4` loses 10m12s the same way.

        THE LOST TIME IS THE QUANTITY THIS MODULE EXISTS TO ITEMISE. The baseline is
        `84 min wall = 11.3 targeted tests + 72.7 residual ceremony`, and the 72.7 lives
        precisely in the gaps BETWEEN timed steps: reading a diff, deciding, waiting on a
        reviewer. An arithmetic blind to those gaps reported the 84-minute merge as an
        11-minute one, met target 3.6 spectacularly, and left the ~90/~63 disagreement exactly
        where it was -- nothing in the receipt attributed the other 73 minutes. Same failure
        class as an unrecorded STEP, one layer up at the arc.

        The summed-children figure is still available, under the name it was always computing:
        `recorded_seconds`.
        """
        span = self._span_seconds()
        return 0.0 if span is None else round(span, 3)

    def recorded_seconds(self) -> float:
        """How much of the arc a stopwatch actually covered, with a RACED GROUP COUNTED ONCE at
        its longest member.

        A COVERAGE FIGURE, NOT A DURATION -- which is what it always was, and naming it that is
        half of `[#750]`'s fix. Summing raced steps would report the serial cost of a parallel
        run and erase the very saving target 3.3 exists to produce; the receipt would show the
        improvement as no improvement. Grouping is by `raced_with` membership, which `race` sets.
        """
        total = 0.0
        seen_groups: set[frozenset[str]] = set()
        for step in self.steps:
            if not step.raced_with:
                total += step.seconds
                continue
            group = frozenset({step.step, *step.raced_with})
            if group in seen_groups:
                continue
            seen_groups.add(group)
            total += max(s.seconds for s in self.steps
                         if s.step in group)
        return total

    def unrecorded_seconds(self) -> float:
        """The arc's time NOBODY TIMED -- `wall - recorded`, floored at zero.

        THE BASELINE'S 72.7 LIVES HERE, so it is reported rather than silently dropped: an
        itemised view that accounts for 11 of 84 minutes cannot adjudicate between two readings
        of the other 73, which is the whole of `[#675]`'s complaint.

        Floored at zero because a RACED group counts once in `recorded` but its members count in
        full in `by_class`, so the two views can disagree by the overlap. `render_summary` names
        that disagreement when it appears rather than hiding it behind the floor.
        """
        return max(0.0, self.wall_seconds() - self.recorded_seconds())

    def serial_seconds(self) -> float:
        """What the same steps would have cost run one after another — the counterfactual the
        parallel saving is measured against, kept explicit rather than implied."""
        return sum(s.seconds for s in self.steps)

    def suite_verdict(self) -> str | None:
        """The suite result's STATE as this receipt recorded it, or None when none was.

        THE LAST ONE WINS, deliberately. `JOBS-UNREADABLE`'s own remedy is "RETRY it", so a
        second read must be able to supersede the first; a predicate taking the FIRST state
        would make the retry pointless, and one demanding a single state would make retrying an
        error. Both reads stay on the receipt and in the rendered summary, so the retry is
        visible rather than a rewrite.
        """
        states = [s.verdict_state for s in self.steps if s.verdict_state]
        return states[-1] if states else None

    def by_class(self) -> dict[str, float]:
        """Seconds per class. Raced steps count in FULL here, deliberately: the question a class
        split answers is "how much work of each kind was done", which concurrency does not
        change. Wall time is the other question, and `wall_seconds` answers it."""
        out = {c: 0.0 for c in STEP_CLASSES}
        for step in self.steps:
            out[step.step_class] = out.get(step.step_class, 0.0) + step.seconds
        return out

    def baseline_split(self) -> tuple[float, float]:
        """`(tests_minutes, residual_ceremony_minutes)` — the baseline's OWN two buckets, with
        `review` folded back into ceremony so the two numbers are commensurable with
        `84 = 11.3 + 72.7`. Folding is stated, never silent.

        THE UNTIMED REMAINDER IS IN THE RESIDUAL BUCKET SINCE `[#750]`, and it belongs nowhere
        else. The baseline's 72.7 is *residual ceremony* — literally the wall figure minus the
        tests — so commensurability is only true if the two buckets sum to the ARC rather than
        to the part of it that happened to be wrapped in a stopwatch. Before this, they summed
        to `recorded_seconds` and the split silently described a different, much shorter event.
        """
        classes = self.by_class()
        tests = classes.get(CLASS_TESTS, 0.0) / 60.0
        residual = (classes.get(CLASS_REVIEW, 0.0)
                    + classes.get(CLASS_CEREMONY, 0.0)
                    + self.unrecorded_seconds()) / 60.0
        return tests, residual

    def missing_required(self) -> list[str]:
        recorded = {s.step for s in self.steps}
        return [s for s in REQUIRED_STEPS if s not in recorded]

    def failed_steps(self) -> list[StepTiming]:
        return [s for s in self.steps if not s.ok]

    def judged_by_verdict(self, step: StepTiming) -> bool:
        """True when this step's EXIT CODE is not read for completeness — ruling AY1-1.

        SCOPED BY CLASS, not by a hard-coded list of step ids, because the class field already
        means "what kind of work this was" and a name list would go stale the first time an
        integrator renamed a step. Every `tests`-class step on a MERGE receipt is a reading of
        the suite, and the suite is judged by its recorded STATE.

        ARCS ARE EXCLUDED, and that is the same decision leg 6 makes for `REQUIRED_STEPS`: an
        arc reads no Actions run for a merge SHA, because there is no merge, so it has no state
        to be judged on and keeps the exit-code reading it always had.
        """
        return self.kind == KIND_MERGE and step.step_class == CLASS_TESTS

    # -- completeness (`[#744]`) --------------------------------------------------------------

    def incompleteness_reason(self) -> str | None:
        """WHY this receipt is not a usable measurement, or None when it is.

        ONE EXPLICIT PREDICATE IN CODE, which is `[#744]`'s own requirement -- "rather than left
        to the reader". Until 2026-09-13 `median_report` filtered by `kind` and by nothing else,
        so an abandoned receipt, a receipt whose suite step exited non-zero and a receipt that
        recorded one step out of four all counted at FULL WEIGHT in a number printed as "median
        merge minutes". The live ledger held two rows, both with failed steps, one of them
        0.0 minutes, and the tool reported `median 9.4 min (target 3.6: MET)` over them.

        THE REASON IS RETURNED, NOT A BARE BOOLEAN, for the same argument `REMEDIES` makes in
        `actions_verdict`: an exclusion a reader cannot account for looks like a bug in the
        tool, and the count alone ("3 excluded") does not say whether the ledger is dirty or the
        merges are.

        THE THIRD LEG WAS RE-POINTED BY RULING AY1-1 (2026-09-14, `[#750]`), and the old one was
        unreachable rather than merely wrong. It read `failed_steps()` -- any step with
        `ok=False` -- and the suite step's `ok` comes from `actions_verdict`, whose `Verdict.ok`
        is `state == STATE_PASS` under a docstring that says "ONLY `PASS` is ok. Every other
        state is non-zero, including PRE-EXISTING". While `main`'s Actions `pytest` job is
        pre-existing red, that leg refused EVERY receipt however clean the merge, target 3.6's
        median stayed UNDEFINED rather than low, and the refusal `[#750]` also builds -- "a merge
        that lands without a COMPLETE receipt is refused" -- would have refused every merge in
        this repo on its first day. A five-state machine had been flattened to one boolean at the
        boundary; the ruling reads the state instead.

        The legs, in the order a reader should think about them:

          1. NEVER CLOSED -- it was opened and abandoned. Its wall time is whatever had elapsed
             when someone stopped writing, which is not a duration of anything.
          2. NO STEPS -- wall time 0.0, the most dangerous plausible value this module can
             produce: it meets target 3.6 spectacularly and means nothing.
          3. WALL TIME UNREADABLE -- `opened`/`closed` do not parse as an ordered pair, so the
             span is not 0.0 minutes but *unknown*, and 0.0 is exactly the flattering value leg 2
             exists to refuse. A new leg, because `[#750]` made wall time derive from those two
             fields and so created a new door to the same lie.
          4. THE RUN IT TIMED IS NOT THE RUN THAT WAS ORDERED -- the lane's transcript recorded a
             model the contract did not name. Fires on BOTH kinds, and only on a receipt that
             carries a reading: a row with NEITHER field keeps the predicate it already had.
             `lane-x-689` ordered `opusplan` and ran 84 of 84 assistant messages on
             `claude-sonnet-5`; a receipt of that arc timed a real event, and not the one its
             median would have claimed. (`[#752]`.)
          5. THE SUITE VERDICT (merge receipts only) -- `PASS` or `PRE-EXISTING` is COMPLETE with
             the state named; `REGRESSED` means this merge broke the suite; anything else, or
             nothing at all, means the suite result could not be read. Only `PASS` and
             `PRE-EXISTING` pass, and the state is in the refusal text either way.
          6. A FAILED STEP WHOSE EXIT CODE IS STILL READ -- i.e. every step `judged_by_verdict`
             does not cover: handback, merge, teardown, review, and every step of an arc. The arc
             did not complete, so its duration times a different event than the median claims.
          7. A MERGE MISSING A REQUIRED STEP -- an unrecorded step reads exactly like a fast one,
             which is this module's founding complaint.

        LEGS 5 AND 7 ARE SCOPED TO `kind == merge`, and that is one decision made twice rather
        than an oversight. `REQUIRED_STEPS` is the INTEGRATOR's walk and this module's own
        docstring says an arc "pays no merge and no teardown"; an arc likewise reads no Actions
        run for a merge SHA, because there is no merge. Holding an arc to either would make
        `median --kind arc` permanently n=0 for a reason that is not incompleteness. Legs 1-4
        and 6 bind both kinds -- and leg 4 binding an ARC is deliberate rather than incidental:
        `lane-x-689` was a lane ARC, not an integrator's merge, so scoping the model leg to
        merges would have put its own witness outside the predicate.
        """
        if self.closed is None:
            return "never closed -- opened and abandoned, so its wall time times nothing"
        if not self.steps:
            return "no steps recorded -- wall time 0.0, which is not a measurement"
        if self._span_seconds() is None:
            return (f"wall time unreadable -- opened={self.opened!r} and closed={self.closed!r} "
                    f"do not parse as an ordered pair of timestamps, so this arc's span is "
                    f"UNKNOWN rather than 0.0, and 0.0 is the value that meets target 3.6 while "
                    f"meaning nothing")
        # LEG 4 (`[#752]`). IT SITS HERE DELIBERATELY: after the three legs that ask whether this
        # is a measurement AT ALL, and before the verdict legs, because a suite verdict read off
        # an arc run at a tier nobody ordered is a fact about a different run -- and reporting a
        # model comparison on an arc that timed nothing would be a comparison about nothing.
        #
        # THE SKIP IS ON `UNREAD` AND ON NO OTHER STATE. A receipt carrying neither field keeps
        # the predicate it already had; every other state -- diverged, half-recorded, an
        # unverifiable split tier, a tier this reader does not know -- is a REPORTED GAP under
        # Z-G4 and never a pass, because a check that cannot compute its ground truth fails.
        model_state, model_detail = _ra.compare_order(self.ordered_model, self.ran_model)
        if model_state not in (_ra.STATE_UNREAD, _ra.STATE_AGREE):
            return (f"ordered/ran model [{model_state}] -- {model_detail}. The receipt times a "
                    f"real arc either way; what it cannot do is stand as a measurement OF THE "
                    f"ORDER, which is what a median printed against a routing decision claims")
        if self.kind == KIND_MERGE:
            state = self.suite_verdict()
            if state is None:
                return ("no suite verdict recorded -- ruling AY1-1 judges completeness on the "
                        "suite step's verdict STATE, and an unread verdict is not a pass. Record "
                        "one: `merge_receipt.py actions --slug <slug> --sha <merge> --baseline "
                        "<its first parent>`")
            if state not in COMPLETE_SUITE_STATES:
                why = ("this merge BROKE the suite" if state == _av.STATE_REGRESSED
                       else "the suite result could not be READ, which is not the same as green")
                return (f"suite verdict {state} -- {why}; only "
                        f"{' or '.join(COMPLETE_SUITE_STATES)} is COMPLETE (ruling AY1-1). "
                        f"-> {_av.REMEDIES.get(state, 'read the verdict and record it')}")
            # A REGRESSION IS STICKY, and this leg is why `suite_verdict`'s last-wins rule is
            # safe. Last-wins exists for `JOBS-UNREADABLE` -> a real read, and it must not also
            # let a re-run overwrite a REGRESSION: a regression once observed is a fact about
            # this merge, whereas a later green read is a fact about a run that was RE-RUN. Those
            # are different claims, and accepting the second as a retraction of the first is
            # `[#744]`'s false pass with a retry in front of it. Both readings stay on the
            # receipt and both print, so the disagreement is visible rather than resolved.
            if regressed := [s.step for s in self.steps
                             if s.verdict_state == _av.STATE_REGRESSED]:
                return (f"a REGRESSED suite verdict was recorded on step(s) "
                        f"{', '.join(regressed)} and the latest reading is {state} -- a re-run "
                        f"does not un-regress a merge, so this receipt stays INCOMPLETE. If the "
                        f"regression was mis-attributed, the baseline was wrong and the fix is a "
                        f"correct read on a new receipt, not a second opinion on this one")
        failed = [s for s in self.failed_steps() if not self.judged_by_verdict(s)]
        if failed:
            return (f"{len(failed)} step(s) failed ({', '.join(s.step for s in failed)}) -- "
                    f"the arc did not complete")
        if self.kind == KIND_MERGE and (missing := self.missing_required()):
            return (f"missing required step(s): {', '.join(missing)} -- an unrecorded step "
                    f"reads exactly like a fast one")
        return None

    def is_complete(self) -> bool:
        """True when this receipt is a usable measurement. See `incompleteness_reason`."""
        return self.incompleteness_reason() is None

    # -- serialisation ------------------------------------------------------------------------

    def to_dict(self) -> dict:
        data = asdict(self)
        data["steps"] = [
            # DERIVED, never a second home for the value -- same argument as `suite_verdict`
            # just above: `ended` is `started` + `seconds`, computed fresh on every read, and
            # this key exists so a ledger row is greppable for it rather than requiring the
            # arithmetic back from a reader.
            {**asdict(s), "raced_with": list(s.raced_with), "ended": s.ended} for s in self.steps]
        data["wall_seconds"] = round(self.wall_seconds(), 3)
        data["recorded_seconds"] = round(self.recorded_seconds(), 3)
        data["unrecorded_seconds"] = round(self.unrecorded_seconds(), 3)
        data["serial_seconds"] = round(self.serial_seconds(), 3)
        # DERIVED, never a second home for the value: the state lives on its step, and this key
        # exists so a ledger row is greppable -- "recorded BY NAME on the receipt" is what
        # ruling AY1-1 asks for, and a median a reader cannot audit is a claim.
        data["suite_verdict"] = self.suite_verdict()
        tests_min, residual_min = self.baseline_split()
        data["baseline_split_minutes"] = {"tests": round(tests_min, 2),
                                          "residual_ceremony": round(residual_min, 2)}
        data["by_class_seconds"] = {k: round(v, 3) for k, v in self.by_class().items()}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Receipt:
        steps = [StepTiming(step=s["step"], step_class=s["step_class"], seconds=s["seconds"],
                            ok=s["ok"], returncode=s.get("returncode"),
                            command=s.get("command", ""), started=s.get("started", ""),
                            raced_with=tuple(s.get("raced_with", ())),
                            verdict_state=s.get("verdict_state"),
                            baseline_sha=s.get("baseline_sha"))
                 for s in data.get("steps", [])]
        # A row written before `kind` existed is a MERGE receipt — that is what the ledger held
        # when the field was absent, so the default reads the history correctly rather than
        # conveniently.
        #
        # `merge_sha` and `verdict_state` DEFAULT TO None FOR THE SAME REASON, read the other
        # way: a row written before `[#750]` named no merge and recorded no state, and None is
        # what that row actually knows. It reads as INCOMPLETE under the new predicate, which is
        # the honest answer -- those merges were never judged on a verdict state, and defaulting
        # either field to something convenient would back-date a judgement nobody made.
        #
        # `ordered_model`/`ran_model` READ THE SAME WAY, and their None pair is the one absence
        # that is not a finding: `compare_order` answers `unread` on it and leg 4 skips. A
        # refusal that evaporated on serialisation would refuse nothing -- `close` appends to the
        # ledger and `median` reads it back, so the pair has to survive the trip to bind at all.
        return cls(slug=data["slug"], batch=data.get("batch", ""), opened=data["opened"],
                   host=data.get("host", ""), concurrent_seats=data.get("concurrent_seats", 0),
                   kind=data.get("kind", KIND_MERGE), merge_sha=data.get("merge_sha"),
                   ordered_model=data.get("ordered_model"), ran_model=data.get("ran_model"),
                   steps=steps, closed=data.get("closed"))


# --- context ---------------------------------------------------------------------------------

def count_concurrent_seats(repo_root: Path) -> int:
    """Lane worktrees live on this machine right now.

    A COUNT, NOT A LOAD MEASUREMENT, and the distinction is the honest limit: three seats each
    running a full suite stretch every duration in this receipt, and a receipt that recorded a
    number without recording how many machines-worth of work were in flight would invite
    comparing a quiet merge with a busy one as though the difference were the process.
    """
    try:
        out = subprocess.run(["git", "-C", str(repo_root), "worktree", "list", "--porcelain"],
                             capture_output=True, text=True, check=True, timeout=60).stdout
    except (OSError, subprocess.SubprocessError):
        return 0
    return sum(1 for line in out.splitlines()
               if line.startswith("worktree ") and ".claude/worktrees" in
               line.replace("\\", "/"))


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def scratch_path(repo_root: Path, slug: str) -> Path:
    return repo_root / SCRATCH_TEMPLATE.format(slug=slug)


def ledger_path(repo_root: Path) -> Path:
    return repo_root / LEDGER_RELPATH


# --- receipt lifecycle -----------------------------------------------------------------------

def open_receipt(repo_root: Path, *, slug: str, batch: str, kind: str = KIND_MERGE) -> Receipt:
    """Start a receipt. Refuses to clobber an in-flight one: an abandoned scratch file is
    evidence that a merge died half-way, and overwriting it destroys the only record of that."""
    path = scratch_path(repo_root, slug)
    if path.exists():
        raise MergeReceiptError(
            f"{path} already exists -- a receipt for {slug!r} is already open. Close it "
            f"(`merge_receipt.py close --slug {slug}`) or delete it deliberately; this does not "
            f"overwrite an in-flight receipt, because an abandoned one is the record of a merge "
            f"that died half-way.")
    if kind not in RECEIPT_KINDS:
        raise MergeReceiptError(f"kind {kind!r} is outside {{{', '.join(RECEIPT_KINDS)}}}")
    receipt = Receipt(slug=slug, batch=batch, opened=_now(),
                      host=platform.node(), kind=kind,
                      concurrent_seats=count_concurrent_seats(repo_root))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt.to_dict(), indent=2), encoding="utf-8", newline="\n")
    return receipt


def load_receipt(repo_root: Path, slug: str) -> Receipt:
    path = scratch_path(repo_root, slug)
    try:
        return Receipt.from_dict(json.loads(path.read_text(encoding="utf-8")))
    except OSError as exc:
        raise MergeReceiptError(
            f"no open receipt for {slug!r} at {path} -- run `merge_receipt.py open --slug "
            f"{slug}` first. A step timed against no receipt is a measurement nothing keeps."
        ) from exc
    except json.JSONDecodeError as exc:
        raise MergeReceiptError(f"{path} is not readable JSON: {exc}") from exc


def save_receipt(repo_root: Path, receipt: Receipt) -> None:
    scratch_path(repo_root, receipt.slug).write_text(
        json.dumps(receipt.to_dict(), indent=2), encoding="utf-8", newline="\n")


def run_timed(command: Sequence[str], *, step: str, step_class: str,
              cwd: Path | None = None) -> StepTiming:
    """Run `command`, timed. The child's stdout/stderr are NOT captured — they go straight to the
    operator's terminal, because a wrapper that swallowed a merge step's output would make itself
    the thing between the integrator and their own merge."""
    started = _now()
    clock = time.perf_counter()
    try:
        proc = subprocess.run(list(command), cwd=str(cwd) if cwd else None, check=False)
        rc: int | None = proc.returncode
    except (OSError, subprocess.SubprocessError) as exc:
        logger.error("step %s could not be run: %r", step, exc)
        rc = None
    elapsed = time.perf_counter() - clock
    return StepTiming(step=step, step_class=step_class, seconds=round(elapsed, 3),
                      ok=rc == 0, returncode=rc, command=" ".join(command), started=started)


def first_parent_of(repo_root: Path, sha: str) -> str:
    """`<sha>^1`, resolved by git. FAILS CLOSED -- raises rather than returning None.

    THE ATTRIBUTION POINT IS DERIVED, NEVER SUPPLIED (`[#750]` follow-up). Returning None on an
    unresolvable SHA would be the worst available answer: None reaches `verdict_for` as "no
    baseline", which produces `UNATTRIBUTED` -- and `UNATTRIBUTED` arriving from a silent git
    failure is indistinguishable, on the receipt, from `UNATTRIBUTED` arriving from an honest
    unknown. Same posture, and the same argument, as `first_parent_merges`.
    """
    command = ["git", "-C", str(repo_root), "rev-parse", "--verify", f"{sha}^1"]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, check=False, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        raise MergeReceiptError(f"git rev-parse {sha}^1 could not be run: {exc!r}") from exc
    if proc.returncode != 0:
        raise MergeReceiptError(
            f"git rev-parse {sha}^1 exited {proc.returncode}: {proc.stderr.strip()[:200]} -- "
            f"the baseline is DERIVED from the merge's first parent and cannot be guessed. A "
            f"root commit, an unknown SHA, or a commit not yet in this repository each land "
            f"here; refusing beats attributing the verdict to nothing")
    resolved = proc.stdout.strip()
    if not resolved:
        raise MergeReceiptError(f"git rev-parse {sha}^1 printed nothing -- refusing to read "
                                f"silence as a baseline")
    return resolved


def _same_commit(left: str, right: str) -> bool:
    """Prefix-tolerant in BOTH directions, the same comparison `audit_merges` already makes: a
    walk is written with short SHAs and a ledger records long ones, and neither is wrong."""
    left, right = left.strip(), right.strip()
    if not left or not right:
        return False
    return left.startswith(right) or right.startswith(left)


def record_actions_verdict(repo_root: Path, *, slug: str, sha: str,
                           baseline: str | None = None, step: str = ACTIONS_STEP,
                           fetch=None, first_parent=None) -> tuple[Receipt, _av.Verdict]:
    """Read this merge's Actions verdict, record its STATE on the receipt, bind the merge SHA.

    RULING AY1-1'S CARRIER. Until `[#750]` this was a `time --step actions -- actions_verdict.py
    …` prefix, which recorded the child's EXIT CODE and threw the state away -- and since
    `Verdict.ok` is `state == PASS`, a `PRE-EXISTING` red arrived as `ok=False` and made every
    receipt incomplete. Calling the reader directly is what makes the state available at all.

    MEASURED, NOT TYPED, and that is why there is no `--state` flag anywhere in this module. A
    flag would put `[#744]`'s false pass one keystroke away: the integrator whose `gh` is
    unavailable could type the green the tool declined to read. So `GH-UNAVAILABLE` refuses the
    merge rather than offering a way round itself -- which is exactly what target 3.2 asks for,
    "record explicitly that the result was NOT read, never that it passed".

    THE EXIT CODE IS UNCHANGED, and the caller passes it through: `ok` is recorded exactly as
    `actions_verdict`'s own CLI would exit (`0 if verdict.ok else 1`), so a `PRE-EXISTING` step
    still reports a failure the integrator must record in the batch packet. COMPLETE is a
    statement about the RECEIPT; it was never a statement about the run.

    AND THE BASELINE IS MEASURED TOO, which it was not until this follow-up. `--baseline` was
    free-form and never checked against `<sha>^1`, so the input that CHOOSES the verdict was the
    one input still typed: hand it any older commit where the suite also failed and a genuinely
    `REGRESSED` merge reads `PRE-EXISTING`, the receipt completes and `require` exits 0. That is
    `[#744]`'s false pass reached through a side door while the front one was bolted, and the
    realistic path to it is an ordinary slip -- `--baseline main` instead of `sha^1`, or a
    baseline copy-pasted from the previous lane's block in a six-merge walk.

    So the first parent is DERIVED, an explicitly-passed baseline is REFUSED unless it is that
    commit, and the SHA actually attributed against is RECORDED on the step. There is no override
    flag, and the omission is deliberate rather than an oversight: adding one would reinstate the
    escape hatch the `--state` absence exists to deny. If a non-first-parent baseline ever has a
    legitimate use it arrives as its own named requirement, recording itself on the receipt so it
    cannot be mistaken for the default reading.

    A REFUSED READ RECORDS NOTHING. The check runs before the reader is called, so a receipt
    never carries half of a rejected reading -- a partially-recorded verdict would be the very
    false pass this guards.

    `fetch` is `actions_verdict`'s own injection seam, passed straight through so a test drives
    the real state machine rather than asserting a state it typed itself. `first_parent` is the
    same shape for the git resolution, so the refusal is testable without a repository fixture.
    """
    receipt = load_receipt(repo_root, slug)
    resolve = first_parent or first_parent_of
    derived = resolve(repo_root, sha)
    if baseline is not None and not _same_commit(baseline, derived):
        raise MergeReceiptError(
            f"baseline {baseline} is not the first parent of {sha}, which is {derived}. The "
            f"differential must mean 'what THIS merge changed', and attributing against any "
            f"other commit silently converts a REGRESSION into a pre-existing red -- ruling "
            f"AY1-1's one forbidden conversion. Omit --baseline and it is derived for you; "
            f"there is deliberately no flag that accepts a different one")
    started = _now()
    clock = time.perf_counter()
    verdict = _av.verdict_for(sha, baseline=derived, fetch=fetch, repo_root=repo_root)
    elapsed = time.perf_counter() - clock
    receipt.steps.append(StepTiming(
        step=step, step_class=CLASS_TESTS, seconds=round(elapsed, 3), ok=verdict.ok,
        returncode=0 if verdict.ok else 1,
        command=f"actions_verdict.verdict_for(sha={sha}, baseline={derived})",
        started=started, verdict_state=verdict.state, baseline_sha=derived))
    receipt.merge_sha = sha
    save_receipt(repo_root, receipt)
    return receipt, verdict


def ordered_model_from_contract(contract) -> str:
    """The tier a FROZEN CONTRACT declares, read off the contract's own routing row.

    THE SURFACE THAT CLOSES THE CIRCLE (`[#787]` clause 1). `record_model_reading` already
    refuses to be TOLD what ran. The other half was still a typed string: `--ordered` took the
    seat's word for what had been asked, so a receipt could agree with itself from the ordered
    side instead of the ran side — the same collapse, one column over, reached by the cheapest
    route the verb had. The two readings must come from independently produced surfaces or the
    check is circular, and these two are:

      * THE ORDERED TIER is written by the ARCHITECT at FREEZE, into the contract's
        `| model | mode | effort |` row, before any session exists. It is read here.
      * THE RAN MODEL is written by the CLI at RUN TIME, into the session transcript, by a
        process that never sees this file.

    Neither can be produced from the other, which is what makes a divergence visible at all. A
    verifier reading both sides off the launcher — the dispatch line for one and the receipt's
    own ordered field for the other — could not detect a launcher that ignored the order, which
    is precisely the defect that went unseen: `lane-x-689` froze `opusplan`, the resolved line
    printed `--model opusplan`, the freeze gate admitted it, `claude --print` resolved it, and
    84 of 84 assistant messages ran on `claude-sonnet-5`. Every surface that could be read
    agreed with the order. The only one that disagreed was the one nobody was reading.

    RAISES rather than defaulting when the contract declares no routing row. A default here
    would invent an order nobody placed and then certify a run against it.
    """
    path = Path(contract)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise MergeReceiptError(f"cannot read the contract {path}: {exc!r}") from exc
    try:
        from scripts import dispatch_surface as _ds  # noqa: PLC0415
    except ImportError:                              # pragma: no cover — path-shim fallback
        import dispatch_surface as _ds               # noqa: PLC0415
    row = _ds.contract_routing(text)
    if not row or not row.get("model"):
        raise MergeReceiptError(
            f"{path} carries no `| model | mode | effort |` routing row, so the tier it ORDERED "
            f"cannot be read from it. Refused rather than defaulted: a default would invent an "
            f"order nobody placed and then certify a run against it")
    return str(row["model"]).strip()


def record_model_reading(repo_root: Path, *, slug: str, ordered: str | None = None,
                         contract=None, worktree=None,
                         read=None) -> tuple[Receipt, _ra.ModelReading]:
    """Record WHAT WAS ORDERED and READ what actually ran, off the lane's own transcript.

    THE ASYMMETRY IS THE POINT, and it is `record_actions_verdict`'s asymmetry one field over.
    `ordered` is an argument because an order IS a declaration -- the contract's routing row says
    it, and nothing else can. The model that RAN is never an argument, here or in the CLI: it is
    read from the session store by `routing_agreement.model_reading`, which counts the assistant
    messages in the transcript filed under this lane's own working directory. A seat able to type
    the second value would produce a receipt that agrees with itself, which is `[#744]`'s false
    pass reached by the shortest route this module has.

    THE READING IS RECORDED WHATEVER IT SAYS -- a divergence, an unverifiable split tier and a
    store with nothing in it all land on the receipt, and leg 4 judges them afterwards. Writing
    only the agreeable readings would make the ledger a record of the times the check passed,
    which is the shape of evidence that cannot be audited.

    IT RECORDS NO STEP, and that is deliberate rather than an omission. A `StepTiming` would add
    the duration of a directory read to `recorded_seconds` and shift the baseline-commensurable
    split; the reading is a FACT ABOUT the arc, not a step OF it, and `merge_sha` -- the other
    fact about the arc -- is likewise a field rather than a step.

    `worktree` defaults to `repo_root`, which is where a lane's own session files its transcript.
    It is a parameter because an integrator recording an arc's reading is not standing in that
    arc's worktree, and the honest answer then is to name the directory rather than to read
    whichever transcript happens to be underfoot.

    `read` is the injection seam, the same shape and the same reason as `verdict_for`'s `fetch`
    in the verb above: a test drives the REAL comparison over a seeded transcript rather than
    asserting a state it typed itself.
    """
    if (ordered is None) == (contract is None):
        raise MergeReceiptError(
            "record_model_reading takes EXACTLY ONE of `ordered` (the tier, typed) and "
            "`contract` (the frozen contract it is read from). `contract` is the one that "
            "closes the circle -- see `ordered_model_from_contract`; `ordered` remains for a "
            "lane whose contract is not on this disk, and its honest limit is that it takes the "
            "caller's word for what was asked")
    if contract is not None:
        ordered = ordered_model_from_contract(contract)
    receipt = load_receipt(repo_root, slug)
    reader = read or _ra.model_reading
    reading = reader(ordered, Path(worktree) if worktree else repo_root)
    receipt.ordered_model = reading.ordered
    receipt.ran_model = reading.ran
    save_receipt(repo_root, receipt)
    return receipt, reading


def first_parent_merges(repo_root: Path, rev_range: str) -> list[str]:
    """The MERGE commits on the first-parent spine of `rev_range`, newest first.

    FAILS CLOSED. A bad range, a missing ref, a directory that is not a repository -- each
    RAISES rather than returning an empty list, because an empty list means "no merges here"
    and `require` would then report every merge in the range as receipted. That is verbatim the
    hole `[#742]` closed one organ over, where an errored `gh` call became an empty job list and
    printed **PASS**: a call that never completed reported as a clean result.
    """
    command = ["git", "-C", str(repo_root), "rev-list", "--first-parent", "--merges", rev_range]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, check=False, timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:
        raise MergeReceiptError(f"git rev-list could not be run: {exc!r}") from exc
    if proc.returncode != 0:
        raise MergeReceiptError(
            f"git rev-list --first-parent --merges {rev_range!r} exited {proc.returncode}: "
            f"{proc.stderr.strip()[:200]} -- refusing to read that as 'no merges in the range', "
            f"because an unreadable range and a clean one are different facts")
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def audit_merges(merge_shas: Sequence[str],
                 receipts: Sequence[Receipt]) -> list[tuple[str, str | None]]:
    """Per merge SHA, the problem with its receipt -- or None when there is none.

    DONE-CONTRACT CLAUSE 1's REFUSAL, as a pure function over a SHA list and a ledger, so the
    enforcement is testable without a git fixture and the git read stays in one place above.

    TWO WAYS TO FAIL, both of them the ruling's:

      * NO RECEIPT names this merge. Before `[#750]` the receipt was opened once per BATCH and
        carried no merge SHA at all, so this question had no answer and the whole enforcement was
        `/lane-integrate`'s own honest limit -- "it times what it is asked to time".
      * A RECEIPT NAMES IT AND IS NOT A USABLE MEASUREMENT. `REGRESSED`, or a verdict that
        cannot be read, is INCOMPLETE and the merge is refused (AY1-1) -- and the reason travels
        with the refusal, because a bar satisfied by opening and closing an empty receipt is not
        a bar.

    AN ARC CANNOT DISCHARGE A MERGE, by the same argument the `kind` filter makes for the
    median: an arc pays no merge and no teardown, so accepting one here would let the cheapest
    row in the ledger satisfy the bar for the most expensive act.

    SHA MATCHING IS PREFIX-TOLERANT IN BOTH DIRECTIONS, because a range's SHAs come from git in
    full and an integrator types short ones. Nothing else about the comparison is fuzzy.
    """
    named: dict[str, Receipt] = {r.merge_sha: r for r in receipts
                                 if r.kind == KIND_MERGE and r.merge_sha}
    out: list[tuple[str, str | None]] = []
    for sha in merge_shas:
        receipt = named.get(sha) or next(
            (r for key, r in named.items()
             if key.startswith(sha) or sha.startswith(key)), None)
        if receipt is None:
            out.append((sha, f"NO RECEIPT -- no kind={KIND_MERGE} row in {LEDGER_RELPATH} names "
                             f"this merge. Open one per merge and record its Actions verdict "
                             f"(`merge_receipt.py actions --slug <lane> --sha {sha[:12]} "
                             f"--baseline <its first parent>`)"))
            continue
        reason = receipt.incompleteness_reason()
        out.append((sha, None if reason is None
                    else f"receipt {receipt.slug!r} is INCOMPLETE: {reason}"))
    return out


def render_require(problems: Sequence[tuple[str, str | None]], rev_range: str) -> str:
    """`require`'s report. It NAMES the merges that passed as well as the ones that did not.

    AND IT NAMES ITS OWN VACUITY. A range holding no merge commit says so, because "0 of 0
    merges unreceipted" is precisely the plausible, flattering value `[#675]` is filed about --
    a mechanism returning a clean answer because the discriminating field is absent from what it
    looked at. An empty check and a clean walk must not render identically.
    """
    if not problems:
        return (f"merge receipts over {rev_range}: NO MERGE COMMIT in the range -- nothing was "
                f"checked, which is NOT the same as a clean walk. If you expected merges here, "
                f"the range is wrong: pass the FIRST merge's first parent as the base, so the "
                f"range covers the walk you actually made.")
    lines = [f"merge receipts over {rev_range}: {len(problems)} merge commit(s)"]
    for sha, problem in problems:
        lines.append(f"  {'ok     ' if problem is None else 'REFUSED'} {sha[:12]}"
                     + ("" if problem is None else f": {problem}"))
    bad = [sha for sha, problem in problems if problem]
    if bad:
        lines.append(f"  -> {len(bad)} of {len(problems)} merge(s) landed without a COMPLETE "
                     f"receipt: {', '.join(s[:12] for s in bad)}. A merge nobody itemised is the "
                     f"opaque wall number this whole programme exists to replace.")
    return "\n".join(lines)


def close_receipt(repo_root: Path, slug: str) -> Receipt:
    """Append the receipt to the durable ledger and remove the scratch.

    APPEND-ONLY: one line added, never a line rewritten (ADR-29/ADR-39, the `logs/TOKEN-LOG.md`
    class). The scratch is removed only AFTER the append succeeds, so a failure leaves the
    in-flight record rather than losing it.
    """
    receipt = load_receipt(repo_root, slug)
    receipt.closed = _now()
    line = json.dumps(receipt.to_dict(), sort_keys=True)
    path = ledger_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    scratch_path(repo_root, slug).unlink(missing_ok=True)
    return receipt


def read_ledger(repo_root: Path) -> list[Receipt]:
    """Every receipt in the ledger, oldest first, WHETHER OR NOT IT IS COMPLETE.

    THE NAME OF THIS FUNCTION IS "READ", and until 2026-09-13 its docstring said "Every closed
    receipt" while it filtered nothing -- the claim was simply untrue, and `median_report` and
    `MedianReport.render` both inherited it (`n=… closed receipt(s)` over rows nothing had
    checked). The read stays unfiltered on purpose, because a caller wanting the ledger's real
    contents should get them; the judgement lives in `Receipt.is_complete` and the filtering in
    `median_report`, where it is reported rather than silent (`[#744]`).

    A malformed line is REPORTED and skipped rather than crashing the read: the ledger is
    append-only, so a bad line cannot be repaired in place, and one bad line must not make every
    good one unreadable.
    """
    path = ledger_path(repo_root)
    if not path.exists():
        return []
    out: list[Receipt] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            out.append(Receipt.from_dict(json.loads(raw)))
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning("%s line %d is unreadable and was skipped: %s", LEDGER_RELPATH,
                           number, exc)
    return out


# --- the numbers -----------------------------------------------------------------------------

@dataclass(frozen=True)
class MedianReport:
    """Target 3.6's answer, and it NEVER collapses to one number.

    `[#675]` is the row about a confident figure with a hidden disagreement inside it, so every
    field a reader needs to weigh the median travels with it: n, the range, the quartiles, and
    the baseline's own spread.
    """
    n: int
    median_minutes: float
    minimum: float
    maximum: float
    quartiles: tuple[float, float, float] | None
    per_merge: tuple[float, ...]
    kind: str = KIND_MERGE
    #: Receipts in the ledger of some OTHER kind. Reported, never silently dropped.
    excluded: int = 0
    #: Receipts of the RIGHT kind that were not usable measurements (`[#744]`). Reported for
    #: exactly the reason `excluded` is: a median over a thinned sample must never render as a
    #: median over a full one.
    incomplete: int = 0
    #: One line per excluded receipt, naming it and WHY. A count alone cannot tell a reader
    #: whether the ledger is dirty or the merges are.
    incomplete_reasons: tuple[str, ...] = ()

    def meets_target(self) -> bool:
        return self.median_minutes < TARGET_MEDIAN_MIN

    def render(self) -> str:
        skipped = (f" ({self.excluded} receipt(s) of another kind EXCLUDED -- a median over "
                   f"mixed arcs answers a different question than target 3.6 asked, and answers "
                   f"it flatteringly)" if self.excluded else "")
        if self.incomplete:
            skipped += (f" ({self.incomplete} INCOMPLETE {self.kind} receipt(s) EXCLUDED -- an "
                        f"incomplete receipt times a different event than the one this median "
                        f"claims to summarise)")
        if self.n == 0:
            head = (f"{self.kind} minutes: NO RECEIPTS. The median is undefined, not zero -- "
                    f"{LEDGER_RELPATH} holds no COMPLETE closed {self.kind} receipt yet."
                    f"{skipped}")
            return "\n".join([head, *(f"  EXCLUDED {r}" for r in self.incomplete_reasons)])
        lines = [
            f"{self.kind} minutes over n={self.n} complete, closed receipt(s){skipped}",
            *(f"  EXCLUDED {r}" for r in self.incomplete_reasons),
            f"  median   {self.median_minutes:.1f} min"
            f"   (target 3.6: under {TARGET_MEDIAN_MIN:.0f} -> "
            f"{'MET' if self.meets_target() else 'NOT MET'})",
            f"  range    {self.minimum:.1f} .. {self.maximum:.1f} min",
        ]
        if self.quartiles is not None:
            q1, q2, q3 = self.quartiles
            lines.append(f"  quartiles {q1:.1f} / {q2:.1f} / {q3:.1f} min")
        lines.append("  per merge " + ", ".join(f"{m:.1f}" for m in self.per_merge))
        lines.append("")
        lines.append(
            f"  AGAINST THE BASELINE frozen {BASELINE_FROZEN}: "
            f"{BASELINE_WALL_MIN:.0f} min wall = {BASELINE_TESTS_MIN} targeted tests + "
            f"{BASELINE_CEREMONY_MIN} residual ceremony.")
        lines.append(
            f"  THE BASELINE'S OWN SPREAD IS PART OF IT and is not hidden here: its two "
            f"itemised views read "
            f"{' and '.join(f'~{v:.0f}' for v in BASELINE_ITEMISED_VIEWS_MIN)} min, which "
            f"disagree with each other and with the {BASELINE_WALL_MIN:.0f} min wall figure"
            + ("" if BASELINE_MEASURED_ON_FREEZE_DAY else
               ", and NOTHING WAS MEASURED on the day it was frozen")
            + ". Any improvement stated against it inherits that uncertainty.")
        if self.n < 5:
            lines.append(
                f"  n={self.n} IS A SMALL SAMPLE. This median is what these {self.n} merge(s) "
                f"cost, not an estimate of what a merge costs.")
        return "\n".join(lines)


def median_report(receipts: Sequence[Receipt], kind: str = KIND_MERGE) -> MedianReport:
    """The median wall time for one KIND of arc, with its spread. Target 3.6.

    Filtering by kind is not a convenience. Target 3.6 asks for median MERGE minutes, and a
    ledger that also holds lane commit arcs would answer a cheaper question under the same name.

    TWO FILTERS, NOT ONE, since `[#744]` (2026-09-13). Kind says whether a receipt is timing the
    right KIND of thing; completeness says whether it is timing anything at all. Before the
    second existed, an abandoned receipt, a receipt with a failed step and a receipt recording
    one step out of four each counted at full weight -- and the live ledger, holding exactly two
    rows with failed steps, one of them 0.0 minutes, reported `median 9.4 min (target 3.6: MET)`.

    COMPLETENESS IS UNCONDITIONAL AND HAS NO FLAG, which is the `--strict` decision `[#744]`'s
    last clause asks for, made here rather than left implicit. `median --strict` means "exit 1
    when the median does not meet target 3.6" and keeps exactly that meaning: a flag that also
    toggled completeness would make this false pass OPT-OUTABLE, and a median over incomplete
    receipts is not a laxer reading of the number -- it is a different number.
    """
    wanted = [r for r in receipts if r.kind == kind]
    excluded = len(receipts) - len(wanted)

    complete = [r for r in wanted if r.is_complete()]
    reasons = tuple(f"{r.slug}: {r.incompleteness_reason()}"
                    for r in wanted if not r.is_complete())
    for reason in reasons:
        logger.warning("excluded from the %s median -- %s", kind, reason)

    minutes = sorted(r.wall_seconds() / 60.0 for r in complete)
    common = dict(kind=kind, excluded=excluded, incomplete=len(reasons),
                  incomplete_reasons=reasons)
    if not minutes:
        return MedianReport(0, 0.0, 0.0, 0.0, None, (), **common)
    quartiles = None
    if len(minutes) >= 4:
        cut = statistics.quantiles(minutes, n=4, method="inclusive")
        quartiles = (cut[0], cut[1], cut[2])
    return MedianReport(n=len(minutes), median_minutes=statistics.median(minutes),
                        minimum=minutes[0], maximum=minutes[-1], quartiles=quartiles,
                        per_merge=tuple(minutes), **common)


def render_summary(receipt: Receipt) -> str:
    """The itemised view -- target 3.1's deliverable. Per-step minutes, then both splits."""
    lines = [f"receipt {receipt.slug}  kind={receipt.kind}  batch={receipt.batch or '-'}  "
             f"merge={receipt.merge_sha[:12] if receipt.merge_sha else '-'}  "
             f"opened={receipt.opened}  host={receipt.host}  "
             f"concurrent_seats={receipt.concurrent_seats}"]
    if not receipt.steps:
        lines.append("  (no steps recorded -- an unrecorded step reads exactly like a fast one)")
    for step in receipt.steps:
        raced = f"  raced with {', '.join(step.raced_with)}" if step.raced_with else ""
        verdict = "ok" if step.ok else f"FAILED rc={step.returncode}"
        # THE STATE PRINTS BESIDE THE EXIT CODE, never instead of it. `[#750]` took the exit
        # code out of the completeness predicate; taking it out of the REPORT as well would have
        # laundered a red step into silence and become the false pass it exists to refuse.
        state = f"  verdict {step.verdict_state}" if step.verdict_state else ""
        # AND THE BASELINE IT WAS ATTRIBUTED AGAINST. A differential means nothing without the
        # commit it is a differential FROM: `PRE-EXISTING` against an unnamed baseline is a claim,
        # not a reading. It is derived rather than typed, and printing it is what lets a reader
        # check that rather than take it on trust.
        against = f" vs {step.baseline_sha[:12]}" if step.baseline_sha else ""
        # START AND END, ALONGSIDE THE MINUTES -- the done-contract's three things, not two
        # shown and one implied. `ended` is None on an unparseable `started` (a receipt written
        # before this field, or this suite's own placeholder), and that gap is named rather
        # than rendered as a fabricated clock reading.
        when = f"  {step.started} -> {step.ended or 'unknown'}"
        lines.append(f"  {step.minutes:6.2f} min  [{step.step_class:8s}] {step.step:12s} "
                     f"{verdict}{state}{against}{raced}{when}")
    wall = receipt.wall_seconds() / 60.0
    recorded = receipt.recorded_seconds() / 60.0
    serial = receipt.serial_seconds() / 60.0
    unrecorded = receipt.unrecorded_seconds() / 60.0
    lines.append("")
    lines.append(f"  WALL   {wall:.2f} min   (opened {receipt.opened} -> "
                 f"closed {receipt.closed or 'STILL OPEN, measured to now'})")
    lines.append(f"  RECORDED {recorded:.2f} min across {len(receipt.steps)} timed step(s); "
                 f"{unrecorded:.2f} min UNRECORDED between them"
                 + (f" -- the baseline's residual ceremony is {BASELINE_CEREMONY_MIN} min and "
                    f"lives exactly here" if unrecorded > 1e-6 else "")
                 + (f"   (serial would be {serial:.2f} min -- {serial - recorded:.2f} min saved "
                    f"by racing)" if serial > recorded + 1e-6 else ""))
    state = receipt.suite_verdict()
    if state:
        lines.append(f"  SUITE VERDICT {state} -- "
                     + ("COMPLETE on this leg (ruling AY1-1), and NOT a statement that the run "
                        "was green" if state in COMPLETE_SUITE_STATES else
                        "INCOMPLETE: this receipt cannot discharge its merge"))
    # THE MODEL LINE ALWAYS PRINTS, including when there is nothing to print -- `[#752]`. An
    # absence a reader cannot SEE reads as a clean bill, and this module exists because a
    # plausible answer was returned where the discriminating field was simply not there. So the
    # `unread` state gets a sentence of its own rather than a blank space where a line would be.
    model_state, model_detail = _ra.compare_order(receipt.ordered_model, receipt.ran_model)
    lines.append(f"  MODEL {model_state} -- {model_detail}"
                 + ("; this receipt makes NO CLAIM about the tier its arc ran at"
                    if model_state == _ra.STATE_UNREAD else ""))
    tests_min, residual_min = receipt.baseline_split()
    lines.append(f"  BASELINE-COMMENSURABLE SPLIT: {tests_min:.2f} tests + "
                 f"{residual_min:.2f} residual ceremony  "
                 f"(review and the UNRECORDED remainder are folded into ceremony here, as the "
                 f"baseline's own two buckets do)")
    if abs(tests_min + residual_min - wall) > 1.0 / 60.0:
        lines.append(f"  THE SPLIT AND THE WALL FIGURE DISAGREE by "
                     f"{tests_min + residual_min - wall:+.2f} min, and the disagreement is "
                     f"REPORTED rather than clamped: a raced group costs its longest member ONCE "
                     f"in wall time and counts IN FULL per class, so concurrency makes the two "
                     f"views differ by the overlap. The baseline carries its own disagreement; "
                     f"this receipt carries its own too.")
    classes = receipt.by_class()
    lines.append("  THREE-WAY SPLIT: "
                 + ", ".join(f"{k} {v / 60.0:.2f} min" for k, v in classes.items())
                 + "   (review is split out because target 3.5 forbids trading it away, and a "
                   "binary split cannot show that it was not)")
    missing = receipt.missing_required()
    if missing:
        lines.append(f"  UNRECORDED required step(s): {', '.join(missing)} -- an unrecorded step "
                     f"reads exactly like a fast one, so this receipt UNDERSTATES the merge")
    failed = receipt.failed_steps()
    if failed:
        lines.append(f"  FAILED step(s): {', '.join(s.step for s in failed)}")
    return "\n".join(lines)


# --- CLI -------------------------------------------------------------------------------------

def _root(repo_root: str | None) -> Path:
    return Path(repo_root) if repo_root else _REPO_ROOT


#: Where a lane's own worktree lives, under the repo root -- `EnterWorktree` and `--worktree`
#: both file it here, so the slug alone names it.
LANE_WORKTREE_TEMPLATE = ".claude/worktrees/{slug}"


def default_lane_worktree(repo_root: Path, slug: str) -> Path | None:
    """The lane's worktree when it exists on this disk, else None (R-W3-5).

    THE INTEGRATOR IS NOT IN THE LANE. `models` reads the transcript filed under a working
    directory, and with no `--worktree` that directory was the caller's own -- the integrator's,
    whose transcript is a different session running a different model. The declared `merge` row
    carries no `--worktree`, so every real merge would have compared the integrator's run to the
    lane's order and refused. The slug is enough to name the lane's directory, so it is read from
    there when it exists; an absent directory returns None and the caller keeps the old, honest
    default of the repo root (a lane that ran in the repo root files its transcript there).
    """
    candidate = repo_root / LANE_WORKTREE_TEMPLATE.format(slug=slug)
    return candidate if candidate.is_dir() else None


@click.group(help="Per-step merge minutes, recorded into a durable receipt ([#675] 3.1/3.3/3.6).")
@click.option("--repo-root", default=None, type=click.Path(file_okay=False),
              help="repo root [default: this script's parent]")
@click.pass_context
def cli(ctx: click.Context, repo_root: str | None) -> None:
    ctx.ensure_object(dict)
    ctx.obj["root"] = _root(repo_root)


@cli.command("open")
@click.option("--slug", required=True, help="what this merge is called, e.g. the batch's lane")
@click.option("--batch", default="", help="the batch this merge belongs to")
@click.option("--kind", type=click.Choice(RECEIPT_KINDS), default=KIND_MERGE, show_default=True,
              help="'merge' is an integrator's merge (what target 3.6 measures); 'arc' is any "
                   "other timed arc, counted separately so it cannot flatter the median")
@click.pass_context
def cmd_open(ctx: click.Context, slug: str, batch: str, kind: str) -> None:
    """Start a receipt for one merge."""
    try:
        receipt = open_receipt(ctx.obj["root"], slug=slug, batch=batch, kind=kind)
    except MergeReceiptError as exc:
        raise click.ClickException(str(exc)) from exc
    logger.info("opened %s receipt %s (concurrent_seats=%d)", receipt.kind, receipt.slug,
                receipt.concurrent_seats)


@cli.command("time", context_settings={"ignore_unknown_options": True})
@click.option("--slug", required=True)
@click.option("--step", required=True, help=f"step id; {', '.join(REQUIRED_STEPS)} are expected")
@click.option("--class", "step_class", type=click.Choice(STEP_CLASSES), default=CLASS_CEREMONY,
              show_default=True)
@click.argument("command", nargs=-1, required=True, type=click.UNPROCESSED)
@click.pass_context
def cmd_time(ctx: click.Context, slug: str, step: str, step_class: str,
             command: tuple[str, ...]) -> None:
    """Run COMMAND, time it, record it. Exits with the CHILD'S code.

    Put `--` before COMMAND so its own flags are not read as this wrapper's.
    """
    root = ctx.obj["root"]
    try:
        receipt = load_receipt(root, slug)
    except MergeReceiptError as exc:
        raise click.ClickException(str(exc)) from exc
    timing = run_timed(command, step=step, step_class=step_class, cwd=root)
    receipt.steps.append(timing)
    save_receipt(root, receipt)
    logger.info("step %s: %.2f min (%s)", step, timing.minutes,
                "ok" if timing.ok else f"FAILED rc={timing.returncode}")
    # The child's verdict is passed through unchanged: a wrapper that swallowed a failing merge
    # step would turn a stopwatch into a gate that lets things through.
    raise SystemExit(0 if timing.ok else (timing.returncode or 1))


@cli.command("race")
@click.option("--slug", required=True)
@click.option("--job", "jobs", multiple=True, required=True,
              help="'<step>:<class>=<command>' -- repeatable; all jobs run CONCURRENTLY")
@click.pass_context
def cmd_race(ctx: click.Context, slug: str, jobs: tuple[str, ...]) -> None:
    """Run several steps CONCURRENTLY and record each (target 3.3).

    Every job's exit code is recorded and this verb exits non-zero if ANY job failed. Running
    checks in parallel is a scheduling change; reporting only the winner would be a coverage
    change wearing one.
    """
    root = ctx.obj["root"]
    try:
        receipt = load_receipt(root, slug)
    except MergeReceiptError as exc:
        raise click.ClickException(str(exc)) from exc

    parsed: list[tuple[str, str, str]] = []
    for spec in jobs:
        head, sep, command = spec.partition("=")
        if not sep or not command.strip():
            raise click.ClickException(
                f"--job {spec!r} is not '<step>:<class>=<command>'; the '=' and a command are "
                f"required, and a job with no command is a step nobody ran")
        step, _, step_class = head.partition(":")
        step_class = step_class or CLASS_CEREMONY
        if step_class not in STEP_CLASSES:
            raise click.ClickException(
                f"--job {spec!r} names class {step_class!r}, outside "
                f"{{{', '.join(STEP_CLASSES)}}}")
        parsed.append((step.strip(), step_class, command))

    names = [step for step, _, _ in parsed]
    if len(set(names)) != len(names):
        raise click.ClickException(
            f"--job names repeat ({', '.join(names)}); one step id is one measurement")

    started = _now()
    clock = time.perf_counter()
    procs = []
    for step, step_class, command in parsed:
        # `shell=True`: a raced job is given as ONE string so the operator writes the same
        # command line they would type. The strings come from the integrator's own terminal,
        # not from a contract file -- the arbitrary-execution concern `Assert-ClaudeCommand`
        # guards belongs to a file the repo passes around, which this is not.
        procs.append((step, step_class, command, time.perf_counter(),
                      subprocess.Popen(command, cwd=str(root), shell=True)))
    for step, step_class, command, job_clock, proc in procs:
        rc = proc.wait()
        receipt.steps.append(StepTiming(
            step=step, step_class=step_class,
            seconds=round(time.perf_counter() - job_clock, 3), ok=rc == 0, returncode=rc,
            command=command, started=started,
            raced_with=tuple(n for n in names if n != step)))
    save_receipt(root, receipt)
    wall = time.perf_counter() - clock
    recorded = [s for s in receipt.steps if s.step in set(names)]
    serial = sum(s.seconds for s in recorded)
    logger.info("raced %d job(s) in %.2f min; serial would be %.2f min (%.2f min saved)",
                len(parsed), wall / 60.0, serial / 60.0, (serial - wall) / 60.0)
    failed = [s.step for s in recorded if not s.ok]
    if failed:
        logger.error("raced job(s) FAILED: %s", ", ".join(failed))
    raise SystemExit(1 if failed else 0)


@cli.command("actions")
@click.option("--slug", required=True)
@click.option("--sha", required=True, help="the MERGE commit whose Actions run is read; this "
                                           "receipt is bound to it")
@click.option("--baseline", default=None,
              help="OPTIONAL and normally OMITTED: the baseline is DERIVED from the merge's "
                   "first parent, so the differential means 'what this merge changed'. Pass it "
                   "only to assert what you expect -- a value that is not <sha>^1 is REFUSED, "
                   "because attributing against any other commit silently converts a REGRESSION "
                   "into a pre-existing red")
@click.option("--step", default=ACTIONS_STEP, show_default=True,
              help="the step id to record under; a retry records under its own id and wins")
@click.pass_context
def cmd_actions(ctx: click.Context, slug: str, sha: str, baseline: str | None,
                step: str) -> None:
    """Read this merge's Actions verdict, RECORD ITS STATE, exit with the verdict's own code.

    There is deliberately no way to hand this verb a verdict; it reads one or it refuses.
    """
    try:
        _receipt, verdict = record_actions_verdict(ctx.obj["root"], slug=slug, sha=sha,
                                                   baseline=baseline, step=step)
    except MergeReceiptError as exc:
        raise click.ClickException(str(exc)) from exc
    # PRINTED ON SUCCESS TOO, inherited from the tool this replaced: a gate silent on success
    # has not been read, it has been assumed -- and target 3.2 is about the integrator READING.
    click.echo(verdict.render())
    logger.info("recorded suite verdict %s on step %s of receipt %s (merge %s)",
                verdict.state, step, slug, sha[:12])
    raise SystemExit(0 if verdict.ok else 1)


@cli.command("models")
@click.option("--slug", required=True)
@click.option("--contract", "contract", type=click.Path(exists=True, dir_okay=False,
                                                       path_type=Path), default=None,
              help="the FROZEN CONTRACT to read the ordered tier off ([#787]) -- preferred: it "
                   "is a surface the launcher did not write. Exactly one of this and --ordered")
@click.option("--ordered", required=False, default=None,
              help="the tier the contract's routing row ORDERED for this lane, e.g. opus. It is "
                   "declared because an order IS a declaration -- and it is the ONLY half of the "
                   "pair this verb accepts")
@click.option("--worktree", default=None, type=click.Path(file_okay=False),
              help="the lane's working directory [default: .claude/worktrees/<slug> under the "
                   "repo root when that exists, else the repo root]; the session store files a "
                   "transcript under it, and that transcript is the measurement. An explicit "
                   "value always wins")
@click.pass_context
def cmd_models(ctx: click.Context, slug: str, contract: Path | None, ordered: str | None,
               worktree: str | None) -> None:
    """Record the ordered tier and READ, off the lane's own transcript, what it actually ran.

    There is deliberately no flag that asserts what ran -- not under any spelling. This verb
    reads it or it records the gap; a receipt able to be told what it ran would agree with
    itself, and agreement with itself is what `lane-x-689` already had.

    Exit follows the STATE: 0 only on agreement. A gap exits non-zero too (Z-G4) -- a check that
    cannot compute its ground truth must not read as a pass to anything shelling out to it.
    """
    if worktree is None:
        worktree = default_lane_worktree(ctx.obj["root"], slug)
    try:
        _receipt, reading = record_model_reading(ctx.obj["root"], slug=slug, ordered=ordered,
                                                 contract=contract, worktree=worktree)
    except MergeReceiptError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(f"{reading.state} -- {reading.detail}")
    raise SystemExit(0 if reading.agrees else 1)


@cli.command("require")
@click.option("--range", "rev_range", required=True,
              help="the integrator's own walk range, e.g. '<the first merge's FIRST PARENT>..HEAD'")
@click.pass_context
def cmd_require(ctx: click.Context, rev_range: str) -> None:
    """REFUSE a merge in RANGE that landed without a COMPLETE receipt (`[#750]`, ruling AY1-1).

    HONEST LIMITS, both of them about scope rather than logic. (1) It judges the RANGE you give
    it, not the repository: it is a checklist row the integrator runs over their own walk, and
    it is wired into no hook, because armed tree-wide it would refuse every merge that predates
    the receipt. (2) It reads the LEDGER, so a receipt still open is a receipt it cannot see --
    close each one at the end of its lane's block, before running this.
    """
    root = ctx.obj["root"]
    try:
        shas = first_parent_merges(root, rev_range)
    except MergeReceiptError as exc:
        raise click.ClickException(str(exc)) from exc
    problems = audit_merges(shas, read_ledger(root))
    click.echo(render_require(problems, rev_range))
    raise SystemExit(1 if any(problem for _sha, problem in problems) else 0)


@cli.command("close")
@click.option("--slug", required=True)
@click.pass_context
def cmd_close(ctx: click.Context, slug: str) -> None:
    """Append this receipt to the durable ledger and print its itemised summary."""
    try:
        receipt = close_receipt(ctx.obj["root"], slug)
    except MergeReceiptError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(render_summary(receipt))
    logger.info("appended to %s", LEDGER_RELPATH)


@cli.command("summary")
@click.option("--slug", default=None, help="an OPEN receipt; omitted, the last closed one")
@click.option("--strict", is_flag=True, default=False,
              help=f"exit 1 unless every required step is recorded ({', '.join(REQUIRED_STEPS)})")
@click.pass_context
def cmd_summary(ctx: click.Context, slug: str | None, strict: bool) -> None:
    """Itemised per-step minutes for one receipt (target 3.1)."""
    root = ctx.obj["root"]
    if slug:
        try:
            receipt = load_receipt(root, slug)
        except MergeReceiptError as exc:
            raise click.ClickException(str(exc)) from exc
    else:
        closed = read_ledger(root)
        if not closed:
            raise click.ClickException(
                f"{LEDGER_RELPATH} holds no closed receipt, and no --slug was given")
        receipt = closed[-1]
    click.echo(render_summary(receipt))
    if strict and receipt.missing_required():
        raise SystemExit(1)


@cli.command("median")
@click.option("--strict", is_flag=True, default=False,
              help="exit 1 when the median does not meet target 3.6. THE TARGET AXIS ONLY -- "
                   "completeness is enforced unconditionally and has no flag ([#744]), because "
                   "a median over incomplete receipts is a different number rather than a laxer "
                   "reading of this one")
@click.option("--kind", type=click.Choice(RECEIPT_KINDS), default=KIND_MERGE, show_default=True)
@click.pass_context
def cmd_median(ctx: click.Context, strict: bool, kind: str) -> None:
    """Median merge minutes with its spread (target 3.6). Never prints a bare number."""
    report = median_report(read_ledger(ctx.obj["root"]), kind=kind)
    click.echo(report.render())
    if strict and not report.meets_target():
        raise SystemExit(1)


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli(obj={})
