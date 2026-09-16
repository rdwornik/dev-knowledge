#!/usr/bin/env python
"""resource_lifecycle.py -- the LOCAL regime of the runtime-resource organ (`[#792]`).

WHAT THIS IS, AND WHAT IT DELIBERATELY IS NOT
=================================================================================================
The harness has organs for decisions, files, tests, gates and process-as-workflow. **Nothing
owns runtime resources** -- who may allocate them, for how long, what reclaims them, and what
refuses when the budget is gone. `QR-RES-001` records the sharpest form of that gap: the quality
attribute the operator described as the least discretionary ("automatic arithmetic, not a
judgement call") is the one with no organ at all. `scripts/seat_refusals.py` carries
`lane-ceiling`, which is ADR-110's 4-6 lane COUNT and reads no memory; `--check-worktrees` reads
the live worktree list, also a count. **Nothing in the tree reads free memory before a dispatch.**

This module is the LOCAL half of that organ, and `scripts/context_reclamation.py` is a DIFFERENT
mechanism in a different file. That separation is the whole design and it is not tidiness:

    per-turn COST is driven by accumulated TURN COUNT   -> context reclamation
    process MEMORY is driven by session AGE             -> session replacement

Measured 2026-09-15 and recorded in `docs/audits/2026-09-15-technical-lane-aa-14-resource-
lifecycle.md`. Cost moves 0.701 -> 1.247 x own median across turn-index bands but only
0.915 -> 1.003 across an eight-fold ELAPSED spread once turn index is held; RSS moves
255.6 MB (< 0.5 h) -> 383.0 MB (0.5-1 h) with r = 0.440. **Clearing context does not free
process memory, and retiring a session to reclaim cost throws away a cache that was not the
problem.** Building one mechanism for both is why neither works today.

AND THE TWO REGIMES ARE NOT ONE RESOURCE. Local is a fixed ceiling you allocate against; cloud
is a meter you run down. This module therefore declares NO cloud-regime threshold at all -- a
property `tests/test_resource_lifecycle.py` asserts rather than a convention, because a constant
tuned for one regime is wrong for the other however sensible its value.

LIBRARY-FIRST CHECK (recorded, per CLAUDE.md section 4)
=================================================================================================
`psutil` is the obvious dependency for a process table and it is NOT used. Two reasons, in the
order the rule asks them: stdlib first -- `subprocess` plus the platform's own process query
answers every question this module asks -- and the global rule "no new deps without
confirmation", which makes adding `psutil` an operator act rather than a lane's. If a later
lane has that confirmation, `process_table()` is the one function to replace and nothing else
in this module needs to change.

WHAT IS DERIVED AND WHAT IS NOT
=================================================================================================
`THRESHOLD_PROVENANCE` below carries one entry per threshold, and a test refuses a threshold
with no entry. Read it before citing any number from here. The short version: the lifetime
bound and the merge bound are derived from this repo's own measurements; **the RSS bound is
NOT properly derived and says so** -- it is a cross-sectional plateau from a single snapshot of
31 different processes, not a longitudinal trace of one process over its life. `sample` exists
to replace it. A sampler with no history supports no threshold, and none is claimed.

CALL SURFACE
=================================================================================================

    uv run --locked python scripts/resource_lifecycle.py session-start   # the hook leg
    uv run --locked python scripts/resource_lifecycle.py ceiling
    uv run --locked python scripts/resource_lifecycle.py admit          # exit 1 = REFUSED
    uv run --locked python scripts/resource_lifecycle.py sample
    uv run --locked python scripts/resource_lifecycle.py retire --pid N
    uv run --locked python scripts/resource_lifecycle.py teardown --pid N
"""
from __future__ import annotations

import ctypes
import json
import logging
import math
import os
import platform
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Sequence

import click

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("resource-lifecycle")

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent

_IS_WINDOWS = platform.system() == "Windows"

