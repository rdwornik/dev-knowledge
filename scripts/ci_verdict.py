#!/usr/bin/env python
"""ci_verdict.py -- CI's verdict read as data, recorded beside the local one (LANE-5A-6).

THE VALUE LINE, verbatim from the contract: "CI runs the full suite in about 8 minutes, but
nothing reads its result as data, so the integrator recomputes locally for an hour. This lane
makes the verdict readable, and tonight it is recorded next to the local verdict. The morning
then shows how often the two agree, which is the evidence needed before CI can become the gate."

NOT A GATE TONIGHT. `/lane-integrate` records this organ's output beside the local verdict; it
does not compare, block or feed the merge decision. Wiring it as a gate before the freeze is
honest is exactly the failure `to-browser/DIGEST-AUDIT-CROSSCHECK-2026-09-23.md` measured:
"the per-batch registry LAUNDERS regressions -- CI regressions rose from 9 to 17 while local said
clean." A gate that compares against a stale baseline would launder the same disagreement it
exists to surface.

WHY THIS IS A NEW ORGAN AND NOT `actions_verdict.py`, one file over. That module is the
INTEGRATOR's per-merge read: given a sha it has ALREADY pushed, it takes a `--baseline` the
caller supplies, returns immediately (never waiting -- `IN-PROGRESS` is its own verdict so the
caller can race a concurrent review instead of idling, `[#675]` target 3.3), and reports one of
EIGHT states because a merge decision needs to distinguish "broke it", "was already broken" and
"could not tell" apart. This organ answers a narrower, different question -- "what did CI say
about this ref" -- asked from OUTSIDE the merge walk, with no concurrent work to race and no
externally-supplied baseline to attribute against. So it WAITS out IN-PROGRESS itself (bounded),
and it reads the baseline CI ITSELF reports -- the frozen SHA the pytest job's own suite-baseline
gate step logs (`scripts/conductor.py::render_suite_gate`), not one the caller has to already
know. The Done-contract's three-state shape (green / red / not-run) is deliberately coarser than
`actions_verdict`'s eight: this organ is not a merge gate, so it does not need to distinguish WHY
a result is unusable, only THAT the CI verdict at this ref is unusable right now, and it says so
in `reason` rather than manufacturing a fourth verdict value the contract does not ask for.

HOW "GREEN / RED / NOT-RUN" ABSORBS THE ABSENCES. `not-run` covers every case in which a
completed, readable, GitHub-confirmed verdict could not be reached: no run matched the sha, `gh`
could not be reached, the run's job list could not be read, or the wait timed out with the run
still in progress. Each of those is still distinguishable via `reason` and (where known) `run_id`
/ `run_url` -- the verdict value stays a closed three-member enum; the detail does not disappear,
it moves to the field the contract did not close.

"NEW REDS", NAMED. When the pytest job's own suite-baseline gate step ran, its log carries the
render `conductor.py::render_suite_gate` already wrote -- `baseline sha`, and one `REGRESSION`
line per test outside the frozen set (`logs/SUITE-BASELINE-FREEZE.md`). This organ reads that
block back out of the job's log via `gh run view --job <id> --log` (READ-ONLY: no artifact
download, no re-run) rather than recomputing it, so the "new reds" named here are the SAME
regressions the runner itself judged, not a second opinion. When that block is absent -- the
`pytest` job never reached the gate step, or failed before it, or the run's `pytest` job is not
even the one that failed -- `new_reds` falls back to the names of the jobs that did not conclude
`success` or `skipped`, and `reason` says which happened.

DO-NOT, from the contract, still binding: this module never writes to `.github/workflows/`,
`scripts/impacted_tests.py`, repository settings or rulesets, and it makes no GitHub write call
of any kind -- `gh run list` / `gh run view` (both read verbs) are the entire surface.

HONEST LIMITS:
  * A RUN IS MATCHED BY HEAD SHA, exactly as in `actions_verdict`. A merge whose run never fired
    reads as `not-run`, correctly; so does a merge whose run fired against a rewritten sha.
  * THE SUITE-GATE BLOCK IS READ AS LOGGED TEXT, not re-parsed from `logs/SUITE-BASELINE-FREEZE.md`
    directly -- this organ trusts the runner's own rendering rather than re-deriving it, so a
    change to `render_suite_gate`'s wording (the `baseline sha   :` / `  REGRESSION    ` prefixes)
    is a breaking change to this parser too. Format confirmed live against
    `gh run view --job 107339568361 --log` on run `35907748018`, 2026-09-24. Parsing is SCOPED
    to the `SUITE_GATE_STEP_NAME` step's own `startedAt`/`completedAt` window (`_step_window`),
    not the log text's step field -- that field renders as the literal `UNKNOWN STEP` on every
    line of a real `run:` step, measured the same day, so it cannot itself discriminate. Without
    a resolvable window (the step never ran, or its timing is missing) parsing falls back to
    unscoped, which is safe exactly because there is then no real gate output anywhere to
    misattribute (Codex terra, 2026-09-24, HIGH).
  * WAITING IS BOUNDED. A run still queued or running past `--timeout` reads as `not-run` with the
    run named in `reason` -- re-run this organ rather than raising the default past what one
    `conductor.yml` push run costs (about 8 minutes, per the batch's measured VERIFY-TIME digest).
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Optional

import click

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: The workflow whose conclusion this organ reads -- the same runner `actions_verdict.py` reads.
WORKFLOW = "conductor.yml"
#: The job whose log carries the suite-baseline gate's own rendered verdict.
PYTEST_JOB = "pytest"
#: How long a single `gh` call gets before it counts as unreachable.
GH_TIMEOUT_S = 120
#: How long, in total, this organ waits for a matched run to reach `completed`.
POLL_TIMEOUT_S = 900
#: How long between polls while a matched run is still in progress.
POLL_INTERVAL_S = 20

STATE_GREEN = "green"
STATE_RED = "red"
STATE_NOT_RUN = "not-run"

_RUN_FIELDS = "databaseId,headSha,status,conclusion,displayTitle,url,createdAt,updatedAt,event"
#: `gh run view --job <id> --log` lines are TAB-separated `<job>\t<step>\t<timestamp> <text>`.
#: Measured live, not assumed -- see the module docstring's honest limit on this format. The
#: step field itself was measured as the literal string `UNKNOWN STEP` on every line of a real
#: `run:`-step log (2026-09-24) -- gh does not resolve it to the step's real name in this text
#: format, so this organ never trusts that field; scoping is done by TIMESTAMP against the
#: step's own `startedAt`/`completedAt` window (`_step_window`), read from `gh run view --json
#: jobs`'s per-job `steps` array, which DOES carry real names and real times.
_LOG_LINE_RE = re.compile(r"^(?:[^\t]*\t){0,2}(\S+Z) ?(.*)$")
_BASELINE_SHA_RE = re.compile(r"^baseline sha\s*:\s*(\S+)$")
_REGRESSION_RE = re.compile(r"^  REGRESSION\s+(\S.*)$")
_SUITE_GATE_HEADER = "conductor suite-baseline gate"
#: `conductor.yml`'s pytest job, step id `gate` -- the ONLY step whose log this organ trusts
#: for a baseline id or a regression list. A rename there is a breaking change here too.
SUITE_GATE_STEP_NAME = "Judge the run against the frozen baseline, by node id ([#802])"


class GhUnavailable(RuntimeError):
    """`gh` could not be reached, or returned something this organ could not read."""


@dataclass(frozen=True)
class CiVerdict:
    """CI's answer for one ref, as this organ read it."""
    ref: str
    sha: str
    verdict: str
    run_id: Optional[int] = None
    run_url: Optional[str] = None
    duration_seconds: Optional[float] = None
    baseline_id: Optional[str] = None
    new_reds: tuple = field(default_factory=tuple)
    reason: str = ""
    #: The fine-grained state behind the closed three-value `verdict` (foundation-4 item 11, G7):
    #: `PASS`, or one of `actions_verdict`'s states (`REGRESSED`, `PRE-EXISTING`, `UNATTRIBUTED`,
    #: `NO-RUN`, `IN-PROGRESS`, `CANCELLED`, `GH-UNAVAILABLE`, `JOBS-UNREADABLE`). Only `PASS` is
    #: `green`; every other state fails closed, and none is ever relabelled as another.
    state: str = ""
    #: Required contexts the run did not show as `success` (see `required_contexts` below).
    missing_contexts: tuple = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return {"ref": self.ref, "sha": self.sha, "verdict": self.verdict, "run_id": self.run_id,
                "run_url": self.run_url, "duration_seconds": self.duration_seconds,
                "baseline_id": self.baseline_id, "new_reds": list(self.new_reds),
                "reason": self.reason, "state": self.state,
                "missing_contexts": list(self.missing_contexts)}


