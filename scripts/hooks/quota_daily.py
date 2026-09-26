#!/usr/bin/env python
"""quota_daily.py -- SessionStart trigger for the silent `quota_watch.py` organ
(LANE-5B3-2-wire-quota-distiller).

THE GAP THIS CLOSES: `quota_watch.py` MERGED 2026-09-25 (LANE-5B2-6) with nobody calling it.
`logs/QUOTA-READS.jsonl` did not exist a day later (DIGEST-WAVE5B-N2-2026-09-26.md G9). This
module is the "once a day at session start" leg of that lane's Value line; the batch-close leg
lives in `templates/integrator-order-template.md`'s close step instead.

PRIOR ART REUSED, NOT DUPLICATED (O-12): the reader/trigger/producer split and the exact
detach mechanism are `scripts/fleet_health.py`'s own ([#962] item 3/4: `_claim_producer`,
`maybe_trigger_producer`, `run_producer`) -- a claim file wins the race exactly once, a
detached worker (`scripts/lane_end_guard.py::spawn_worker` -- Windows job-object breakaway,
closed stdio, its own process group) does the slow part outside this hook's own execution,
and the hook itself only ever claims-and-spawns, never blocks. The SAME reason fleet_health.py
gives for never running its slow part inline applies here with more force, not less: this
very settings.json's own `//hooks-EMERGENCY-DISABLED-2026-09-17` entry records SEVEN sessions
wedged 12-18 hours by an ungated network call inside a hook. `quota_watch.py record` calls
`gh api` over the network -- so this guard NEVER attempts the live read inline. It always
claims and detaches; there is no "try inline, fall back to detached" branch to reason about.

GUARD CONTRACT (Done-contract item 2): fail-open on every error (`main()`'s outer try/except
prints the cause and returns 0 -- a SessionStart hook must never block a session); skipped
in every LINKED WORKTREE (`_is_linked_worktree`, REFUSED-lane-wire-quota-distiller.md repair
1 -- `logs/QUOTA-READS.jsonl` is a TRACKED ledger, and this hook's own `$CLAUDE_PROJECT_DIR`
is whichever checkout started the session, so firing from every lane worktree would write N
diverging tracked copies; the batch-close leg alone writes it, from the pinned primary);
skipped when `logs/QUOTA-READS.jsonl` already carries a row measured today (UTC, matching
`quota_watch.py`'s own `_now_iso()`); a same-day claim file (`logs/receipts/
QUOTA-DAILY-CLAIM.json`, the same O_CREAT|O_EXCL exclusive-create as `_claim_producer`)
de-duplicates spawns across SessionStart calls inside the same stale window, and is reaped
(as stale-day or stale-running, `_CLAIM_STALE_S`) so a dead worker does not block the rest of
the day.

CALL SURFACE
    uv run --locked python scripts/hooks/quota_daily.py            # the SessionStart guard
    uv run --locked python scripts/hooks/quota_daily.py --producer # the detached worker only
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_HOOKS_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _HOOKS_DIR.parent
_REPO_ROOT = _SCRIPTS_DIR.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import quota_watch as qw
except ImportError:  # pragma: no cover
    import quota_watch as qw  # type: ignore

_PRODUCER_FLAG = "--producer"
_CLAIM_NAME = "QUOTA-DAILY-CLAIM.json"

#: Bounds the one `quota_watch.py record` subprocess (a handful of `gh api` calls) -- generous
#: versus a live network round trip, well under `_CLAIM_STALE_S` so a run that finishes late is
#: still reaped and retried inside the same day rather than blocking it (Codex terra HIGH,
#: 2026-09-26: an unbounded `subprocess.run` could hang past the SessionStart hook's own life).
_PRODUCER_TIMEOUT_S = 120

#: Generous versus a `gh api` round trip, tight versus a worker that died mid-call --
#: `fleet_health._PRODUCER_STALE_RUNNING_S` (1800s) sizes for a multi-minute audit; this
#: organ's live read is a handful of `gh api` calls, not an audit, so ten minutes is ample
#: headroom without leaving a dead claim uncollected for most of a day.
_CLAIM_STALE_S = 600


def _today_utc() -> str:
    """The same UTC calendar day `quota_watch.QuotaRead.measured` (`_now_iso()`) stamps --
    so "already read today" means the same day the ledger itself would say, not a local-
    timezone approximation of it."""
    return datetime.now(timezone.utc).date().isoformat()


def _now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _has_read_today(ledger_path: Path, today: str) -> bool:
    """`quota_watch.read_ledger` already tolerates a missing file (returns `[]`) and a
    malformed line (skips it, logs a warning) -- reused here rather than re-parsed, so a
    read that is "already there" for the skip check is defined identically to a read the
    ledger itself would report."""
    for row in qw.read_ledger(ledger_path):
        if row.measured[:10] == today:
            return True
    return False


def _git_rev_parse(repo_root: Path, arg: str) -> Optional[str]:
    """One `git rev-parse` call, textual stdout on success, `None` on any failure (git
    missing, `repo_root` not a repository, timeout) -- never raises."""
    try:
        proc = subprocess.run(["git", "rev-parse", arg], cwd=str(repo_root),
                              capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _is_linked_worktree(repo_root: Path) -> bool:
    """DECIDED-BY-LANE (REFUSED-lane-wire-quota-distiller.md repair 1): the daily read fires
    from the PRIMARY checkout only, detected the way git itself distinguishes a linked
    worktree from its primary (git-worktree(1)) -- `--git-dir` is worktree-specific
    (`<primary>/.git/worktrees/<name>`) while `--git-common-dir` always resolves to the
    primary's own `.git`; the two are equal only in the primary. Chosen over "write to a
    gitignored path" or "resolve the primary and redirect the write there" because it needs
    no new path convention and no cross-checkout write -- it just leaves every OTHER
    checkout's SessionStart a no-op for this organ, exactly as the batch-close leg (which
    writes from the pinned primary alone) already assumes.

    Returns True -- SKIP, not fire -- when git itself cannot answer (not a repository, no git
    on PATH, a timeout): Codex terra HIGH, 2026-09-26 (this repair): an unconfirmed checkout
    is exactly the class this guard exists to distrust, and returning False there would let a
    checkout git cannot identify recreate the very divergent-tracked-ledger bug being fixed.
    Fail-open still holds -- the SessionStart hook itself never blocks the session (`main()`'s
    outer try/except) -- but "never block the session" and "prove I am the primary before
    writing a tracked file" are different guarantees, and only skipping satisfies both.
    """
    git_dir = _git_rev_parse(repo_root, "--git-dir")
    common_dir = _git_rev_parse(repo_root, "--git-common-dir")
    if git_dir is None or common_dir is None:
        return True
    return (repo_root / git_dir).resolve() != (repo_root / common_dir).resolve()


def _claim_path(repo_root: Path) -> Path:
    return repo_root / "logs" / "receipts" / _CLAIM_NAME


def _read_claim(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _age_s(path: Path) -> float:
    try:
        return time.time() - path.stat().st_mtime
    except OSError:
        return 0.0


def _reap_stale_claim(path: Path, today: str) -> None:
    """A claim from a PRIOR day is always stale (a new day's guard must be free to claim
    fresh); a `running` claim from TODAY is stale only past `_CLAIM_STALE_S` (its worker
    likely died). A `today`-dated terminal claim (status `ok`/`FAILED`) is left alone --
    that is this day's real answer, not an abandoned attempt."""
    current = _read_claim(path)
    if not current:
        return
    stale_day = current.get("date") != today
    stale_running = current.get("status") == "running" and _age_s(path) > _CLAIM_STALE_S
    if stale_day or stale_running:
        try:
            path.unlink()
        except OSError:
            pass


