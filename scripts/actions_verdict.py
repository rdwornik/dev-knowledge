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

NEVER GREEN-BY-SKIP, WITH FOUR DISTINCT ABSENCES. "No run for this SHA", "still in progress",
"`gh` unavailable" and "the run was found but its JOB LIST was not read" are four different next
actions -- investigate, wait, install, retry -- so they are four verdicts, not one. Collapsing
them would be the `[#675]` defect itself: one plausible word standing in for states that differ
in what they ask you to do.

THE FOURTH ABSENCE WAS A REALISED INSTANCE OF EXACTLY THAT, closed 2026-09-13 by `[#742]`.
Until then `fetch_run`'s second `gh` call collapsed a non-zero exit, an `OSError`, a
`subprocess.TimeoutExpired` and malformed JSON alike onto `match["jobs"] = []`. `verdict_for`
computed `failing = set()` over that empty list and returned `STATE_PASS`, so a job-details call
that never completed printed a GREEN verdict for the merge. The distinction the fix rests on is
that `None` means "not read" and `[]` means "read, and there were none" -- two facts the old
code spelled the same way, in a module whose whole argument is that it never does that.

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
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import click

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("actions-verdict")

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: foundation-4-merge-gate (items 10, 11; G4, G7). A pytest job is judged at TEST level, per OS
#: leg, against that leg's own base run -- never by job name. Every other job keeps the job-level
#: differential below. The module's header above is the pre-foundation-4 argument and still
#: holds for those jobs; what changed is that "pytest failed at both ends" is no longer
#: PRE-EXISTING by itself (DVA A2: the `424d6c72` cut merge turned a registered check red for 16
#: runs while the pytest job was already red).
PYTEST_JOB = "pytest"
#: The contexts a push run must show completed-and-successful before a sha is mergeable.
#: `tests/test_conductor_governance_jobs.py` pins this to the ruleset JSON, so the two cannot
#: drift.
REQUIRED_CONTEXTS = ("pytest (ubuntu-latest)", "pytest (windows-latest)", "ruff", "seal",
                     "spine", "anchor")
#: The one file the base registry is read from, AT THE BASE SHA -- a lane that registers its own
#: red in the same diff cannot launder it, because the tip's registry is never consulted.
_REGISTRY_RELPATH = "logs/KNOWN-REDS-REGISTRY.json"

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
#: The run was found and its JOB LIST was not. A FOURTH absence (`[#742]`), and it is its own
#: state for the same reason the other three are: "no failing jobs" and "no readable jobs" ask
#: the reader to do different things. Until 2026-09-13 every failure of the job-details call
#: became `jobs = []`, which `verdict_for` read as "nothing failed" and reported as PASS.
STATE_JOBS_UNREADABLE = "JOBS-UNREADABLE"
#: The RUN was cancelled (`cancel-in-progress` when a newer push lands, or a manual cancel). Its
#: jobs may read success/skipped; it is still not a verdict on the sha. Its own state because the
#: next action (wait for the newer run, or re-run) is not "investigate a failure" (G7).
STATE_CANCELLED = "CANCELLED"

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
    STATE_JOBS_UNREADABLE: ("the run exists but its JOB LIST could not be read -- `gh run view "
                            "<id> --json jobs` errored, timed out or returned unreadable JSON. "
                            "RETRY it; if it keeps failing, open the run in the browser and "
                            "record the jobs by hand. This merge's suite result is UNKNOWN, "
                            "which is not the same as green and must never be recorded as it"),
    STATE_CANCELLED: ("the run was CANCELLED, so it says nothing about this sha. A newer push "
                      "to the same ref cancels an older run (`cancel-in-progress`): read the "
                      "newer run, or re-run this one. Never land on it"),
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
    #: Test-level findings (item 10). Each entry is `"<leg>: <node id>"`. `new_tests` are ids red
    #: at the tip that the base leg did not fail, or that the registry does not vouch for;
    #: `signature_changed` are ids red on both sides that fail differently now; `non_test` are a
    #: leg's failures that name no test (a job timeout, a collection error, an xdist crash).
    new_tests: tuple[str, ...] = ()
    signature_changed: tuple[str, ...] = ()
    non_test: tuple[str, ...] = ()
    #: One line saying WHY, for the states whose name alone does not (UNATTRIBUTED, REGRESSED).
    reason: str = ""
    #: The registry the test-level read used (its baseline id), when it read one.
    registry_baseline_id: Optional[str] = None

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
        for label, items in (("NEW RED TEST", self.new_tests),
                             ("CHANGED-SIGNATURE TEST", self.signature_changed),
                             ("NON-TEST FAILURE", self.non_test)):
            for item in items:
                lines.append(f"  {label}: {item}")
        if self.reason:
            lines.append(f"  reason: {self.reason}")
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
                "new_tests": list(self.new_tests),
                "signature_changed": list(self.signature_changed),
                "non_test": list(self.non_test), "reason": self.reason,
                "registry_baseline_id": self.registry_baseline_id,
                "covers_index_regeneration": self.covers_index_regeneration}