def resolve_sha(ref: str, *, repo_root: Path) -> str:
    """The full sha `ref` names, by LOCAL git (never GitHub) -- so a branch name or short sha
    can be handed to `find_run`, which matches on `headSha`. Falls back to `ref` itself when
    local git cannot resolve it (a foreign sha this checkout has not fetched, for instance),
    because a literal sha is still a valid match candidate even when this git cannot name it."""
    try:
        proc = subprocess.run(["git", "rev-parse", ref], cwd=str(repo_root),
                              capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return ref
    return proc.stdout.strip() if proc.returncode == 0 and proc.stdout.strip() else ref


def _gh_json(command: list, *, repo_root: Path, timeout: int = GH_TIMEOUT_S):
    try:
        proc = subprocess.run(command, cwd=str(repo_root), capture_output=True, text=True,
                              timeout=timeout, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise GhUnavailable(f"gh could not be run: {exc}") from exc
    if proc.returncode != 0:
        raise GhUnavailable(f"gh exited {proc.returncode}: {proc.stderr.strip()[:200]}")
    try:
        return json.loads(proc.stdout or "null")
    except json.JSONDecodeError as exc:
        raise GhUnavailable(f"gh returned unreadable JSON: {exc}") from exc


def _gh_text(command: list, *, repo_root: Path, timeout: int = GH_TIMEOUT_S) -> str:
    try:
        proc = subprocess.run(command, cwd=str(repo_root), capture_output=True, text=True,
                              timeout=timeout, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise GhUnavailable(f"gh could not be run: {exc}") from exc
    if proc.returncode != 0:
        raise GhUnavailable(f"gh exited {proc.returncode}: {proc.stderr.strip()[:200]}")
    return proc.stdout


def list_runs(*, repo_root: Path, workflow: str = WORKFLOW, limit: int = 40) -> list:
    # PUSH RUNS ONLY (item 11, G7): the ruleset's required check-runs belong to the push run on
    # the sha. `find_run` repeats the filter, so a listing carrying another event (or none) can
    # never be chosen either.
    return _gh_json(["gh", "run", "list", "--workflow", workflow, "--event", "push",
                     "--limit", str(limit), "--json", _RUN_FIELDS], repo_root=repo_root) or []


def find_run(sha: str, *, repo_root: Path, workflow: str = WORKFLOW,
            list_fn: Callable = list_runs) -> Optional[dict]:
    runs = list_fn(repo_root=repo_root, workflow=workflow)
    return next((r for r in runs if r.get("event") == "push"
                 and str(r.get("headSha", "")).startswith(sha)), None)


def fetch_run_status(run_id, *, repo_root: Path) -> dict:
    """A single re-read of one run's status, cheaper than re-listing while polling."""
    return _gh_json(["gh", "run", "view", str(run_id), "--json", _RUN_FIELDS],
                    repo_root=repo_root)


def fetch_jobs(run_id, *, repo_root: Path) -> Optional[list]:
    """The run's job list, or `None` when it could not be read -- distinct from a genuinely
    job-less `[]`, the same distinction `actions_verdict._jobs_were_read` guards (`[#742]`)."""
    try:
        result = _gh_json(["gh", "run", "view", str(run_id), "--json", "jobs"],
                          repo_root=repo_root)
    except GhUnavailable:
        return None
    return (result or {}).get("jobs") if result is not None else None


def fetch_job_log(run_id, job_id, *, repo_root: Path) -> Optional[str]:
    """One job's full log text, or `None` when it could not be read."""
    try:
        return _gh_text(["gh", "run", "view", str(run_id), "--job", str(job_id), "--log"],
                        repo_root=repo_root)
    except GhUnavailable:
        return None


#: `gh run view --json jobs`'s `steps[].startedAt`/`completedAt` carry SECOND resolution only;
#: the log text's own timestamps carry microseconds. A step measured 2026-09-24 completed in
#: under one second -- `startedAt == completedAt == "...:47Z"` -- so its true content, logged at
#: "...:47.2155844Z", falls AFTER that second's zero-microsecond instant and would be excluded
#: by an unpadded window. One second of pad on each side absorbs the resolution gap; it can
#: never admit a DIFFERENT step's whole output, since steps run sequentially and are each
#: measured in single-digit seconds at worst.
_STEP_WINDOW_PAD = timedelta(seconds=1)


def _step_window(job: dict, step_name: str) -> Optional[tuple]:
    """The `(started, completed)` datetimes of `step_name` in `job`'s own `steps` array, padded
    for the resolution gap above, or `None` when that step is not there -- it never ran, or the
    run predates this organ's step name. `None` means "cannot scope"; callers fall back to
    unscoped parsing rather than silently finding nothing."""
    for step in job.get("steps") or []:
        if step.get("name") != step_name:
            continue
        started, completed = step.get("startedAt"), step.get("completedAt")
        if not started or not completed:
            return None
        try:
            return (datetime.fromisoformat(str(started).replace("Z", "+00:00")) - _STEP_WINDOW_PAD,
                    datetime.fromisoformat(str(completed).replace("Z", "+00:00")) + _STEP_WINDOW_PAD)
        except ValueError:
            return None
    return None


def parse_suite_gate_block(log_text: str, *, window: Optional[tuple] = None) -> dict:
    """The baseline sha and named regressions `render_suite_gate` logged, read back out of the
    job's own log text. `found=False` means the block never printed -- the gate step did not
    run -- which the caller must not confuse with "printed and found nothing wrong".

    `window`, when given, is a `(started, completed)` pair (see `_step_window`): only log lines
    whose OWN timestamp falls inside it are read. Unscoped (`window=None`), a line anywhere in
    the job's log that happens to shape-match `baseline sha   : ...` or `  REGRESSION    ...`
    -- pytest's own captured stdout can, in principle, echo arbitrary text -- would be misread
    as the gate's verdict. Scoping by the step's real `startedAt`/`completedAt` (not the log
    text's own step field, which gh renders as the literal string `UNKNOWN STEP` -- see the
    module docstring) closes that.
    """
    baseline_id = None
    regressions = []
    found = False
    for raw in log_text.splitlines():
        m = _LOG_LINE_RE.match(raw)
        if not m:
            continue
        ts_text, line = m.group(1), m.group(2)
        if window is not None:
            try:
                ts = datetime.fromisoformat(ts_text.replace("Z", "+00:00"))
            except ValueError:
                continue
            if not (window[0] <= ts <= window[1]):
                continue
        if line.startswith(_SUITE_GATE_HEADER):
            found = True
        bm = _BASELINE_SHA_RE.match(line)
        if bm:
            baseline_id = bm.group(1)
        rm = _REGRESSION_RE.match(line)
        if rm:
            regressions.append(rm.group(1))
    return {"baseline_id": baseline_id, "regressions": tuple(regressions), "found": found}


def _duration_seconds(run: dict) -> Optional[float]:
    started, ended = run.get("createdAt"), run.get("updatedAt")
    if not started or not ended:
        return None
    try:
        t0 = datetime.fromisoformat(str(started).replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(str(ended).replace("Z", "+00:00"))
    except ValueError:
        return None
    return (t1 - t0).total_seconds()


def _actions_verdict():
    """`actions_verdict`, imported lazily and through the dual-import shim: it is the ONE
    classifier, and importing it at module load would make the two modules a cycle the moment it
    reaches back for anything here."""
    try:
        from scripts import actions_verdict as _av
    except ImportError:                                           # pragma: no cover -- shim
        import actions_verdict as _av
    return _av


def _is_pytest_job(name: str) -> bool:
    return name == PYTEST_JOB or name.startswith(PYTEST_JOB + " (")


def _classify(sha: str, baseline: str, run: dict, jobs: list, root: Path, *, log_fn: Callable,
              fetch_base: Optional[Callable], registry_loader: Optional[Callable]):
    """The tip run's classification against `baseline`, by `actions_verdict.verdict_for` -- this
    module owns no second classifier. The tip run is handed over already read (the run and jobs
    this call fetched); the base run is read through `fetch_base` (default `actions_verdict.
    fetch_run`); job logs come through this call's own `log_fn`."""
    av = _actions_verdict()
    tip_run = {**run, "jobs": jobs}
    base_fetch = fetch_base or av.fetch_run

    def fetch(s, *, repo_root=None, workflow=None):
        if s == sha:
            return tip_run
        return base_fetch(s, repo_root=repo_root, workflow=workflow)

    def fetch_logs(r, job, *, repo_root=None):
        job_id = job.get("databaseId")
        if job_id is None:
            return None
        return log_fn(r.get("databaseId"), job_id, repo_root=repo_root)

    return av.verdict_for(sha, baseline=baseline, fetch=fetch, repo_root=root,
                          fetch_logs=fetch_logs, registry_loader=registry_loader)


def wait_for_run(sha: str, *, repo_root: Path, workflow: str = WORKFLOW,
                 timeout_s: int = POLL_TIMEOUT_S, interval_s: int = POLL_INTERVAL_S,
                 list_fn: Callable = list_runs, view_fn: Callable = fetch_run_status,
                 sleep_fn: Callable = time.sleep,
                 clock_fn: Callable = time.monotonic) -> tuple:
    """Poll IN-PROCESS until a run matching `sha` reaches `completed`, or `timeout_s` elapses.

    Returns `(run_or_None, reason)`. `reason` is only ever non-empty when the wait did NOT end
    in a completed run -- a completed run's reason is decided by its verdict, not by the wait.
    """
    deadline = clock_fn() + timeout_s
    run: Optional[dict] = None
    while True:
        previously_known = run
        try:
            run = view_fn(run["databaseId"], repo_root=repo_root) if run is not None \
                else find_run(sha, repo_root=repo_root, workflow=workflow, list_fn=list_fn)
        except GhUnavailable as exc:
            # A run already FOUND is not un-found by a later poll's transient failure -- the
            # caller still gets its id and url, with the honest reason that the LATEST read
            # failed, rather than losing everything it already knew.
            if previously_known is not None:
                return previously_known, (f"run {previously_known.get('databaseId')} was "
                                          f"found, but a later poll could not read it: {exc}")
            return None, f"gh unavailable: {exc}"
        if run is not None and run.get("status") == "completed":
            return run, ""
        if clock_fn() >= deadline:
            if run is None:
                return None, f"no Actions run matched {sha[:12]} after waiting {timeout_s}s"
            return run, (f"run {run.get('databaseId')} still {run.get('status')} after "
                        f"waiting {timeout_s}s -- re-run this organ")
        sleep_fn(interval_s)


def verdict_for(ref: str, *, repo_root: Optional[Path] = None, workflow: str = WORKFLOW,
                timeout_s: int = POLL_TIMEOUT_S, interval_s: int = POLL_INTERVAL_S,
                list_fn: Optional[Callable] = None, view_fn: Optional[Callable] = None,
                jobs_fn: Optional[Callable] = None, log_fn: Optional[Callable] = None,
                sleep_fn: Callable = time.sleep,
                clock_fn: Callable = time.monotonic,
                baseline: Optional[str] = None, required_contexts: tuple = (),
                fetch_base: Optional[Callable] = None,
                registry_loader: Optional[Callable] = None) -> CiVerdict:
    """CI's verdict for `ref`: green, red (with the new reds named), or not-run.

    THE ONE "CI VERDICT FOR A SHA" FUNCTION (foundation-4-merge-gate item 11, N2): the merge path
    and BD-ci (`handoff_state.row_ci`) both call this and nothing else. PUSH RUNS ONLY, COMPLETED
    ONLY -- a run still queued or running at the poll timeout is `not-run` / `IN-PROGRESS`, never
    a pass; a cancelled run is `not-run` / `CANCELLED`; `gh` failing is `not-run` /
    `GH-UNAVAILABLE`. `green` means `PASS` and nothing else.

    `required_contexts` (the merge path passes the ruleset's six) makes green ALSO require every
    named job to be present and `success` -- not `skipped`, not absent -- so this verdict agrees
    with what the server-side ruleset will accept. `baseline` (the merge's first parent, the
    base `main` sha) makes a red run be CLASSIFIED by `actions_verdict.verdict_for` -- the one
    classifier -- so `new_reds` names the NEW tests per OS leg, and `state` says REGRESSED /
    PRE-EXISTING / UNATTRIBUTED. Without a baseline the red is named from the gate's own log as
    before.

    The four `_fn` defaults resolve by NAME, here, rather than as bound parameter defaults --
    a default bound at `def` time would freeze the ORIGINAL function object, so a caller (the
    CLI, a test) that monkeypatches `ci_verdict.list_runs` et al. would silently keep calling
    the un-patched one. Resolving inside the body re-reads the module's current attribute on
    every call, which is what makes the CLI's own defaults patchable at all.
    """
    root = repo_root or _REPO_ROOT
    list_fn = list_fn or list_runs
    view_fn = view_fn or fetch_run_status
    jobs_fn = jobs_fn or fetch_jobs
    log_fn = log_fn or fetch_job_log
    sha = resolve_sha(ref, repo_root=root)
    run, wait_reason = wait_for_run(sha, repo_root=root, workflow=workflow, timeout_s=timeout_s,
                                    interval_s=interval_s, list_fn=list_fn, view_fn=view_fn,
                                    sleep_fn=sleep_fn, clock_fn=clock_fn)
    if run is None:
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_NOT_RUN, reason=wait_reason,
                         state=("GH-UNAVAILABLE" if wait_reason.startswith("gh unavailable")
                                else "NO-RUN"))

    run_id, run_url = run.get("databaseId"), run.get("url")
    duration = _duration_seconds(run)
    if run.get("status") != "completed":
        # The wait ended without a completed run: the poll timed out (IN-PROGRESS) or a later
        # poll could not read a run already found (GH-UNAVAILABLE). Neither is a pass.
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_NOT_RUN, run_id=run_id, run_url=run_url,
                         duration_seconds=duration, reason=wait_reason,
                         state=("GH-UNAVAILABLE" if "could not read it" in wait_reason
                                else "IN-PROGRESS"))
    if run.get("conclusion") == "cancelled":
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_NOT_RUN, run_id=run_id, run_url=run_url,
                         duration_seconds=duration, state="CANCELLED",
                         reason=(f"run {run_id} was cancelled (`cancel-in-progress` cancels the "
                                 f"older run when a newer push lands) -- it is not a verdict"))

    jobs = jobs_fn(run_id, repo_root=root)
    if jobs is None:
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_NOT_RUN, run_id=run_id, run_url=run_url,
                         duration_seconds=duration, state="JOBS-UNREADABLE",
                         reason=f"run {run_id} completed but its job list could not be read")

    job_map = {j.get("name"): j.get("conclusion") for j in jobs}
    failing = sorted(n for n, c in job_map.items() if c not in ("success", "skipped", None))

    # THE RUN'S OWN CONCLUSION IS ALWAYS CHECKED TOO, never inferred solely from job
    # conclusions. A completed run can conclude non-success (`cancelled`, `timed_out`, a
    # startup failure) with an EMPTY job list or with every listed job reading success/skipped
    # -- GitHub's run-level and job-level bookkeeping are separate facts, and reading only the
    # job map would report such a run GREEN (Codex terra, 2026-09-24, HIGH).
    run_conclusion = run.get("conclusion")
    workflow_level_failure = not failing and run_conclusion not in ("success", "skipped", None)

    # REQUIRED CONTEXTS (G7): present AND `success`. A skipped or absent one is not a success --
    # the ruleset would not count it, so neither does this verdict.
    missing = tuple(c for c in required_contexts if job_map.get(c) != "success")

    baseline_id = None
    regressions: list = []
    gate_found = False
    # EVERY pytest leg, not only a job named exactly `pytest`: the OS matrix renamed the jobs to
    # `pytest (<os>)`, and the exact-name lookup this replaces silently found none of them.
    pytest_jobs = [j for j in jobs if _is_pytest_job(j.get("name") or "")]
    for pytest_job in pytest_jobs:
        if pytest_job.get("databaseId") is None:
            continue
        log_text = log_fn(run_id, pytest_job["databaseId"], repo_root=root)
        if log_text:
            window = _step_window(pytest_job, SUITE_GATE_STEP_NAME)
            block = parse_suite_gate_block(log_text, window=window)
            baseline_id = baseline_id or block["baseline_id"]
            gate_found = gate_found or block["found"]
            leg = pytest_job.get("name")
            regressions += [r if leg == PYTEST_JOB else f"{leg}: {r}"
                            for r in block["regressions"]]

    if not failing and not workflow_level_failure and not missing:
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_GREEN, run_id=run_id, run_url=run_url,
                         duration_seconds=duration, baseline_id=baseline_id, state="PASS",
                         reason="every job concluded success or skipped"
                                + (f"; every required context is success ({len(required_contexts)})"
                                   if required_contexts else ""))

    if not failing and not workflow_level_failure and missing:
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_RED, run_id=run_id, run_url=run_url,
                         duration_seconds=duration, baseline_id=baseline_id, state="RED",
                         new_reds=tuple(f"missing required context: {c}" for c in missing),
                         missing_contexts=missing,
                         reason=(f"required context(s) not `success`: {', '.join(missing)} -- the "
                                 f"ruleset would not accept this sha either"))

    if baseline:
        classified = _classify(sha, baseline, run, jobs, root, log_fn=log_fn,
                               fetch_base=fetch_base, registry_loader=registry_loader)
        names = (classified.new_tests + classified.signature_changed + classified.non_test
                 + classified.newly_failing)
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_RED, run_id=run_id, run_url=run_url,
                         duration_seconds=duration,
                         baseline_id=classified.registry_baseline_id or baseline_id,
                         new_reds=names, missing_contexts=missing, state=classified.state,
                         reason=(classified.reason or f"classified {classified.state} against "
                                 f"baseline {baseline[:12]}"))

    if regressions:
        new_reds = tuple(regressions)
        reason = (f"{len(new_reds)} new red(s) named by the pytest job's own suite-baseline "
                  f"gate, against baseline {baseline_id}")
    elif failing:
        new_reds = tuple(failing)
        reason = f"job(s) did not conclude success: {', '.join(failing)}"
        if not gate_found:
            reason += (" (the pytest job's suite-baseline gate block was not found in its log "
                      "-- naming jobs, not tests)")
    else:
        new_reds = (f"workflow:{run_conclusion}",)
        reason = (f"no job named a failure, but the workflow itself concluded "
                  f"'{run_conclusion}'")
    return CiVerdict(ref=ref, sha=sha, verdict=STATE_RED, run_id=run_id, run_url=run_url,
                     duration_seconds=duration, baseline_id=baseline_id, new_reds=new_reds,
                     reason=reason, state="RED", missing_contexts=missing)


@click.command()
@click.option("--ref", required=True, help="a ref, branch or sha to read CI's verdict for")
@click.option("--repo-root", default=None, type=click.Path(file_okay=False))
@click.option("--timeout", default=POLL_TIMEOUT_S, type=int,
             help="seconds to wait, in-process, for the matched run to complete")
@click.option("--interval", default=POLL_INTERVAL_S, type=int, help="seconds between polls")
def cli(ref: str, repo_root: Optional[str], timeout: int, interval: int) -> None:
    """Read CI's verdict for --ref, waiting for its Actions run. Read-only against GitHub;
    prints one JSON object and is never a gate -- see the module docstring."""
    verdict = verdict_for(ref, repo_root=Path(repo_root) if repo_root else None,
                          timeout_s=timeout, interval_s=interval)
    click.echo(json.dumps(verdict.to_dict(), indent=2))
    raise SystemExit(0 if verdict.verdict == STATE_GREEN else 1)


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
