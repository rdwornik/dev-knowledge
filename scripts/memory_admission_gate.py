#!/usr/bin/env python
"""memory_admission_gate.py -- the heavy-run admission gate (LANE-5A-3, D7).

WHAT THIS REFUSES. `to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md` D7: "8+ reaps, 2 lanes lost to
OOM, `-n` set by hand -- no admission control". A heavy run (pytest, `audit.py ship-gate`) was
launched with no regard for how much memory the box actually had free, and its worker count
was a number typed into a batch order rather than read off the machine. This module is the
mechanism DECLARE-NIGHT-AUTONOMY mechanism 1 names: wait for a memory reserve AND a
machine-wide slot before running a heavy command, run it in the foreground, size its `-n` from
the free memory that is actually there, and write a receipt of what happened.

WHAT THIS IS NOT. It is not `scripts/resource_lifecycle.py`'s LOCAL regime organ, and the two
read memory through two DIFFERENT instruments on purpose -- see the psutil library-first note
in `pyproject.toml` next to this module's dependency row. `resource_lifecycle.py` governs SEAT
admission (may another Claude Code session start) and session retirement; this module governs
COMMAND admission (may this one heavy subprocess start now) inside an already-running session.
Unifying them is future work this lane does not owe.

THE TWO GATES, IN THE ORDER A CALLER CROSSES THEM.
  1. MEMORY: `wait_for_memory` polls free memory until it clears `reserve + estimate`. No
     timeout by default (DECLARE-NIGHT-AUTONOMY N2 wants a run RESUMED, not abandoned); a
     caller that wants one sets `wait_timeout_s` in the YAML config or passes one explicitly.
  2. SLOT: `acquire_slot` claims one of `slots` machine-wide lock files under
     `logs/receipts/memory-gate-slots/` (gitignored, `HARNESS_MEMORY_GATE_SLOTS_DIR` overrides).
     DELIBERATELY its own env var, never `HARNESS_RECEIPTS_DIR`: that var is `test_pairing.py`'s
     per-test registry-home redirection convention, and a caller (`test_pairing.py` itself,
     gating its own subprocess pytest runs) that inherits its FULL environment into a gated
     command would otherwise steer this machine-wide semaphore into a test's throwaway tmp_path
     -- found live via `test_write_registry_never_replaces_an_existing_registry_unless_told_to`
     going red with a `memory-gate-slots` dir beside the registry it asserts is alone. `filelock`
     is the arbiter because every contender here shares one machine by construction -- contrast
     `scripts/single_flight.py`, whose git-ref lock exists for racers that may NOT share a
     filesystem, a stronger and more expensive property this gate does not need.

THE RECEIPT (`run_gated`'s callers get one per call): `waited_s`, `gated`, `ran`, `workers`
(`-n` computed, or null when no `workers_flag` was requested), `peak_used_mb` (system-wide
`used` memory, sampled every `sample_interval_s` while the command runs -- the tightest point
the box reached, not a per-process reading, because the reserve this gate protects is
SYSTEM-WIDE headroom), `returncode`, `argv`. Written UPPERCASE-KEBAB and undated under the
receipts home, same convention as `gates.py`'s `MOMENT-MERGE-GATES-VERDICT.json`.

OLD BEHAVIOUR, BY A FLAG (LANE-5A-3 done-contract item 2). Set `HARNESS_MEMORY_GATE_DISABLE=1`
(or pass `disabled=True` to `run_gated`) to skip both gates entirely: the command runs
immediately, `gated` is `False` in the receipt, and no `-n` is computed or inserted even when
`workers_flag` was requested -- the caller's own argv is used verbatim.

CONFIG. `ecosystem/memory-gate-config.yaml`, cited home, read by `load_config()`. Every number
in it is a chosen margin over a measured watermark, not itself a measurement -- the file's own
header says so and says where each figure comes from.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional, Sequence

import click

try:
    import psutil
except ImportError as exc:  # pragma: no cover - declared dependency
    raise SystemExit(f"memory_admission_gate: psutil is required: {exc!r}")

try:
    import filelock
except ImportError as exc:  # pragma: no cover - declared dependency
    raise SystemExit(f"memory_admission_gate: filelock is required: {exc!r}")

try:
    import yaml
except ImportError as exc:  # pragma: no cover - declared dependency
    raise SystemExit(f"memory_admission_gate: pyyaml is required: {exc!r}")

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
_CONFIG_PATH = _REPO_ROOT / "ecosystem" / "memory-gate-config.yaml"
_SLOT_LOCK_SUBDIR = "memory-gate-slots"
_RECEIPT_PREFIX = "MEMORY-GATE-RECEIPT"

#: Old behaviour, by a flag (done-contract item 2). Non-empty disables BOTH gates.
DISABLE_ENV = "HARNESS_MEMORY_GATE_DISABLE"

#: The slot lock directory's own override -- deliberately NOT `HARNESS_RECEIPTS_DIR` (see the
#: module docstring's gate-2 paragraph for why the two must never share a var).
SLOTS_DIR_ENV = "HARNESS_MEMORY_GATE_SLOTS_DIR"

#: `run` subcommand only: the wrapped command's own `subprocess.TimeoutExpired` fired. The
#: POSIX `timeout(1)` convention -- distinguishable from any real exit code the wrapped
#: command itself could produce (pytest's own codes top out at 5). A caller invoking this CLI
#: (rather than importing `run_gated`, e.g. `test_pairing.py`'s stdlib-only import boundary --
#: see that module's own comment at its `run_pytest_full` call site) checks for this code to
#: tell "the command timed out" apart from "the command ran and failed".
TIMEOUT_EXIT_CODE = 124


class MemoryGateTimeout(Exception):
    """A wait (memory or slot) exceeded its configured timeout without being admitted."""


# ============================================================================== configuration

@dataclass(frozen=True)
class GateConfig:
    reserve_gb: float
    per_worker_mb: float
    slots: int
    min_workers: int
    max_workers: int
    poll_interval_s: float
    sample_interval_s: float
    wait_timeout_s: Optional[float]

    @property
    def reserve_mb(self) -> float:
        return self.reserve_gb * 1024.0


_DEFAULTS = GateConfig(reserve_gb=2.0, per_worker_mb=646.1, slots=4, min_workers=1,
                       max_workers=6, poll_interval_s=5.0, sample_interval_s=2.0,
                       wait_timeout_s=None)


def load_config(path: Optional[Path] = None) -> GateConfig:
    """`ecosystem/memory-gate-config.yaml`, or `path`. A missing file yields the built-in
    defaults rather than refusing -- the gate must still work in a checkout that has not yet
    synced the config (e.g. a test fixture), and the defaults are the same numbers the shipped
    YAML carries."""
    path = Path(path) if path else _CONFIG_PATH
    if not path.is_file():
        return _DEFAULTS
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    timeout = raw.get("wait_timeout_s", _DEFAULTS.wait_timeout_s)
    return GateConfig(
        reserve_gb=float(raw.get("reserve_gb", _DEFAULTS.reserve_gb)),
        per_worker_mb=float(raw.get("per_worker_mb", _DEFAULTS.per_worker_mb)),
        slots=int(raw.get("slots", _DEFAULTS.slots)),
        min_workers=int(raw.get("min_workers", _DEFAULTS.min_workers)),
        max_workers=int(raw.get("max_workers", _DEFAULTS.max_workers)),
        poll_interval_s=float(raw.get("poll_interval_s", _DEFAULTS.poll_interval_s)),
        sample_interval_s=float(raw.get("sample_interval_s", _DEFAULTS.sample_interval_s)),
        wait_timeout_s=(float(timeout) if timeout is not None else None),
    )


# ==================================================================================== reading

def free_memory_mb() -> float:
    """System-wide AVAILABLE memory, in MB. The one platform-agnostic call psutil buys this
    module over `resource_lifecycle.py`'s two hand-rolled parsers (WMI via PowerShell, and
    `/proc/meminfo`) -- see the library-first note in `pyproject.toml`."""
    return psutil.virtual_memory().available / (1024 * 1024)


def used_memory_mb() -> float:
    """System-wide USED memory, in MB -- what the peak-memory sampler reads."""
    return psutil.virtual_memory().used / (1024 * 1024)


# ============================================================================ workers from RAM

def compute_workers(free_mb: float, *, reserve_mb: float, per_worker_mb: float,
                    min_workers: int, max_workers: int) -> int:
    """`-n`, computed from free memory rather than typed into a batch order.

    The floor and ceiling are never crossed regardless of the reading: `min_workers` because a
    memory-tight box still gets to run SOMETHING (0 workers is `pytest -n 0`, a different and
    slower mode, not "wait longer" -- waiting is `wait_for_memory`'s job, not this function's),
    and `max_workers` because xdist worker count has its own non-memory ceiling (CPU count,
    import contention, disk) that a memory-only formula cannot see.
    """
    if per_worker_mb <= 0:
        return max(min_workers, 0)
    budget_mb = max(0.0, free_mb - reserve_mb)
    computed = int(budget_mb // per_worker_mb)
    return max(min_workers, min(max_workers, computed))


# ======================================================================= gate 1: free memory

@dataclass(frozen=True)
class WaitResult:
    waited_s: float
    checks: int
    free_mb_final: float


def wait_for_memory(*, reserve_mb: float, estimate_mb: float, poll_interval_s: float,
                    timeout_s: Optional[float] = None,
                    free_mb_fn: Callable[[], float] = free_memory_mb,
                    sleep_fn: Callable[[float], None] = time.sleep,
                    clock_fn: Callable[[], float] = time.monotonic) -> WaitResult:
    """Block until free memory clears `reserve_mb + estimate_mb`. BOTH legs are one number here
    (unlike `resource_lifecycle.admit`, which reports them separately for a seat) because this
    gate has only one caller-visible question: is there room for THIS command. Raises
    `MemoryGateTimeout` if `timeout_s` is set and elapses first -- never runs the command under
    the reserve and calls that success."""
    start = clock_fn()
    checks = 0
    needed = reserve_mb + estimate_mb
    while True:
        free = free_mb_fn()
        checks += 1
        if free >= needed:
            return WaitResult(waited_s=clock_fn() - start, checks=checks, free_mb_final=free)
        elapsed = clock_fn() - start
        if timeout_s is not None and elapsed >= timeout_s:
            raise MemoryGateTimeout(
                f"free memory {free:.0f} MB stayed below {needed:.0f} MB "
                f"(reserve {reserve_mb:.0f} + estimate {estimate_mb:.0f} MB) after "
                f"{elapsed:.1f}s and {checks} check(s)")
        sleep_fn(poll_interval_s)


# ========================================================================= gate 2: the slot

def _slot_lock_dir(lock_dir: Optional[Path]) -> Path:
    if lock_dir is not None:
        base = Path(lock_dir)
    else:
        base = Path(os.environ.get(SLOTS_DIR_ENV) or (_REPO_ROOT / "logs" / "receipts" / _SLOT_LOCK_SUBDIR))
    base.mkdir(parents=True, exist_ok=True)
    return base


@dataclass
class SlotHandle:
    slot_id: int
    _lock: "filelock.FileLock"

    def release(self) -> None:
        self._lock.release()


def acquire_slot(*, slots: int, lock_dir: Optional[Path] = None,
                 poll_interval_s: float = 1.0, timeout_s: Optional[float] = None,
                 sleep_fn: Callable[[float], None] = time.sleep,
                 clock_fn: Callable[[], float] = time.monotonic) -> SlotHandle:
    """Claim one of `slots` machine-wide slots. Tries every slot file once per round (not just
    slot 0) so a released slot elsewhere in the range is picked up without waiting a full extra
    `poll_interval_s` for slot 0 specifically. Raises `MemoryGateTimeout` if none frees up
    before `timeout_s`."""
    directory = _slot_lock_dir(lock_dir)
    start = clock_fn()
    while True:
        for slot_id in range(slots):
            # `thread_local=False`: filelock's DEFAULT stores the fd/counter in
            # `threading.local()`, so a release from a different thread than the one that
            # acquired is a silent no-op (the releasing thread's own context was never
            # marked locked, so `release()` returns early having never touched the real OS
            # lock -- measured live, `_dbg_filelock2.py`/`_dbg_filelock3.py` during this
            # lane's own development). A machine-wide slot must not depend on which thread
            # inside a process happens to call `release()`.
            lock = filelock.FileLock(str(directory / f"slot-{slot_id}.lock"), thread_local=False)
            try:
                lock.acquire(timeout=0)
            except filelock.Timeout:
                continue
            return SlotHandle(slot_id=slot_id, _lock=lock)
        elapsed = clock_fn() - start
        if timeout_s is not None and elapsed >= timeout_s:
            raise MemoryGateTimeout(f"no free slot among {slots} after {elapsed:.1f}s")
        sleep_fn(poll_interval_s)


# ======================================================================== peak-memory sampler

def _sample_peak(stop: threading.Event, interval_s: float, samples: list[float],
                 used_mb_fn: Callable[[], float]) -> None:
    """Append one reading, then wait -- so a run shorter than `interval_s` still yields one
    sample rather than none."""
    while not stop.is_set():
        try:
            samples.append(used_mb_fn())
        except Exception:  # noqa: BLE001 -- a sampler must never abort the run it is watching
            pass
        stop.wait(interval_s)


# ================================================================================== the gate

@dataclass(frozen=True)
class GateResult:
    ran: bool
    gated: bool
    waited_s: float
    slot_id: Optional[int]
    workers: Optional[int]
    peak_used_mb: Optional[float]
    returncode: Optional[int]
    argv: list[str]
    completed: Optional[subprocess.CompletedProcess] = None


def _default_receipt_dir() -> Path:
    return Path(os.environ.get("HARNESS_RECEIPTS_DIR") or (_REPO_ROOT / "logs" / "receipts"))


def _write_receipt(result: GateResult, path: Optional[Path]) -> Path:
    out = Path(path) if path else (_default_receipt_dir() / f"{_RECEIPT_PREFIX}-{uuid.uuid4().hex}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": 1,
        "ran": result.ran,
        "gated": result.gated,
        "waited_s": round(result.waited_s, 3),
        "slot_id": result.slot_id,
        "workers": result.workers,
        "peak_used_mb": round(result.peak_used_mb, 1) if result.peak_used_mb is not None else None,
        "returncode": result.returncode,
        "argv": result.argv,
        "written_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    tmp = out.with_name(out.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8", newline="\n")
    os.replace(tmp, out)
    return out


def run_gated(argv: Sequence[str], *, cwd: Optional[Path] = None,
             estimate_mb: Optional[float] = None,
             workers_flag: Optional[str] = None,
             config: Optional[GateConfig] = None,
             disabled: Optional[bool] = None,
             receipt_path: Optional[Path] = None,
             lock_dir: Optional[Path] = None,
             free_mb_fn: Callable[[], float] = free_memory_mb,
             used_mb_fn: Callable[[], float] = used_memory_mb,
             sleep_fn: Callable[[float], None] = time.sleep,
             clock_fn: Callable[[], float] = time.monotonic,
             subprocess_run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
             **subprocess_kwargs) -> GateResult:
    """Wait for memory, wait for a slot, run `argv` in the foreground, write a receipt.

    `workers_flag`, when given (e.g. `"-n"`), makes this call COMPUTE `-n` from free memory and
    append `<workers_flag> <n>` to `argv` -- the caller's own `-n`, if any, must not already be
    in `argv`. With `workers_flag=None` the command runs unmodified; the memory and slot gates
    still apply (a non-pytest heavy command, e.g. `audit.py ship-gate`, has no `-n` to compute
    but still needs the same admission).

    `disabled=True` (or env `HARNESS_MEMORY_GATE_DISABLE` set), the LANE-5A-3 done-contract's
    "old behaviour by a flag": both gates are skipped, `argv` runs verbatim and immediately,
    and the receipt records `gated: false`.
    """
    cfg = config or load_config()
    if disabled is None:
        disabled = bool(os.environ.get(DISABLE_ENV))
    full_argv = list(argv)
    cwd_str = str(cwd) if cwd is not None else None

    if disabled:
        proc = subprocess_run(full_argv, cwd=cwd_str, **subprocess_kwargs)
        result = GateResult(ran=True, gated=False, waited_s=0.0, slot_id=None, workers=None,
                            peak_used_mb=None, returncode=proc.returncode, argv=full_argv,
                            completed=proc)
        _write_receipt(result, receipt_path)
        return result

    workers: Optional[int] = None
    estimate = estimate_mb if estimate_mb is not None else cfg.per_worker_mb
    if workers_flag:
        workers = compute_workers(free_mb_fn(), reserve_mb=cfg.reserve_mb,
                                  per_worker_mb=cfg.per_worker_mb,
                                  min_workers=cfg.min_workers, max_workers=cfg.max_workers)
        full_argv = [*full_argv, workers_flag, str(workers)]
        if estimate_mb is None:
            estimate = cfg.per_worker_mb * max(1, workers)

    # `waited_s` in the receipt is BOTH gates' wait time, summed -- a caller reading the
    # receipt asks "how long did admission cost me", not "which of the two gates cost it",
    # and `acquire_slot` (unlike `wait_for_memory`) has no return value to carry its own
    # duration, so it is timed here rather than inside it.
    slot_wait_start = clock_fn()
    slot = acquire_slot(slots=cfg.slots, lock_dir=lock_dir, poll_interval_s=cfg.poll_interval_s,
                        timeout_s=cfg.wait_timeout_s, sleep_fn=sleep_fn, clock_fn=clock_fn)
    slot_waited_s = clock_fn() - slot_wait_start
    try:
        wait = wait_for_memory(reserve_mb=cfg.reserve_mb, estimate_mb=estimate,
                               poll_interval_s=cfg.poll_interval_s, timeout_s=cfg.wait_timeout_s,
                               free_mb_fn=free_mb_fn, sleep_fn=sleep_fn, clock_fn=clock_fn)
        samples: list[float] = []
        stop = threading.Event()
        sampler = threading.Thread(target=_sample_peak,
                                   args=(stop, cfg.sample_interval_s, samples, used_mb_fn),
                                   daemon=True)
        sampler.start()
        try:
            proc = subprocess_run(full_argv, cwd=cwd_str, **subprocess_kwargs)
        finally:
            stop.set()
            sampler.join(timeout=5.0)
        peak = max(samples) if samples else None
        result = GateResult(ran=True, gated=True, waited_s=slot_waited_s + wait.waited_s,
                            slot_id=slot.slot_id, workers=workers, peak_used_mb=peak,
                            returncode=proc.returncode, argv=full_argv, completed=proc)
        _write_receipt(result, receipt_path)
        return result
    finally:
        slot.release()


# ============================================================================================ CLI

@click.group()
def cli() -> None:
    """The heavy-run admission gate ([#D7])."""


@cli.command("ceiling")
def cmd_ceiling() -> None:
    """Print the config, the live reading, and the `-n` it would compute right now."""
    cfg = load_config()
    free = free_memory_mb()
    n = compute_workers(free, reserve_mb=cfg.reserve_mb, per_worker_mb=cfg.per_worker_mb,
                        min_workers=cfg.min_workers, max_workers=cfg.max_workers)
    click.echo(f"free           {free:10.1f} MB")
    click.echo(f"reserve        {cfg.reserve_mb:10.1f} MB")
    click.echo(f"per worker     {cfg.per_worker_mb:10.1f} MB")
    click.echo(f"slots          {cfg.slots:10d}")
    click.echo(f"COMPUTED -n    {n:10d}")


@cli.command("run", context_settings={"ignore_unknown_options": True})
@click.option("--workers-flag", default=None, help='e.g. "-n" -- compute and append it')
@click.option("--estimate-mb", type=float, default=None)
@click.option("--timeout", "timeout_s", type=float, default=None,
             help="seconds allowed for the wrapped command; exit code "
                  f"{TIMEOUT_EXIT_CODE} on expiry")
@click.option("--receipt", "receipt_path", type=click.Path(dir_okay=False), default=None)
@click.argument("argv", nargs=-1, type=click.UNPROCESSED, required=True)
def cmd_run(workers_flag: Optional[str], estimate_mb: Optional[float],
           timeout_s: Optional[float], receipt_path: Optional[str], argv: tuple[str, ...]) -> None:
    """Gate, then run ARGV (everything after `--`) in the FOREGROUND, inheriting this
    process's stdio and cwd so a caller capturing THIS process's output transparently
    captures the wrapped command's -- no output is read or re-printed by this command itself.
    Exits with the wrapped command's own returncode, or `TIMEOUT_EXIT_CODE` on a timeout.

    THE PROCESS-BOUNDARY ENTRY POINT, for a caller that must not import this module's Python
    API -- `test_pairing.py`'s own "parsing and isolation use only the standard library"
    invariant (`tests/test_test_pairing.py::test_parsing_and_isolation_use_only_the_standard_library`)
    is exactly that caller: it shells out to this command via `subprocess`, stdlib, rather
    than `import memory_admission_gate`, which would pull click/psutil/filelock/pyyaml into a
    module whose whole point is to stay correct even when the dependency graph is broken.
    """
    kwargs: dict = {}
    if timeout_s is not None:
        kwargs["timeout"] = timeout_s
    try:
        result = run_gated(list(argv), workers_flag=workers_flag, estimate_mb=estimate_mb,
                           receipt_path=Path(receipt_path) if receipt_path else None, **kwargs)
    except subprocess.TimeoutExpired:
        sys.exit(TIMEOUT_EXIT_CODE)
    sys.exit(result.returncode if result.returncode is not None else 1)


@cli.command("wait")
@click.option("--estimate-mb", type=float, default=None)
@click.option("--timeout", "timeout_s", type=float, default=None)
def cmd_wait(estimate_mb: Optional[float], timeout_s: Optional[float]) -> None:
    """Block until admission would succeed; exit 1 on timeout. Manual/diagnostic use."""
    cfg = load_config()
    estimate = estimate_mb if estimate_mb is not None else cfg.per_worker_mb
    timeout = timeout_s if timeout_s is not None else cfg.wait_timeout_s
    try:
        result = wait_for_memory(reserve_mb=cfg.reserve_mb, estimate_mb=estimate,
                                 poll_interval_s=cfg.poll_interval_s, timeout_s=timeout)
    except MemoryGateTimeout as exc:
        click.echo(f"wait: TIMEOUT: {exc}")
        sys.exit(1)
    click.echo(f"wait: admitted after {result.waited_s:.1f}s ({result.checks} check(s)); "
              f"{result.free_mb_final:.1f} MB free")


if __name__ == "__main__":
    cli()
