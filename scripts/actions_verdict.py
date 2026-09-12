#!/usr/bin/env python
"""actions_verdict.py -- the integrator READS the Actions result (`[#675]` target 3.2).

THE TARGET, verbatim from `[#675]`'s Done-when:

    (2) full suite and index regeneration on GitHub Actions, with the integrator READING the
    result -- not merely running there, because a green run nobody reads is not a gate

THE PREMISE IS WORSE THAN THE ROW STATES. Measured 2026-09-12, the three most recent
`conductor.yml` runs on `main` all concluded `failure`, and job-level the failing job is
`pytest` while `ruff`, `seal`, `phase-gate` and `terra` pass:

    ec18875e  failure    9136f133  failure    cec75ebc  failure

Every one of those verdicts was ALREADY being printed, at SessionStart, by
`conductor.py session-start`. Every merge proceeded anyway. So the live state is not "a green
run nobody reads" -- it is a RED run nobody reads, which is the same defect with the loss
already realised. The gap this module closes is therefore not *surfacing*; it is making the
reading a STEP OF THE MERGE with an exit code, at the point where acting on it is still cheap.

WHY A DIFFERENTIAL AND NOT A BLOCK, and this is the design decision the measurement forced. A
gate refusing any non-green run would refuse every merge in this repo today. A gate that
refuses everything gets turned off inside a window -- the failure mode `seat_refusals` names in
its own contract, and the reason that module's refusals are narrow. So the integrator is made
to read WHAT THIS MERGE CHANGED:

    a job this merge BROKE        -> REGRESSED, non-zero. The merge owns it.
    a job already failing at base -> PRE-EXISTING, non-zero, job NAMED. Not this merge's, and
                                     not laundered into a pass either.
    a job this merge FIXED        -> reported, because a tool that only ever complains is read
                                     as noise.
    no baseline given             -> UNATTRIBUTED. Missing evidence is not evidence.

NEVER GREEN-BY-SKIP, WITH THREE DISTINCT ABSENCES. "No run for this SHA", "still in progress"
and "`gh` unavailable" are three different next actions -- investigate, wait, install -- so they
are three verdicts, not one. Collapsing them would be the `[#675]` defect itself: one plausible
word standing in for states that differ in what they ask you to do.

WHAT THIS DOES NOT COVER, stated rather than implied. Target 3.2 asks for the full suite AND
index regeneration on Actions. The suite is there; INDEX REGENERATION IS NOT a job in
`conductor.yml` today, so a green run does not mean both halves ran. `verdict.render()` says so
until the job appears, and stops saying it the moment it does -- a gap notice that retires
itself rather than becoming a stale line.

Closing that gap means writing `.github/workflows/conductor.yml`, which is `[#689]`'s DECLARED
footprint and not this lane's -- measured with this lane's own
`seat_refusals.declared_footprint`, which reports exactly one path for each contract. Writing it
from here would be the collision `[#675]` target 3.4 exists to refuse, in the same commit range
that built the refusal. A proposed diff rides in the end-of-lane artifact instead.

HONEST LIMITS:

  * IT READS A CONCLUSION, NOT A SUITE. A job that passed vacuously -- collected nothing, or
    skipped on a condition -- reports `success` here, exactly as it does in the Actions UI.
  * THE BASELINE IS WHATEVER SHA IT IS HANDED. Hand it the merge's first parent and the
    differential means "what this merge changed"; hand it something else and it means something
    else. The caller owns that choice and `/lane-integrate` states which it passes.
  * A RUN IS MATCHED BY HEAD SHA. A merge whose run never fired reads as NO_RUN, which is
    correct, but so does a merge whose run fired against a rewritten SHA.
"""
from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import click

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("actions-verdict")

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: The workflow whose conclusion the integrator reads. `[#689]`'s runner.
WORKFLOW = "conductor.yml"
#: The job name that WOULD carry target 3.2's index-regeneration half. Absent from the runner
#: today; naming it here is what lets the gap notice retire itself when it appears.
INDEX_REGEN_JOB = "index-regen"
#: How long to wait for `gh`. A merge step that hangs is a merge step nobody runs twice.
GH_TIMEOUT_S = 120

STATE_PASS = "PASS"
STATE_REGRESSED = "REGRESSED"
STATE_PRE_EXISTING = "PRE-EXISTING"
STATE_UNATTRIBUTED = "UNATTRIBUTED"
STATE_NO_RUN = "NO-RUN"
STATE_IN_PROGRESS = "IN-PROGRESS"
STATE_UNAVAILABLE = "GH-UNAVAILABLE"