#: The append-only sampler ledger, and it lives OUTSIDE THE REPO.
#:
#: Three reasons, in the order they decided it. (1) A SessionStart hook writes this file on
#: every session, and an artifact a hook writes must never dirty the tree it reports on -- the
#: repo's own `logs/FLEET-HEALTH.md` and `logs/ENFORCEMENT-COVERAGE.md` carry that rule as
#: `.gitignore` entries. (2) The measurement is OF THIS BOX: an RSS-vs-age curve mixed across
#: two machines is one meaningless line, so a per-box history is the right scope and a shared
#: one is actively wrong. (3) It sits beside the data it complements -- the transcripts under
#: `~/.claude/projects/` that the cost half of this lane's derivation reads.
#:
#: The route NOT taken, recorded so it is not re-tried: an in-repo `logs/` home plus a
#: `.gitignore` entry. `scripts/logs_retention.py` would relocate a DATED file into
#: `logs/YYYY-MM/`, whose ignore patterns are `.md`-only, so a relocated `.jsonl` lands
#: untracked and leaves the tree permanently dirty, and `validate_hermetization` then refuses
#: that home as unallowlisted -- `[#785]` records the two organs disagreeing. An undated name
#: sidesteps retention, but the `.gitignore` edit itself is UNCLAIMABLE by `graph-task-coverage`
#: (measured here): `file_purpose_graph._REL_PATH_RE` requires a `/` in a path token, so a row
#: body cannot name a root dotfile, and root files are outside `IMPLEMENTS_SCAN_DIRS`, so the
#: file cannot name the row either. Neither direction of the `implements` edge can exist.
SAMPLE_LEDGER_PATH = Path.home() / ".claude" / "resource-samples.jsonl"

#: The process name a seat runs under on this box.
SEAT_PROCESS_NAME = "claude"


# ================================================================== the thresholds, LOCAL regime

#: Memory held back from the budget entirely, so the box has somewhere to breathe.
RESERVE_GB = 3.0
#: What one SEAT costs. A seat is not a process -- see `count_seats`.
PER_SEAT_MB = 413.3
#: Above this age a seat is retired and re-booted.
LIFETIME_HOURS = 4.0
#: Above this resident size a seat is retired.
RSS_PLATEAU_MB = 385.0
#: Above this many merges an integrator seat is retired.
MERGE_COUNT_BOUND = 5
#: The resident size that separates a session process from its helper.
HEAVY_FLOOR_MB = 200.0

#: WHAT EACH THRESHOLD MEASURES, as a declared unit rather than as a suffix a reader infers.
#: `tests/test_context_reclamation.py` asserts this map and the reclamation module's are
#: DISJOINT -- that is the checkable form of "the two regimes are not one resource". Units are
#: the right test and equal VALUES are not: `MERGE_COUNT_BOUND` (5, the batch merge median) and
#: the reclamation module's `SUSTAINED_TURNS` (5, the run length its fire-rate table was
#: computed with) are independently derived from different data and coincide by accident.
#: Forcing either off 5 to break the collision would break its derivation, which is a worse
#: outcome than the coincidence. What must never happen is the two modules both declaring a
#: threshold in, say, gigabytes -- and that is what a disjoint-units assertion catches.
THRESHOLD_UNITS: dict[str, str] = {
    "RESERVE_GB": "gigabytes-of-memory",
    "PER_SEAT_MB": "megabytes-of-memory",
    "LIFETIME_HOURS": "hours-of-process-age",
    "RSS_PLATEAU_MB": "megabytes-of-memory",
    "MERGE_COUNT_BOUND": "merges-landed",
    "HEAVY_FLOOR_MB": "megabytes-of-memory",
}

