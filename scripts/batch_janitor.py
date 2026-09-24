#!/usr/bin/env python
"""batch_janitor.py — stops a named batch's FINISHED sessions (`[#1014]`, DIGEST-WAVE5A blind
spot 3's own line item: "Lanes reported memory/reaper kills ... several lane jobs' stop/rm
printed nothing" and "~7 finished lane/repair `claude` processes stayed resident (~360-400 MB
each), which held a repair below the 3 GB threshold").

WHAT "FINISHED" MEANS, and where that answer comes from. A `--bg` session is a daemon job:
`claude agents --json` keeps listing it, at a TERMINAL state (`done`, `stopped`, `failed`,
`error`, `exited`, `cancelled`/`canceled`), long after the work is over — it does not vanish
the moment the lane hands back. This module reads that listing once per run and calls a job
FINISHED when its listed state is terminal, or it is absent from the listing at all (the same
"absent is ended too" convention `dispatch.py::lane_alive` already states, because an ended
`--bg` job normally stays listed rather than disappearing — an absence is the ended case with
no state to name).

WHICH JOBS BELONG TO THE BATCH, and why that question has exactly one answer surface.
`claude agents --json` names no batch at all — nothing in the live listing says which night's
work a job was. `scripts/dispatch.py` is the one thing that DOES know: every launch writes
`logs/receipts/LAUNCH-JOB-<job_id>.json` carrying `batch`, `slug` and `job_id` together
(`dispatch._write_launch_records`). This module reads that record, never re-derives the
mapping, for the same reason `merge_receipt.py` reads `actions_verdict`/`routing_agreement`
rather than restating their vocabulary: a job either belongs to a batch or it does not, and
that fact has one home.

THE STOP VERB IS `claude stop <job_id>`, NOT `claude rm`. `claude stop` ends the daemon job
(the resident process the DIGEST's blind spot is about) and leaves the worktree and the job
record in place — measured on this fleet (2026-09-19, CLI 2.1.278): stopping a session whose
record already reads `done` does NOT get resumed by the daemon (a stop issued on a job still
`running`/`working` can be — this module never targets one of those, because a job in either
state is LIVE and is never in the "finished" set `run_janitor` stops). `claude rm` additionally
deletes the worktree and the job record, which is a second, more destructive act this
contract's Done-when does not ask for; a lane wanting that runs it by hand.

HONEST LIMITS:
  * A lane launched by hand, outside `dispatch.py launch`, wrote no `LAUNCH-JOB-*.json` and is
    INVISIBLE to this module — it can stop only what dispatch's own receipts named.
  * The live listing is read ONCE per `run_janitor` call (before) and once more after stopping
    (after); a job that changes state between those two reads is reported honestly, not
    re-polled to a fixpoint.
  * `claude agents --json` failing to read at all REFUSES the whole run (`BatchJanitorError`)
    rather than guessing which jobs are safe to stop — the same fail-closed posture
    `merge_receipt.first_parent_of` takes on an unreadable git call.
  * This module drives no state on its own initiative: it names dispatch's own receipts and
    runs the same `claude stop` a person would type. Wiring it into a moment (when it runs, and
    on whose behalf) is `lane-organ-wirings`' surface, not this one's.
"""
from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass
from typing import Callable, Mapping, Optional, Sequence

import click

# THE BATCH-TO-JOB MAP, AND THE LIVE LISTING, imported rather than restated -- same shape and
# argument as `merge_receipt.py`'s `actions_verdict`/`routing_agreement` imports just above it:
# "does this job belong to this batch" and "is this job still running" each have ONE home, and
# a second copy of either question would drift from the launcher that actually answers it.
try:
    from scripts import dispatch as _ds
except ImportError:  # pragma: no cover -- exercised by the scripts/-on-sys.path entrypoint
    import dispatch as _ds

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("batch-janitor")

#: Terminal job-listing states. MIRRORS `dispatch.py`'s OWN `_ENDED` set — that name is
#: private to that module (no public "is this listing entry live" reader exists to import), so
#: the small vocabulary is duplicated here rather than reached into across the module boundary.
#: It is git's/the CLI's own fixed enum, not expected to drift the way a structured protocol
#: would; if it ever does, `tests/test_batch_janitor.py` and `tests/test_dispatch_py.py` both
#: pin their own copy and would disagree.
_ENDED_STATES = frozenset({"done", "stopped", "failed", "error", "exited", "cancelled",
                           "canceled"})


