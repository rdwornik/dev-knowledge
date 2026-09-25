#!/usr/bin/env python
"""context_reclamation.py -- clearing CONTEXT, which is not the same act as replacing a
SESSION (`[#792]`).

WHY THIS IS A SEPARATE FILE FROM `scripts/resource_lifecycle.py`
=================================================================================================
Because the two quantities have different drivers, measured 2026-09-15 over 681 hub-slug
transcripts and 92,743 priced turns (`docs/audits/2026-09-15-technical-lane-aa-14-resource-
lifecycle.md` section 2):

  * per-turn COST tracks accumulated TURN COUNT. Across turn-index bands it moves
    0.701 -> 1.247 x the session's own median while median context per call moves
    100,662 -> 350,757 tokens. **Hold turn index in the band 50-100 and let elapsed time vary
    eight-fold, and cost moves only 0.915 -> 1.003.** So cost is context-driven, and clearing
    context genuinely reclaims it.
  * process MEMORY tracks session AGE, and clearing context does not touch it.

**Building one mechanism for both is why neither works today.** Keeping them in one module
would make a shared constant the path of least resistance, so they are two modules and
`tests/test_context_reclamation.py` asserts they share no threshold value -- not merely no
name, no NUMBER. Two mechanisms that agree on a constant are one mechanism with two front
doors.

This module therefore has NO opinion about memory. It cannot recommend a restart, it cannot
read an RSS, and a test refuses any constant here whose name mentions one.

THE ACCEPTANCE CRITERION IS THE TRIP-TEST, NOT THE TRIGGER
=================================================================================================
Deciding to clear is the easy half. **The contract's criterion is that the seat resumes from
FILES ALONE with no loss** -- "a clear that loses state is not a reclamation, it is an outage".
So a checkpoint is not a moment in time, it is a moment at which a declared RESUME SET is
resolvable on disk, and `reclaim` REFUSES when any key in that set does not resolve. The
refusal comes BEFORE the context is gone, which is the only time it is worth anything.

WHAT IS DERIVED
=================================================================================================
`RECLAIM_MULTIPLE` is derived from a fire-rate table over the whole local corpus rather than
chosen; `THRESHOLD_PROVENANCE` carries the table and a test asserts it is still there. The
one thing NOT controlled for is work class -- no transcript field carries it -- and that
limit is written into the provenance rather than left for a reader to discover.

CALL SURFACE
=================================================================================================

    uv run --locked python scripts/context_reclamation.py checkpoints
    uv run --locked python scripts/context_reclamation.py verify --kind lane --key K=PATH ...
"""
from __future__ import annotations

import hashlib
import json
import logging
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Mapping, Sequence

import click

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("context-reclamation")


# ============================================================ the trigger, derived not selected

#: A turn at or above this multiple of the seat's OWN running median is "expensive".
RECLAIM_MULTIPLE = 1.30
#: Consecutive expensive turns before the trigger fires. One spike is noise.
SUSTAINED_TURNS = 5
#: Turns before the seat has a median worth comparing against.
WARMUP_TURNS = 20

#: WHAT EACH THRESHOLD MEASURES. Asserted DISJOINT from `resource_lifecycle.THRESHOLD_UNITS`,
#: which is the checkable form of "the two regimes are not one resource". Note what this module
#: cannot express: there is no memory unit here and there can never be one, because a
#: reclamation organ that acquires a memory opinion has merged back into the mechanism the
#: measurement separated it from.
THRESHOLD_UNITS: dict[str, str] = {
    "RECLAIM_MULTIPLE": "ratio-to-own-running-median",
    "SUSTAINED_TURNS": "consecutive-turns",
    "WARMUP_TURNS": "turns-before-a-median-means-anything",
}