#: EVERY threshold above, with the measurement behind it or the admission that there is none.
#: `tests/test_resource_lifecycle.py` refuses a threshold missing from here. The point is not
#: documentation -- it is that a number nobody can trace is a number somebody picked, and this
#: repo's recorded failure mode is a chosen constant dressed as a measurement.
THRESHOLD_PROVENANCE: dict[str, str] = {
    "RESERVE_GB": (
        "CARRIED, NOT DERIVED. 3.0 GB is the frozen contract's own figure and this lane did "
        "not re-derive it; it is recorded as carried so a later reader does not cite it as a "
        "measurement of ours. What supports it circumstantially: the OOM-killed full-suite "
        "attempts and the OOM-killed merge (job 9b8de937, batch Z) both happened at roughly "
        "1.4-1.6 GB free, so a reserve below ~2 GB is demonstrably too small on this box."
    ),
    "PER_SEAT_MB": (
        "MEASURED 2026-09-15T12:33Z. 62 live claude processes split EXACTLY 31 heavy / 31 "
        "light -- one session process (mean 287.0 MB) plus one helper (mean 126.3 MB) per "
        "seat, totalling 413.3 MB. The frozen contract's ~392-400 MB per lane is confirmed "
        "within 5%. A per-PROCESS figure (207.2 MB) would double the ceiling and be wrong."
    ),
    "LIFETIME_HOURS": (
        "DERIVED 2026-09-15 from the RSS-vs-age curve. RSS reaches its plateau inside the "
        "first hour; the 4-8 h band is the first in which the sample thins to n=3 and the "
        "mean falls, i.e. the first band where the population stops being comparable. Below "
        "4 h, 30 of 31 live processes sit on one interpretable curve. A bound is set where "
        "the evidence still supports it. p90 of actual session spans is 7.96 h, so this "
        "retires roughly the top decile. Session spans measured: median 88.0 min, p90 477.3 "
        "min, 8 sessions over 24 h, longest 262.3 h carrying 75 turns."
    ),
    "RSS_PLATEAU_MB": (
        "UNDERIVABLE FROM THE PRESCRIBED DATA, THEN CHOSEN -- and the two halves are stated "
        "separately because they are different kinds of claim. "
        "(1) UNDERIVABLE, and this is a property of the DATA, not a failure of the "
        "derivation. The frozen contract directs that the RSS threshold be computed from "
        "transcripts. It cannot be: NO transcript record type carries any memory field (all "
        "15 types enumerated), so the quantity is simply absent from the corpus. The "
        "contract's fallback proxy -- per-turn latency against own median -- is FALSIFIED, "
        "not merely weak: it is flat to three decimal places from 0-15 min to 480+ min "
        "across 92,743 turns, so there is no rise for a threshold to sit on. Recorded in the "
        "register at QR-PERF-006, struck rather than deleted, so it is not re-prescribed. "
        "(2) CHOSEN. 385 MB is an explicit choice made by batch AA lane aa-14, not a "
        "measurement of the thing it names, and its basis is the CROSS-SECTIONAL plateau of "
        "a single 2026-09-15 snapshot of 31 live processes doing different work. The "
        "weakness of that basis is the reason it is labelled: a snapshot cannot distinguish "
        "'processes grow' from 'older processes are a different population'. It is set where "
        "it is because a bound above the observed plateau would retire nothing and a bound "
        "below it would retire healthy seats mid-lane. "
        "WHAT REPLACES IT: `sample` writes a longitudinal trace to "
        "~/.claude/resource-samples.jsonl; once that has enough history to show a single "
        "process's own curve, this number is re-derived from it and this provenance is "
        "rewritten. A sampler with no history supports no threshold, and none is claimed."
    ),
    "MERGE_COUNT_BOUND": (
        "DERIVED 2026-09-15 from `logs/MERGE-RECEIPTS.jsonl`, and DOMINATED -- which is the "
        "more useful fact. Batches Y and Z ran 5 and 6 merges over 3.83 h and 4.94 h, so a "
        "seat reaching 5 merges has typically been alive about 4 hours and LIFETIME_HOURS "
        "has already tripped. 'Whichever trips first' therefore resolves to lifetime at our "
        "measured merge rate. The leg is kept because the rate is not a law: a fast batch "
        "would reach 5 merges inside the lifetime bound, and this is the leg that catches it."
    ),
    "HEAVY_FLOOR_MB": (
        "MEASURED 2026-09-15. The 62-process population is sharply bimodal: the light class "
        "tops out at 161.6 MB and the heavy class starts at 246.9 MB. 200 MB sits in the "
        "empty gap between them, so the split is read off the data rather than chosen. If a "
        "future sample fills that gap the constant is wrong and `count_seats` needs a "
        "different discriminator -- a parent/child link rather than a size."
    ),
}


# ============================================================================ the process table

