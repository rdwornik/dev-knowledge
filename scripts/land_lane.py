#!/usr/bin/env python
"""land_lane.py -- the harness map's `land` transition as ONE script, for ONE lane, no model call.

WHY IT EXISTS. The lane-integrate sequence (fetch, merge, regenerate, carry the ledger, push the
integration branch, wait for CI, push main, close the receipt) was driven by a seat typing each
verb, and a seat is a model call per step. DIGEST-INTEGRATION-THROUGHPUT-2026-10-22 option (e) asks
for that sequence as code. This module is that code and nothing else: it CALLS `merge_path.land()`
for everything that pushes -- the only `git push` of the landing lives there, in the
integration-branch-first, single-sha construction -- and it writes receipts only through
`merge_receipt.open_receipt` / `close_receipt` (plus what `land()` records).

THE STEPS (STEPS, in order; a step that did not run is not reported)
  fetch             `git fetch origin`; BASE = `origin/main`; a dirty worktree is refused, else it is detached at BASE
                    (it is the integration worktree: local edits in it are discarded).
  merge             `git merge --no-ff` of the lane ref. A conflict collects the files, aborts the
                    merge and leaves the worktree clean at BASE.
  regenerate        the injected `regenerate_fn` (none by default) names files to fold in.
  carry             the carry file's receipt lines join `logs/MERGE-RECEIPTS.jsonl`. Regeneration and
                    carry are folded into the merge commit with `commit --amend --no-edit`: `land()`
                    demands a TWO-parent merge whose first parent is BASE, so no second commit.
  push-integration  `land()`: the merge commit to `worktree-integrate-<batch>`.
  poll              `land()`: CI's verdict for that sha (a poll, in this process).
  land              `land()`: the SAME sha to main. Then `origin/main` is re-read.
  receipt           close the receipt; its ledger line goes to the carry file, and the ledger is
                    restored (`git checkout --`) so main's ledger only ever grows by a later merge.
  teardown          `teardown_fn` (default: fetch, then reset the worktree to `origin/main`).
The three `land()` steps are one call: their seconds come from the receipt's `push-integration` and
`push-main` timings and from wall time around the call (poll = wall minus both pushes, floored at 0).

EXIT CODES  0 landed | 2 conflict | 3 CI red | 4 BASE-MOVED | 5 refused | 64 usage.

HONEST LIMITS
  * The re-read of `origin/main` after `land()` DETECTS an unjudged sha on main; it cannot prevent
    one. Prevention is `land()`'s construction: one sha, pushed to the integration branch, judged,
    then pushed to main.
  * The local `ci wait` is a poll inside this process: it holds the worktree for up to
    `--timeout` seconds and is lost with the process.
  * A real landing against a non-local origin needs `--i-am-the-integrator`; that is a statement,
    not a check of who the caller is.
  * No process changes until the ADR is ratified; this script is the shape of the transition, not
    its authorisation.
"""
from __future__ import annotations

import shlex
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional, Sequence

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

import merge_path  # noqa: E402
from merge_path import Runner  # noqa: E402

STEPS = ("fetch", "merge", "regenerate", "carry", "push-integration", "poll", "land", "receipt",
         "teardown")

EXIT_OK = 0
EXIT_CONFLICT = 2
EXIT_RED = 3
EXIT_BASE_MOVED = 4
EXIT_REFUSED = 5
EXIT_USAGE = 64

DEFAULT_TIMEOUT_S = 1800
DEFAULT_INTERVAL_S = 20
#: What lane-integrate §2 regenerates after a merge (`merge=ours` pins the audits index, so it is
#: stale by construction). A command whose script is absent from the worktree is skipped.
DEFAULT_REGEN_CMDS = (("uv", "run", "--locked", "python", "scripts/gen_audit_index.py", "--write"),)


def default_regen_cmds(worktree: Path) -> list:
    return [list(c) for c in DEFAULT_REGEN_CMDS if (Path(worktree) / c[-2]).is_file()]

LEDGER_RELPATH = "logs/MERGE-RECEIPTS.jsonl"


@dataclass
class LandReport:
    state: str
    exit_code: int
    message: str
    sha: str = ""
    steps: list = field(default_factory=list)
    conflicts: tuple = ()
    failing: tuple = ()

    @property
    def ok(self) -> bool:
        return self.exit_code == EXIT_OK