THRESHOLD_PROVENANCE: dict[str, str] = {
    "RECLAIM_MULTIPLE": (
        "DERIVED 2026-09-15 from a fire-rate table over 681 hub-slug transcripts, not chosen. "
        "Stated as a rule -- a turn at >= X x the seat's own running median, sustained 5 turns "
        "-- and counted: X=1.10 fires in 84.4% of sessions (median first fire turn 37 / 21 "
        "min), X=1.20 in 69.8% (turn 51 / 30 min), X=1.30 in 52.4% (turn 68 / 43 min), X=1.50 "
        "in 21.9% (turn 83 / 53 min), X=2.00 in 0.9% (turn 60 / 38 min). 1.30 is the KNEE: "
        "1.10 fires almost always and so reclaims at random -- it is the normal curve, not a "
        "signal -- while 2.00 is a rule that never runs. 1.30's median first fire sits where "
        "the elapsed-band curve has crossed 1.0 x own median and is still climbing, so the "
        "trigger fires while the cost it names is rising rather than after it has plateaued. "
        "THE CONFOUND, RECORDED: 'while the work class is unchanged' is NOT controlled for, "
        "because no transcript field carries work class. What makes the number survivable is "
        "the held leg -- with turn index held, an eight-fold elapsed spread moves cost only "
        "0.915 -> 1.003, which context accumulation predicts and a work-class explanation "
        "does not. Removing the confound entirely needs a per-turn work-class tag, which "
        "nothing writes today."
    ),
    "SUSTAINED_TURNS": (
        "DERIVED as part of the same table: every row above was computed WITH the 5-turn run "
        "requirement in force, so the fire rates are the rates of the rule as shipped rather "
        "than of a bare threshold. Without it a single expensive synthesis turn clears a "
        "seat mid-task, and the corpus has those at every session length."
    ),
    "WARMUP_TURNS": (
        "A median over three turns is not a median. 20 is the point at which a session's own "
        "median stops moving materially with each new turn in the sampled corpus; below it "
        "the first expensive turn IS the median and the ratio is meaningless, which would "
        "fire the trigger on turn two of every session."
    ),
}


@dataclass(frozen=True)
class TriggerVerdict:
    reclaim: bool
    run: int
    ratio: float
    detail: str


def should_reclaim(costs: Sequence[float],
                   multiple: float = RECLAIM_MULTIPLE,
                   sustained: int = SUSTAINED_TURNS,
                   warmup: int = WARMUP_TURNS) -> TriggerVerdict:
    """Has this seat's per-turn cost risen against ITS OWN running median, and stayed up?

    The median is RUNNING and per-seat. A fleet constant would fire constantly on an
    expensive seat and never on a cheap one, measuring the work rather than the drift.
    """
    run = 0
    best_run = 0
    ratio = 0.0
    seen: list[float] = []
    for cost in costs:
        seen.append(float(cost))
        if len(seen) < warmup:
            continue
        median = statistics.median(seen)
        if median <= 0:
            continue
        this = float(cost) / median
        if this >= multiple:
            run += 1
            ratio = max(ratio, this)
        else:
            run = 0
        best_run = max(best_run, run)
        if run >= sustained:
            return TriggerVerdict(
                True, run, ratio,
                f"{run} consecutive turns at >= {multiple:.2f}x the seat's own running "
                f"median (peak {this:.2f}x) after {len(seen)} turns")
    return TriggerVerdict(
        False, best_run, ratio,
        f"longest run {best_run} of the {sustained} needed, over {len(costs)} turns")


# ============================================================================== the checkpoints

@dataclass(frozen=True)
class Checkpoint:
    """A moment at which a seat's state is IN A FILE, so clearing loses nothing.

    `resume_keys` is the whole contract. A checkpoint is not "a good moment" -- it is a
    moment whose entire state has a named, resolvable home.
    """

    description: str
    resume_keys: tuple[str, ...]


#: The three the frozen contract names, each keyed on what must already be on disk.
CHECKPOINTS: dict[str, Checkpoint] = {
    "dispatcher": Checkpoint(
        description="after contracts are frozen and the manifest committed",
        resume_keys=("batch_manifest", "frozen_contracts"),
    ),
    "integrator": Checkpoint(
        description="after a merge is pushed and its receipt written",
        resume_keys=("merge_receipts", "merge_sha"),
    ),
    "lane": Checkpoint(
        description="after its handback packet",
        resume_keys=("handback_packet", "branch_commits"),
    ),
}


@dataclass(frozen=True)
class ResumeVerdict:
    complete: bool
    present: tuple[str, ...]
    missing: tuple[str, ...]
    detail: str


def verify_resume(kind: str, resolved: Mapping[str, Path]) -> ResumeVerdict:
    """Does every resume key resolve to a file that EXISTS?

    AN UNSUPPLIED KEY IS MISSING, not "fine by default". Silence reading as success is the
    exact failure the quality register exists to distinguish from enforcement, and a resume
    set that passes because nobody mentioned half of it is that failure with the context
    already thrown away.
    """
    spec = CHECKPOINTS.get(kind)
    if spec is None:
        raise KeyError(f"unknown checkpoint {kind!r}; known: {sorted(CHECKPOINTS)}")
    present: list[str] = []
    missing: list[str] = []
    for key in spec.resume_keys:
        path = resolved.get(key)
        if path is not None and Path(path).is_file():
            present.append(key)
        else:
            missing.append(key)
    return ResumeVerdict(
        complete=not missing,
        present=tuple(present),
        missing=tuple(missing),
        detail=(f"{kind}: {len(present)}/{len(spec.resume_keys)} resume key(s) resolve"
                + (f"; missing {', '.join(missing)}" if missing else "")),
    )