@dataclass(frozen=True)
class Proc:
    """One process, in a shape that is the same on every platform."""

    pid: int
    ppid: int
    rss_bytes: int
    age_seconds: float
    name: str

    @property
    def rss_mb(self) -> float:
        return self.rss_bytes / (1024 * 1024)

    @property
    def age_hours(self) -> float:
        return self.age_seconds / 3600.0


def _windows_process_table() -> list[Proc]:
    """Win32_Process via PowerShell. One call, not one per pid."""
    script = (
        "Get-CimInstance Win32_Process | "
        "Select-Object ProcessId,ParentProcessId,WorkingSetSize,CreationDate,Name | "
        "ConvertTo-Json -Compress -Depth 2"
    )
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True, text=True, timeout=120,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    try:
        rows = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    if isinstance(rows, dict):
        rows = [rows]
    now = datetime.now(timezone.utc)
    table: list[Proc] = []
    for row in rows:
        pid = row.get("ProcessId")
        if not isinstance(pid, int):
            continue
        created = row.get("CreationDate")
        age = 0.0
        if isinstance(created, str):
            # ConvertTo-Json renders a CIM datetime as `/Date(1789…)/` epoch milliseconds.
            digits = "".join(ch for ch in created if ch.isdigit() or ch == "-")
            if digits.lstrip("-").isdigit():
                try:
                    started = datetime.fromtimestamp(int(digits) / 1000.0, tz=timezone.utc)
                    age = max(0.0, (now - started).total_seconds())
                except (ValueError, OSError, OverflowError):
                    age = 0.0
        name = str(row.get("Name") or "")
        table.append(Proc(
            pid=pid,
            ppid=int(row.get("ParentProcessId") or 0),
            rss_bytes=int(row.get("WorkingSetSize") or 0),
            age_seconds=age,
            name=name[:-4] if name.lower().endswith(".exe") else name,
        ))
    return table


def _posix_process_table() -> list[Proc]:
    """`ps` in a fixed, parseable column order. `etimes` is elapsed SECONDS, not a clock."""
    proc = subprocess.run(
        ["ps", "-eo", "pid=,ppid=,rss=,etimes=,comm="],
        capture_output=True, text=True, timeout=120,
    )
    if proc.returncode != 0:
        return []
    table: list[Proc] = []
    for line in proc.stdout.splitlines():
        parts = line.split(None, 4)
        if len(parts) < 5:
            continue
        pid, ppid, rss_kb, etimes, comm = parts
        try:
            table.append(Proc(
                pid=int(pid), ppid=int(ppid),
                rss_bytes=int(rss_kb) * 1024,       # ps reports RSS in KiB
                age_seconds=float(etimes), name=comm.strip(),
            ))
        except ValueError:
            continue
    return table


def process_table() -> list[Proc]:
    """Every process on this box. The ONE platform seam in this module."""
    return _windows_process_table() if _IS_WINDOWS else _posix_process_table()


# ============================================================================ liveness and kills

_STILL_ACTIVE = 259
_PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


def pid_is_alive(pid: int) -> bool:
    """True while `pid` names a live process.

    NOT `os.kill(pid, 0)`. On Windows that call maps onto `TerminateProcess(handle, 0)` and
    would KILL the process it was asked about -- a liveness probe that kills is the worst
    possible shape for a teardown verifier. The Windows arm therefore opens a query-only
    handle and reads the exit code.

    HONEST LIMIT: a Windows process that legitimately exits with code 259 reads as alive
    here. 259 is `STILL_ACTIVE` and the API cannot distinguish the two cases; nothing in this
    repo exits 259 deliberately, and the alternative (treating 259 as dead) would report a
    running process reaped, which is the more dangerous error.
    """
    if pid <= 0:
        return False
    if _IS_WINDOWS:
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle = kernel32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return False
        try:
            code = ctypes.c_ulong()
            ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
            return bool(ok) and code.value == _STILL_ACTIVE
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True          # exists, is not ours -- still alive for our purposes
    # A zombie answers signal 0 while being dead for every purpose a teardown cares about.
    status = Path(f"/proc/{pid}/stat")
    if status.is_file():
        try:
            fields = status.read_text().rsplit(")", 1)[-1].split()
            if fields and fields[0] == "Z":
                return False
        except OSError:
            pass
    return True


