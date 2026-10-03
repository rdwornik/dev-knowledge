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
    except OSError as exc:
        print(f"merge_path: run event for {organ} NOT written -- {exc}", file=sys.stderr)
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


def _same(left: str, right: str) -> bool:
    left, right = left.strip(), right.strip()
    return bool(left and right) and (left.startswith(right) or right.startswith(left))


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
                 verdict_fn: Optional[Callable] = None):
    """THE one CI verdict for `sha` -- `ci_verdict.verdict_for`, required contexts and baseline
    included. `verdict_fn` is the test seam."""
    if verdict_fn is None:
        import ci_verdict as civ
        verdict_fn = civ.verdict_for
    return verdict_fn(sha, repo_root=root, timeout_s=timeout_s, interval_s=interval_s,
                      baseline=base, required_contexts=required_contexts())


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


def land(root: Path, *, slug: str, batch: str, sha: str, base: str,
         timeout_s: int = 900, interval_s: int = 20, git: Optional[Runner] = None,
         verdict_fn: Optional[Callable] = None, record_push_fn: Optional[Callable] = None,
         record_suite_fn: Optional[Callable] = None) -> LandResult:
    """Integration branch first, then the SAME sha to main. See the module docstring.

    Refuses (never lands) when: `sha` is not a merge commit whose first parent is `base`;
    `origin/main` is no longer `base` (before the integration push AND again before the push to
    main); the push to the integration branch fails; CI's verdict for `sha` is not landable. The
    first refusal wins and nothing after it runs."""
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

    code, out = git(["rev-list", "--parents", "-n", "1", sha])
    parts = out.split()
    if code != 0 or len(parts) != 3 or not _same(parts[1], base):
        return refuse("NOT-A-MERGE-ON-BASE",
                      f"{sha} is not a two-parent merge commit whose first parent is the "
                      f"integration base {base} (git said: {out.strip()[:160]!r})")
    sha = parts[0]

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
        record_suite_fn(root, slug=slug, sha=sha)
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


def apply_preconditions(sha: str, *, root: Path, go: str, verdict_fn: Optional[Callable] = None,
                        legs: Sequence[str] = ("pytest (ubuntu-latest)", "pytest (windows-latest)")
                        ) -> list[str]:
    """G1: BOTH pytest legs completed and successful on the named rehearsal sha, and the
    operator's recorded GO named. Returns the unmet preconditions."""
    unmet: list[str] = []
    if not go.strip():
        unmet.append("no operator GO named (--go '<the recorded GO>')")
    if verdict_fn is None:
        import ci_verdict as civ
        verdict_fn = civ.verdict_for
    verdict = verdict_fn(sha, repo_root=root, timeout_s=0, interval_s=1,
                         required_contexts=tuple(legs))
    if getattr(verdict, "state", "") != "PASS":
        unmet.append(f"{sha[:12]}: both pytest legs must be completed and `success` on the "
                     f"rehearsal sha (G1); CI says {getattr(verdict, 'state', '?')} -- "
                     f"{getattr(verdict, 'reason', '')}")
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
@click.pass_context
def cmd_verdict(ctx: click.Context, sha: str, base: str, timeout_s: int, interval_s: int) -> None:
    """Read the ONE CI verdict for a sha. Exit 0 only when it is landable."""
    with timed_event("merge_path.verdict", sha=sha[:12]) as result:
        verdict = read_verdict(sha, base=base, root=ctx.obj["root"], timeout_s=timeout_s,
                               interval_s=interval_s)
        landable = is_landable(verdict)
        result["outcome"] = "ok" if landable else "fail"
    click.echo(json.dumps(verdict.to_dict(), indent=2))
    raise SystemExit(0 if landable else 1)


@cli.command("land")
@click.option("--slug", required=True, help="the open merge receipt")
@click.option("--batch", required=True)
@click.option("--sha", required=True, help="the merge commit")
@click.option("--base", required=True, help="the integration base: origin/main when the merge "
                                            "was made, and the merge's first parent")
@click.option("--timeout", "timeout_s", default=900, type=int)
@click.option("--interval", "interval_s", default=20, type=int)
@click.pass_context
def cmd_land(ctx: click.Context, slug: str, batch: str, sha: str, base: str, timeout_s: int,
             interval_s: int) -> None:
    """Integration branch first, CI there, then the same sha to main."""
    started = time.monotonic()
    result = land(ctx.obj["root"], slug=slug, batch=batch, sha=sha, base=base,
                  timeout_s=timeout_s, interval_s=interval_s)
    emit_run_event("merge_path.land", "ok" if result.landed else "fail", time.monotonic() - started,
                   state=result.state, sha=result.sha[:12])
    click.echo(f"land: {'LANDED' if result.landed else 'REFUSED'} {result.state} -- {result.reason}")
    raise SystemExit(0 if result.landed else 1)


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
        emit_run_event(f"gate:{row['name']}", "ok" if row["exit_code"] == 0 else "fail",
                       row["duration_ms"] / 1000.0, lane=lane)
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


@ruleset_group.command("apply")
@click.option("--repo", required=True, help="owner/name")
@click.option("--sha", required=True, help="the rehearsal sha: both pytest legs must be green on it")
@click.option("--go", default="", help="the operator's recorded GO, named")
@click.option("--execute", is_flag=True, default=False,
              help="actually apply. Without it this is a DRY RUN and writes nothing.")
@click.pass_context
def cmd_ruleset_apply(ctx: click.Context, repo: str, sha: str, go: str, execute: bool) -> None:
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
    unmet = problems + (apply_preconditions(sha, root=root, go=go) if execute else [])
    for item in unmet:
        click.echo(f"  UNMET   : {item}")
    if not execute:
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
