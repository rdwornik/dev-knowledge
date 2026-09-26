#!/usr/bin/env python
"""ci_red_age.py -- how long has main's CI been red, and since when (LANE-5B2-17, [#802]).

THE GAP THIS CLOSES, from the contract's Value line: main CI has been red on every one of the
last 30 `conductor.yml` runs (`to-browser/DIGEST-CAPABILITY-MAP-2026-09-25.md`), so a new red
raises no alarm and every gate that reads CI reads noise. This organ turns "how long" into a
number: it reads main's own `conductor.yml` run history, walks back from the newest JUDGED
(completed) run, and names the run where the current unbroken red streak began -- so a main
that stays red for a day stops being silent (`lane_digest.py`'s `OPERATOR-ACTION` line, wired
at batch close, is this organ's one declared consumer).

WHAT COUNTS AS RED. `conclusion` is read from `gh run list`, never `status`: a run still
`in_progress`/`queued` carries `conclusion: null` and is SKIPPED when walking the streak -- it
is neither evidence the streak continues nor evidence it broke, because it has not finished
judging anything yet. `success` is the only green conclusion; every other non-null conclusion
(`failure`, `cancelled`, `timed_out`, `action_required`, `startup_failure`, ...) is red --
`conductor.yml` reports red on a real failure, not on a shape this organ has to enumerate.

WHY WALK BACK RATHER THAN TRUST ONE RUN'S OWN AGE. A single run's `createdAt` says when THAT
run started, not when main first went red -- the streak can span many runs (30, per the
digest's own measurement). "Red since" is the CREATED-AT of the OLDEST run in the unbroken red
run ending at the newest judged run -- the same "first bad" idea `known_reds.py::attribute`
uses for one test, applied to a run history instead of a `git bisect`.

LIBRARY-FIRST (O-12): stdlib `datetime` for the age arithmetic; `gh run list --json` is this
repo's already-established GitHub-read pattern (`ci_verdict.py`, `actions_verdict.py`) rather
than a new API client dependency.

HONEST LIMITS:
  * A run history capped at `--limit` (default 30, matching the capability-map digest's own
    "last 30 runs" measurement) can under-report a streak older than that window -- `truncated`
    is then `True` and `hours` is a LOWER bound, never a fabricated exact one.
  * Read-only: no GitHub write call of any kind, the same posture as `ci_verdict.py`.
  * `--out-json` is this organ's own name for its structured product, deliberately not `--out`:
    every sibling organ's `--out` writes the RENDERED human report; this organ's declared
    consumer (`lane_digest.py`) needs the four fields (`since`, `hours`, `sha`, `url`) as data,
    not text to re-parse. Naming it differently says so rather than overloading the convention.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import click

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: The workflow and branch this organ reads -- main's own signal, never a lane's.
WORKFLOW = "conductor.yml"
BRANCH = "main"
GREEN_CONCLUSION = "success"
#: Done-contract item 3: "exiting non-zero when main has been red for more than 24 h."
RED_AGE_THRESHOLD_H = 24.0
GH_TIMEOUT_S = 120
_RUN_FIELDS = "databaseId,headSha,conclusion,status,url,createdAt"


class GhUnavailable(RuntimeError):
    """`gh` could not be reached, or returned something this organ could not read."""


@dataclass(frozen=True)
class RedAge:
    """main's current red streak, as this organ read it. `hours` is always >= 0."""
    since: str            # ISO 8601 createdAt of the oldest run in the current red streak
    hours: float
    sha: str
    url: str
    #: True when every JUDGED run this fetch reached was red -- the streak may extend further
    #: back than `--limit` reached, so `hours`/`since` are a lower bound / an upper bound on age.
    truncated: bool = False

    def to_dict(self) -> dict:
        return {"since": self.since, "hours": self.hours, "sha": self.sha, "url": self.url,
                "truncated": self.truncated}


