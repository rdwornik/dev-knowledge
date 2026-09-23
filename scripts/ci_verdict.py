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
    `gh run view --job 107339568361 --log` on run `35907748018`, 2026-09-24.
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
from datetime import datetime
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

_RUN_FIELDS = "databaseId,headSha,status,conclusion,displayTitle,url,createdAt,updatedAt"
#: `gh run view --job <id> --log` lines are TAB-separated `<job>\t<step>\t<timestamp> <text>`.
#: Measured live, not assumed -- see the module docstring's honest limit on this format.
_LOG_TIMESTAMP_RE = re.compile(r"^\S+Z ?")
_BASELINE_SHA_RE = re.compile(r"^baseline sha\s*:\s*(\S+)$")
_REGRESSION_RE = re.compile(r"^  REGRESSION\s+(\S.*)$")
_SUITE_GATE_HEADER = "conductor suite-baseline gate"


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

    def to_dict(self) -> dict:
        return {"ref": self.ref, "sha": self.sha, "verdict": self.verdict, "run_id": self.run_id,
                "run_url": self.run_url, "duration_seconds": self.duration_seconds,
                "baseline_id": self.baseline_id, "new_reds": list(self.new_reds),
                "reason": self.reason}


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
    return _gh_json(["gh", "run", "list", "--workflow", workflow, "--limit", str(limit),
                     "--json", _RUN_FIELDS], repo_root=repo_root) or []


def find_run(sha: str, *, repo_root: Path, workflow: str = WORKFLOW,
            list_fn: Callable = list_runs) -> Optional[dict]:
    runs = list_fn(repo_root=repo_root, workflow=workflow)
    return next((r for r in runs if str(r.get("headSha", "")).startswith(sha)), None)


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


def parse_suite_gate_block(log_text: str) -> dict:
    """The baseline sha and named regressions `render_suite_gate` logged, read back out of the
    job's own log text. `found=False` means the block never printed -- the gate step did not
    run -- which the caller must not confuse with "printed and found nothing wrong"."""
    baseline_id = None
    regressions = []
    found = False
    for raw in log_text.splitlines():
        tail = raw.rsplit("\t", 1)[-1] if "\t" in raw else raw
        line = _LOG_TIMESTAMP_RE.sub("", tail)
        if line.startswith(_SUITE_GATE_HEADER):
            found = True
        m = _BASELINE_SHA_RE.match(line)
        if m:
            baseline_id = m.group(1)
        m = _REGRESSION_RE.match(line)
        if m:
            regressions.append(m.group(1))
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
                clock_fn: Callable = time.monotonic) -> CiVerdict:
    """CI's verdict for `ref`: green, red (with the new reds named), or not-run.

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
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_NOT_RUN, reason=wait_reason)

    run_id, run_url = run.get("databaseId"), run.get("url")
    duration = _duration_seconds(run)
    if run.get("status") != "completed":
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_NOT_RUN, run_id=run_id, run_url=run_url,
                         duration_seconds=duration, reason=wait_reason)

    jobs = jobs_fn(run_id, repo_root=root)
    if jobs is None:
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_NOT_RUN, run_id=run_id, run_url=run_url,
                         duration_seconds=duration,
                         reason=f"run {run_id} completed but its job list could not be read")

    job_map = {j.get("name"): j.get("conclusion") for j in jobs}
    failing = sorted(n for n, c in job_map.items() if c not in ("success", "skipped", None))

    baseline_id = None
    regressions: tuple = ()
    gate_found = False
    pytest_job = next((j for j in jobs if j.get("name") == PYTEST_JOB), None)
    if pytest_job is not None and pytest_job.get("databaseId") is not None:
        log_text = log_fn(run_id, pytest_job["databaseId"], repo_root=root)
        if log_text:
            block = parse_suite_gate_block(log_text)
            baseline_id = block["baseline_id"]
            gate_found = block["found"]
            regressions = block["regressions"]

    if not failing:
        return CiVerdict(ref=ref, sha=sha, verdict=STATE_GREEN, run_id=run_id, run_url=run_url,
                         duration_seconds=duration, baseline_id=baseline_id,
                         reason="every job concluded success or skipped")

    if regressions:
        new_reds = regressions
        reason = (f"{len(new_reds)} new red(s) named by the pytest job's own suite-baseline "
                  f"gate, against baseline {baseline_id}")
    else:
        new_reds = tuple(failing)
        reason = f"job(s) did not conclude success: {', '.join(failing)}"
        if not gate_found:
            reason += (" (the pytest job's suite-baseline gate block was not found in its log "
                      "-- naming jobs, not tests)")
    return CiVerdict(ref=ref, sha=sha, verdict=STATE_RED, run_id=run_id, run_url=run_url,
                     duration_seconds=duration, baseline_id=baseline_id, new_reds=new_reds,
                     reason=reason)


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