def naive_kill(pid: int) -> None:
    """Kill exactly ONE process and nothing else.

    This is the WRONG verb for a teardown and it exists so the wrong verb has a name: it is
    what `tests/test_resource_lifecycle.py` uses to reproduce the defect -- a grandchild that
    outlives its parent's death. Upstream confirms the reparenting; we measured it twice
    (`QR-AVAIL-004`, `QR-AVAIL-005`). Callers wanting a teardown want `teardown_tree`.
    """
    if pid <= 0:
        return
    if _IS_WINDOWS:
        subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                       capture_output=True, text=True, timeout=60)
        return
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def tree_pids(root_pid: int, table: Optional[Sequence[Proc]] = None) -> tuple[int, ...]:
    """`root_pid` and every transitive descendant, deepest LAST.

    THE SNAPSHOT IS THE MECHANISM. This walk must happen while the parent is still alive: on
    POSIX an orphan is reparented to init the instant its parent dies, so a walk taken after
    the root is killed finds nothing and a teardown built that way reaps nothing while
    reporting success. `tests/test_resource_lifecycle.py::
    test_teardown_snapshots_the_tree_before_killing_the_root` pins the ordering.
    """
    rows = list(table) if table is not None else process_table()
    children: dict[int, list[int]] = {}
    for proc in rows:
        children.setdefault(proc.ppid, []).append(proc.pid)
    ordered: list[int] = []
    frontier = [root_pid]
    seen = {root_pid}
    while frontier:
        ordered.extend(frontier)
        nxt: list[int] = []
        for pid in frontier:
            for child in children.get(pid, ()):
                if child not in seen:
                    seen.add(child)
                    nxt.append(child)
        frontier = nxt
    return tuple(ordered)


@dataclass(frozen=True)
class TeardownResult:
    """What a teardown ACTUALLY did, including what it failed to do."""

    root: int
    targeted: tuple[int, ...]
    killed: tuple[int, ...]
    survivors: tuple[int, ...]

    @property
    def clean(self) -> bool:
        return not self.survivors


def teardown_tree(root_pid: int, timeout_s: float = 30.0,
                  table: Optional[Sequence[Proc]] = None) -> TeardownResult:
    """Kill the whole process TREE and VERIFY the kill rather than assuming it.

    Three properties, each of which a naive implementation loses:

      1. THE TREE IS SNAPSHOT FIRST (see `tree_pids`).
      2. DESCENDANTS DIE BEFORE THE ROOT. Killing the root first lets a child spawn another
         child in the window before its own kill arrives.
      3. THE RESULT REPORTS SURVIVORS. `QR-AVAIL-004`'s metric is "processes surviving a
         teardown: 0", which is only checkable if the teardown says who survived. A teardown
         that returns None has asserted nothing, and the 53-hour orphan it would have missed
         was found by a human looking rather than by a check.
    """
    targeted = tree_pids(root_pid, table=table)
    for pid in reversed(targeted):          # deepest first
        naive_kill(pid)

    deadline = time.time() + timeout_s
    survivors = [pid for pid in targeted if pid_is_alive(pid)]
    while survivors and time.time() < deadline:
        time.sleep(0.1)
        for pid in survivors:
            naive_kill(pid)
        survivors = [pid for pid in survivors if pid_is_alive(pid)]

    killed = tuple(pid for pid in targeted if pid not in survivors)
    return TeardownResult(root=root_pid, targeted=targeted,
                          killed=killed, survivors=tuple(survivors))


# ================================================================================== allocation

@dataclass(frozen=True)
class Allocation:
    """The ceiling as ARITHMETIC over live readings, never as a stored integer.

    A ceiling re-derived per batch drifts; a ceiling typed into prose is stale at the next
    commit and is one a seat can not-read. This dataclass is the third option: the inputs are
    recorded, the ceiling is computed from them every time, and it MOVES when the box does.
    """

    total_gb: float
    free_gb: float
    claude_gb: float
    nonclaude_gb: float
    reserve_gb: float
    budget_gb: float
    per_seat_mb: float
    ceiling: int