def fetch_run(sha: str, *, repo_root: Optional[Path] = None,
              workflow: str = WORKFLOW) -> Optional[dict]:
    """The Actions run whose head is `sha`, or None when there is none.

    Raises `ActionsUnavailable` when `gh` cannot be reached -- never returns None for that,
    because "nothing ran" and "I could not look" are different facts.
    """
    # PUSH RUNS ONLY (item 11, G7): the ruleset's required check-runs belong to the `push` run on
    # the sha, so a `pull_request` or `workflow_dispatch` run for the same sha is not that
    # verdict. `--event push` narrows the listing server-side; the `event` filter below repeats it
    # so a listing that carries another event (or none) can never be chosen.
    command = ["gh", "run", "list", "--workflow", workflow, "--event", "push", "--limit", "40",
               "--json", "databaseId,headSha,status,conclusion,displayTitle,event,createdAt,url"]
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

    match = next((r for r in runs if r.get("event") == "push"
                  and str(r.get("headSha", "")).startswith(sha)), None)
    if match is None:
        return None

    # `None` MEANS "NOT READ", `[]` MEANS "READ, AND THERE WERE NONE" (`[#742]`). Until
    # 2026-09-13 both were `[]`, so an errored, timed-out or unparseable job-details call
    # produced a run object that `verdict_for` read as "nothing failed" and reported as PASS --
    # the integrator was told a merge was green by a call that never completed. The two facts
    # ask for different actions (retry vs proceed), so they get different values, and the
    # sentinel is checked rather than truthiness: `not jobs` is true for both.
    jobs = ["gh", "run", "view", str(match["databaseId"]), "--json", "jobs"]
    try:
        proc = subprocess.run(jobs, cwd=str(repo_root or _REPO_ROOT), capture_output=True,
                              text=True, timeout=GH_TIMEOUT_S, check=False)
        if proc.returncode != 0:
            logger.warning("gh run view %s exited %d; the job list for this run was NOT read: %s",
                           match["databaseId"], proc.returncode, proc.stderr.strip()[:200])
            match["jobs"] = None
        else:
            match["jobs"] = json.loads(proc.stdout or "{}").get("jobs", [])
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        logger.warning("the job list for run %s could not be read: %s", match["databaseId"], exc)
        match["jobs"] = None
    return match


def _jobs_were_read(run: dict) -> bool:
    """False only when the job-details call FAILED. A run dict built by hand -- every test
    fixture in this repo, and `conductor.py`'s own -- carries a real list and reads as read."""
    return run.get("jobs", []) is not None


def _job_map(run: dict) -> dict[str, Optional[str]]:
    return {j["name"]: j.get("conclusion") for j in run.get("jobs", []) or []}


def is_pytest_job(name: str) -> bool:
    """`pytest` (the pre-matrix name) or a matrix leg, `pytest (<os>)`."""
    return name == PYTEST_JOB or name.startswith(PYTEST_JOB + " (")


def _leg_os_key(name: str) -> Optional[str]:
    """`pytest (windows-latest)` -> `windows-latest`, the registry's `members_by_os` key."""
    m = re.match(r"^pytest \((.+)\)$", name)
    return m.group(1) if m else None


#: `gh run view --job <id> --log` lines are `<job>\t<step>\t<timestamp> <text>`; pytest's own text
#: is everything after the timestamp. A line that does not carry the prefix is used as it stands.
_GH_LOG_LINE_RE = re.compile(r"^(?:[^\t]*\t){0,2}\d{4}-\d\d-\d\dT[\d:.]+Z ?(.*)$")
#: A leg that is red WITHOUT naming a test. Each is a regression: a timeout, a collection abort,
#: an xdist worker crash and the suite gate's own NOT COMPARABLE carry no node id to put in the
#: truth table, and "no test failed" must never be the reading of a red leg.
_NON_TEST_MARKERS = (
    (re.compile(r"INTERNALERROR"), "pytest INTERNALERROR"),
    (re.compile(r"worker '[^']*' crashed"), "an xdist worker crashed"),
    (re.compile(r"Interrupted: \d+ errors? during collection"), "a collection error"),
    (re.compile(r"NOT COMPARABLE"), "the suite gate said NOT COMPARABLE"),
)


