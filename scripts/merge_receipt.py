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

HONEST LIMITS, stated so a number from here is not over-read:

  * **It times what it is asked to time.** A merge step run without the prefix is invisible, and
    an unrecorded step reads exactly like a fast one. `summary --strict` refuses a receipt whose
    recorded steps do not cover `REQUIRED_STEPS`; nothing forces `--strict`.
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
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Sequence

import click

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
    returncode: Optional[int]
    command: str
    started: str
    #: Set when this step ran concurrently with others, naming the `race` group it belonged to.
    raced_with: tuple[str, ...] = ()

    @property
    def minutes(self) -> float:
        return self.seconds / 60.0


@dataclass
class Receipt:
    """One merge, itemised. Serialised to the scratch file between steps."""
    slug: str
    batch: str
    opened: str
    host: str
    concurrent_seats: int
    kind: str = KIND_MERGE
    steps: list[StepTiming] = field(default_factory=list)
    closed: Optional[str] = None

    # -- arithmetic ---------------------------------------------------------------------------

    def wall_seconds(self) -> float:
        """Total wall time, with a RACED GROUP COUNTED ONCE at its longest member.

        Summing raced steps would report the serial cost of a parallel run and erase the very
        saving target 3.3 exists to produce — the receipt would show the improvement as no
        improvement. Grouping is by `raced_with` membership, which `race` sets.
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

    def serial_seconds(self) -> float:
        """What the same steps would have cost run one after another — the counterfactual the
        parallel saving is measured against, kept explicit rather than implied."""
        return sum(s.seconds for s in self.steps)

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
        `84 = 11.3 + 72.7`. Folding is stated, never silent."""
        classes = self.by_class()
        tests = classes.get(CLASS_TESTS, 0.0) / 60.0
        residual = (classes.get(CLASS_REVIEW, 0.0)
                    + classes.get(CLASS_CEREMONY, 0.0)) / 60.0
        return tests, residual

    def missing_required(self) -> list[str]:
        recorded = {s.step for s in self.steps}
        return [s for s in REQUIRED_STEPS if s not in recorded]

    def failed_steps(self) -> list[StepTiming]:
        return [s for s in self.steps if not s.ok]

    # -- completeness (`[#744]`) --------------------------------------------------------------

    def incompleteness_reason(self) -> Optional[str]:
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

        The legs, in the order a reader should think about them:

          1. NEVER CLOSED -- it was opened and abandoned. Its wall time is whatever had elapsed
             when someone stopped writing, which is not a duration of anything.
          2. NO STEPS -- wall time 0.0, the most dangerous plausible value this module can
             produce: it meets target 3.6 spectacularly and means nothing.
          3. A FAILED STEP -- the arc did not complete, so its duration times a different event
             than the one the median claims to summarise.
          4. A MERGE MISSING A REQUIRED STEP -- an unrecorded step reads exactly like a fast
             one, which is this module's founding complaint.

        LEG 4 IS SCOPED TO `kind == merge`, and that is a decision rather than an oversight.
        `REQUIRED_STEPS` is the INTEGRATOR's walk, and this module's own docstring says an arc
        "pays no merge and no teardown"; holding an arc to it would make `median --kind arc`
        permanently n=0 for a reason that is not incompleteness. Legs 1-3 bind both kinds.
        """
        if self.closed is None:
            return "never closed -- opened and abandoned, so its wall time times nothing"
        if not self.steps:
            return "no steps recorded -- wall time 0.0, which is not a measurement"
        failed = self.failed_steps()
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
            {**asdict(s), "raced_with": list(s.raced_with)} for s in self.steps]
        data["wall_seconds"] = round(self.wall_seconds(), 3)
        data["serial_seconds"] = round(self.serial_seconds(), 3)
        tests_min, residual_min = self.baseline_split()
        data["baseline_split_minutes"] = {"tests": round(tests_min, 2),
                                          "residual_ceremony": round(residual_min, 2)}
        data["by_class_seconds"] = {k: round(v, 3) for k, v in self.by_class().items()}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Receipt":
        steps = [StepTiming(step=s["step"], step_class=s["step_class"], seconds=s["seconds"],
                            ok=s["ok"], returncode=s.get("returncode"),
                            command=s.get("command", ""), started=s.get("started", ""),
                            raced_with=tuple(s.get("raced_with", ())))
                 for s in data.get("steps", [])]
        # A row written before `kind` existed is a MERGE receipt — that is what the ledger held
        # when the field was absent, so the default reads the history correctly rather than
        # conveniently.
        return cls(slug=data["slug"], batch=data.get("batch", ""), opened=data["opened"],
                   host=data.get("host", ""), concurrent_seats=data.get("concurrent_seats", 0),
                   kind=data.get("kind", KIND_MERGE), steps=steps, closed=data.get("closed"))


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
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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
              cwd: Optional[Path] = None) -> StepTiming:
    """Run `command`, timed. The child's stdout/stderr are NOT captured — they go straight to the
    operator's terminal, because a wrapper that swallowed a merge step's output would make itself
    the thing between the integrator and their own merge."""
    started = _now()
    clock = time.perf_counter()
    try:
        proc = subprocess.run(list(command), cwd=str(cwd) if cwd else None, check=False)
        rc: Optional[int] = proc.returncode
    except (OSError, subprocess.SubprocessError) as exc:
        logger.error("step %s could not be run: %r", step, exc)
        rc = None
    elapsed = time.perf_counter() - clock
    return StepTiming(step=step, step_class=step_class, seconds=round(elapsed, 3),
                      ok=rc == 0, returncode=rc, command=" ".join(command), started=started)


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
             f"opened={receipt.opened}  host={receipt.host}  "
             f"concurrent_seats={receipt.concurrent_seats}"]
    if not receipt.steps:
        lines.append("  (no steps recorded -- an unrecorded step reads exactly like a fast one)")
    for step in receipt.steps:
        raced = f"  raced with {', '.join(step.raced_with)}" if step.raced_with else ""
        verdict = "ok" if step.ok else f"FAILED rc={step.returncode}"
        lines.append(f"  {step.minutes:6.2f} min  [{step.step_class:8s}] {step.step:12s} "
                     f"{verdict}{raced}")
    wall = receipt.wall_seconds() / 60.0
    serial = receipt.serial_seconds() / 60.0
    lines.append("")
    lines.append(f"  WALL   {wall:.2f} min"
                 + (f"   (serial would be {serial:.2f} min -- "
                    f"{serial - wall:.2f} min saved by racing)" if serial > wall + 1e-6 else ""))
    tests_min, residual_min = receipt.baseline_split()
    lines.append(f"  BASELINE-COMMENSURABLE SPLIT: {tests_min:.2f} tests + "
                 f"{residual_min:.2f} residual ceremony  "
                 f"(review is folded into ceremony here, as the baseline's own two buckets do)")
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

def _root(repo_root: Optional[str]) -> Path:
    return Path(repo_root) if repo_root else _REPO_ROOT


@click.group(help="Per-step merge minutes, recorded into a durable receipt ([#675] 3.1/3.3/3.6).")
@click.option("--repo-root", default=None, type=click.Path(file_okay=False),
              help="repo root [default: this script's parent]")
@click.pass_context
def cli(ctx: click.Context, repo_root: Optional[str]) -> None:
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
def cmd_summary(ctx: click.Context, slug: Optional[str], strict: bool) -> None:
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
