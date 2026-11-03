#!/usr/bin/env python
"""land_on_handback.py -- a lane's HANDBACK lands it on main by code; a model only on a stop. [#1859]

WHY IT EXISTS. `land_lane.py` is the whole landing as one script, but a seat still typed the verb
when a lane handed back. This module is the trigger: `land_one` takes ONE handback, refuses before
any `land_lane` call unless the handback is well-formed, current and this batch's, then runs
`land_lane.land_lane` IN PROCESS under one machine-wide lock. A conflict, a red CI and BASE-MOVED
are land_lane's own stops (ADR-131 D6): the lander writes `LAND-STOP-<SLUG>.json`, prints ONE
`QUESTION land-on-handback ...` line and does not retry. It changes NO landing gate: BASE-MOVED
twice, the integration-branch-first single-sha push, CI's verdict, the substitution gate and lane
G's stage-receipt refusal all live inside `land_lane` and the landing function it calls, and are only
CALLED here.

THE VERBS
  once   --lane SLUG   land one lane now (the call-site contract of the W-track arming lane).
  watch                the same landing driven by the wake files E2's handback and the Stop hook
                       write; this lane ARMS NOTHING -- no flow runs `watch` by hand.
  clock  [--last N]    median and p90 of handback -> main over the merge clock.

THE MERGE CLOCK (C13). Every landing that reaches `land_lane` appends one `merge-clock/1` line to
`logs/MERGE-CLOCK.jsonl` of the primary checkout (machine-written runtime state, gitignored by
name). `LandReport.steps` holds DURATIONS, not timestamps, so `main_at` is an ESTIMATE of the main
push: the lander's clock when `land_lane` returned, minus the `receipt` and `teardown` seconds.
The `land` stage is land_lane's own proxy (one `ls-remote` round trip), so every line carries
`land_is_proxy: true`. A value the run did not measure is null AND named in `unmeasured`, never 0.
"""
from __future__ import annotations

import dataclasses
import inspect
import json
import math
import os
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import click
from filelock import FileLock, Timeout

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

import handback_schema  # noqa: E402
import land_lane  # noqa: E402
import subst_gate  # noqa: E402


def _guard():
    """`lane_end_guard`, imported on first use and not at module level: it stamps `_T0` at import
    and tests/test_lane_end_guard.py asserts its 15 s hook limit against that stamp, so an import
    at collection time (same xdist worker) would fail that test."""
    import lane_end_guard  # noqa: PLC0415
    return lane_end_guard


#: the function actually called; `land_one(land_lane_fn=)` is a test seam of the Python function only
DEFAULT_LAND_FN = land_lane.land_lane
LOCK_NAME = "land-on-handback.lock"
CLOCK_SCHEMA = "merge-clock/1"
DEFAULT_LOCK_WAIT_VERB_S = 900
_STATE_APP_NAME = "dev-knowledge"       # the per-user state directory lane_end_guard uses
_SLUG_CHARS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-")

#: land_lane's own steps, in order: fetch .. land (the landing proper), then receipt, teardown (after main)
MAIN_STEPS = tuple(land_lane.STEPS[:7])
AFTER_MAIN = tuple(land_lane.STEPS[7:])
STAGE_ORDER = ("wait", *MAIN_STEPS, "unattributed")
_PROXY_STAGE = MAIN_STEPS[-1]

EXIT_OK = land_lane.EXIT_OK
EXIT_REFUSED = land_lane.EXIT_REFUSED

_REQUIRE_GATE = "require_phase_receipts"
_CONDUCTOR = "conductor"


@dataclass
class LandOutcome:
    state: str
    exit_code: int
    message: str
    report: Optional[land_lane.LandReport] = None
    recorded: bool = False          # True: the wake may be recorded in the cursor; False: a stop
    lines: list = field(default_factory=list)   # dry-run only


class LanderStop(Exception):
    """Raised by `watch`'s callback after a stop, so `watch_wakes` appends nothing to the cursor."""

    def __init__(self, exit_code: int, message: str = "") -> None:
        super().__init__(message or f"land-on-handback stopped (exit {exit_code})")
        self.exit_code = exit_code


# --- small helpers -----------------------------------------------------------------------------

def _slug_ok(slug: str) -> bool:
    return bool(slug) and all(ch in _SLUG_CHARS for ch in slug)


def _default_state_dir() -> Path:
    import platformdirs  # noqa: PLC0415 -- only a landing needs the private state directory
    return Path(platformdirs.user_state_dir(_STATE_APP_NAME, appauthor=False))


