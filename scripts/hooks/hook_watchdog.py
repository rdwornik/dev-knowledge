#!/usr/bin/env python
"""hook_watchdog.py -- `[#863]`: a hook process created SUSPENDED never runs a single line, so
no bound living INSIDE it can ever fire. Only an external watchdog that reads the OS process
table from outside that process's own tree can see it at all. This module is that watchdog.

WHY THE PROCESS IS CREATED SUSPENDED IN THE FIRST PLACE (Done-item 1) -- cited, not inferred.
Every child process Node.js spawns on Windows goes through libuv's `uv_spawn`
(`src/win/process.c`). For the class of spawn a hook's top-level command needs -- its own
process group, so it survives independently of the harness process and can be killed as a
whole tree at the hook's declared `timeout` (`UV_PROCESS_DETACHED`) -- libuv's own sequence is
TWO separate Win32 calls, never one (quoted verbatim, libuv v1.x, fetched 2026-09-29 from
`https://raw.githubusercontent.com/libuv/libuv/v1.x/src/win/process.c`, around line 1120-1174;
a copy is kept beside this lane's handback):

    process_flags |= DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP;
    process_flags |= CREATE_SUSPENDED;
    ...
    CreateProcessW(application_path, arguments, NULL, NULL, 1, process_flags, ..., &info)
    ...
    if (process_flags & CREATE_SUSPENDED) {
      if (ResumeThread(info.hThread) == ((DWORD)-1)) {
        err = GetLastError();
        TerminateProcess(info.hProcess, 1);
        goto done;
      }
    }

`CreateProcessW` is called WITH `CREATE_SUSPENDED`; the child's one thread is resumed only by
the SEPARATE, LATER `ResumeThread` call. Standard-handle inheritance (the harness's own
stdout/stderr pipes) is wired up by `CreateProcessW` itself, before any thread ever runs --
this repo's own measurement (`bounded_hook.py`'s docstring, lane ab-808 step 1) already
established that "the harness waits for [an inherited] pipe to close" past a hook's bound with
no record at all. Put the two facts together: a child created suspended holds that inherited
pipe open from the instant `CreateProcessW` returns, whether or not its thread is ever resumed.

If the process that would next call `ResumeThread` -- the intermediate shell layer Claude Code
hook commands run through, or Node itself -- exits or is killed in the window between those two
calls, the child is orphaned already-suspended: one thread in `Wait/Suspended`, zero CPU, an
inherited pipe held open forever, parent already gone. That is `[#863]`'s measured signature,
verbatim ("0 s CPU, no image path, one thread in Wait/Suspended, parent shell dead"). It is also
why `[#808]`'s bound cannot reach this mode: the bound fires on, and can only kill, the hook's
TOP process -- and killing that top process while a grandchild's `uv_spawn` is mid-flight
between its own `CreateProcessW` and `ResumeThread` is precisely what orphans the grandchild
suspended. Nothing thereafter ever calls `ResumeThread` for it; the one process responsible for
that call is the one the bound just killed. The measured 18-22 s interpreter cold-start jitter
(`bounded_hook.py`'s `HARNESS_HEADROOM_S` comment) widens this window rather than closing it.

OPERATOR-ACTION (honest limit, R15): confirming that Claude Code's own hook-command spawn
passes Node's `detached: true` (the option that reaches `UV_PROCESS_DETACHED`) would upgrade
this from a grounded synthesis of two cited, independently-verified facts to a confirmed one.
That requires reading the installed client's own bundled source outside this repository, which
is out of this batch's scope (R15). Path to check, if a future lane is given that scope: the
installed Claude Code CLI's own child_process spawn call for a hook command (look for
`detached` alongside the `shell` option in its bundled JS).

WHAT THIS MODULE DOES. `sweep()` takes ONE shared CPU-time sample of every candidate hook
process (a live process whose command line names a script `.claude/settings.json` registers as
a hook AND whose parent is already gone -- the incident's own "parent shell dead" half),
sleeps `threshold_s`, samples again, and treats a candidate whose sampled CPU time did not move
in that whole window as the `[#863]` signature: it kills that process's whole tree and records
the kill to a durable, named surface (hook id, pid, age, session id -- best-effort, since a
process that never ran a line never read a session id off its own stdin; see `_session_id_for`)
never silently.

WHAT THIS MODULE DOES NOT DO. It is not a per-hook wrapper -- `bounded_hook.py` already bounds
a hook's execution time once its top process has started running a line, and its settings-file
wiring is deliberately HELD (operator ruling 2026-09-17 item 1) for the very reason this bug
exists: wrapping adds another interpreter to spawn, which is one more chance to create one
suspended. This module reads the OS process table from OUTSIDE the hook's own process tree,
which is the only vantage a process that has not executed one instruction can be seen from at
all. It carries no settings.json wiring of its own (`ecosystem/harness.yaml`'s `fates:` block
records it `manual_until` the date this lane's handback states) -- it is run by hand,
`sweep`, until a later lane judges an automatic trigger safe.

Stdlib + `psutil` only (already declared, `pyproject.toml`; the same library `resource_lifecycle.py`
and `memory_admission_gate.py` already use for process-tree reads -- library-first). The kill
itself uses `taskkill /T /F` on Windows, fired and not awaited, the identical pattern
`bounded_hook.py::_kill_tree` already uses and for the same reason: a wrapper that waits on its
own kill has moved the unbounded wait one level down.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psutil

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from bounded_hook import _SCRIPT_RE, _transcript_hook_id, primary_root  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parents[2]

RECORD_ENV = "DEV_KNOWLEDGE_HOOK_WATCHDOG_LOG"
RECORD_RELPATH = Path("logs") / "HOOK-WATCHDOG-KILLS.jsonl"

#: How long a candidate must show zero CPU movement before it is treated as suspended-at-
#: creation rather than merely a slow start. The incident's own orphans were found aged minutes
#: to 47 h with 0 s CPU throughout, so this errs toward a wide margin over a legitimate but slow
#: interpreter boot (measured 18-22 s, `bounded_hook.HARNESS_HEADROOM_S`) rather than a tight one.
#:
#: HONEST LIMIT: the same wide margin is what protects a genuinely-runnable-but-starved process
#: from a false kill under heavy CPU contention (`tests/test_hook_watchdog.py::test_a_process_
#: whose_cpu_time_is_moving_is_never_a_candidate` needed a 3 s threshold, not this module's own
#: 1 s minimum test bound, to stay deterministic on this repo's own loaded box) -- a process
#: starved of every scheduling quantum for the WHOLE threshold window reads identically to one
#: that never had a thread to schedule at all. Zero CPU movement is the only signal; a shorter
#: threshold trades false-kill risk for faster detection, never the other way round.
DEFAULT_THRESHOLD_S = 30.0

SURFACE_WINDOW_H = 72
_SURFACE_TAIL_LINES = 5000

#: The `[#863]` signature is "0 s CPU" from the moment the process was CREATED, not merely flat
#: during whatever window this sweep happens to sample it in. A process that ran for a while and
#: is now legitimately blocked (I/O, a lock, a long sleep -- `bounded_hook.py`'s OWN "pipe held
#: after exit" mode) has ALREADY accumulated real CPU time by the time `sweep` first samples it,
#: even though that total is flat for the whole `threshold_s` window that follows. Requiring the
#: FIRST sample itself to be near-zero is what tells the two apart (Codex terra review, LANE-5B5-
#: 5-lane-hook-watchdog Critical finding: without this, ANY orphaned process that happens to get
#: no scheduling quantum for one window -- this repo's own box measured that happening to a
#: genuinely busy-looping process under load -- reads identically to one that never ran at all).
#: A small, non-zero allowance rather than an exact `== 0.0`: a genuinely suspended-at-creation
#: process never executes an instruction, so its true CPU time IS zero -- the allowance is for
#: `cpu_times()`'s own measurement granularity, not for any legitimate work the process did.
_NEAR_ZERO_BASELINE_CPU_S = 0.1


# --- candidate detection -----------------------------------------------------------------------

def _candidate_hook_names(settings_path: Path) -> set[str]:
    """Every hook script basename `.claude/settings.json` registers, across every event -- read
    live rather than hardcoded a second time, so a new hook registration is covered for free."""
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    names: set[str] = set()
    for blocks in (settings.get("hooks") or {}).values():
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            if not isinstance(block, dict):
                continue
            for hook in block.get("hooks", []):
                if isinstance(hook, dict):
                    names.update(_SCRIPT_RE.findall(str(hook.get("command", ""))))
    return names


def _is_orphaned(proc: psutil.Process) -> bool:
    """The incident's own "parent shell dead" half -- platform-aware (Codex terra review,
    LANE-5B5-5-lane-hook-watchdog: an EARLIER version checked only `parent() is None`, which
    NEVER holds on POSIX -- a child whose parent exits is reparented to PID 1 (or a configured
    subreaper), not orphaned into a null parent, so that check silently found nothing on Linux
    CI). On Windows, a genuinely dead parent's pid is simply gone (`parent()` returns `None`,
    and `Process.parent()` guards against pid REUSE by checking the candidate's creation time
    predates this process, so a later process reusing the dead parent's pid does not fool it).
    On POSIX, a reparented-to-init process reads `ppid() == 1`; `0` is included for the same
    reason a defensive read never trusts a single sentinel to be the only one an OS ever uses."""
    try:
        if proc.parent() is None:
            return True
        return proc.ppid() in (0, 1)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def _is_candidate(proc: psutil.Process, hook_names: set[str]) -> bool:
    """A live process naming a registered hook script, orphaned (`_is_orphaned`)."""
    try:
        cmdline = " ".join(proc.cmdline())
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False
    if not cmdline or not any(name in cmdline for name in hook_names):
        return False
    return _is_orphaned(proc)


def _cpu_total(proc: psutil.Process) -> float | None:
    try:
        times = proc.cpu_times()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None
    return times.user + times.system


def _cpu_total_tree(proc: psutil.Process) -> float | None:
    """`sweep`'s real signal, root-only was not (integrator repair-1, LANE-5B5-5-lane-hook-
    watchdog): a hook command run through a venv `python.exe` on Windows is a flat-CPU
    LAUNCHER whose child does the real work -- `CreateProcess`s the base interpreter, then
    idles. Sampling `_cpu_total` on the launcher's own pid alone reads a live, working hook as
    motionless from the first sample onward, which is exactly the `[#863]` signature this
    module kills on. Summing CPU across the whole tree (this process plus every descendant) is
    what tells a truly suspended-at-creation process (nothing in its tree ever runs) apart from
    a flat launcher over a busy child. Returns `None` only when the root itself is gone or
    unreadable -- a child that vanishes mid-walk is simply left out of the sum (best-effort,
    the same posture `_session_id_for` and `kill_tree` already take)."""
    total = _cpu_total(proc)
    if total is None:
        return None
    try:
        children = proc.children(recursive=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        children = []
    for child in children:
        child_total = _cpu_total(child)
        if child_total is not None:
            total += child_total
    return total


def _session_id_for(proc: psutil.Process) -> str:
    """Best-effort ONLY, and that is an honest limit rather than a bug: a process created
    suspended never read its own stdin payload (where every OTHER hook surface in this repo --
    `bounded_hook.py`'s `_payload_fields` -- gets a session id from), so the environment block
    (set up at `CreateProcessW` time, independent of whether the thread ever ran) is the one
    channel left. Any env var naming SESSION is taken; `unknown` otherwise."""
    try:
        env = proc.environ()
    except (psutil.NoSuchProcess, psutil.AccessDenied, NotImplementedError, OSError):
        return "unknown"
    for key, value in env.items():
        if "SESSION" in key.upper() and value:
            return value
    return "unknown"


# --- the record ----------------------------------------------------------------------------

def record_path() -> Path:
    override = os.environ.get(RECORD_ENV, "").strip()
    if override:
        return Path(override)
    return primary_root(_REPO_ROOT) / RECORD_RELPATH


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_record(row: dict) -> Path | None:
    path = record_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError:
        return None
    return path


# --- kill ------------------------------------------------------------------------------------

def kill_tree(pid: int) -> None:
    """FIRED, NOT AWAITED on Windows (`taskkill /T` runs on after this returns) -- identical
    posture to `bounded_hook.py::_kill_tree` and for the same reason: a watchdog that waits on
    its own kill has moved the unbounded wait one level down.

    ON POSIX, `.kill()` is a single non-blocking syscall per process (SIGKILL is not caught or
    ignorable, so it is not a wait either): the recursive `children()` walk is a `psutil` read
    of the live process tree (`/proc` on Linux), not a wait on anything the killed processes do.
    A bare `os.kill(pid, 9)` -- an EARLIER version of this function -- kills only the named pid,
    contradicting the whole-tree contract (Codex terra review, LANE-5B5-5-lane-hook-watchdog);
    `bounded_hook.py::_kill_tree`'s own `os.killpg` is not reused here because it depends on the
    target being its own process-group leader (`start_new_session=True` at spawn time), which
    this module does not control -- the process it is killing was created by something else
    entirely (that is the whole point: it never ran a line of its own)."""
    if os.name == "nt":
        try:
            subprocess.Popen(["taskkill", "/T", "/F", "/PID", str(pid)],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        except OSError:
            pass
        return
    try:
        root = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return
    try:
        descendants = root.children(recursive=True)
    except psutil.Error:
        descendants = []
    for proc in (*descendants, root):
        try:
            proc.kill()
        except psutil.Error:
            pass


def _record_kill(proc: psutil.Process, threshold_s: float, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    try:
        cmdline = " ".join(proc.cmdline())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        cmdline = ""
    try:
        age_s = round(time.time() - proc.create_time(), 3)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        age_s = None
    row = {
        "ts": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hook_id": _transcript_hook_id(cmdline) if cmdline else "unknown",
        "pid": proc.pid,
        "age_s": age_s,
        "session_id": _session_id_for(proc),
        "threshold_s": threshold_s,
        "reason": "zero-cpu-after-threshold",
    }
    append_record(row)
    return row


# --- sweep -----------------------------------------------------------------------------------

def sweep(*, threshold_s: float = DEFAULT_THRESHOLD_S,
          settings_path: Path | None = None,
          process_iter=None, sleep=time.sleep, now: datetime | None = None) -> list[dict]:
    """One pass: sample every candidate's CPU time, sleep `threshold_s`, sample again. A
    candidate is the `[#863]` signature -- killed, whole tree, and recorded -- only when BOTH
    hold: its very FIRST sample is already near-zero (`_NEAR_ZERO_BASELINE_CPU_S` -- it never
    ran, not merely "not running just now"), AND that total does not move across the whole
    window. Either alone is not enough (Codex terra review, LANE-5B5-5-lane-hook-watchdog
    Critical finding): a live-then-blocked hook can be flat for one window without ever having
    been suspended-at-creation, and a process with real accumulated CPU is never this module's
    business regardless of what it does next. Returns the kill rows (also durably logged).

    ONE SHARED SLEEP, not one per candidate: every candidate is sampled at t0 before the single
    `threshold_s` sleep, so N candidates cost one wait, not N."""
    settings_path = settings_path or (_REPO_ROOT / ".claude" / "settings.json")
    process_iter = process_iter or (lambda: psutil.process_iter())
    hook_names = _candidate_hook_names(settings_path)
    if not hook_names:
        return []

    baseline: dict[int, tuple[psutil.Process, float]] = {}
    for proc in process_iter():
        try:
            if not _is_candidate(proc, hook_names):
                continue
            cpu0 = _cpu_total_tree(proc)
        except psutil.Error:
            continue
        # The FIRST sample already has to look suspended-at-creation -- see `sweep`'s own
        # docstring and `_NEAR_ZERO_BASELINE_CPU_S`. A candidate that already ran real work is
        # never tracked into the window at all, so it costs nothing in the sleep that follows.
        if cpu0 is not None and cpu0 < _NEAR_ZERO_BASELINE_CPU_S:
            baseline[proc.pid] = (proc, cpu0)
    if not baseline:
        return []

    sleep(threshold_s)

    killed: list[dict] = []
    for pid, (proc, cpu0) in baseline.items():
        cpu1 = _cpu_total_tree(proc)
        if cpu1 is None or cpu1 != cpu0:
            # exited on its own; ran and is still running; OR ran and a child that did the
            # work already exited by t1 -- `_cpu_total_tree` only sums LIVE descendants, so a
            # short-lived busy child dropping out of the walk can make the tree's total FALL
            # between samples (repair-1 gap, agy substitute review High finding). A fall is
            # still movement, and movement of either sign is proof this was never a
            # suspended-at-creation process: only a total that reads bit-identical at both
            # samples is that signature.
            continue
        row = _record_kill(proc, threshold_s, now)
        kill_tree(pid)
        killed.append(row)
    return killed


# --- surface ---------------------------------------------------------------------------------

def surface_lines(window_h: float = SURFACE_WINDOW_H) -> list[str]:
    """SessionStart surfacing: recent kills, never silent. Fail-soft on its own account, like
    every other digest line in `fleet_health.py` -- a surfacing organ never breaks the digest."""
    try:
        raw_lines = record_path().read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=window_h)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    rows = []
    for line in raw_lines[-_SURFACE_TAIL_LINES:]:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and str(row.get("ts", "")) >= cutoff:
            rows.append(row)
    if not rows:
        return []
    report = [f"[hook-watchdog] {len(rows)} suspended-at-creation kill(s) in the last "
              f"{window_h:g} h -- a hook created suspended never ran a line, so no per-hook "
              f"bound could have caught it ([#863]). Record: {record_path()}"]
    for row in rows:
        report.append(f"[hook-watchdog]   {row.get('hook_id')}: pid {row.get('pid')}, age "
                       f"{row.get('age_s')}s, session {row.get('session_id')}, killed "
                       f"{row.get('ts')}")
    return report


# --- CLI -------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="verb", required=True)
    p_sweep = sub.add_parser("sweep", help="one pass: kill and record any suspended-at-"
                                            "creation hook process found now")
    p_sweep.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD_S)
    p_sweep.add_argument("--settings", type=Path,
                         default=_REPO_ROOT / ".claude" / "settings.json")
    p_surface = sub.add_parser("surface", help="print recent kills (SessionStart)")
    p_surface.add_argument("--hours", type=float, default=SURFACE_WINDOW_H)
    args = parser.parse_args(argv)

    if args.verb == "sweep":
        killed = sweep(threshold_s=args.threshold, settings_path=args.settings)
        for row in killed:
            print(f"[hook-watchdog] KILLED {row['hook_id']} pid={row['pid']} "
                  f"age={row['age_s']}s session={row['session_id']}")
        if not killed:
            print("[hook-watchdog] sweep: no suspended-at-creation candidate found")
        return 0
    lines = surface_lines(args.hours)
    if lines:
        sys.stdout.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