#: Every not-green state names its next action. A verdict that names no way forward gets worked
#: around rather than acted on -- `SeatRefusal`'s rule, one organ over.
REMEDIES: dict[str, str] = {
    STATE_PASS: "nothing owed",
    STATE_REGRESSED: ("this merge broke these jobs. Fix or revert BEFORE the next merge in the "
                      "queue -- a serial queue means the next lane inherits the break"),
    STATE_PRE_EXISTING: ("these jobs were already failing at the baseline. This merge did not "
                         "cause them and does not fix them; record the verdict, name the jobs "
                         "in the batch packet, and do NOT report the run as green"),
    STATE_UNATTRIBUTED: ("no baseline was given, so nothing can be attributed. Re-run with "
                         "--baseline <the merge's first parent> to learn whether this merge "
                         "caused the failure"),
    STATE_NO_RUN: ("no Actions run exists for this SHA. Either the push has not landed, the "
                   "workflow did not fire, or the run is against a different SHA -- check "
                   "`gh run list` before assuming the suite ran"),
    STATE_IN_PROGRESS: ("the run has not finished. WAIT for it rather than merging the next "
                        "lane; that is what target 3.3's `race` is for -- run the review "
                        "concurrently instead of idling"),
    STATE_UNAVAILABLE: ("`gh` is not installed or not authenticated, so the result could not "
                        "be read at all. Install/authenticate it, or record explicitly that "
                        "this merge's Actions result was NOT read -- never that it passed"),
}


class ActionsUnavailable(RuntimeError):
    """`gh` could not be reached. Distinct from a failing run, on purpose."""


@dataclass(frozen=True)
class Verdict:
    """One SHA's Actions result, as the integrator must read it."""
    sha: str
    state: str
    jobs: dict[str, Optional[str]] = field(default_factory=dict)
    run_id: Optional[int] = None
    title: str = ""
    baseline: Optional[str] = None
    newly_failing: tuple[str, ...] = ()
    pre_existing: tuple[str, ...] = ()
    newly_passing: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        """ONLY `PASS` is ok. Every other state is non-zero, including PRE-EXISTING: this merge
        did not cause those failures, and it must still not be recorded as having run green."""
        return self.state == STATE_PASS

    @property
    def covers_index_regeneration(self) -> bool:
        return INDEX_REGEN_JOB in self.jobs

    def render(self) -> str:
        lines = [f"actions verdict for {self.sha[:12]}: {self.state}"
                 + (f"   run {self.run_id}" if self.run_id else "")
                 + (f"   baseline {self.baseline[:12]}" if self.baseline else "   (no baseline)")]
        if self.title:
            lines.append(f"  {self.title}")
        for name in sorted(self.jobs):
            conclusion = self.jobs[name] or "(no conclusion yet)"
            mark = "ok  " if conclusion == "success" else "FAIL"
            lines.append(f"  {mark} {name}: {conclusion}")
        if self.newly_failing:
            lines.append(f"  BROKEN BY THIS MERGE: {', '.join(self.newly_failing)}")
        if self.pre_existing:
            lines.append(f"  PRE-EXISTING failures, not caused by this merge and NOT a pass: "
                         f"{', '.join(self.pre_existing)}")
        if self.newly_passing:
            lines.append(f"  FIXED BY THIS MERGE: {', '.join(self.newly_passing)}")
        if self.state == STATE_UNATTRIBUTED:
            lines.append("  no baseline was given, so this failure is UNATTRIBUTED -- missing "
                         "evidence, not evidence of innocence")
        if self.jobs and not self.covers_index_regeneration:
            # Retires itself: the moment the runner gains the job, this line stops printing.
            lines.append(f"  NOTE: this runner has no `{INDEX_REGEN_JOB}` job, so index "
                         f"regeneration did NOT run on Actions. Target 3.2 asks for both "
                         f"halves; a green run here covers the suite only.")
        lines.append(f"  -> {REMEDIES[self.state]}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {"sha": self.sha, "state": self.state, "jobs": dict(self.jobs),
                "run_id": self.run_id, "title": self.title, "baseline": self.baseline,
                "newly_failing": list(self.newly_failing),
                "pre_existing": list(self.pre_existing),
                "newly_passing": list(self.newly_passing),
                "covers_index_regeneration": self.covers_index_regeneration}