def _log_text(raw: str) -> str:
    out = []
    for line in raw.splitlines():
        m = _GH_LOG_LINE_RE.match(line)
        out.append(m.group(1) if m else line)
    return "\n".join(out)


def _leg_failures(raw_log: str) -> dict:
    """What one leg's log says failed: `{"ids", "signatures", "markers"}`. `markers` names every
    non-test failure the log shows, whether or not node ids were also printed."""
    try:
        from scripts import conductor as _conductor, known_reds as _kr
    except ImportError:                                           # pragma: no cover -- shim
        import conductor as _conductor
        import known_reds as _kr
    text = _log_text(raw_log)
    markers = [why for pattern, why in _NON_TEST_MARKERS if pattern.search(text)]
    return {"ids": _conductor.parse_failed_node_ids(text),
            "signatures": _kr.extract_failure_signatures(text), "markers": markers}


def _load_registry_at(ref: str, *, repo_root: Optional[Path] = None):
    """The known-reds registry as committed at `ref` (the BASE sha), validated exactly as
    `known_reds.load_registry` validates a file. A lane's own diff to the registry is never
    consulted, so a lane cannot launder its red by registering it. Raises `KnownRedsError`."""
    try:
        from scripts import known_reds as _kr
    except ImportError:                                           # pragma: no cover -- shim
        import known_reds as _kr
    root = str(repo_root or _REPO_ROOT)
    try:
        proc = subprocess.run(["git", "show", f"{ref}:{_REGISTRY_RELPATH}"], cwd=root,
                              capture_output=True, text=True, timeout=GH_TIMEOUT_S, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise _kr.KnownRedsError(f"git could not read the registry at {ref}: {exc}") from exc
    if proc.returncode != 0:
        raise _kr.KnownRedsError(f"no {_REGISTRY_RELPATH} at {ref}: {proc.stderr.strip()[:160]}")
    try:
        registry = _kr.Registry.from_json(json.loads(proc.stdout), f"{ref}:{_REGISTRY_RELPATH}")
    except ValueError as exc:
        raise _kr.KnownRedsError(f"{ref}:{_REGISTRY_RELPATH} is not valid JSON: {exc}") from exc
    problems = _kr.registry_problems(registry)
    if problems:
        raise _kr.KnownRedsError(f"{ref}:{_REGISTRY_RELPATH}: {len(problems)} problem(s), "
                                 f"first: {problems[0]}")
    return registry


def _default_fetch_logs(run: dict, job: dict, *, repo_root: Optional[Path] = None) -> Optional[str]:
    """One job's full log text, or None when it could not be read (never an empty string)."""
    job_id = job.get("databaseId")
    if job_id is None:
        return None
    command = ["gh", "run", "view", str(run.get("databaseId")), "--job", str(job_id), "--log"]
    try:
        proc = subprocess.run(command, cwd=str(repo_root or _REPO_ROOT), capture_output=True,
                              text=True, timeout=GH_TIMEOUT_S, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return proc.stdout if proc.returncode == 0 and proc.stdout.strip() else None


def _judge_pytest_legs(failing_legs: list, tip_run: dict, base_run: dict, *, registry,
                       fetch_logs: Callable, repo_root: Optional[Path]) -> dict:
    """The test-level read of every failing pytest leg: `{new_tests, signature_changed, non_test,
    unattributed}`. One leg is compared only to the SAME-named leg of the base run."""
    try:
        from scripts import known_reds as _kr
    except ImportError:                                           # pragma: no cover -- shim
        import known_reds as _kr
    found = {"new_tests": [], "signature_changed": [], "non_test": [], "unattributed": []}
    base_jobs = {j.get("name"): j for j in base_run.get("jobs") or []}
    for job in failing_legs:
        leg, conclusion = job["name"], job.get("conclusion")
        if conclusion in ("cancelled", "timed_out", "startup_failure", "action_required"):
            found["non_test"].append(f"{leg}: job {conclusion}")
            continue
        tip_log = fetch_logs(tip_run, job, repo_root=repo_root)
        if tip_log is None:
            found["unattributed"].append(f"{leg}: the tip job log could not be read")
            continue
        tip = _leg_failures(tip_log)
        for why in tip["markers"]:
            found["non_test"].append(f"{leg}: {why}")
        if not tip["ids"] and not tip["markers"]:
            found["non_test"].append(f"{leg}: red, and its log names no failing test node id")
            continue
        base_job = base_jobs.get(leg)
        if base_job is None:
            found["unattributed"].append(f"{leg}: the base run has no {leg!r} job to compare to")
            continue
        base_failed, base_sigs = frozenset(), {}
        if base_job.get("conclusion") not in ("success", "skipped", None):
            base_log = fetch_logs(base_run, base_job, repo_root=repo_root)
            if base_log is None:
                found["unattributed"].append(f"{leg}: the base job log could not be read")
                continue
            base = _leg_failures(base_log)
            base_failed, base_sigs = base["ids"], base["signatures"]
        result = _kr.compare_to_base(
            tip["ids"], base_failed, registry, workers=registry.workers,
            os_key=_leg_os_key(leg), tip_signatures=tip["signatures"],
            base_signatures=base_sigs)
        found["new_tests"] += [f"{leg}: {n}" for n in (result["new"] + result["base_unregistered"]
                                                       + result["registry_regressions"])]
        found["signature_changed"] += [f"{leg}: {n}" for n in result["signature_changed"]]
    return {k: tuple(v) for k, v in found.items()}


def verdict_for(sha: str, *, baseline: Optional[str] = None,
                fetch: Optional[Callable[..., Optional[dict]]] = None,
                repo_root: Optional[Path] = None,
                fetch_logs: Optional[Callable] = None,
                registry_loader: Optional[Callable] = None) -> Verdict:
    """Read the Actions result for `sha`, attributed against `baseline` when one is given.

    foundation-4-merge-gate: a failing PYTEST leg is judged at test level (node id, per OS leg,
    signature, registry at the baseline sha), every other job at job level. A cancelled run is
    CANCELLED, an in-progress one IN-PROGRESS, and a `success` run that never showed a pytest leg
    is not a PASS -- none of those is ever `ok`.
    """
    fetch = fetch or fetch_run
    fetch_logs = fetch_logs or _default_fetch_logs
    registry_loader = registry_loader or _load_registry_at
    try:
        run = fetch(sha, repo_root=repo_root, workflow=WORKFLOW)
    except ActionsUnavailable:
        return Verdict(sha=sha, state=STATE_UNAVAILABLE, baseline=baseline)
    if run is None:
        return Verdict(sha=sha, state=STATE_NO_RUN, baseline=baseline)
    if run.get("status") == "completed" and run.get("conclusion") == "cancelled":
        # BEFORE the job list is read: a cancelled run's job list is beside the point, and its
        # jobs routinely read success/skipped for the steps that finished before the cancel.
        return Verdict(sha=sha, state=STATE_CANCELLED, run_id=run.get("databaseId"),
                       title=run.get("displayTitle", ""), baseline=baseline,
                       jobs=_job_map(run) if _jobs_were_read(run) else {},
                       reason="the run's own conclusion is cancelled")
    if not _jobs_were_read(run):
        # BEFORE the status check, and that ordering is the decision. "I could not read the
        # jobs" is a fact about the READ, not about the run, and it is the one fact that must
        # never be laundered into a verdict about the suite. An in-progress run whose job call
        # also failed is reported here rather than as IN-PROGRESS: both say "do not merge on
        # this", and only this one says why the evidence is missing.
        return Verdict(sha=sha, state=STATE_JOBS_UNREADABLE, run_id=run.get("databaseId"),
                       title=run.get("displayTitle", ""), baseline=baseline)

    jobs = _job_map(run)
    common = dict(run_id=run.get("databaseId"), title=run.get("displayTitle", ""),
                  jobs=jobs, baseline=baseline)
    if run.get("status") != "completed":
        return Verdict(sha=sha, state=STATE_IN_PROGRESS, **common)

    failing = {name for name, c in jobs.items() if c not in ("success", "skipped", None)}

    base_jobs: dict[str, Optional[str]] = {}
    base_read = False
    base_run = None
    if baseline:
        try:
            base_run = fetch(baseline, repo_root=repo_root, workflow=WORKFLOW)
        except ActionsUnavailable:
            base_run = None
        # `_jobs_were_read` GUARDS THIS TOO, and it is the same hole with the sign flipped
        # (`[#742]`, found resolving its locator). An unreadable BASELINE job list used to give
        # `base_jobs = {}` with `base_read = True`, so `base_failing` was empty and every
        # failure at the tip became `newly_failing` -- REGRESSED, naming jobs this merge may
        # not have broken. A false accusation costs as much as a false pass: the integrator
        # reverts an innocent merge. Unread means UNATTRIBUTED, which is what it always meant.
        if (base_run is not None and base_run.get("status") == "completed"
                and _jobs_were_read(base_run)):
            base_jobs = _job_map(base_run)
            base_read = True

    base_failing = {name for name, c in base_jobs.items()
                    if c not in ("success", "skipped", None)}
    # Job-level differential for every job that is NOT a pytest leg. A pytest leg is judged at
    # test level below -- "the leg is red at both ends" says nothing about WHICH tests.
    other_failing = {n for n in failing if not is_pytest_job(n)}
    other_base_failing = {n for n in base_failing if not is_pytest_job(n)}
    newly_failing = tuple(sorted(other_failing - other_base_failing)) if base_read else ()
    pre_existing = tuple(sorted(other_failing & other_base_failing)) if base_read else ()
    newly_passing = tuple(sorted(base_failing - failing)) if base_read else ()

    pytest_legs = [j for j in run["jobs"] if is_pytest_job(j["name"])]
    failing_legs = [j for j in pytest_legs if j["name"] in failing]
    legs_ok = bool(pytest_legs) and not failing_legs and all(
        j.get("conclusion") == "success" for j in pytest_legs)
    run_conclusion = run.get("conclusion")
    # A completed run can conclude non-success while every listed job reads success/skipped
    # (a startup failure, an empty job list): GitHub's run-level and job-level books are separate.
    workflow_level = (not failing and run_conclusion not in ("success", "skipped", None))

    findings = {"new_tests": (), "signature_changed": (), "non_test": (), "unattributed": ()}
    registry_baseline_id: Optional[str] = None
    reasons: list[str] = []
    if failing_legs and base_read and base_run is not None:
        try:
            registry = registry_loader(baseline, repo_root=repo_root)
        except Exception as exc:                  # KnownRedsError and anything git raises
            findings["unattributed"] = (f"the known-reds registry at the baseline could not be "
                                        f"read ({exc}): a test-level compare has no registry",)
        else:
            registry_baseline_id = registry.baseline_id
            findings = _judge_pytest_legs(failing_legs, run, base_run, registry=registry,
                                          fetch_logs=fetch_logs, repo_root=repo_root)
    non_test = findings["non_test"] + ((f"workflow: concluded {run_conclusion}",)
                                       if workflow_level else ())
    reasons += list(findings["unattributed"])

    if failing_legs and not base_read:
        # A failure with nothing to compare against. Not a regression (we cannot say this merge
        # caused it) and not pre-existing (we cannot say it did not).
        state = STATE_UNATTRIBUTED
        reasons.append("no readable baseline run to compare the failing pytest leg(s) against")
    elif not failing and not workflow_level:
        if not pytest_legs:
            # `success` with no pytest leg is not a pass on the SUITE: the leg that carries the
            # verdict never ran (a skipped matrix, a renamed job). Missing evidence again.
            state = STATE_NO_RUN
            reasons.append("the run shows no pytest leg, so the suite did not run on this sha")
        elif not legs_ok:
            state = STATE_UNATTRIBUTED
            reasons.append("a pytest leg concluded neither success nor failure "
                           f"({', '.join(j['name'] + '=' + str(j.get('conclusion')) for j in pytest_legs)})")
        else:
            state = STATE_PASS
    elif (newly_failing or findings["new_tests"] or findings["signature_changed"] or non_test):
        state = STATE_REGRESSED
        reasons.insert(0, f"{len(findings['new_tests'])} new red test(s), "
                          f"{len(findings['signature_changed'])} changed signature(s), "
                          f"{len(non_test)} non-test failure(s), {len(newly_failing)} job(s) broken")
    elif not base_read or reasons:
        state = STATE_UNATTRIBUTED
    else:
        state = STATE_PRE_EXISTING

    return Verdict(sha=sha, state=state, newly_failing=newly_failing,
                   pre_existing=pre_existing, newly_passing=newly_passing,
                   new_tests=findings["new_tests"], signature_changed=findings["signature_changed"],
                   non_test=non_test, reason="; ".join(reasons),
                   registry_baseline_id=registry_baseline_id, **common)


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
