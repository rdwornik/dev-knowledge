#!/usr/bin/env python
"""merge_path.py -- the integrator's ONE tracked merge path (foundation-4-merge-gate).

WHY IT EXISTS (A1/A2). The integrators' real path was the order template's "Per handback -- the
one path", executed with job-tmp scripts and hand-typed failing-id lists that no review ever saw;
`moment:merge` and `gates.py` ran zero times. This module is the tracked home of what those
scripts did, plus the two things the contract adds: the INTEGRATION-BRANCH-FIRST landing (G5/G6)
and a fail-closed read of CI (G7). Nothing here is clever: every verb is a thin, injectable
composition of organs that already exist (`ci_verdict`, `merge_receipt`, `gates`).

THE VERBS
  integration-name   the integration branch a batch pushes to: `worktree-integrate-<batch>`.
  verdict            the ONE CI-verdict function (`ci_verdict.verdict_for`) for a sha, required
                     contexts and baseline included; exit 0 only when the sha is landable.
  land               push the merge commit to the integration branch, wait for CI THERE, re-check
                     `origin/main` is still the integration base, then push the SAME sha to main.
                     Fails closed: IN-PROGRESS, CANCELLED, poll timeout, GH-UNAVAILABLE, a
                     REGRESSION or an unattributable red never land.
  verify-local       the declared gate list (`gates.py`) with one receipt step per gate.
  target-line        the pre-push stdin line the server-side `spine`/`anchor` organs read, for an
                     integration-branch push judged AS IF it were a push to main (G3).
  seal-base          the commit the server-side `seal` organ diffs against on such a push.
  ruleset check      validate `deploy/conductor-required-checks.ruleset.json`.
  ruleset apply      DRY-RUN by default; `--execute` applies it. A lane never executes it -- the
                     integrator does, after the lane merges, on the operator's recorded GO (G1).

RUN EVENTS (A4, R17). Every verb, and (through `emit_run_event`) every gate, every `dodo` organ,
`ship_gate_diff` and each receipt stage, appends ONE line `{organ, outcome, duration_ms}` to
`MERGE-PATH-RUN-EVENTS.jsonl` in the per-user state directory (`platformdirs.user_state_dir`, the
home `quota_watch` uses for the same kind of fact) -- never into a git tree and never under
`~/.claude/`. An emit that cannot write says so on stderr and returns None; telemetry must not be
able to fail a merge, and must not be able to claim it was written when it was not.

HONEST LIMITS
  * `land` is as sound as the CI it reads: a green `pytest` job means the in-CI known-reds
    compare passed. The test-level compare in `actions_verdict` is what refuses a NEW red inside
    an already-red leg when the job itself did not.
  * Until the ruleset is applied, GitHub does not itself refuse a bad push to main; `land` is
    then the only hard stop, and it is a script a person can bypass. After `ruleset apply`, the
    server is.
  * The local suite race stays: removing it needs a RATIFICATION recording Q7(a) and N6, and
    none was on the transport when this was built.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional, Sequence

import click
import platformdirs

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

# --- run events (A4) -------------------------------------------------------------------------

EVENT_SCHEMA = "merge-path-run-event/1"
EVENTS_FILENAME = "MERGE-PATH-RUN-EVENTS.jsonl"
EVENTS_PATH_ENV = "DEV_KNOWLEDGE_MERGE_PATH_EVENTS"
_STATE_APP_NAME = "dev-knowledge"
OUTCOMES = ("ok", "fail", "error")


def events_path() -> Path:
    """`$DEV_KNOWLEDGE_MERGE_PATH_EVENTS` if set (test plumbing), else the per-user OS state
    directory -- the R17 private home, the one `quota_watch.reads_ledger_path` uses."""
    override = os.environ.get(EVENTS_PATH_ENV)
    if override:
        return Path(override)
    return Path(platformdirs.user_state_dir(_STATE_APP_NAME, appauthor=False)) / EVENTS_FILENAME


def _forbidden_home(path: Path) -> Optional[str]:
    """Why `path` may not hold run events, or None. A run event is private account state: it
    never goes into a git tree (the repo would carry a file per machine) and never under
    `~/.claude/` (contract Do-not)."""
    resolved = path.resolve()
    try:
        resolved.relative_to((Path.home() / ".claude").resolve())
        return "it is under ~/.claude/"
    except ValueError:
        pass
    for parent in (resolved, *resolved.parents):
        if (parent / ".git").exists():
            return f"it is inside a git tree ({parent})"
    return None


def emit_run_event(organ: str, outcome: str, duration_s: float, **detail) -> Optional[Path]:
    """Append one run event; return the path written, or None when nothing was written.

    NEVER RAISES. A failed write prints one line on stderr and returns None, so an instrumented
    organ cannot be failed by its own telemetry -- and a caller can tell a written event from a
    dropped one, which a silent `except: pass` would hide."""
    if outcome not in OUTCOMES:
        outcome = "error"
    if not os.environ.get(EVENTS_PATH_ENV) and os.environ.get("PYTEST_CURRENT_TEST"):
        return None          # a test run writes the real home only when it redirects it on purpose
    try:
        path = events_path()
        why = _forbidden_home(path)
        if why:
            print(f"merge_path: run event for {organ} NOT written -- {why}", file=sys.stderr)
            return None
        path.parent.mkdir(parents=True, exist_ok=True)
        row = {"schema": EVENT_SCHEMA, "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "organ": organ, "outcome": outcome, "duration_ms": int(round(duration_s * 1000)),
               **{k: v for k, v in detail.items() if v is not None}}
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
        return path
    except Exception as exc:  # noqa: BLE001 -- any telemetry failure, not only OSError (grok-4.7 review)
        print(f"merge_path: run event for {organ} NOT written -- {exc!r}", file=sys.stderr)
        return None


@contextmanager
def timed_event(organ: str, **detail):
    """Time a block and emit ONE event for it: `ok` on a normal exit, `error` when it raised,
    `fail` when the block set `result["outcome"] = "fail"`. The exception still propagates."""
    result = {"outcome": "ok"}
    started = time.monotonic()
    try:
        yield result
    except BaseException:
        emit_run_event(organ, "error", time.monotonic() - started, **detail)
        raise
    emit_run_event(organ, result["outcome"], time.monotonic() - started, **detail)


def read_events(path: Optional[Path] = None) -> list[dict]:
    path = path or events_path()
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue
    return rows


# --- git plumbing (injectable) ----------------------------------------------------------------

Runner = Callable[[Sequence[str]], "tuple[int, str]"]


def _run_git(root: Path) -> Runner:
    def run(args: Sequence[str]) -> "tuple[int, str]":
        try:
            proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=300, check=False)
        except (OSError, subprocess.SubprocessError) as exc:
            return 127, f"git could not be run: {exc!r}"
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    return run


_FULL_SHA = re.compile(r"[0-9a-f]{40}")


def _same(left: str, right: str) -> bool:
    """EXACT equality of two commit ids -- a prefix is not a match (a short id can name a different
    commit; grok-4.7 review, Low)."""
    left, right = left.strip().lower(), right.strip().lower()
    return bool(left) and left == right


# --- the integration branch and the stdin the server-side organs read (G3) -------------------

INTEGRATION_BRANCH_PREFIX = "worktree-integrate-"
ZERO_SHA = "0" * 40


def integration_branch(batch: str) -> str:
    batch = batch.strip().lower().replace(" ", "-")
    if not batch or any(c in batch for c in "/\\:~^?*[@"):
        raise click.ClickException(f"{batch!r} is not a usable batch slug")
    return f"{INTEGRATION_BRANCH_PREFIX}{batch}"


def is_integration_ref(ref: str) -> bool:
    return ref.startswith(f"refs/heads/{INTEGRATION_BRANCH_PREFIX}")


def pre_push_stdin(tip: str, origin_main_sha: str) -> str:
    """The line `block_ff_push` / `block_unanchored_push` read, for an integration-branch push
    judged AS IF it were a push to main: the remote ref is `refs/heads/main`, the tip is the
    pushed sha, and the REMOTE SHA is `origin/main`'s -- not `event.before`, which is all-zero on
    a branch CREATION and the previous integration tip on an UPDATE; neither is what the push
    would replace on main (G3). Without a remote sha the organs judge an empty range and pass."""
    for label, value in (("tip", tip), ("origin/main", origin_main_sha)):
        if not value or not all(c in "0123456789abcdef" for c in value.lower()) or len(value) < 7:
            raise ValueError(f"{label} sha {value!r} is not a commit id")
    if set(origin_main_sha) == {"0"}:
        raise ValueError("origin/main resolved to the all-zero sha: the target is unknown, and "
                         "an unknown target must not be read as an empty one")
    return f"refs/heads/main {tip} refs/heads/main {origin_main_sha}\n"


# --- the verdict ------------------------------------------------------------------------------

#: The states a sha may LAND on. `PASS` is the only green. `PRE-EXISTING` (every failing test and
#: job accounted for against the registry at the base) is complete under ruling AY1-1 and keeps
#: landing possible while main carries registered reds; once the ruleset is applied GitHub itself
#: refuses a context that is not `success`. Everything else fails closed -- IN-PROGRESS,
#: CANCELLED, NO-RUN, GH-UNAVAILABLE, JOBS-UNREADABLE, UNATTRIBUTED, REGRESSED, RED (G7).
LANDABLE_STATES = ("PASS", "PRE-EXISTING")


def required_contexts() -> tuple[str, ...]:
    import actions_verdict as av
    return av.REQUIRED_CONTEXTS


def read_verdict(sha: str, *, base: str, root: Path, timeout_s: int, interval_s: int,
                 verdict_fn: Optional[Callable] = None, run_id: Optional[int] = None):
    """THE one CI verdict for `sha` -- `ci_verdict.verdict_for`, required contexts and baseline
    included. `verdict_fn` is the test seam. `run_id` pins the read to one run (the replay
    acceptance offers a cancelled run alone); it is passed only when given, so a verdict function
    that predates the pin is called exactly as before."""
    if verdict_fn is None:
        import ci_verdict as civ
        verdict_fn = civ.verdict_for
    extra = {"run_id": run_id} if run_id is not None else {}
    return verdict_fn(sha, repo_root=root, timeout_s=timeout_s, interval_s=interval_s,
                      baseline=base, required_contexts=required_contexts(), **extra)


def is_landable(verdict) -> bool:
    return (getattr(verdict, "state", "") in LANDABLE_STATES
            and not getattr(verdict, "missing_contexts", ()))


# --- land -------------------------------------------------------------------------------------

@dataclass
class LandResult:
    landed: bool
    state: str
    reason: str
    sha: str = ""
    branch: str = ""
    verdict: Optional[object] = None
    commands: list = field(default_factory=list)
    #: NO-PUSH MODE ONLY: whether the verdict read WOULD have let `sha` land. `landed` is always
    #: False in that mode; this is the answer it exists to give.
    would_land: bool = False


def land(root: Path, *, slug: str, batch: str, sha: str, base: str,
         timeout_s: int = 900, interval_s: int = 20, git: Optional[Runner] = None,
         verdict_fn: Optional[Callable] = None, record_push_fn: Optional[Callable] = None,
         record_suite_fn: Optional[Callable] = None, no_push: bool = False,
         run_id: Optional[int] = None) -> LandResult:
    """Integration branch first, then the SAME sha to main. See the module docstring.

    Refuses (never lands) when: `sha` is not a merge commit whose first parent is `base`;
    `origin/main` is no longer `base` (before the integration push AND again before the push to
    main); the push to the integration branch fails; CI's verdict for `sha` is not landable. The
    first refusal wins and nothing after it runs.

    `no_push=True` (b2-merge-gate, item 4) is the REPLAY mode: it judges `sha` against `base`
    exactly as a landing would -- the same merge-on-base check, the same ONE verdict -- and then
    stops. It pushes NOTHING (the replay's sha was pushed to a scratch branch by hand), asks
    `origin/main` nothing (a merge already on main is not on its base any more), records no receipt
    step, and never reports `landed`. `run_id` pins the verdict to one run."""
    git = git or _run_git(root)
    if record_push_fn is None or record_suite_fn is None:
        import merge_receipt as mr
        record_push_fn = record_push_fn or mr.record_push
        record_suite_fn = record_suite_fn or mr.record_actions_verdict
    branch = integration_branch(batch)
    commands: list = []

    def refuse(state: str, reason: str, verdict=None) -> LandResult:
        return LandResult(False, state, reason, sha=sha, branch=branch, verdict=verdict,
                          commands=commands)

    if not _FULL_SHA.fullmatch(base.strip().lower()):
        return refuse("BASE-NOT-FULL", f"--base {base!r} is not a full 40-hex sha; pass "
                                       f"`git rev-parse origin/main` as fetched before the merge")
    code, out = git(["rev-list", "--parents", "-n", "1", sha])
    parts = out.split()
    if code != 0 or len(parts) != 3 or not _same(parts[1], base):
        return refuse("NOT-A-MERGE-ON-BASE",
                      f"{sha} is not a two-parent merge commit whose first parent is the "
                      f"integration base {base} (git said: {out.strip()[:160]!r})")
    sha = parts[0]

    if no_push:
        verdict = read_verdict(sha, base=base, root=root, timeout_s=timeout_s,
                               interval_s=interval_s, verdict_fn=verdict_fn, run_id=run_id)
        state = getattr(verdict, "state", "UNKNOWN") or "UNKNOWN"
        return LandResult(False, state, getattr(verdict, "reason", "") or "", sha=sha,
                          branch=branch, verdict=verdict, commands=commands,
                          would_land=is_landable(verdict))

    def origin_main() -> "tuple[bool, str]":
        c, o = git(["ls-remote", "origin", "refs/heads/main"])
        fields = o.split()
        return (c == 0 and bool(fields)), (fields[0] if fields else o.strip()[:160])

    ok, remote = origin_main()
    if not ok or not _same(remote, base):
        return refuse("BASE-MOVED", f"origin/main is {remote!r}, not the integration base {base}: "
                                    f"re-merge on the new main rather than landing on a stale one")

    push = ["push", "origin", f"{sha}:refs/heads/{branch}"]
    commands.append(push)
    started = time.monotonic()
    code, out = git(push)
    pushed_s = time.monotonic() - started
    if code != 0:
        return refuse("INTEGRATION-PUSH-FAILED", out.strip()[:300])
    record_push_fn(root, slug=slug, target="integration", branch=branch, sha=sha, seconds=pushed_s)

    verdict = read_verdict(sha, base=base, root=root, timeout_s=timeout_s, interval_s=interval_s,
                           verdict_fn=verdict_fn)
    try:
        # The receipt's suite step is a SECOND read of the same run: it is handed the same six
        # required contexts the landing decision above judged, so a receipt cannot complete on a
        # state `land` refused, and its FLAGGED buckets are what the receipt records.
        record_suite_fn(root, slug=slug, sha=sha, required_contexts=required_contexts())
    except Exception as exc:                  # noqa: BLE001 -- recorded in the refusal, never hidden
        return refuse("RECEIPT-REFUSED", f"the suite read could not be recorded: {exc}", verdict)
    if not is_landable(verdict):
        return refuse(getattr(verdict, "state", "UNKNOWN") or "UNKNOWN",
                      getattr(verdict, "reason", "") or "CI's verdict is not landable", verdict)

    ok, remote = origin_main()
    if not ok or not _same(remote, base):
        return refuse("BASE-MOVED", f"origin/main moved to {remote!r} while CI ran on the "
                                    f"integration branch; the judged sha is no longer the next "
                                    f"commit on main", verdict)
    push_main = ["push", "origin", f"{sha}:refs/heads/main"]
    commands.append(push_main)
    started = time.monotonic()
    code, out = git(push_main)
    main_s = time.monotonic() - started
    if code != 0:
        return refuse("MAIN-PUSH-REFUSED", out.strip()[:300], verdict)
    record_push_fn(root, slug=slug, target="main", branch="main", sha=sha, seconds=main_s)
    return LandResult(True, getattr(verdict, "state", "PASS"),
                      f"{sha[:12]} landed on main after CI on {branch}", sha=sha, branch=branch,
                      verdict=verdict, commands=commands)


# --- the ruleset (items 7, 13, 14) ------------------------------------------------------------

RULESET_RELPATH = "deploy/conductor-required-checks.ruleset.json"


def ruleset_problems(payload: dict) -> list[str]:
    """Everything wrong with the payload as a FILE (it arrives `enforcement: disabled`)."""
    problems: list[str] = []
    if payload.get("bypass_actors") != []:
        problems.append("bypass_actors must be an empty list: a bypass actor is the rule's escape")
    if payload.get("conditions", {}).get("ref_name", {}).get("include") != ["refs/heads/main"]:
        problems.append("conditions.ref_name.include must be exactly ['refs/heads/main']")
    if payload.get("enforcement") != "disabled":
        problems.append("the FILE must say enforcement: disabled -- `ruleset apply` is the only "
                        "thing that sets it active")
    rules = payload.get("rules") or []
    if [r.get("type") for r in rules] != ["required_status_checks"]:
        problems.append("rules must be exactly one required_status_checks rule")
        return problems
    contexts = [c.get("context") for c in rules[0].get("parameters", {})
                .get("required_status_checks", [])]
    expected = list(required_contexts())
    if sorted(contexts) != sorted(expected):
        problems.append(f"required contexts are {contexts}, expected exactly {expected}")
    return problems


def apply_plan(payload: dict, repo: str) -> dict:
    """The command and the body `ruleset apply` would send: the file's payload with
    `enforcement: active`. The FILE is never rewritten."""
    body = json.loads(json.dumps(payload))
    body["enforcement"] = "active"
    return {"argv": ["gh", "api", f"repos/{repo}/rulesets", "--input", "-"], "body": body}


#: THE REHEARSAL RECORD (b2-merge-gate item 5, R64; foundation-4's G1). The ruleset is armed only
#: after a rehearsal that comes FIRST: a push run on a named sha in which both pytest legs and every
#: other required context are `success`. `ruleset rehearse` writes the record from the run's own
#: job list; `ruleset apply --execute` refuses without one that shows exactly that. It replaces a
#: live CI read inside `apply`, which asked for the two pytest legs only and left nothing on disk
#: for the integrator (or a later reader) to point at.
REHEARSAL_SCHEMA = "merge-path-rehearsal/1"


def read_rehearsal(sha: str, *, root: Path, run_fn: Optional[Callable] = None,
                   jobs_fn: Optional[Callable] = None) -> dict:
    """The rehearsal record for `sha`, read from its newest PUSH run's own jobs: every required
    context's conclusion (`not-run` when the run has no such job, or there is no push run at all).
    `run_fn` / `jobs_fn` are the test seams. Writes nothing; the verb saves the dict."""
    import ci_verdict as civ
    run_fn = run_fn or (lambda s, **kw: civ.find_run(s, **kw))
    jobs_fn = jobs_fn or civ.fetch_jobs
    run = run_fn(sha, repo_root=root)
    jobs = jobs_fn(run["databaseId"], repo_root=root) if run else None
    conclusions = {j.get("name"): j.get("conclusion") for j in (jobs or [])}
    required = required_contexts()
    contexts = {c: (conclusions.get(c, "not-run") if run else "not-run") for c in required}
    return {"schema": REHEARSAL_SCHEMA, "sha": sha, "run_id": run.get("databaseId") if run else None,
            "run_url": run.get("url") if run else None, "event": run.get("event") if run else None,
            "run_status": run.get("status") if run else None,
            "run_conclusion": run.get("conclusion") if run else None, "contexts": contexts,
            "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def rehearsal_problems(record: object, sha: str) -> list[str]:
    """What is wrong with a rehearsal record as the evidence to arm the ruleset on `sha`: another
    schema, another sha, a run that is not a push run, or ANY required context (both pytest legs
    included) that is not `success`. An empty list is the only thing `apply` accepts."""
    if not isinstance(record, dict):
        return ["the rehearsal record is not an object"]
    problems: list[str] = []
    if record.get("schema") != REHEARSAL_SCHEMA:
        problems.append(f"the rehearsal record's schema is {record.get('schema')!r}, expected "
                        f"{REHEARSAL_SCHEMA!r}")
    if not _same(str(record.get("sha", "")), sha):
        problems.append(f"the rehearsal record is for {str(record.get('sha', ''))[:12] or 'no sha'}, "
                        f"not the sha named for arming ({sha[:12]}): a rehearsal vouches for the "
                        f"sha it ran on and no other")
    if record.get("event") != "push":
        problems.append(f"the rehearsal record is of a {record.get('event')!r} run; only a `push` "
                        f"run carries the check-runs the ruleset reads")
    run_id = record.get("run_id")
    if not isinstance(run_id, int) or isinstance(run_id, bool):
        problems.append(f"the rehearsal record names no run (run_id {run_id!r}): the evidence is a "
                        f"run's own job list, so a record that cannot say which run it read is "
                        f"not a rehearsal")
    if record.get("run_status") != "completed":
        problems.append(f"the rehearsal record's run_status is {record.get('run_status')!r}, not "
                        f"'completed': a run still going has not shown its contexts")
    contexts = record.get("contexts") if isinstance(record.get("contexts"), dict) else {}
    for context in required_contexts():
        conclusion = contexts.get(context, "not-run")
        if conclusion != "success":
            problems.append(f"{context}: {conclusion if conclusion is not None else 'in-progress'}"
                            f" on the rehearsal sha -- both pytest legs and every required context "
                            f"must be `success` before a ruleset targets main (G1)")
    return problems


def apply_preconditions(sha: str, *, root: Path, go: str,
                        rehearsal_path: Optional[Path] = None) -> list[str]:
    """G1: the operator's recorded GO named, and a REHEARSAL RECORD for the named sha showing both
    pytest legs and every required context `success` (`rehearsal_problems`). No record is its own
    unmet precondition: arming is refused without one. Returns the unmet preconditions."""
    unmet: list[str] = []
    if not go.strip():
        unmet.append("no operator GO named (--go '<the recorded GO>')")
    if rehearsal_path is None:
        unmet.append("no rehearsal record named (--rehearsal <file written by `ruleset "
                     "rehearse`>): the ruleset is armed only after a rehearsal that comes first (R64)")
        return unmet
    try:
        record = json.loads(Path(rehearsal_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        unmet.append(f"the rehearsal record {rehearsal_path} cannot be read: {exc}")
        return unmet
    unmet += rehearsal_problems(record, sha)
    return unmet


# --- CLI --------------------------------------------------------------------------------------

def _root(repo_root: Optional[str]) -> Path:
    return Path(repo_root) if repo_root else _REPO_ROOT


@click.group(help="The integrator's tracked merge path (foundation-4-merge-gate).")
@click.option("--repo-root", default=None, type=click.Path(file_okay=False))
@click.pass_context
def cli(ctx: click.Context, repo_root: Optional[str]) -> None:
    ctx.ensure_object(dict)
    ctx.obj["root"] = _root(repo_root)


@cli.command("integration-name")
@click.option("--batch", required=True)
def cmd_integration_name(batch: str) -> None:
    """Print the integration branch for a batch."""
    click.echo(integration_branch(batch))


@cli.command("target-line")
@click.option("--tip", required=True, help="the pushed sha")
@click.option("--remote-sha", default=None,
              help="origin/main's sha [default: resolved from origin/main in --repo-root]")
@click.option("--out", default=None, type=click.Path(dir_okay=False),
              help="write the line here (a FILE, so the consuming organ reads it by `<`, never a "
                   "pipe that would mask a failing first stage)")
@click.pass_context
def cmd_target_line(ctx: click.Context, tip: str, remote_sha: Optional[str],
                    out: Optional[str]) -> None:
    """The stdin line the server-side spine/anchor organs read for an integration-branch push."""
    if remote_sha is None:
        code, text = _run_git(ctx.obj["root"])(["rev-parse", "--verify", "origin/main"])
        if code != 0:
            raise click.ClickException(f"origin/main does not resolve: {text.strip()[:160]}")
        remote_sha = text.strip()
    try:
        line = pre_push_stdin(tip, remote_sha)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
    if out:
        Path(out).write_text(line, encoding="utf-8", newline="\n")
    else:
        click.echo(line, nl=False)


@cli.command("seal-base")
@click.option("--head", default="HEAD")
@click.pass_context
def cmd_seal_base(ctx: click.Context, head: str) -> None:
    """The commit `seal` diffs against on an integration-branch push: merge-base(origin/main,
    HEAD). An unresolvable base is an error -- an unknown base must not read as 'no ADDs'."""
    code, text = _run_git(ctx.obj["root"])(["merge-base", "origin/main", head])
    if code != 0 or not text.strip():
        raise click.ClickException(f"no merge-base of origin/main and {head}: {text.strip()[:160]}")
    click.echo(text.strip())


@cli.command("verdict")
@click.option("--sha", required=True)
@click.option("--base", required=True, help="the integration base (the merge's first parent)")
@click.option("--timeout", "timeout_s", default=900, type=int)
@click.option("--interval", "interval_s", default=20, type=int)
@click.option("--run-id", "run_id", default=None, type=int,
              help="read THIS run alone instead of the newest push run for the sha")
@click.pass_context
def cmd_verdict(ctx: click.Context, sha: str, base: str, timeout_s: int, interval_s: int,
                run_id: Optional[int]) -> None:
    """Read the ONE CI verdict for a sha. Exit 0 only when it is landable."""
    with timed_event("merge_path.verdict", sha=sha[:12]) as result:
        verdict = read_verdict(sha, base=base, root=ctx.obj["root"], timeout_s=timeout_s,
                               interval_s=interval_s, run_id=run_id)
        landable = is_landable(verdict)
        result["outcome"] = "ok" if landable else "fail"
    click.echo(json.dumps(verdict.to_dict(), indent=2))
    raise SystemExit(0 if landable else 1)


@cli.command("land")
@click.option("--slug", default="", help="the open merge receipt (not used by --no-push)")
@click.option("--batch", required=True)
@click.option("--sha", required=True, help="the merge commit")
@click.option("--base", required=True, help="the integration base: origin/main when the merge "
                                            "was made, and the merge's first parent")
@click.option("--timeout", "timeout_s", default=900, type=int)
@click.option("--interval", "interval_s", default=20, type=int)
@click.option("--no-push", "no_push", is_flag=True, default=False,
              help="judge only: read the verdict a landing would read, print it with its flagged "
                   "buckets, push NOTHING and write no receipt step (the run event every verb "
                   "emits to the private state home is still written, with no_push=true). "
                   "Exit 0 when the sha WOULD land")
@click.option("--run-id", "run_id", default=None, type=int,
              help="read THIS run alone instead of the newest push run for the sha")
@click.pass_context
def cmd_land(ctx: click.Context, slug: str, batch: str, sha: str, base: str, timeout_s: int,
             interval_s: int, no_push: bool, run_id: Optional[int]) -> None:
    """Integration branch first, CI there, then the same sha to main."""
    if not no_push and not slug:
        raise click.UsageError("--slug is required unless --no-push")
    started = time.monotonic()
    result = land(ctx.obj["root"], slug=slug, batch=batch, sha=sha, base=base,
                  timeout_s=timeout_s, interval_s=interval_s, no_push=no_push, run_id=run_id)
    ok = result.would_land if no_push else result.landed
    emit_run_event("merge_path.land", "ok" if ok else "fail", time.monotonic() - started,
                   state=result.state, sha=result.sha[:12], no_push=no_push)
    if no_push:
        click.echo(f"land: NO-PUSH {result.state} -- {result.reason or 'no reason given'}")
        click.echo(f"land: would land: {'YES' if result.would_land else 'NO'}")
    else:
        click.echo(f"land: {'LANDED' if result.landed else 'REFUSED'} {result.state} -- "
                   f"{result.reason}")
    _echo_flagged(result.verdict)
    raise SystemExit(0 if ok else 1)


def _echo_flagged(verdict: object) -> None:
    """The verdict's flagged buckets and the rows they owe, printed by name: a red that is
    present on both sides is not refused, and it is not allowed to be silent either."""
    import merge_receipt as mr
    run_id = getattr(verdict, "run_id", None)
    if run_id is not None:
        click.echo(f"land: run {run_id}")
    flagged = tuple(getattr(verdict, "flagged", ()) or ())
    for item in flagged:
        click.echo(f"land: FLAGGED (red on both sides, NOT a refusal) {item}")
    for owed in mr.rows_owed(flagged):
        click.echo(f"land: {owed}")
    for item in getattr(verdict, "missing_contexts", ()) or ():
        click.echo(f"land: NON-PASS REQUIRED CHECK (refuses) {item}")


@cli.command("verify-local")
@click.option("--lane", required=True)
@click.option("--slug", default=None, help="record each gate as a `gate:<name>` receipt step")
@click.option("--base", default=None)
@click.pass_context
def cmd_verify_local(ctx: click.Context, lane: str, slug: Optional[str],
                     base: Optional[str]) -> None:
    """Run the declared gate list once (`gates.py`), one run event and -- with --slug -- one
    receipt step per gate. A red gate fails the verb; none is skipped."""
    import gates
    import merge_receipt as mr
    root = ctx.obj["root"]
    verdict = gates.run_gates(gates.GATES, lane=lane, cwd=root, base=base)
    for row in verdict["gates"]:
        click.echo(f"verify-local: {'ok ' if row['exit_code'] == 0 else 'RED'} {row['name']} "
                   f"exit={row['exit_code']} {row['duration_ms']}ms")
    if slug:
        receipt = mr.load_receipt(root, slug)
        for row in verdict["gates"]:
            receipt.steps.append(mr.StepTiming(
                step=f"gate:{row['name']}", step_class=mr.CLASS_TESTS,
                seconds=round(row["duration_ms"] / 1000.0, 3), ok=row["exit_code"] == 0,
                returncode=row["exit_code"], command=" ".join(row["argv"]) or row["name"],
                started=mr._now()))
        mr.save_receipt(root, receipt)
    click.echo(f"verify-local: {verdict['verdict']}")
    raise SystemExit(gates.exit_code_for(verdict))


@cli.group("ruleset")
def ruleset_group() -> None:
    """Check and apply the required-checks ruleset payload."""


def _load_ruleset(root: Path) -> dict:
    return json.loads((root / RULESET_RELPATH).read_text(encoding="utf-8"))


@ruleset_group.command("check")
@click.pass_context
def cmd_ruleset_check(ctx: click.Context) -> None:
    problems = ruleset_problems(_load_ruleset(ctx.obj["root"]))
    for problem in problems:
        click.echo(f"ruleset: PROBLEM {problem}")
    click.echo(f"ruleset: {'FAIL' if problems else 'OK'} ({RULESET_RELPATH})")
    raise SystemExit(1 if problems else 0)


@ruleset_group.command("rehearse")
@click.option("--sha", required=True, help="the rehearsal sha: its push run is read, test by test "
                                           "none of it -- every required context's own conclusion")
@click.option("--out", required=True, type=click.Path(dir_okay=False),
              help="write the rehearsal record here (JSON); `ruleset apply --rehearsal` reads it")
@click.pass_context
def cmd_ruleset_rehearse(ctx: click.Context, sha: str, out: str) -> None:
    """Record whether `sha` is a green rehearsal: both pytest legs and every required context
    `success` on its push run. The record is written EVEN WHEN it is not green -- an honest
    failure on disk -- and exits 0 only when it is. Writes nothing to GitHub."""
    with timed_event("merge_path.ruleset-rehearse", sha=sha[:12]) as result:
        record = read_rehearsal(sha, root=ctx.obj["root"])
        problems = rehearsal_problems(record, sha)
        result["outcome"] = "fail" if problems else "ok"
    Path(out).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    for context in required_contexts():
        click.echo(f"rehearse: {context}: {record['contexts'].get(context)}")
    for item in problems:
        click.echo(f"rehearse: PROBLEM {item}")
    click.echo(f"rehearse: {'NOT GREEN' if problems else 'GREEN'} {sha[:12]} "
               f"run {record.get('run_id')} -> {out}")
    raise SystemExit(1 if problems else 0)


@ruleset_group.command("apply")
@click.option("--repo", required=True, help="owner/name")
@click.option("--sha", required=True, help="the rehearsal sha: both pytest legs and every "
                                           "required context must be `success` on it")
@click.option("--go", default="", help="the operator's recorded GO, named")
@click.option("--rehearsal", "rehearsal", default=None, type=click.Path(dir_okay=False),
              help="the rehearsal record written by `ruleset rehearse` for --sha; --execute is "
                   "refused without one that shows every required context `success`")
@click.option("--execute", is_flag=True, default=False,
              help="actually apply. Without it this is a DRY RUN and writes nothing.")
@click.pass_context
def cmd_ruleset_apply(ctx: click.Context, repo: str, sha: str, go: str, rehearsal: Optional[str],
                      execute: bool) -> None:
    """Apply the ruleset to main with `enforcement: active`, then read it back. DRY-RUN by
    default. A lane never passes --execute."""
    root = ctx.obj["root"]
    payload = _load_ruleset(root)
    problems = ruleset_problems(payload)
    plan = apply_plan(payload, repo)
    click.echo("ruleset apply: " + ("EXECUTE" if execute else "DRY RUN (nothing is sent)"))
    click.echo(f"  command : {' '.join(plan['argv'])}")
    click.echo(f"  contexts: {', '.join(required_contexts())}")
    click.echo(f"  sets    : enforcement {payload.get('enforcement')} -> active")
    preconditions = apply_preconditions(sha, root=root, go=go,
                                        rehearsal_path=Path(rehearsal) if rehearsal else None)
    unmet = problems + (preconditions if execute else [])
    for item in unmet:
        click.echo(f"  UNMET   : {item}")
    if not execute:
        for item in preconditions:
            click.echo(f"  WOULD REFUSE --execute: {item}")
        raise SystemExit(1 if problems else 0)
    if unmet:
        raise SystemExit(1)
    started = time.monotonic()
    proc = subprocess.run(plan["argv"], input=json.dumps(plan["body"]), capture_output=True,
                          text=True, cwd=str(root), check=False)
    emit_run_event("merge_path.ruleset-apply", "ok" if proc.returncode == 0 else "fail",
                   time.monotonic() - started, repo=repo)
    if proc.returncode != 0:
        raise click.ClickException(f"gh api exited {proc.returncode}: {proc.stderr.strip()[:300]}")
    back = subprocess.run(["gh", "api", f"repos/{repo}/rulesets"], capture_output=True, text=True,
                          cwd=str(root), check=False)
    names = [r.get("name") for r in json.loads(back.stdout or "[]")] if back.returncode == 0 else []
    if payload["name"] not in names:
        raise click.ClickException("applied, but the read-back does not list the ruleset")
    click.echo(f"ruleset apply: APPLIED and read back ({payload['name']})")


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