def allocation(total_gb: Optional[float] = None, claude_gb: Optional[float] = None,
               free_gb: Optional[float] = None, per_seat_mb: float = PER_SEAT_MB,
               reserve_gb: float = RESERVE_GB,
               table: Optional[Sequence[Proc]] = None) -> Allocation:
    """The ceiling, computed. Any argument left None is READ FROM THE BOX."""
    if total_gb is None or free_gb is None or claude_gb is None:
        rows = list(table) if table is not None else process_table()
        measured_total, measured_free = _memory_gb()
        total_gb = measured_total if total_gb is None else total_gb
        free_gb = measured_free if free_gb is None else free_gb
        if claude_gb is None:
            claude_gb = sum(p.rss_bytes for p in rows
                            if p.name.lower() == SEAT_PROCESS_NAME) / (1024 ** 3)
    nonclaude_gb = max(0.0, total_gb - claude_gb - free_gb)
    budget_gb = max(0.0, total_gb - nonclaude_gb - reserve_gb)
    per_seat_gb = per_seat_mb / 1024.0
    ceiling = int(math.floor(budget_gb / per_seat_gb)) if per_seat_gb > 0 else 0
    return Allocation(total_gb=total_gb, free_gb=free_gb, claude_gb=claude_gb,
                      nonclaude_gb=nonclaude_gb, reserve_gb=reserve_gb,
                      budget_gb=budget_gb, per_seat_mb=per_seat_mb, ceiling=ceiling)


def _memory_gb() -> tuple[float, float]:
    """(total, free) in GB, from the platform."""
    if _IS_WINDOWS:
        script = ("$o=Get-CimInstance Win32_OperatingSystem;"
                  "\"$($o.TotalVisibleMemorySize) $($o.FreePhysicalMemory)\"")
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True, text=True, timeout=60)
        parts = proc.stdout.split()
        if len(parts) == 2:
            try:                      # both are KiB
                return int(parts[0]) / (1024 ** 2), int(parts[1]) / (1024 ** 2)
            except ValueError:
                pass
        return 0.0, 0.0
    total = free = 0
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                total = int(line.split()[1])
            elif line.startswith("MemAvailable:"):
                free = int(line.split()[1])
    except OSError:
        return 0.0, 0.0
    return total / (1024 ** 2), free / (1024 ** 2)


@dataclass(frozen=True)
class AdmissionVerdict:
    admitted: bool
    reason: str


def admit(alloc: Allocation, live_seats: int) -> AdmissionVerdict:
    """May another LOCAL seat be dispatched? **A refusal, not a report.**

    BOTH LEGS ARE REPORTED, not just the first that fires, and that is deliberate. A seat
    refused on its count that was ALSO out of reserve looks, from a one-leg message, like a
    box that merely has too many lanes -- and the operator's next move (wait for one to
    finish) is wrong for the second condition. The 2026-09-15 reading was over on both.
    """
    breaches: list[str] = []
    if alloc.free_gb < alloc.reserve_gb:
        breaches.append(
            f"free memory {alloc.free_gb:.2f} GB is below the {alloc.reserve_gb:.2f} GB "
            f"reserve")
    if live_seats >= alloc.ceiling:
        breaches.append(
            f"{live_seats} live seats against a computed ceiling of {alloc.ceiling} "
            f"({alloc.budget_gb:.2f} GB budget / {alloc.per_seat_mb:.1f} MB per seat; "
            f"{alloc.nonclaude_gb:.2f} GB held by non-Claude)")
    if breaches:
        return AdmissionVerdict(False, "REFUSED: " + "; and ".join(breaches))
    return AdmissionVerdict(
        True,
        f"admitted: {live_seats} of {alloc.ceiling} seats, {alloc.free_gb:.2f} GB free "
        f"against a {alloc.reserve_gb:.2f} GB reserve")


def count_seats(table: Sequence[Proc], name: str = SEAT_PROCESS_NAME) -> int:
    """SEATS, not processes.

    Measured 2026-09-15: 62 claude processes are 31 seats -- one session process plus one
    helper each, an exact split. Counting processes doubles the apparent load and halves the
    apparent ceiling, and the two errors do not cancel.
    """
    return sum(1 for p in table
               if p.name.lower() == name and p.rss_mb >= HEAVY_FLOOR_MB)