def fetch_run(sha: str, *, repo_root: Optional[Path] = None,
              workflow: str = WORKFLOW) -> Optional[dict]:
    """The Actions run whose head is `sha`, or None when there is none.

    Raises `ActionsUnavailable` when `gh` cannot be reached -- never returns None for that,
    because "nothing ran" and "I could not look" are different facts.
    """
    command = ["gh", "run", "list", "--workflow", workflow, "--limit", "40",
               "--json", "databaseId,headSha,status,conclusion,displayTitle"]
    try:
        proc = subprocess.run(command, cwd=str(repo_root or _REPO_ROOT), capture_output=True,
                              text=True, timeout=GH_TIMEOUT_S, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ActionsUnavailable(f"gh could not be run: {exc}") from exc
    if proc.returncode != 0:
        raise ActionsUnavailable(f"gh exited {proc.returncode}: {proc.stderr.strip()[:200]}")
    try:
        runs = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise ActionsUnavailable(f"gh returned unreadable JSON: {exc}") from exc

    match = next((r for r in runs if str(r.get("headSha", "")).startswith(sha)), None)
    if match is None:
        return None

    jobs = ["gh", "run", "view", str(match["databaseId"]), "--json", "jobs"]
    try:
        proc = subprocess.run(jobs, cwd=str(repo_root or _REPO_ROOT), capture_output=True,
                              text=True, timeout=GH_TIMEOUT_S, check=False)
        match["jobs"] = json.loads(proc.stdout or "{}").get("jobs", []) if proc.returncode == 0 \
            else []
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        match["jobs"] = []
    return match


def _job_map(run: dict) -> dict[str, Optional[str]]:
    return {j["name"]: j.get("conclusion") for j in run.get("jobs", [])}


def verdict_for(sha: str, *, baseline: Optional[str] = None,
                fetch: Optional[Callable[..., Optional[dict]]] = None,
                repo_root: Optional[Path] = None) -> Verdict:
    """Read the Actions result for `sha`, attributed against `baseline` when one is given."""
    fetch = fetch or fetch_run
    try:
        run = fetch(sha, repo_root=repo_root, workflow=WORKFLOW)
    except ActionsUnavailable:
        return Verdict(sha=sha, state=STATE_UNAVAILABLE, baseline=baseline)
    if run is None:
        return Verdict(sha=sha, state=STATE_NO_RUN, baseline=baseline)

    jobs = _job_map(run)
    common = dict(run_id=run.get("databaseId"), title=run.get("displayTitle", ""),
                  jobs=jobs, baseline=baseline)
    if run.get("status") != "completed":
        return Verdict(sha=sha, state=STATE_IN_PROGRESS, **common)

    failing = {name for name, c in jobs.items() if c not in ("success", "skipped", None)}

    base_jobs: dict[str, Optional[str]] = {}
    base_read = False
    if baseline:
        try:
            base_run = fetch(baseline, repo_root=repo_root, workflow=WORKFLOW)
        except ActionsUnavailable:
            base_run = None
        if base_run is not None and base_run.get("status") == "completed":
            base_jobs = _job_map(base_run)
            base_read = True

    base_failing = {name for name, c in base_jobs.items()
                    if c not in ("success", "skipped", None)}
    newly_failing = tuple(sorted(failing - base_failing)) if base_read else ()
    pre_existing = tuple(sorted(failing & base_failing)) if base_read else ()
    newly_passing = tuple(sorted(base_failing - failing)) if base_read else ()

    if not failing:
        state = STATE_PASS
    elif not base_read:
        # A failure with nothing to compare against. Not a regression (we cannot say this merge
        # caused it) and not pre-existing (we cannot say it did not).
        state = STATE_UNATTRIBUTED
    elif newly_failing:
        state = STATE_REGRESSED
    else:
        state = STATE_PRE_EXISTING

    return Verdict(sha=sha, state=state, newly_failing=newly_failing,
                   pre_existing=pre_existing, newly_passing=newly_passing, **common)


@click.command()
@click.option("--sha", required=True, help="the merge commit whose run is read")
@click.option("--baseline", default=None,
              help="the SHA to attribute against -- normally the merge's FIRST PARENT, so the "
                   "differential means 'what this merge changed'")
@click.option("--repo-root", default=None, type=click.Path(file_okay=False))
def cli(sha: str, baseline: Optional[str], repo_root: Optional[str]) -> None:
    """Read this merge's GitHub Actions result. Exits non-zero unless it is a clean PASS."""
    verdict = verdict_for(sha, baseline=baseline,
                          repo_root=Path(repo_root) if repo_root else None)
    # PRINTED ON SUCCESS TOO: a gate silent on success has not been read, it has been assumed.
    click.echo(verdict.render())
    raise SystemExit(0 if verdict.ok else 1)


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