def plan(slug: str, batch: str, timeout_s: int = DEFAULT_TIMEOUT_S,
         lane_ref: Optional[str] = None) -> list[str]:
    """One line per STEP, naming what it would run. Pure: touches nothing."""
    lane_ref = lane_ref or f"origin/worktree-{slug}"
    branch = merge_path.integration_branch(batch)
    text = {
        "fetch": "git fetch origin; BASE = origin/main; worktree detached at BASE",
        "merge": f"git merge --no-ff {lane_ref} (conflict: list files, merge --abort, stop)",
        "regenerate": "run the regenerate hook; stage what it changed into the merge commit",
        "carry": "append the carry file's receipt lines to the ledger; git commit --amend --no-edit",
        "push-integration": f"merge_path.land: git push origin <sha>:refs/heads/{branch}",
        "poll": f"merge_path.land: wait for CI on {branch}, up to {timeout_s / 60:g} min",
        "land": "merge_path.land: git push origin <same sha>:refs/heads/main; re-read origin/main",
        "receipt": f"close the receipt for {slug}; ledger line -> carry file; restore the ledger",
        "teardown": "git fetch origin; git reset --hard origin/main in the integration worktree",
    }
    return [f"{step}: {text[step]}" for step in STEPS]


def _default_teardown(worktree: Path) -> None:
    git = merge_path._run_git(worktree)
    for args in (["fetch", "origin"], ["reset", "--hard", "origin/main"]):
        code, out = git(args)
        if code != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {out.strip()[:200]}")


def _changed_paths(git: Runner) -> list[str]:
    """Paths the working tree changed, from `status --porcelain -z` (no quoting, renames explicit)."""
    code, out = git(["status", "--porcelain", "-z"])
    if code != 0:
        return []
    tokens, paths, i = out.split("\0"), [], 0
    while i < len(tokens):
        entry = tokens[i]
        i += 1
        if len(entry) < 4:
            continue
        paths.append(entry[3:])
        if entry[0] in "RC":                        # a rename/copy carries its origin as the next token
            i += 1
    return paths