# ================================================================== session replacement (retire)

@dataclass(frozen=True)
class RetirementVerdict:
    retire: bool
    tripped: tuple[str, ...]
    detail: str


def retirement_verdict(rss_mb: float, age_hours: float, merges: int) -> RetirementVerdict:
    """Retire and re-boot on RSS, wall-clock lifetime, or merge count -- whichever trips first.

    THIS INVERTS A STANDING PRACTICE AND SAYS SO. Long sessions were kept because "context is
    expensive to rebuild". Given that the memory growth is time-based rather than
    context-based, a long session is the WORST available shape and a restart repairs it. **It
    is a performance requirement, not hygiene** -- "a fresh seat at the start of a wave" was
    written three times and enforced zero times, and prose is what a rule looks like when it
    is not a mechanism.

    EVERY TRIPPED LEG IS REPORTED even though the first one decides the action: a seat retired
    on lifetime that was also over on RSS is a different fact from one that was merely old,
    and collapsing them loses the signal that would re-derive the thresholds.
    """
    tripped: list[str] = []
    if rss_mb >= RSS_PLATEAU_MB:
        tripped.append("rss")
    if age_hours >= LIFETIME_HOURS:
        tripped.append("lifetime")
    if merges >= MERGE_COUNT_BOUND:
        tripped.append("merges")
    detail = (f"rss {rss_mb:.1f} MB / {RSS_PLATEAU_MB:.0f}; "
              f"age {age_hours:.2f} h / {LIFETIME_HOURS:.1f}; "
              f"merges {merges} / {MERGE_COUNT_BOUND}")
    return RetirementVerdict(bool(tripped), tuple(tripped), detail)


# ========================================================================================= sample

def sample(ledger_path: Optional[Path] = None,
           table: Optional[Sequence[Proc]] = None,
           name: str = SEAT_PROCESS_NAME) -> list[dict]:
    """Append one row per seat process to the longitudinal ledger.

    THIS IS THE ONLY THING THAT CAN EVER REPLACE `RSS_PLATEAU_MB` WITH A REAL FIGURE. Today
    that threshold rests on one cross-sectional snapshot, which cannot tell "processes grow"
    from "older processes are a different population". Following the SAME pid across its own
    life can. Append-only in the ADR-29/39 sense: a row is added and no earlier row is ever
    rewritten, because a rewritten history is not a history.
    """
    rows_in = list(table) if table is not None else process_table()
    path = Path(ledger_path) if ledger_path else SAMPLE_LEDGER_PATH
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out: list[dict] = []
    for proc in rows_in:
        if proc.name.lower() != name:
            continue
        out.append({
            "sampled": now,
            "pid": proc.pid,
            "ppid": proc.ppid,
            "rss_mb": round(proc.rss_mb, 1),
            "age_hours": round(proc.age_hours, 4),
            "seat_class": "session" if proc.rss_mb >= HEAVY_FLOOR_MB else "helper",
        })
    if out:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as fh:
            for row in out:
                fh.write(json.dumps(row, sort_keys=True) + "\n")
    return out


# ============================================================================================ CLI

@click.group()
def cli() -> None:
    """The LOCAL regime of the runtime-resource organ ([#792])."""


@cli.command("ceiling")
def cmd_ceiling() -> None:
    """Print the allocation arithmetic with its inputs."""
    table = process_table()
    alloc = allocation(table=table)
    seats = count_seats(table)
    click.echo(f"total          {alloc.total_gb:8.2f} GB")
    click.echo(f"free           {alloc.free_gb:8.2f} GB")
    click.echo(f"claude         {alloc.claude_gb:8.2f} GB")
    click.echo(f"non-Claude     {alloc.nonclaude_gb:8.2f} GB")
    click.echo(f"reserve        {alloc.reserve_gb:8.2f} GB")
    click.echo(f"budget         {alloc.budget_gb:8.2f} GB")
    click.echo(f"per seat       {alloc.per_seat_mb:8.1f} MB")
    click.echo(f"CEILING        {alloc.ceiling:8d} seats")
    click.echo(f"live seats     {seats:8d}")