def list_runs(*, repo_root: Path, workflow: str = WORKFLOW, branch: str = BRANCH,
             limit: int = 30) -> list[dict]:
    """`gh run list`'s own newest-first order, `conclusion`/`status`/`createdAt`/`headSha`/`url`
    per run. Raises `GhUnavailable` rather than returning a shape that reads as "no runs"."""
    try:
        proc = subprocess.run(
            ["gh", "run", "list", "--workflow", workflow, "--branch", branch,
             "--limit", str(limit), "--json", _RUN_FIELDS],
            cwd=str(repo_root), capture_output=True, text=True, timeout=GH_TIMEOUT_S, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise GhUnavailable(f"gh could not be run: {exc}") from exc
    if proc.returncode != 0:
        raise GhUnavailable(f"gh exited {proc.returncode}: {proc.stderr.strip()[:200]}")
    try:
        return json.loads(proc.stdout or "[]") or []
    except json.JSONDecodeError as exc:
        raise GhUnavailable(f"gh returned unreadable JSON: {exc}") from exc


def _parse(iso: str) -> datetime:
    return datetime.fromisoformat(str(iso).replace("Z", "+00:00"))


def red_since(runs: list[dict], *, now: datetime) -> Optional[RedAge]:
    """`None` when the newest JUDGED (completed, non-null `conclusion`) run is green, or when
    no run in `runs` has been judged at all -- both read as "main is not currently red".
    Otherwise the oldest run of the unbroken red streak counting back from the newest judged
    run, an in-progress/queued run (`conclusion` is `None`) neither breaking nor extending it.
    """
    judged = [r for r in runs if r.get("conclusion")]
    if not judged or judged[0]["conclusion"] == GREEN_CONCLUSION:
        return None
    streak = [judged[0]]
    for r in judged[1:]:
        if r["conclusion"] == GREEN_CONCLUSION:
            break
        streak.append(r)
    truncated = len(streak) == len(judged)  # ran out of judged runs before finding a green one
    oldest = streak[-1]
    since_dt = _parse(oldest["createdAt"])
    hours = max(0.0, (now - since_dt).total_seconds() / 3600.0)
    return RedAge(since=str(oldest["createdAt"]), hours=hours, sha=str(oldest.get("headSha") or ""),
                 url=str(oldest.get("url") or ""), truncated=truncated)


def render(result: Optional[RedAge]) -> str:
    """`RED-SINCE <iso> <hours>` (Done-contract item 3's own wording), or a clean-verdict line."""
    if result is None:
        return "RED-SINCE none -- main's newest judged conductor run is green"
    line = f"RED-SINCE {result.since} {result.hours:.1f}"
    if result.truncated:
        line += " (truncated -- the red streak may extend past the fetched window)"
    return line


def compute(*, repo_root: Path, workflow: str = WORKFLOW, branch: str = BRANCH, limit: int = 30,
           list_fn: Optional[Callable] = None, clock_fn: Optional[Callable] = None) -> Optional[RedAge]:
    """`list_fn`/`clock_fn` resolve BY NAME inside the body, never as bound defaults -- a
    default bound at `def` time would freeze the original function object, so a test that
    monkeypatches `ci_red_age.list_runs` would silently keep calling the un-patched one (the
    same reasoning `ci_verdict.verdict_for`'s docstring gives for its own `_fn` parameters)."""
    list_fn = list_fn or list_runs
    clock_fn = clock_fn or (lambda: datetime.now(timezone.utc))
    runs = list_fn(repo_root=repo_root, workflow=workflow, branch=branch, limit=limit)
    return red_since(runs, now=clock_fn())


@click.command()
@click.option("--repo-root", default=None, type=click.Path(file_okay=False))
@click.option("--workflow", default=WORKFLOW)
@click.option("--branch", default=BRANCH)
@click.option("--limit", default=30, type=int)
@click.option("--out-json", default=None, type=click.Path(dir_okay=False),
             help="write the structured result here, for lane_digest.py to read")
def cli(repo_root: Optional[str], workflow: str, branch: str, limit: int,
       out_json: Optional[str]) -> None:
    """Report how long main's `conductor.yml` has been red, and since when. Read-only against
    GitHub; exits non-zero when the streak exceeds `RED_AGE_THRESHOLD_H` (Done-contract item 3)."""
    root = Path(repo_root) if repo_root else _REPO_ROOT
    try:
        result = compute(repo_root=root, workflow=workflow, branch=branch, limit=limit)
    except GhUnavailable as exc:
        click.echo(f"ci_red_age: {exc}", err=True)
        raise SystemExit(2)
    click.echo(render(result))
    if out_json:
        payload = result.to_dict() if result else None
        Path(out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8",
                                  newline="\n")
    raise SystemExit(0 if result is None or result.hours <= RED_AGE_THRESHOLD_H else 1)


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