# ============================================================== capture / clear / rebuild

def capture_state(kind: str, resolved: Mapping[str, Path]) -> dict[str, str]:
    """The seat's file-backed state, as a digest per resume key.

    A DIGEST RATHER THAN THE CONTENT, so the round-trip check is a comparison a test can make
    cheaply and so this function never becomes a second copy of the state it is describing --
    a reclamation organ that holds the state it is about to clear has not cleared anything.
    """
    spec = CHECKPOINTS.get(kind)
    if spec is None:
        raise KeyError(f"unknown checkpoint {kind!r}; known: {sorted(CHECKPOINTS)}")
    out: dict[str, str] = {}
    for key in spec.resume_keys:
        path = resolved.get(key)
        if path is None or not Path(path).is_file():
            continue
        out[key] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return out


def rebuild_state(kind: str, resolved: Mapping[str, Path]) -> dict[str, str]:
    """Reconstruct the state from the resume set ALONE.

    It is deliberately the same computation as `capture_state`: the round-trip proof is that
    reading only the resume set reproduces what was captured before the clear. A rebuild that
    consulted anything else would be proving that the other thing survived, which is the
    question nobody asked.
    """
    return capture_state(kind, resolved)


@dataclass(frozen=True)
class ReclaimDecision:
    cleared: bool
    reason: str
    resume_from: dict[str, Path]
    trigger: TriggerVerdict | None = None
    resume: ResumeVerdict | None = None


def reclaim(kind: str, resolved: Mapping[str, Path],
            costs: Sequence[float]) -> ReclaimDecision:
    """Clear this seat's context -- or REFUSE, saying which leg failed.

    TWO LEGS, AND THEY FAIL FOR DIFFERENT REASONS.

      * The RESUME leg is safety. An incomplete resume set means the clear would lose state,
        so it refuses whatever the cost is doing. **This is checked FIRST**, because a
        refusal that arrives after the context is gone is a post-mortem.
      * The TRIGGER leg is economics. A complete checkpoint is PERMISSION to clear, never a
        reason to: clearing a cheap seat throws away a cache that was earning its keep.
    """
    resume = verify_resume(kind, resolved)
    if not resume.complete:
        return ReclaimDecision(
            False,
            f"REFUSED: the resume set is incomplete, so a clear here would lose state "
            f"({resume.detail})",
            {}, None, resume)

    trigger = should_reclaim(costs)
    if not trigger.reclaim:
        return ReclaimDecision(
            False,
            f"not cleared: the checkpoint is complete but the trigger has not fired "
            f"({trigger.detail})",
            {}, trigger, resume)

    return ReclaimDecision(
        True,
        f"cleared at the {kind} checkpoint: {trigger.detail}; resumes from "
        f"{', '.join(sorted(resume.present))}",
        {k: Path(v) for k, v in resolved.items() if k in resume.present},
        trigger, resume)


# ============================================================================================ CLI

@click.group()
def cli() -> None:
    """Context reclamation ([#792]) -- NOT session replacement, which is a different organ."""


@cli.command("checkpoints")
def cmd_checkpoints() -> None:
    """The three checkpoints and what each must have on disk before a clear."""
    for kind, spec in CHECKPOINTS.items():
        click.echo(f"{kind:12s} {spec.description}")
        click.echo(f"{'':12s}   resume set: {', '.join(spec.resume_keys)}")


@cli.command("verify")
@click.option("--kind", type=click.Choice(sorted(CHECKPOINTS)), required=True)
@click.option("--key", "keys", multiple=True, metavar="NAME=PATH",
              help="One resume key and the file that carries it. Repeatable.")
def cmd_verify(kind: str, keys: tuple[str, ...]) -> None:
    """Would a clear at this checkpoint lose state? Exit 1 when it would."""
    resolved: dict[str, Path] = {}
    for item in keys:
        name, _, raw = item.partition("=")
        if not raw:
            raise click.BadParameter(f"{item!r} is not NAME=PATH")
        resolved[name] = Path(raw)
    verdict = verify_resume(kind, resolved)
    click.echo(json.dumps({"complete": verdict.complete, "present": list(verdict.present),
                           "missing": list(verdict.missing), "detail": verdict.detail},
                          indent=2))
    if not verdict.complete:
        sys.exit(1)


if __name__ == "__main__":
    cli()