class BatchJanitorError(RuntimeError):
    """The janitor could not determine what is safe to touch. Raised, never guessed past: an
    unreadable live listing must refuse the run rather than pick a side on which jobs are
    finished."""


@dataclass(frozen=True)
class LaneSession:
    """One batch lane's session, as the janitor sees it: dispatch's own launch record, joined
    to the live listing's reading of that job (or the honest absence of one)."""
    slug: str
    job_id: str
    worktree: str
    #: The listing's own state string; `"ABSENT"` when the job carries no listing entry at all.
    state: str
    #: False = FINISHED -- a terminal state, or absent from the listing entirely (the same
    #: "absent is ended too" rule `dispatch.py::lane_alive` states for a `--bg` job).
    live: bool


@dataclass(frozen=True)
class StopOutcome:
    """What happened when the janitor tried to stop one session."""
    session: LaneSession
    ran: bool
    returncode: Optional[int]
    output: str

    @property
    def ok(self) -> bool:
        return self.ran and self.returncode == 0


@dataclass(frozen=True)
class JanitorReport:
    """One run of the janitor over one batch. `before`/`after` are BOTH the full session list —
    a report that only ever names the finished ones could not show a session the run's own
    action changed, or one it left alone."""
    batch: str
    dry_run: bool
    before: tuple[LaneSession, ...]
    stopped: tuple[StopOutcome, ...]
    after: tuple[LaneSession, ...]

    def finished(self, sessions: Sequence[LaneSession]) -> tuple[LaneSession, ...]:
        return tuple(s for s in sessions if not s.live)

    def render(self) -> str:
        before_finished = self.finished(self.before)
        lines = [f"batch janitor {self.batch!r}: {len(self.before)} lane job(s) on record, "
                 f"{len(before_finished)} finished before this run"]
        if not self.before:
            lines.append("  NO JOB RECORDS for this batch -- nothing dispatch.py launched is "
                         "known here, which is not the same as 'nothing to stop'")
        if self.dry_run:
            lines.append("  DRY RUN -- nothing stopped")
            for s in before_finished:
                lines.append(f"    would stop {s.slug} (job {s.job_id}, state={s.state})")
            return "\n".join(lines)
        for outcome in self.stopped:
            s = outcome.session
            verdict = ("ok" if outcome.ok else
                      "SKIPPED (no job_id)" if not outcome.ran else
                      f"FAILED rc={outcome.returncode}")
            lines.append(f"    stopped {s.slug} (job {s.job_id}, was {s.state}): {verdict}")
        after_finished = self.finished(self.after)
        lines.append(f"  {len(before_finished)} finished before -> "
                     f"{len(after_finished)} finished after "
                     f"({len(self.after) - len(after_finished)} of {len(self.after)} now live)")
        return "\n".join(lines)