def _claim(path: Path, today: str) -> bool:
    """The once-per-day claim: an exclusive create, so of several SessionStart calls in the
    same stale window exactly one spawns a worker (`fleet_health._claim_producer`'s own
    pattern). Never raises -- a claim directory that cannot be made is a guard error the
    caller's own try/except turns into a fail-open return."""
    path.parent.mkdir(parents=True, exist_ok=True)
    _reap_stale_claim(path, today)
    payload = json.dumps({"schema": 1, "organ": "quota_daily", "status": "running",
                          "date": today, "started_at": _now_stamp()},
                         sort_keys=True).encode("utf-8")
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    with os.fdopen(fd, "wb") as f:
        f.write(payload)
    return True


def _write_claim_result(path: Path, **fields) -> None:
    """Never raises -- a receipt write failing must not become a second failure stacked on
    whatever it is trying to record (`fleet_health._write_producer_receipt`'s own posture)."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema": 1, "organ": "quota_daily", "finished_at": _now_stamp(), **fields}
        tmp = path.with_name(f".{path.name}.tmp")
        tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        pass


def _import_lane_end_guard():
    """Lazy sibling import, the same shape `fleet_health._import_lane_end_guard` uses: keeps
    the reader/trigger path's import graph free of anything only the detached worker needs."""
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import lane_end_guard  # noqa: E402
    return lane_end_guard