@cli.command("admit")
@click.option("--seats", type=int, default=None,
              help="Live seat count; read from the box when omitted.")
def cmd_admit(seats: Optional[int]) -> None:
    """REFUSE (exit 1) when another local seat would breach the budget."""
    table = process_table()
    alloc = allocation(table=table)
    live = count_seats(table) if seats is None else seats
    verdict = admit(alloc, live)
    click.echo(verdict.reason)
    if not verdict.admitted:
        sys.exit(1)


@cli.command("sample")
@click.option("--ledger", type=click.Path(path_type=Path), default=None)
def cmd_sample(ledger: Optional[Path]) -> None:
    """Append one longitudinal sample of every seat process."""
    rows = sample(ledger_path=ledger)
    click.echo(f"sampled {len(rows)} seat process(es) -> {ledger or SAMPLE_LEDGER_PATH}")


@cli.command("retire")
@click.option("--pid", type=int, required=True)
@click.option("--merges", type=int, default=0)
def cmd_retire(pid: int, merges: int) -> None:
    """Should this seat be retired? Exit 1 when it should."""
    match = next((p for p in process_table() if p.pid == pid), None)
    if match is None:
        click.echo(f"pid {pid} is not running")
        sys.exit(2)
    verdict = retirement_verdict(match.rss_mb, match.age_hours, merges)
    click.echo(f"{'RETIRE' if verdict.retire else 'keep'} pid {pid}: {verdict.detail}")
    if verdict.tripped:
        click.echo(f"tripped: {', '.join(verdict.tripped)}")
    if verdict.retire:
        sys.exit(1)


@cli.command("session-start")
def cmd_session_start() -> None:
    """The SessionStart leg: SURFACE the allocation, and take one longitudinal sample.

    TWO JOBS IN ONE HOOK ENTRY, because a session start is the one moment that is both.
    A new session IS a seat allocation, so it is when the arithmetic is worth reading; and
    it is a free, regular tick for the sampler whose history is the only thing that can ever
    replace `RSS_PLATEAU_MB`'s cross-sectional provenance with a real one.

    IT SURFACES AND DOES NOT REFUSE, and that is a property of the hook type rather than a
    softening. A `SessionStart` hook cannot stop a session -- measured; only `PreToolUse`
    can -- so a refusal written here would be declared enforcement without enforcement, the
    exact shape `QR-RES-004` records. **The refusal lives in the `admit` verb**, which exits
    1 and which a dispatcher runs BEFORE spending a seat. This leg makes the number visible
    so that nobody has to remember to look.

    FAIL-SOFT IN FULL. A session must never fail to start because a reporter could not read
    a process table.
    """
    try:
        table = process_table()
        alloc = allocation(table=table)
        seats = count_seats(table)
        verdict = admit(alloc, seats)
        click.echo(
            f"[resource] {seats} seat(s) / ceiling {alloc.ceiling} · "
            f"{alloc.free_gb:.2f} GB free / {alloc.reserve_gb:.1f} GB reserve · "
            f"{alloc.claude_gb:.2f} GB claude, {alloc.nonclaude_gb:.2f} GB other")
        if not verdict.admitted:
            click.echo(f"[resource] {verdict.reason}")
            click.echo("[resource] this leg SURFACES; the refusal is "
                       "`resource_lifecycle.py admit`, which exits 1")
        sample(table=table)
    except Exception as exc:  # noqa: BLE001 -- a reporter never blocks a session start
        click.echo(f"[resource] surfacing skipped: {type(exc).__name__}: {exc}")


@cli.command("teardown")
@click.option("--pid", type=int, required=True)
@click.option("--timeout", type=float, default=30.0)
def cmd_teardown(pid: int, timeout: float) -> None:
    """Kill the whole process TREE and report survivors. Exit 1 if any survived."""
    result = teardown_tree(pid, timeout_s=timeout)
    click.echo(f"targeted {len(result.targeted)}: {result.targeted}")
    click.echo(f"killed   {len(result.killed)}")
    if result.survivors:
        click.echo(f"SURVIVORS {result.survivors}")
        sys.exit(1)
    click.echo("clean -- no survivor")


if __name__ == "__main__":
    cli()