def _iso(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _parse_iso(text: Optional[str]) -> Optional[float]:
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(str(text).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def _git_runner(root: Path) -> Callable:
    """`git -C <root> ...` -> (returncode, stdout + stderr); an absent git is code 127, never a raise."""
    def run(args) -> "tuple[int, str]":
        try:
            proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=300, check=False)
        except (OSError, subprocess.SubprocessError) as exc:
            return 127, f"git could not be run: {exc!r}"
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    return run


def _same_sha(left: str, right: str) -> bool:
    """EXACT equality of two commit ids: a prefix is not a match."""
    left, right = left.strip().lower(), right.strip().lower()
    return bool(left) and left == right


def _primary(worktree: Path) -> Path:
    """The primary checkout: the parent of `git rev-parse --git-common-dir` run in the worktree."""
    code, out = _git_runner(worktree)(["rev-parse", "--path-format=absolute", "--git-common-dir"])
    first = out.strip().splitlines()[0] if code == 0 and out.strip() else ""
    return Path(first).parent if first else worktree


def _resolve_receipts(explicit: Optional[Path], worktree: Path) -> "tuple[Optional[Path], str]":
    """ONE receipts directory: `--receipts`, else an already-set HARNESS_RECEIPTS_DIR, else the
    primary checkout's logs/receipts. An explicit value that differs from a set env is a conflict."""
    env = os.environ.get("HARNESS_RECEIPTS_DIR") or ""
    if explicit is not None:
        if env and Path(env).resolve() != Path(explicit).resolve():
            return None, (f"--receipts {explicit} differs from HARNESS_RECEIPTS_DIR={env}: the "
                          f"preflight and the landing gate would judge different receipts")
        return Path(explicit), ""
    if env:
        return Path(env), ""
    return _primary(worktree) / "logs" / "receipts", ""


def _stop_path(receipts: Path, slug: str) -> Path:
    return receipts / f"LAND-STOP-{slug.upper()}.json"


def _launch_body(receipts: Path, slug: str) -> Optional[dict]:
    try:
        body = json.loads((receipts / f"LAUNCH-{slug.upper()}.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return body if isinstance(body, dict) else None


def _has_named_param(fn: Callable, name: str) -> bool:
    """A NAMED parameter only: a `**kwargs` catch-all does not count (fail closed)."""
    try:
        param = inspect.signature(fn).parameters.get(name)
    except (TypeError, ValueError):
        return False
    return param is not None and param.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                                inspect.Parameter.KEYWORD_ONLY)


def _question(outcome: LandOutcome, slug: str, evidence: str) -> None:
    text = " ".join(outcome.message.split())[:200]
    print(f"QUESTION land-on-handback {slug} {datetime.now().strftime('%H:%M')}: {outcome.state} "
          f"exit {outcome.exit_code} - {text} | evidence: {evidence}", flush=True)


def _refuse(state: str, message: str, *, recorded: bool = False, code: int = EXIT_REFUSED) -> LandOutcome:
    return LandOutcome(state, code, message, recorded=recorded)


def _write_json(path: Path, body: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8", newline="\n")


def _write_stop(path: Path, body: dict) -> str:
    """Write LAND-STOP; a write that fails still ends in the one QUESTION line, never a traceback."""
    try:
        _write_json(path, body)
    except OSError as exc:
        return f"none (LAND-STOP write failed at {path}: {exc})"
    return str(path)


# --- the preflight checks ------------------------------------------------------------------------

@dataclass
class _Ctx:
    slug: str
    closing: str
    batch: str
    worktree: Path
    transport: Path
    receipts: Path
    integrator: bool
    dry_run: bool
    git: Callable
    parsed: Optional[handback_schema.HandbackLine] = None
    engine: str = "model"

    @property
    def session(self) -> Path:
        return self.transport / "to-browser" / f"SESSION-{self.slug}.md"


def _check_context(ctx: _Ctx) -> Optional[LandOutcome]:
    """(ii) a lane never lands: not from a lane's env, branch or own worktree."""
    if os.environ.get("HARNESS_LANE"):
        return _refuse("LANE-CONTEXT", "env HARNESS_LANE is set: a lane never lands")
    code, out = _git_runner(Path.cwd())(["rev-parse", "--abbrev-ref", "HEAD"])
    branch = out.strip().splitlines()[0] if code == 0 and out.strip() else ""
    if branch.startswith("worktree-") and not branch.startswith("worktree-integrate-"):
        return _refuse("LANE-CONTEXT", f"the current directory is on lane branch {branch}: a lane "
                                       f"never lands")
    wt = ctx.worktree
    if wt.name == ctx.slug and wt.parent.name == "worktrees" and wt.parent.parent.name == ".claude":
        return _refuse("LANE-CONTEXT", f"--worktree {wt} is the lane's own worktree")
    return None


def _check_integrator(ctx: _Ctx) -> Optional[LandOutcome]:
    """(iii) against a non-local origin the integrator statement is required (never defaulted here)."""
    code, url = ctx.git(["remote", "get-url", "origin"])
    if code != 0:
        return _refuse("NO-ORIGIN", f"no origin in {ctx.worktree}: {url.strip()[:200]}")
    if land_lane._origin_is_remote(url) and not ctx.integrator:
        return _refuse("NEEDS-INTEGRATOR-STATEMENT",
                       "landing against a remote origin requires --i-am-the-integrator")
    return None


def _check_handback(ctx: _Ctx) -> Optional[LandOutcome]:
    """(iv) the handback is well-formed and current."""
    if not _slug_ok(ctx.slug):
        return _refuse("HANDBACK-SLUG", f"{ctx.slug!r} is not a lane slug (letters, digits, . _ -)")
    parsed = handback_schema.HandbackLine.parse(ctx.closing)
    if parsed is None:
        return _refuse("HANDBACK-UNPARSED", f"the closing line does not parse: {ctx.closing[:120]!r}")
    ctx.parsed = parsed
    if parsed.branch != f"worktree-{ctx.slug}":
        return _refuse("HANDBACK-BRANCH", f"the line's branch is {parsed.branch}, not worktree-{ctx.slug}")
    try:
        text = ctx.session.read_text(encoding="utf-8")
    except OSError as exc:
        return _refuse("HANDBACK-FILE", f"cannot read {ctx.session}: {exc}")
    if ctx.closing not in [ln.rstrip("\r") for ln in text.splitlines()]:
        return _refuse("HANDBACK-FILE", f"{ctx.session} has no flush-left line {ctx.closing[:80]!r}")
    if ctx.dry_run:
        code, out = ctx.git(["ls-remote", "origin", f"refs/heads/worktree-{ctx.slug}"])
        fields = out.split() if code == 0 else []
        tip = fields[0] if fields else ""
    else:
        code, out = ctx.git(["fetch", "origin"])
        if code != 0:
            return _refuse("FETCH-FAILED", f"git fetch origin failed: {out.strip()[:200]}")
        code, out = ctx.git(["rev-parse", "--verify", "-q", f"origin/worktree-{ctx.slug}"])
        tip = out.strip() if code == 0 else ""
    if not _same_sha(tip, parsed.sha):
        return _refuse("STALE-HANDBACK", f"origin/worktree-{ctx.slug} is {tip[:12] or 'absent'}, the "
                                         f"handback says {parsed.sha[:12]}: the lane pushed after "
                                         f"handing back")
    return None


def _check_batch(ctx: _Ctx) -> Optional[LandOutcome]:
    """(v) batch membership: the gate's own predicate first; another batch's wake is skipped."""
    problems = subst_gate.launch_receipt_problems(ctx.worktree, ctx.slug, ctx.batch, ctx.receipts)
    if not problems:
        return None
    body = _launch_body(ctx.receipts, ctx.slug)
    if body is not None and body.get("organ") == "launch" and body.get("batch") != ctx.batch:
        return LandOutcome("NOT-THIS-BATCH", EXIT_OK,
                           f"lane {ctx.slug} belongs to batch {body.get('batch')!r}, not {ctx.batch}",
                           recorded=True)
    return _refuse("NO-LAUNCH-RECEIPT", " | ".join(problems))


def _check_already_landed(ctx: _Ctx) -> Optional[LandOutcome]:
    """(vi) a sha already an ancestor of origin/main is landed, unless a stop receipt is unresolved."""
    sha = ctx.parsed.sha if ctx.parsed else ""
    code, _ = ctx.git(["merge-base", "--is-ancestor", sha, "origin/main"])
    if code != 0:
        return None
    stop = _stop_path(ctx.receipts, ctx.slug)
    if stop.exists():
        return _refuse("UNRESOLVED-STOP",
                       f"{sha[:12]} is on origin/main but {stop} exists: land_lane may have stopped "
                       f"after the main push. Verify the carry file, then delete that receipt")
    return LandOutcome("ALREADY-LANDED", EXIT_OK, f"{sha[:12]} is already on origin/main", recorded=True)


def _check_engine(ctx: _Ctx, fn: Callable) -> Optional[LandOutcome]:
    """(vii) a conductor lane is never landed without lane G's stage-receipt gate."""
    body = _launch_body(ctx.receipts, ctx.slug)
    ctx.engine = _CONDUCTOR if body is not None and body.get("engine") == _CONDUCTOR else "model"
    if ctx.engine == _CONDUCTOR and not _has_named_param(fn, _REQUIRE_GATE):
        return _refuse("ENGINE-GATE-MISSING",
                       f"conductor lane {ctx.slug}: land_lane lacks require_phase_receipts (lane G not "
                       f"landed); missing round directory: {ctx.receipts / ('LANE-' + ctx.slug)}/")
    return None


# --- the merge clock --------------------------------------------------------------------------------

def _clock_line(slug: str, batch: str, lane_sha: str, report, handback: Optional[float],
                pickup: float, end: float) -> dict:
    steps = {name: seconds for name, seconds in report.steps}
    carry_refused = report.state == "REFUSED" and report.message.startswith("LANDED ")
    main_pushed = report.state == "LANDED" or carry_refused
    unmeasured: list = []
    stages: dict = {}
    if handback is None:
        stages["wait"] = None
        unmeasured += ["stages.wait", "handback_to_main_s"]
    else:
        stages["wait"] = round(max(0.0, pickup - handback), 3)
    for name in MAIN_STEPS:
        if name in steps:
            stages[name] = round(steps[name], 3)
        else:
            stages[name] = None
            unmeasured.append(f"stages.{name}")
    main_at = after_main = h2m = unattributed = main_sha = None
    if main_pushed:
        after_main = {name: (round(steps[name], 3) if name in steps else None) for name in AFTER_MAIN}
        unmeasured += [f"after_main.{n}" for n, v in after_main.items() if v is None]
        main_at = end - sum(steps.get(name, 0.0) for name in AFTER_MAIN)
        main_sha = report.main_sha or None
        if main_sha is None:
            unmeasured.append("main_sha")
        if handback is not None:
            h2m = round(main_at - handback, 3)
        landing = sum(v for name, v in stages.items() if name in MAIN_STEPS and v is not None)
        unattributed = round(max(0.0, (main_at - pickup) - landing), 3)
    else:
        unmeasured += ["main_at", "main_sha", "after_main", "stages.unattributed"]
        if handback is not None:
            unmeasured.append("handback_to_main_s")
    stages["unattributed"] = unattributed
    return {"schema": CLOCK_SCHEMA, "slug": slug, "batch": batch, "lane_sha": lane_sha,
            "main_sha": main_sha, "state": report.state, "exit_code": report.exit_code,
            "handback_at": _iso(handback) if handback is not None else None, "pickup_at": _iso(pickup),
            "main_at": _iso(main_at) if main_at is not None else None, "handback_to_main_s": h2m,
            "stages": stages, "after_main": after_main, "unmeasured": unmeasured,
            "land_is_proxy": True}


def _append_clock(path: Optional[Path], worktree: Path, line: dict) -> None:
    """Never blocks or changes a landing: a failed write is one stderr line."""
    if path is None:
        if "PYTEST_CURRENT_TEST" in os.environ:
            return
        path = _primary(worktree) / "logs" / "MERGE-CLOCK.jsonl"
    try:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(line, sort_keys=True) + "\n")
    except OSError as exc:
        print(f"land-on-handback: merge-clock write failed ({path}): {exc}; the landing is unchanged: "
              f"{line['state']} exit {line['exit_code']}", file=sys.stderr, flush=True)


# --- the landing -----------------------------------------------------------------------------------

def land_one(slug: str, closing_line: str, *, batch: str, worktree: Path, transport: Path,
             receipts: Optional[Path] = None, carry_file: Optional[Path] = None,
             handback_at: Optional[str] = None, integrator: bool = False, lock_wait_s: float = 0,
             state_dir: Optional[Path] = None, clock_path: Optional[Path] = None,
             timeout_s: int = land_lane.DEFAULT_TIMEOUT_S, interval_s: int = land_lane.DEFAULT_INTERVAL_S,
             land_lane_fn: Callable = DEFAULT_LAND_FN, now: Callable[[], float] = time.time,
             dry_run: bool = False) -> LandOutcome:
    """Land ONE handback (or, with `dry_run`, report what each check says and touch nothing)."""
    pickup = now()
    worktree = Path(worktree).resolve()
    closing = (closing_line or "").strip()
    git = _git_runner(worktree)
    resolved, problem = _resolve_receipts(Path(receipts) if receipts is not None else None, worktree)
    if resolved is None:
        return _finish(_refuse("RECEIPTS-CONFLICT", problem), slug, None, dry_run)
    ctx = _Ctx(slug=slug, closing=closing, batch=batch, worktree=worktree, transport=Path(transport),
               receipts=resolved, integrator=integrator, dry_run=dry_run, git=git)
    if dry_run:
        return _dry_run(ctx, timeout_s, land_lane_fn)
    for check in (_check_context, _check_integrator):
        refusal = check(ctx)
        if refusal is not None:
            return _finish(refusal, slug, None, dry_run)
    state_dir = Path(state_dir) if state_dir is not None else _default_state_dir()
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        lock = FileLock(str(state_dir / LOCK_NAME), timeout=lock_wait_s)
        lock.acquire()
    except Timeout:
        return _finish(_refuse("LANDER-BUSY", f"another landing holds {state_dir / LOCK_NAME}"),
                       slug, None, dry_run)
    except OSError as exc:
        return _finish(_refuse("LOCK-FAILED", f"cannot take {state_dir / LOCK_NAME}: {exc}"),
                       slug, None, dry_run)
    try:
        return _land_locked(ctx, pickup, handback_at, carry_file, clock_path, timeout_s, interval_s,
                            land_lane_fn, now)
    finally:
        lock.release()


def _land_locked(ctx: _Ctx, pickup: float, handback_at: Optional[str], carry_file: Optional[Path],
                 clock_path: Optional[Path], timeout_s: int, interval_s: int, fn: Callable,
                 now: Callable[[], float]) -> LandOutcome:
    slug = ctx.slug
    for check in (_check_handback, _check_batch, _check_already_landed):
        skipped = check(ctx)
        if skipped is not None:
            return _finish(skipped, slug, None, False)
    gate_missing = _check_engine(ctx, fn)
    if gate_missing is not None:
        stop = _stop_path(ctx.receipts, slug)
        evidence = _write_stop(stop, _stop_body(ctx, gate_missing, None))
        return _finish(gate_missing, slug, evidence, False)
    carry = Path(carry_file) if carry_file else ctx.worktree.parent / f"{ctx.worktree.name}-land-carry.jsonl"
    kwargs = dict(slug=slug, batch=ctx.batch, carry_file=carry, timeout_s=timeout_s,
                  interval_s=interval_s, handback=ctx.session,
                  regen_cmds=land_lane.default_regen_cmds(ctx.worktree))
    gated = ctx.engine == _CONDUCTOR
    if gated:
        kwargs[_REQUIRE_GATE] = True
    prior = os.environ.get("HARNESS_RECEIPTS_DIR")
    os.environ["HARNESS_RECEIPTS_DIR"] = str(ctx.receipts)
    stop = _stop_path(ctx.receipts, slug)
    try:
        try:
            report = fn(ctx.worktree, **kwargs)
        except Exception as exc:                    # noqa: BLE001 -- a stop, never a crash of the watch
            outcome = _refuse("LAND-FN-RAISED", f"land_lane raised {type(exc).__name__}: {exc}. "
                                                f"origin/main may already hold {ctx.parsed.sha[:12]}")
            raised = land_lane.LandReport(outcome.state, outcome.exit_code, outcome.message)
            _append_clock(clock_path, ctx.worktree,
                          _clock_line(slug, ctx.batch, ctx.parsed.sha, raised,
                                      _parse_iso(handback_at), pickup, now()))
            evidence = _write_stop(stop, _stop_body(ctx, outcome, None))
            return _finish(outcome, slug, evidence, False)
    finally:
        if prior is None:
            os.environ.pop("HARNESS_RECEIPTS_DIR", None)
        else:
            os.environ["HARNESS_RECEIPTS_DIR"] = prior
    end = now()
    round_dir = ctx.receipts / f"LANE-{slug}"
    if (gated and report.exit_code == land_lane.EXIT_REFUSED and not round_dir.exists()
            and str(round_dir) not in report.message):
        report = dataclasses.replace(report, message=f"{report.message} | missing round directory: "
                                                     f"{round_dir}/")
    wake_at = _parse_iso(handback_at)
    _append_clock(clock_path, ctx.worktree,
                  _clock_line(slug, ctx.batch, ctx.parsed.sha, report, wake_at, pickup, end))
    outcome = LandOutcome(report.state, report.exit_code, report.message, report,
                          recorded=report.exit_code == EXIT_OK)
    if outcome.exit_code != EXIT_OK:
        evidence = _write_stop(stop, _stop_body(ctx, outcome, report))
        return _finish(outcome, slug, evidence, False)
    stop.unlink(missing_ok=True)                    # an earlier stop of this lane is resolved by this landing
    return _finish(outcome, slug, None, False)


def _stop_body(ctx: _Ctx, outcome: LandOutcome, report) -> dict:
    return {"slug": ctx.slug, "batch": ctx.batch, "sha": ctx.parsed.sha if ctx.parsed else "",
            "state": outcome.state, "exit_code": outcome.exit_code, "message": outcome.message,
            "conflicts": list(report.conflicts) if report else [],
            "failing": list(report.failing) if report else [],
            "main_sha": (report.main_sha if report else "") or "",
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}


def _finish(outcome: LandOutcome, slug: str, stop: Optional[Path], dry_run: bool) -> LandOutcome:
    """One line out: the QUESTION for a stop, a plain status line otherwise."""
    if dry_run:
        return outcome
    if outcome.exit_code != EXIT_OK:
        _question(outcome, slug, str(stop) if stop is not None else "none (nothing was landed)")
    else:
        print(f"land-on-handback {slug} {outcome.state}: {' '.join(outcome.message.split())[:200]}",
              flush=True)
    return outcome


def _dry_run(ctx: _Ctx, timeout_s: int, fn: Callable) -> LandOutcome:
    """The plan and each check's verdict; no lock, no fetch, no receipt, no clock line."""
    lines = list(land_lane.plan(ctx.slug, ctx.batch, timeout_s))
    first: Optional[LandOutcome] = None

    def record(label: str, result: Optional[LandOutcome]) -> None:
        nonlocal first
        if result is None:
            lines.append(f"check {label}: PASS")
            return
        lines.append(f"check {label}: {'PASS (skip)' if result.exit_code == EXIT_OK else 'FAIL'} "
                     f"{result.state} - {' '.join(result.message.split())[:160]}")
        if first is None and result.exit_code != EXIT_OK:
            first = result

    record("(ii) context", _check_context(ctx))
    record("(iii) integrator", _check_integrator(ctx))
    record("(iv) handback", _check_handback(ctx))
    if ctx.parsed is not None or _slug_ok(ctx.slug):
        record("(v) batch", _check_batch(ctx))
    lines.append("check (vi) already-landed: not evaluated in dry-run")
    record("(vii) engine-gate", _check_engine(ctx, fn))
    lines.append(f"engine: {ctx.engine}")
    for line in lines:
        print(line, flush=True)
    outcome = first or LandOutcome("DRY-RUN", EXIT_OK, "dry run: nothing was landed", recorded=True)
    outcome.lines = lines
    return outcome


# --- the verbs ----------------------------------------------------------------------------------------

def _wake_written_at(slug: str, closing: str, wake_home: Optional[Path]) -> Optional[str]:
    """The wake file's `written_at`, looked up READ-ONLY in the home and its fallback sibling."""
    if not _slug_ok(slug):
        return None
    try:
        home = Path(wake_home) if wake_home else _guard().wake_dir(os.environ)
    except (ValueError, OSError, ImportError):
        return None
    name = f"{_guard().WAKE_PREFIX}{slug}-{_guard().handback_key(closing)}.json"
    for where in (home, _guard().fallback_home(home)):
        try:
            data = json.loads((where / name).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict) and isinstance(data.get("written_at"), str):
            return data["written_at"]
    return None


def once(slug: str, *, batch: str, worktree: Path, transport: Path, receipts: Optional[Path] = None,
         carry_file: Optional[Path] = None, handback_line: Optional[str] = None,
         handback_at: Optional[str] = None, wake_home: Optional[Path] = None, integrator: bool = False,
         lock_wait_s: float = 0, state_dir: Optional[Path] = None, clock_path: Optional[Path] = None,
         timeout_s: int = land_lane.DEFAULT_TIMEOUT_S, interval_s: int = land_lane.DEFAULT_INTERVAL_S,
         land_lane_fn: Callable = DEFAULT_LAND_FN, now: Callable[[], float] = time.time,
         dry_run: bool = False) -> int:
    """Land one lane now. With no `handback_line` the lane's last flush-left HANDBACK line is read from
    its SESSION file; the `written_at` of its wake file (when one exists) is the handback time."""
    closing = handback_line
    if closing is None and _slug_ok(slug):
        try:
            text = (Path(transport) / "to-browser" / f"SESSION-{slug}.md").read_text(encoding="utf-8")
        except OSError:
            text = ""
        closing = _guard().last_handback(text)
        if closing is None:
            outcome = _refuse("HANDBACK-FILE", f"no flush-left HANDBACK line in the SESSION file of {slug}")
            _finish(outcome, slug, None, dry_run)
            return outcome.exit_code
    closing = closing or ""
    stamp = handback_at or _wake_written_at(slug, closing.strip(), wake_home)
    outcome = land_one(slug, closing, batch=batch, worktree=worktree, transport=transport,
                       receipts=receipts, carry_file=carry_file, handback_at=stamp, integrator=integrator,
                       lock_wait_s=lock_wait_s, state_dir=state_dir, clock_path=clock_path,
                       timeout_s=timeout_s, interval_s=interval_s, land_lane_fn=land_lane_fn, now=now,
                       dry_run=dry_run)
    return outcome.exit_code


def cursor_path(wake_home: Path, batch: str) -> Path:
    """This lander's OWN cursor, one per batch, beside the wake home (never the seat Monitor's)."""
    return wake_home.with_name(f"{wake_home.name}.land-seen-{batch.lower()}")


def watch(*, batch: str, worktree: Path, transport: Path, wake_home: Path,
          receipts: Optional[Path] = None, carry_file: Optional[Path] = None, integrator: bool = False,
          lock_wait_s: float = 0, state_dir: Optional[Path] = None, clock_path: Optional[Path] = None,
          poll_s: Optional[float] = None, max_wait_s: Optional[float] = None,
          timeout_s: int = land_lane.DEFAULT_TIMEOUT_S, interval_s: int = land_lane.DEFAULT_INTERVAL_S,
          land_lane_fn: Callable = DEFAULT_LAND_FN, now: Callable[[], float] = time.time) -> int:
    """Land each wake, oldest first, once. A stop ends the watch with that stop's exit code and leaves
    its wake (and every later one) unrecorded: the unlanded sha now sits on the integration branch."""
    home = Path(wake_home)
    cursor = cursor_path(home, batch)
    cursor.parent.mkdir(parents=True, exist_ok=True)
    if not cursor.exists():     # watch_wakes' own first start would record wakes older than 3 h unemitted
        cursor.write_text("", encoding="utf-8", newline="\n")

    def emit(line: str) -> None:
        _, _, rest = line.partition(" ")            # "WAKE <lane> <closing line>"
        lane, _, closing = rest.partition(" ")
        outcome = land_one(lane, closing, batch=batch, worktree=worktree, transport=transport,
                           receipts=receipts, carry_file=carry_file,
                           handback_at=_wake_written_at(lane, closing.strip(), home), integrator=integrator,
                           lock_wait_s=lock_wait_s, state_dir=state_dir, clock_path=clock_path,
                           timeout_s=timeout_s, interval_s=interval_s, land_lane_fn=land_lane_fn, now=now)
        if not outcome.recorded:
            raise LanderStop(outcome.exit_code, outcome.message)

    try:
        guard = _guard()
        guard.watch_wakes(home, ledger=cursor, poll_s=guard.WATCH_POLL_S if poll_s is None else poll_s,
                          max_wait_s=max_wait_s, emit=emit)
    except LanderStop as stop:
        return stop.exit_code
    return EXIT_OK


# --- the report ---------------------------------------------------------------------------------------

def _figures(values: list) -> str:
    if not values:
        return "UNMEASURED"
    ordered = sorted(values)
    p90 = ordered[max(0, math.ceil(0.9 * len(ordered)) - 1)]
    return f"median={statistics.median(ordered):.1f}s p90={p90:.1f}s"


def clock_report(clock_path: Path, last: int) -> str:
    """Median and p90 (nearest rank) of handback -> main and of each stage, over the last `last`
    lines whose state is LANDED. A figure with no value reads UNMEASURED, never 0."""
    try:
        raw = [ln for ln in Path(clock_path).read_text(encoding="utf-8").splitlines() if ln.strip()]
    except OSError:
        raw = []
    window = raw[-last:] if last > 0 else []
    rows = []
    for text in window:
        try:
            row = json.loads(text)
        except ValueError:
            continue
        if isinstance(row, dict) and row.get("state") == "LANDED":
            rows.append(row)
    out = [f"merge-clock: n={len(rows)} landed of {len(window)} lines (last {last})"]
    totals = [row["handback_to_main_s"] for row in rows if isinstance(row.get("handback_to_main_s"), (int, float))]
    out.append(f"handback->main: {_figures(totals)}")
    if not window:
        return "\n".join(out)
    for name in STAGE_ORDER:
        values = [row["stages"][name] for row in rows
                  if isinstance(row.get("stages"), dict) and isinstance(row["stages"].get(name), (int, float))]
        label = f"{name} (proxy)" if name == _PROXY_STAGE else name
        out.append(f"stage {label}: {_figures(values)}")
    return "\n".join(out)


# --- the CLI ------------------------------------------------------------------------------------------

def _common(fn):
    for option in reversed((
        click.option("--batch", required=True, help="the batch; the integration branch follows from it"),
        click.option("--worktree", "worktree", default=".", type=click.Path(path_type=Path),
                     help="the INTEGRATION worktree (default: the current directory)"),
        click.option("--transport", required=True, type=click.Path(path_type=Path),
                     help="the transport root holding to-browser/SESSION-<lane>.md"),
        click.option("--receipts", default=None, type=click.Path(path_type=Path),
                     help="the receipts directory (default: HARNESS_RECEIPTS_DIR, else the primary's)"),
        click.option("--carry-file", "carry_file", default=None, type=click.Path(path_type=Path),
                     help="receipt lines waiting for the next landing (default: next to the worktree)"),
        click.option("--clock", "clock_path", default=None, type=click.Path(path_type=Path),
                     help="the merge clock (default: <primary>/logs/MERGE-CLOCK.jsonl)"),
        click.option("--state-dir", "state_dir", default=None, type=click.Path(path_type=Path),
                     help="the private state directory holding the lock"),
        click.option("--lock-wait-s", "lock_wait_s", default=DEFAULT_LOCK_WAIT_VERB_S, type=float,
                     help="seconds to wait for another landing's lock (0: LANDER-BUSY at once)"),
        click.option("--i-am-the-integrator", "integrator", is_flag=True, default=False,
                     help="required to land against a non-local origin; a statement, never defaulted"),
    )):
        fn = option(fn)
    return fn


@click.group()
def cli() -> None:
    """Land a lane by code when it hands back. Calls land_lane in process; no model call."""


@cli.command("once")
@click.option("--lane", "slug", required=True, help="the lane slug")
@click.option("--handback-line", "handback_line", default=None,
              help="the closing line (default: the lane's last HANDBACK line in its SESSION file)")
@click.option("--handback-at", "handback_at", default=None, help="ISO time the lane handed back")
@click.option("--wake-home", "wake_home", default=None, type=click.Path(path_type=Path),
              help="the wake home to read the handback time from (read-only)")
@click.option("--dry-run", "dry_run", is_flag=True, default=False,
              help="print the plan and the result of each check; touch nothing")
@_common
def once_cmd(slug, handback_line, handback_at, wake_home, dry_run, batch, worktree, transport, receipts,
             carry_file, clock_path, state_dir, lock_wait_s, integrator) -> None:
    """Land ONE lane now."""
    sys.exit(once(slug, batch=batch, worktree=worktree, transport=transport, receipts=receipts,
                  carry_file=carry_file, handback_line=handback_line, handback_at=handback_at,
                  wake_home=wake_home, integrator=integrator, lock_wait_s=lock_wait_s, state_dir=state_dir,
                  clock_path=clock_path, dry_run=dry_run))


@cli.command("watch")
@click.option("--wake-home", "wake_home", default=None, type=click.Path(path_type=Path),
              help="the wake home (default: the per-user state directory's integrator-wake)")
@click.option("--poll-s", "poll_s", default=None, type=float)
@click.option("--max-wait-s", "max_wait_s", default=None, type=float, help="stop after this long (tests)")
@_common
def watch_cmd(wake_home, poll_s, max_wait_s, batch, worktree, transport, receipts, carry_file, clock_path,
              state_dir, lock_wait_s, integrator) -> None:
    """Land each wake file of this batch, once, oldest first; halt at the first stop."""
    home = wake_home or _guard().wake_dir(os.environ)
    sys.exit(watch(batch=batch, worktree=worktree, transport=transport, wake_home=home, receipts=receipts,
                   carry_file=carry_file, integrator=integrator, lock_wait_s=lock_wait_s,
                   state_dir=state_dir, clock_path=clock_path, poll_s=poll_s, max_wait_s=max_wait_s))


@cli.command("clock")
@click.option("--clock", "clock_path", default=None, type=click.Path(path_type=Path),
              help="the merge clock (default: <primary>/logs/MERGE-CLOCK.jsonl)")
@click.option("--last", "last", default=10, type=int, help="how many of the last lines to read")
def clock_cmd(clock_path, last) -> None:
    """Print the median and p90 of handback -> main over the last N lines."""
    path = clock_path or _primary(Path.cwd().resolve()) / "logs" / "MERGE-CLOCK.jsonl"
    click.echo(clock_report(path, last))


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