def maybe_trigger_read(repo_root: Path = _REPO_ROOT, environ: Optional[dict] = None) -> None:
    """The trigger: called only once the guard has decided today has no read yet. Takes the
    exclusive claim; a second call in the same stale window does nothing. Spawning reuses
    `lane_end_guard.spawn_worker` directly, never a re-implementation of it. Never raises --
    a worker that could not start is a FAILED claim result, exactly as a crashing moment is
    in `lane_end_guard` and `fleet_health`.
    """
    environ = os.environ if environ is None else environ
    today = _today_utc()
    claim_path = _claim_path(repo_root)
    if not _claim(claim_path, today):
        print("[quota] a live read is already in flight for today; SessionStart guard skips")
        return
    worker_argv = [sys.executable, str(Path(__file__).resolve()), _PRODUCER_FLAG]
    try:
        le = _import_lane_end_guard()
        broke_away = le.spawn_worker(worker_argv, repo_root, dict(environ))
    except BaseException as exc:  # noqa: BLE001 -- no worker means no read: record it, never block SessionStart
        _write_claim_result(claim_path, status="FAILED",
                            reason=f"could not start the worker: {type(exc).__name__}: {exc}")
        print(f"[quota] could not spawn the live read (fail-open): {exc}")
        return
    if not broke_away:
        # Codex terra HIGH, 2026-09-26: `spawn_worker` returning False means the worker started
        # INSIDE this hook's own job (breakaway was refused), so it can be killed the instant
        # this SessionStart hook's process ends -- a `running` claim from a worker that never
        # gets to finish would otherwise suppress every read for the rest of `_CLAIM_STALE_S`.
        # Treated as failed immediately so the NEXT SessionStart retries instead of waiting it out.
        _write_claim_result(
            claim_path, status="FAILED",
            reason="spawn_worker could not break the worker away from this hook's own job; "
                  "it may be killed with the hook, so this read is not trusted")
        print("[quota] worker could not detach from this hook's job (fail-open, treated as failed)")
        return
    print("[quota] no read recorded today; spawned a detached live read")


def run_producer(repo_root: Path = _REPO_ROOT, environ: Optional[dict] = None) -> int:
    """The detached worker's own entry point (`--producer`): the ONE place this organ
    actually calls `gh api`, via `quota_watch.py record` -- reused as a subprocess, not
    re-implemented, so this module carries no billing-read logic of its own. `sys.executable`
    is used directly rather than re-wrapped in `uv run --locked`, the same choice
    `fleet_health.py`'s own worker_argv makes and for the same reason: this process's own
    interpreter is already the locked venv's, and the detached worker must start as fast as
    the parent that spawned it, not pay a second `uv run` resolution.
    """
    environ = os.environ if environ is None else environ
    claim_path = _claim_path(repo_root)
    quota_watch_path = _SCRIPTS_DIR / "quota_watch.py"
    try:
        proc = subprocess.run([sys.executable, str(quota_watch_path), "record"],
                              cwd=str(repo_root), capture_output=True, env=dict(environ),
                              timeout=_PRODUCER_TIMEOUT_S)
    except subprocess.TimeoutExpired as exc:
        # Codex terra HIGH, 2026-09-26: an unbounded `subprocess.run` could hang past this
        # worker's own useful life with no claim result ever written -- bounded and turned into
        # a terminal FAILED result so a later session's `_reap_stale_claim` is not the only thing
        # standing between a hung `gh api` call and a claim stuck at `running` all day.
        _write_claim_result(
            claim_path, status="FAILED",
            reason=f"quota_watch.py record exceeded the {_PRODUCER_TIMEOUT_S}s producer "
                  f"timeout: {exc}")
        return 1
    except OSError as exc:
        _write_claim_result(
            claim_path, status="FAILED",
            reason=f"could not launch quota_watch.py record: {type(exc).__name__}: {exc}")
        return 1
    ok = proc.returncode == 0
    _write_claim_result(
        claim_path, status=("ok" if ok else "FAILED"), returncode=proc.returncode,
        stdout=proc.stdout.decode("utf-8", "replace")[-2000:],
        stderr=("" if ok else proc.stderr.decode("utf-8", "replace")[-2000:]))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if _PRODUCER_FLAG in argv:
        return run_producer()
    try:
        if _is_linked_worktree(_REPO_ROOT):
            print("[quota] linked worktree; the daily read fires from the primary checkout "
                  "only (skip, fail-open)")
            return 0
        today = _today_utc()
        ledger_path = qw.reads_ledger_path(_REPO_ROOT)
        if _has_read_today(ledger_path, today):
            print(f"[quota] already read today ({today}); SessionStart guard skips")
            return 0
        maybe_trigger_read(_REPO_ROOT)
        return 0
    except Exception as exc:  # noqa: BLE001 -- fail-open: a SessionStart guard never blocks the session
        print(f"[quota] guard error, failing open: {type(exc).__name__}: {exc}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