def _read_lines(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    return [ln for ln in text.splitlines() if ln.strip()]


def _append_lines(path: Path, lines: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    prefix = "" if not existing or existing.endswith("\n") else "\n"
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(prefix + "".join(f"{ln}\n" for ln in lines))


def _push_seconds(worktree: Path, slug: str) -> "tuple[float, float]":
    import merge_receipt as mr
    try:
        steps = mr.load_receipt(worktree, slug).steps
    except mr.MergeReceiptError:
        return 0.0, 0.0
    found = {s.step: s.seconds for s in steps}
    return found.get(mr.STEP_PUSH_INTEGRATION, 0.0), found.get(mr.STEP_PUSH_MAIN, 0.0)


def land_lane(worktree: Path, *, slug: str, batch: str, carry_file: Path,
              timeout_s: int = DEFAULT_TIMEOUT_S, interval_s: int = DEFAULT_INTERVAL_S,
              lane_ref: Optional[str] = None, git: Optional[Runner] = None,
              land_fn: Optional[Callable] = None, verdict_fn: Optional[Callable] = None,
              record_suite_fn: Optional[Callable] = None,
              regenerate_fn: Optional[Callable[[Path], Sequence[str]]] = None,
              regen_cmds: Sequence[Sequence[str]] = (), handback: Optional[Path] = None,
              teardown_fn: Optional[Callable[[Path], None]] = None,
              sleep: Callable[[float], None] = time.sleep) -> LandReport:
    """Run the lane-integrate sequence for one lane. Never raises for an expected stop: every
    outcome is a LandReport. `sleep` is accepted for the injection contract; the poll itself runs
    inside `land()`'s verdict read."""
    import merge_receipt as mr
    worktree = Path(worktree)
    git = git or merge_path._run_git(worktree)
    land_fn = land_fn or merge_path.land
    teardown_fn = teardown_fn or _default_teardown
    lane_ref = lane_ref or f"origin/worktree-{slug}"
    carry_file = Path(carry_file)
    ledger = mr.ledger_path(worktree)
    steps: list = []

    def report(state: str, code: int, message: str, **kw) -> LandReport:
        return LandReport(state, code, message, steps=steps, **kw)

    def timed(name: str, started: float) -> None:
        steps.append((name, time.monotonic() - started))

    # fetch
    started = time.monotonic()
    code, out = git(["fetch", "origin"])
    if code != 0:
        return report("REFUSED", EXIT_REFUSED, f"git fetch origin failed: {out.strip()[:200]}")
    code, out = git(["rev-parse", "origin/main"])
    base = out.strip()
    if code != 0 or len(base) != 40:
        return report("REFUSED", EXIT_REFUSED, f"cannot resolve origin/main: {out.strip()[:200]}")
    code, out = git(["status", "--porcelain"])
    if code != 0 or out.strip():
        return report("REFUSED", EXIT_REFUSED, "the integration worktree is not clean; this script "
                                               f"discards nothing: {out.strip()[:200]}")
    code, out = git(["checkout", "--detach", base])
    if code != 0:
        return report("REFUSED", EXIT_REFUSED, f"cannot move the worktree to {base[:12]}: "
                                               f"{out.strip()[:200]}")
    timed("fetch", started)

    # merge
    started = time.monotonic()
    code, out = git(["merge", "--no-ff", "-m", f"land {slug} ({batch})", lane_ref])
    if code != 0:
        _, names = git(["diff", "--name-only", "--diff-filter=U"])
        conflicts = tuple(n.strip() for n in names.splitlines() if n.strip())
        abort_code, abort_out = git(["merge", "--abort"])
        timed("merge", started)
        if abort_code != 0:
            return report("REFUSED", EXIT_REFUSED,
                          f"git merge {lane_ref} stopped ({', '.join(conflicts) or 'no conflicts named'}) "
                          f"and `git merge --abort` FAILED: {abort_out.strip()[:200]}. The worktree is "
                          f"NOT clean; resolve it by hand. Nothing was pushed.", conflicts=conflicts)
        if not conflicts:
            return report("REFUSED", EXIT_REFUSED,
                          f"git merge {lane_ref} failed without conflicts: {out.strip()[:200]}")
        return report("CONFLICT", EXIT_CONFLICT,
                      f"CONFLICT merging {lane_ref} onto {base[:12]}: {', '.join(conflicts)}. "
                      f"The merge was aborted; the worktree is clean at BASE and nothing was pushed.",
                      conflicts=conflicts)
    code, out = git(["rev-list", "--parents", "-n", "1", "HEAD"])
    if code != 0 or len(out.split()) != 3:
        timed("merge", started)
        return report("REFUSED", EXIT_REFUSED,
                      f"{lane_ref} produced no merge commit (already contained in {base[:12]}?)")
    timed("merge", started)

    # regenerate
    started = time.monotonic()
    regenerated = list(regenerate_fn(worktree)) if regenerate_fn else []
    for cmd in regen_cmds:
        # A regeneration command runs BEFORE CI judges the merge, with the integrator's
        # credentials: refuse one whose own path argument the lane changed (the lane could
        # otherwise ship the code that runs here).
        _, changed = git(["diff", "--name-only", base, "HEAD"])
        touched = {n.strip() for n in changed.splitlines()}
        tampered = [a.replace("\\", "/") for a in cmd if a.replace("\\", "/") in touched]
        if tampered:
            timed("regenerate", started)
            return report("REFUSED", EXIT_REFUSED,
                          f"regenerate command {' '.join(cmd)!r} names {tampered}, which this lane "
                          f"changed: not run before CI has judged it. The merge commit is local "
                          f"only; nothing was pushed.")
        proc = subprocess.run(list(cmd), cwd=str(worktree), capture_output=True, text=True,
                              encoding="utf-8", errors="replace", check=False)
        if proc.returncode != 0:
            timed("regenerate", started)
            return report("REFUSED", EXIT_REFUSED,
                          f"regenerate command {' '.join(cmd)!r} exited {proc.returncode}: "
                          f"{(proc.stderr or proc.stdout).strip()[:200]}. The merge commit is "
                          f"local only; nothing was pushed.")
    if regen_cmds:
        regenerated += _changed_paths(git)
    timed("regenerate", started)

    # carry
    started = time.monotonic()
    committed = _read_lines(ledger)
    carried = [ln for ln in _read_lines(carry_file) if ln not in committed]
    if carried:
        _append_lines(ledger, carried)
    to_stage = [*regenerated, *([LEDGER_RELPATH] if carried else [])]
    if to_stage:
        for args in (["add", "--", *to_stage], ["commit", "--amend", "--no-edit"]):
            code, out = git(args)
            if code != 0:
                timed("carry", started)
                return report("REFUSED", EXIT_REFUSED,
                              f"folding changes into the merge commit failed "
                              f"(git {args[0]}): {out.strip()[:200]}")
    timed("carry", started)
    code, out = git(["rev-parse", "HEAD"])
    sha = out.strip()
    ledger_before = len(_read_lines(ledger))

    # push-integration, poll, land: one call to merge_path.land
    try:
        mr.open_receipt(worktree, slug=slug, batch=batch)
    except mr.MergeReceiptError as exc:
        return report("REFUSED", EXIT_REFUSED, f"cannot open the receipt: {exc}", sha=sha)
    kwargs = dict(slug=slug, batch=batch, sha=sha, base=base, timeout_s=timeout_s,
                  interval_s=interval_s, git=git)
    if verdict_fn is not None:
        kwargs["verdict_fn"] = verdict_fn
    if record_suite_fn is not None:
        kwargs["record_suite_fn"] = record_suite_fn
    if handback is not None:
        kwargs["handback"] = handback
    started = time.monotonic()
    try:
        result = land_fn(worktree, **kwargs)
    except Exception as exc:                        # noqa: BLE001 -- e.g. a receipt write after the push
        steps.append(("land", time.monotonic() - started))
        return report("REFUSED", EXIT_REFUSED,
                      f"land() raised {type(exc).__name__}: {exc}. origin/main may already hold "
                      f"{sha[:12]}: re-read it before retrying. The receipt for {slug} is left "
                      f"open.", sha=sha)
    wall = time.monotonic() - started
    pushed = bool(result.commands)
    branch = result.branch or merge_path.integration_branch(batch)
    if pushed:
        push_s, main_s = _push_seconds(worktree, slug)
        steps.append(("push-integration", push_s))
        steps.append(("poll", max(0.0, wall - push_s - main_s)))
        if result.landed:
            steps.append(("land", main_s))
    else:
        mr.scratch_path(worktree, slug).unlink(missing_ok=True)   # nothing pushed: no half-done record

    if not result.landed:
        return _refusal(report, result, sha, branch, pushed)

    # land, verified: main must hold exactly the judged sha
    code, out = git(["ls-remote", "origin", "refs/heads/main"])
    fields = out.split()
    remote = fields[0] if code == 0 and fields else ""
    if not merge_path._same(remote, sha):
        return report("REFUSED", EXIT_REFUSED,
                      f"unjudged sha on main: origin/main is {remote or out.strip()[:80]!r}, CI "
                      f"judged {sha}. main was changed by a push other than the judged one; the "
                      f"receipt for {slug} is left open as the record.", sha=sha)

    # receipt
    started = time.monotonic()
    new_lines: list = []
    try:
        mr.close_receipt(worktree, slug)
        new_lines = _read_lines(ledger)[ledger_before:]
        carry_file.parent.mkdir(parents=True, exist_ok=True)
        carry_file.write_text("".join(f"{ln}\n" for ln in new_lines), encoding="utf-8",
                              newline="\n")
        tracked, _ = git(["ls-files", "--error-unmatch", LEDGER_RELPATH])
        if tracked == 0:
            code, out = git(["checkout", "--", LEDGER_RELPATH])
        else:                                       # the ledger is new in this tree: nothing to restore
            ledger.unlink(missing_ok=True)
            code, out = 0, ""
    except (OSError, mr.MergeReceiptError) as exc:
        timed("receipt", started)
        return report("REFUSED", EXIT_REFUSED,
                      f"LANDED {sha[:12]} on main, but the receipt step failed: {exc}. main is "
                      f"correct. Save this ledger line for the next landing (carry file "
                      f"{carry_file}) and clean the worktree by hand: "
                      f"{' | '.join(new_lines) or 'not read'}", sha=sha)
    timed("receipt", started)
    if code != 0:
        return report("REFUSED", EXIT_REFUSED,
                      f"landed {sha[:12]} but the ledger could not be restored: {out.strip()[:200]}",
                      sha=sha)

    # teardown
    started = time.monotonic()
    try:
        teardown_fn(worktree)
    except Exception as exc:                        # noqa: BLE001 -- reported, the landing stands
        timed("teardown", started)
        return report("LANDED", EXIT_OK, f"LANDED {sha[:12]} on main via {branch}; teardown "
                                         f"failed: {exc}", sha=sha)
    timed("teardown", started)
    return report("LANDED", EXIT_OK,
                  f"LANDED {sha[:12]} on main after CI on {branch}. Receipt line carried to "
                  f"{carry_file}.", sha=sha)


def _refusal(report: Callable, result, sha: str, branch: str, pushed: bool) -> LandReport:
    verdict = result.verdict
    where = "after the integration push" if pushed else "before any push"
    if result.state == "BASE-MOVED":
        if pushed:
            msg = (f"BASE-MOVED after the push: {branch} already holds {sha[:12]} but "
                   f"origin/main moved. {result.reason} Receipt left open.")
        else:
            msg = f"BASE-MOVED before any push: {result.reason}"
        return report("BASE-MOVED", EXIT_BASE_MOVED, msg, sha=sha)
    if (verdict is not None and not merge_path.is_landable(verdict)
            and result.state not in ("RECEIPT-REFUSED", "MAIN-PUSH-REFUSED")):
        failing = tuple(str(n) for n in (*getattr(verdict, "newly_failing", ()),
                                         *getattr(verdict, "non_pass", ()),
                                         *getattr(verdict, "new_tests", ())))
        listed = ", ".join(failing) or "none named"
        return report("RED", EXIT_RED,
                      f"RED {result.state}: {result.reason}. Failing: {listed}. {branch} holds "
                      f"{sha[:12]}; main was not touched. The scratch receipt stays in place: it is "
                      f"the record of this half-done landing. Retrying needs a human or model: "
                      f"{branch} holds this unlanded sha, so a new merge is rejected as a "
                      f"non-fast-forward until that branch is deleted deliberately.",
                      sha=sha, failing=failing)
    tail = " Receipt left open." if pushed else ""
    return report("REFUSED", EXIT_REFUSED,
                  f"REFUSED {result.state} ({where}): {result.reason}{tail}", sha=sha)


def _origin_is_remote(url: str) -> bool:
    """Fail CLOSED: an origin is a throwaway only when it is an existing local directory; a
    `file://`, scp-style or unknown URL counts as remote and needs the flag."""
    return not Path(url.strip()).is_dir()


@click.command("land-lane")
@click.option("--worktree", "worktree", default=".", type=click.Path(path_type=Path),
              help="the integration worktree (default: the current directory)")
@click.option("--slug", required=True, help="the lane slug; its branch is origin/worktree-<slug>")
@click.option("--batch", required=True, help="the batch; the integration branch follows from it")
@click.option("--lane-ref", "lane_ref", default=None, help="the ref to merge (default above)")
@click.option("--carry-file", "carry_file", default=None, type=click.Path(path_type=Path),
              help="receipt lines waiting for the next landing (default: next to the worktree)")
@click.option("--timeout", "timeout_s", default=DEFAULT_TIMEOUT_S, type=int,
              help="seconds to wait for CI on the integration branch")
@click.option("--interval", "interval_s", default=DEFAULT_INTERVAL_S, type=int)
@click.option("--regen-cmd", "regen_cmds", multiple=True,
              help="a command (shlex-split) that regenerates files; repeatable "
                   "(default: the audits index)")
@click.option("--handback", "handback", default=None, type=click.Path(path_type=Path),
              help="the lane's handback file, read by the substitution gate for batches from E2.0")
@click.option("--dry-run", "dry_run", is_flag=True, default=False,
              help="print the plan and touch nothing")
@click.option("--i-am-the-integrator", "integrator", is_flag=True, default=False,
              help="required to land against a non-local origin")
def cli(worktree: Path, slug: str, batch: str, lane_ref: Optional[str], carry_file: Optional[Path],
        timeout_s: int, interval_s: int, regen_cmds: tuple, handback: Optional[Path],
        dry_run: bool, integrator: bool) -> None:
    """Land ONE lane: merge, carry, integration push, CI, main push, receipt. No model call."""
    try:
        merge_path.integration_branch(batch)
    except click.ClickException as exc:
        click.echo(f"land_lane: {exc.message}", err=True)
        sys.exit(EXIT_USAGE)
    if dry_run:
        for line in plan(slug, batch, timeout_s, lane_ref):
            click.echo(line)
        sys.exit(EXIT_OK)
    worktree = worktree.resolve()
    if not worktree.is_dir():
        click.echo(f"land_lane: {worktree} is not a directory", err=True)
        sys.exit(EXIT_USAGE)
    code, url = merge_path._run_git(worktree)(["remote", "get-url", "origin"])
    if code != 0:
        click.echo(f"land_lane: no origin in {worktree}: {url.strip()[:200]}", err=True)
        sys.exit(EXIT_USAGE)
    if _origin_is_remote(url) and not integrator:
        click.echo("landing against a remote origin requires --i-am-the-integrator", err=True)
        sys.exit(EXIT_REFUSED)
    carry = carry_file or worktree.parent / f"{worktree.name}-land-carry.jsonl"
    report = land_lane(worktree, slug=slug, batch=batch, carry_file=carry, timeout_s=timeout_s,
                       interval_s=interval_s, lane_ref=lane_ref, handback=handback,
                       regen_cmds=[shlex.split(c) for c in regen_cmds] or default_regen_cmds(worktree))
    click.echo(report.message)
    for name, seconds in report.steps:
        click.echo(f"{name}: {seconds:.1f}")
    sys.exit(report.exit_code)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