def _job_records() -> list[dict]:
    """Every `LAUNCH-JOB-*.json` record under dispatch's own `receipts_dir()`.

    NO `repo_root` PARAMETER, DELIBERATELY: `dispatch.receipts_dir()` is driven by
    `HARNESS_RECEIPTS_DIR` (else the hub's own `logs/receipts/`), never by a directory argument
    -- the same surface dispatch.py's own launch/receipt functions read, so this reads it the
    same way rather than threading a path nothing downstream would use.

    NOT the live listing -- this is the only place a job is tied to a BATCH at all. A record
    that fails to parse is LOGGED and skipped, the same posture `merge_receipt.read_ledger`
    takes on a bad ledger line: one bad file must not make every good one unreadable.
    """
    directory = _ds.receipts_dir()
    if not directory.is_dir():
        return []
    out: list[dict] = []
    for path in sorted(directory.glob("LAUNCH-JOB-*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("%s is unreadable and was skipped: %s", path, exc)
            continue
        if isinstance(body, dict):
            out.append(body)
    return out


def batch_jobs(batch: str) -> list[dict]:
    """The `_job_records` belonging to `batch`, slug-sorted for a stable report."""
    return sorted((r for r in _job_records() if r.get("batch") == batch),
                 key=lambda r: str(r.get("slug") or ""))


def _find_entry(listing: Sequence[Mapping], job_id: str) -> Optional[Mapping]:
    return next((e for e in listing if str(e.get("id") or "") == job_id), None)


def read_sessions(batch: str, *,
                  agents: Optional[Callable[[], list[dict]]] = None) -> tuple[LaneSession, ...]:
    """The batch's lanes, each joined to the live listing's reading of its job.

    FAILS CLOSED on an unreadable listing (`BatchJanitorError`): a batch janitor that could not
    read `claude agents --json` and guessed "probably finished" would be the one mechanism in
    this repo where that guess KILLS a live session. Refusing beats guessing here more than it
    does almost anywhere else in this codebase.
    """
    fetch = agents or _ds.list_agents
    try:
        listing = fetch()
    except _ds.ListingUnreadable as exc:
        raise BatchJanitorError(
            f"`claude agents --json` could not be read: {exc}. Refusing to guess which of "
            f"batch {batch!r}'s jobs are finished -- an unread listing is not evidence of "
            f"either state") from exc
    out = []
    for job in batch_jobs(batch):
        job_id = str(job.get("job_id") or "")
        entry = _find_entry(listing, job_id) if job_id else None
        state = str(entry.get("state") or "") if entry is not None else "ABSENT"
        live = entry is not None and str(entry.get("state") or "").lower() not in _ENDED_STATES
        out.append(LaneSession(slug=str(job.get("slug") or ""), job_id=job_id,
                               worktree=str(job.get("worktree") or ""), state=state, live=live))
    return tuple(out)


def stop_session(session: LaneSession, *,
                 run: Optional[Callable[[list[str]], "subprocess.CompletedProcess[str]"]] = None
                 ) -> StopOutcome:
    """`claude stop <job_id>` -- ends the daemon job. See the module docstring for why `stop`
    and not `rm`, and why this is safe on a FINISHED record specifically."""
    if not session.job_id:
        return StopOutcome(session=session, ran=False, returncode=None,
                           output="no job_id on this record -- nothing to stop")
    caller = run or (lambda argv: subprocess.run(
        argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60))
    try:
        proc = caller(["claude", "stop", session.job_id])
    except (OSError, subprocess.SubprocessError) as exc:
        return StopOutcome(session=session, ran=True, returncode=None, output=repr(exc))
    return StopOutcome(session=session, ran=True, returncode=proc.returncode,
                       output=(proc.stdout or "") + (proc.stderr or ""))


def run_janitor(batch: str, *, dry_run: bool = False,
                agents: Optional[Callable[[], list[dict]]] = None,
                run: Optional[Callable[[list[str]], "subprocess.CompletedProcess[str]"]] = None
                ) -> JanitorReport:
    """The whole act: read, and — unless `dry_run` — stop every FINISHED session, then read
    again. `dry_run` returns before `stop_session` is ever called, which is what proves a
    dry run lists and stops nothing (`stopped == ()`, `after is before`)."""
    before = read_sessions(batch, agents=agents)
    if dry_run:
        return JanitorReport(batch=batch, dry_run=True, before=before, stopped=(), after=before)
    targets = tuple(s for s in before if not s.live)
    stopped = tuple(stop_session(s, run=run) for s in targets)
    after = read_sessions(batch, agents=agents)
    return JanitorReport(batch=batch, dry_run=False, before=before, stopped=stopped, after=after)


# --- CLI -------------------------------------------------------------------------------------

@click.group(help="Stops a named batch's FINISHED --bg sessions (`[#1014]`).")
def cli() -> None:
    pass


@cli.command("run")
@click.option("--batch", required=True, help="the batch whose finished sessions are stopped")
@click.option("--dry-run", is_flag=True, default=False,
             help="list what would be stopped; stop and touch nothing")
def cmd_run(batch: str, dry_run: bool) -> None:
    try:
        report = run_janitor(batch, dry_run=dry_run)
    except BatchJanitorError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(report.render())
    failed = [o for o in report.stopped if o.ran and not o.ok]
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
