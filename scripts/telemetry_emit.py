#!/usr/bin/env python
"""telemetry_emit.py -- [#529] Stage-1 telemetry EMIT library. Library only; no call sites.

WHAT THIS IS. The write half of telemetry v1, exactly as specified by the landed memo
`docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md` (Stage 1) and the
`[#529]` row that owns it. Three event types, one append-only SQLite table in WAL mode, one
`emit_event()` helper. Nothing more: the memo's Stage 2 (`test_run`, `mutation_run`,
`dep_scan`) and Stage 3 (the `dispatch report` / Datasette read surfaces) are later slices,
and the memo's own instruction for Stage 1 is "Ship nothing else yet."

WHAT THIS IS NOT, and this is the load-bearing scope line: **it wires nothing.** No check, no
hook, no dispatcher calls into this module yet. Wiring the call sites is an explicitly owed
phase-3 step, and the surface that step consumes is the CALL SURFACE section below. A grep
for `telemetry_emit` outside this file and its test is expected to return nothing today; that
is the state of the slice, not a defect in it.

LAYER-2 POSTURE (ADR-28/36, CLAUDE.md rule 4). This module WRITES, which the "read-only
validators only" invariant is worth reading against. The barred class is orchestration that
drives state in child repos; a local ephemeral artifact under `logs/` is an established
in-repo pattern with four live instances -- `logs/FLEET-HEALTH.md` (fleet_health.py),
`logs/ENFORCEMENT-COVERAGE.md` (enforcement_coverage.py), `logs/COHERENCE-NUDGE.log`
(coherence_nudge.py) and `logs/PARITY-EVENTS.jsonl`. This store joins that class: one local
file, never committed, never touching a sibling repo.

WHY SQLITE AND NOT JSONL. Memo line 52: "Start with SQLite in WAL mode as the event store,
not raw JSONL ... Set journal_mode=WAL, synchronous=NORMAL, busy_timeout=5000." The reason
those three pragmas are in the row's Done-when and in `WAL_PRAGMAS` below is concurrency:
pre-commit hooks, pre-push hooks and parallel agent lanes write this store at the same time,
and per SQLite's WAL documentation (quoted in the memo, line 15) "readers do not block
writers and a writer does not block readers."

STRUCTLOG IS OPTIONAL HERE, DELIBERATELY. The memo (line 54) and the `[#529]` row both name
structlog for the emit helper, and it stays the preferred backend -- but it is NOT a declared
dependency of this repo (absent from `pyproject.toml` `[dependency-groups]` and from
`uv.lock`). So the structured-log side-channel binds structlog WHEN IMPORTABLE and otherwise
falls back to the option the memo itself names as the least-deps fallback on the same line:
stdlib `logging` emitting one JSON object per event. `logger_backend()` reports which is live,
so a caller never has to guess. The durable record is the SQLite row either way, and no event
is lost by the fallback.

  RULED AND MEASURED -- `[#529]` leg 3, ruling R6(a) ("stdlib logging unless a MEASURED gap on
  this repo demands structlog; record the measurement or its absence either way"). Measured
  here 2026-08-21, Windows 11, CPython 3.12, per event, N=5000 for the side-channel legs and
  N=300 for the store leg:

      store leg (connect + insert + commit)   16364.92 us   98.5% of one emit
      side-channel `_log_event`                 480.60 us    2.9%
        - of which: failed `import structlog`  ~471    us
        - of which: `json.dumps(row)`             8.85 us
        - of which: `logger.info(...)`            0.37 us

  THE DECISION IS STDLIB, and the measurement is the reason rather than a shrug: the gap it
  found does not favour structlog, it favours not ASKING for structlog per event. A failed
  import is not cached (`sys.modules` records successes only), so the old per-call `try: import
  structlog` re-walked `sys.path` on every event and cost 50x the logging it guarded. Resolving
  the backend once removes that without adding a dependency -- which is what "library-first"
  buys here. Re-measured after the change, same host, same script: `_log_event` 480.60 us ->
  **9.79 us**, a 49x drop landing where the components predict (8.32 + 0.38). structlog is
  therefore NOT declared: no measured gap demands it, and P0 "no new deps without confirmation"
  is not spent on a side-channel that now costs 9.79 us against a 16.4 ms store write.

  REPORTED, NOT FIXED, because it is outside this row's four legs: that 16.4 ms store leg is
  98.5% of an emit, and `audit.py health` emits one `check_run` per check. A connection opened
  and torn down per event is the cause. Left to the operator as a candidate rather than
  redesigned here.

NO INDEX ON (event_type, ts) -- also deliberate. The memo puts that index behind an explicit
threshold (line 141: "If the event log exceeds millions of rows or query latency degrades ->
add indexes on (event_type, ts)"). Adding it now would be building against a condition that
does not hold.

===============================================================================
CALL SURFACE -- what the phase-3 wiring step consumes
===============================================================================

    from telemetry_emit import emit_check_run, emit_hook_run, emit_blocker_fired

    emit_check_run("journal_spine_anchor", "pass", duration_ms=812)
    emit_hook_run("block-unanchored-push", "block", duration_ms=44)
    emit_blocker_fired("block-unanchored-push", reason="range carries 3 unanchored entries")

Every emitter returns the new row id (`int`). Every emitter accepts:

  * `context`   -- a JSON-serializable mapping, stored as `context_json`. The memo's freeform
                   disambiguation field (line 38).
  * `db_path`   -- override the store location. Defaults to `default_db_path()`.
  * `ts`        -- override the timestamp (tests and replay only; defaults to now, UTC).
  * `run_id`    -- override the correlation id. Defaults to `current_run_id()`.

CORRELATION -- `run_id` ([#565]). Every event carries one, and it is the field that makes the
store readable at all: `check_run` rows from two concurrent gate runs in two worktrees land
interleaved in ONE store, and without a correlation column a reader either re-derives the
grouping from timestamps (wrong the moment two runs overlap, which is this repo's normal state)
or gets rebuilt. `current_run_id()` resolves it once per process and EXPORTS it, so a runner and
everything it spawns share one id while two independent runners do not. Its honest limit --
siblings under one `pre-commit` do not share an id -- is stated on that function, and it bounds
what a read path is allowed to claim a run_id means. Scope here is the field and its plumbing
only; no consumer, no query, no dashboard (the row is explicit that those are the read-path
lane's, and that lane's row is filed after this one).

Programming errors raise (`TelemetryError` and its subclasses). A wiring site that must never
break its host gate wraps the call in `safe_emit()`, which swallows store/IO failures and
returns `None` -- telemetry is never worth failing a commit over.

    from telemetry_emit import safe_emit, emit_check_run
    safe_emit(emit_check_run, "no_ff_merges", "pass")

Reading back is `sqlite3` and SQL; this module owns no read surface (memo Stage 3).

THE THREE BINDING CONSTRAINTS also live on that surface, and each is enforced by a REFUSAL
rather than by a convention a wiring site could forget:

    emit_check_run("commit_cadence", "pass", git_derived=True)   # refuses on a shallow clone
    emit_check_run("doc_code_edge", "pass", coverage=None)       # context coverage="unknown"
    emit_check_run("fleet_parity", "pass", skipped=3)            # context carries capabilities

  1. GIT-DERIVED METRICS REFUSE ON A SHALLOW CLONE. `git_derived=True` runs
     `git rev-parse --is-shallow-repository` first and raises `ShallowRepositoryRefusal`
     unless the answer is `false`; nothing is written. A truncated history yields a number
     that looks measured and is wrong, which is worse than no number at all. "Cannot
     determine" refuses too -- an unverifiable provenance claim is not a verified one.
  2. UNRESOLVED COVERAGE IS `"unknown"`, NEVER `0`. Pass `coverage=None` when the signal's
     only evidence is a non-call reference; it stores the string `"unknown"`. `coverage=0`
     stays available and means a MEASURED zero. Putting a raw `coverage` key in `context`
     is refused, because from a raw `0` a reader cannot tell the two apart -- which is the
     whole defect.
  3. SKIP COUNTS CARRY THE HOST CAPABILITY VECTOR. Pass `skipped=<n>`; the event gains
     `capabilities` -- git / grep / pre-commit / powershell / pandas presence on THIS host.
     A bare skip count is unreadable later: 3 skips on a host without `grep` and 3 skips on
     a fully-equipped host are different facts. A raw skip key in `context` is refused.
"""
from __future__ import annotations

import importlib.util
import json
import logging
import os
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import uuid
from collections.abc import Callable, Mapping
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# NO MODULE-LEVEL `_REPO_ROOT` -- see `repo_root()`. `[#529]` leg 4 / ruling R6(c).

# The [#355] git-env scrub, single-sourced in the LEAF module `scripts/gitenv.py` ([#396]).
# Loaded BY PATH, never by name: `import gitenv` and `from scripts import gitenv` each have a
# shadow hole that silently empties the scrub, and ordering them only moves it. Full argument
# in gitenv.py's docstring. Without the scrub an inherited GIT_DIR would answer the shallow
# question about the PARENT repo while this module labelled it as the target's -- exactly the
# provenance lie constraint 1 exists to refuse.
_gitenv_spec = importlib.util.spec_from_file_location(
    "dev_knowledge_gitenv", Path(__file__).resolve().with_name("gitenv.py"))
_gitenv = importlib.util.module_from_spec(_gitenv_spec)
_gitenv_spec.loader.exec_module(_gitenv)

#: Env var that relocates the store. Set it in a test, a sandbox, or a satellite checkout.
DB_PATH_ENV = "DEV_KNOWLEDGE_TELEMETRY_DB"

#: Default store location. UPPERCASE-KEBAB stem per the 2026-07-22 `logs/` naming ruling
#: (CLAUDE.md section 9); the `.db` extension stays honest to the format, as that ruling asks.
DEFAULT_DB_RELPATH = Path("logs") / "TELEMETRY.db"

#: Env var carrying the [#565] correlation id across a gate invocation's PROCESS TREE. Set by
#: `current_run_id()` on first use so children inherit it; an outer wrapper may set it FIRST to
#: widen the correlation window (see `current_run_id`'s honest limit).
RUN_ID_ENV = "DEV_KNOWLEDGE_TELEMETRY_RUN_ID"

#: The three Stage-1 event types. Memo lines 82-84; `[#529]` Done-when names exactly these.
EVENT_TYPES: frozenset[str] = frozenset({"check_run", "hook_run", "blocker_fired"})

#: Memo line 82: outcome (pass/block/error). Line 36: "you want outcome in {pass, block} per
#: fire" -- `error` is the third because a check that crashed is neither.
OUTCOMES: frozenset[str] = frozenset({"pass", "block", "error"})

#: Memo line 52, verbatim: "Set journal_mode=WAL, synchronous=NORMAL, busy_timeout=5000."
#: Applied on every connection, because a pragma set is per-connection except journal_mode,
#: which is persistent -- re-applying it is idempotent and makes a fresh file correct too.
WAL_PRAGMAS: tuple[tuple[str, str], ...] = (
    ("journal_mode", "WAL"),
    ("synchronous", "NORMAL"),
    ("busy_timeout", "5000"),
)

#: Memo line 79: "Single table events(id, ts, event_type, name, outcome, duration_ms,
#: context_json)", plus the `[#565]` correlation column. Append-only by discipline -- there is
#: no UPDATE or DELETE path in this module (retention pruning is the memo's separate
#: maintenance check, line 93).
SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    ts           TEXT    NOT NULL,
    event_type   TEXT    NOT NULL,
    name         TEXT    NOT NULL,
    outcome      TEXT,
    duration_ms  INTEGER,
    context_json TEXT    NOT NULL DEFAULT '{}',
    run_id       TEXT    NOT NULL DEFAULT ''
)
"""

#: `[#565]`'s migration. A store written before the column existed is REAL -- the library has
#: been importable since `4ad2025d` -- so `connect()` adds the column rather than assuming a
#: fresh file. `ALTER TABLE ADD COLUMN` is O(1) in SQLite and its `NOT NULL DEFAULT ''` backfills
#: existing rows with the empty string, which reads as "emitted before correlation existed" and
#: is deliberately NOT a synthesized id: inventing a run_id for rows that never had one would
#: make two uncorrelated events look like one run, the exact confusion this column closes.
_MIGRATIONS: tuple[tuple[str, str], ...] = (
    ("run_id", "ALTER TABLE events ADD COLUMN run_id TEXT NOT NULL DEFAULT ''"),
)


#: Constraint 2's sentinel. A coverage signal whose only evidence is a non-call reference is
#: UNRESOLVED, and unresolved is not zero. Stored as this string so no reader can average it
#: into a number by accident.
UNKNOWN = "unknown"

#: Constraint 3's probe set, in the order the row names them: git / grep / pre-commit /
#: powershell / pandas. The first four are executables on PATH; pandas is an importable
#: module (the `analytics` dependency group), so it is probed as one.
CAPABILITY_PROBES: tuple[str, ...] = ("git", "grep", "pre-commit", "powershell", "pandas")

#: Context keys that carry a skip count. Any of these arriving through raw `context` is
#: refused -- constraint 3 is structural, not a convention a wiring site can forget.
_SKIP_KEYS = frozenset({"skipped", "skips", "skip_count", "skipped_count"})

#: `coverage=None` MEANS "unresolved" (constraint 2), so it cannot double as "not supplied".
#: This sentinel is the third state: the caller said nothing about coverage at all.
_UNSET: Any = object()


#: `[#565]`'s per-process cache. Resolved once and reused, so every event a runner emits
#: carries one id; `None` until the first `current_run_id()` call.
_RUN_ID: str | None = None

#: Guards the FIRST mint of `_RUN_ID`. `audit.run_checks` emits from worker THREADS on its error
#: path, so an unguarded read-then-mint lets one gate invocation produce two ids.
_RUN_ID_LOCK = threading.Lock()

#: `logger_backend()`'s per-process cache -- which packages are installed does not change under
#: a running process. `None` until first asked; a test that needs it re-asked resets it.
_LOGGER_BACKEND: str | None = None


class TelemetryError(Exception):
    """Base for every refusal this module raises. Callers that must not break their host
    catch this (or use `safe_emit`); callers that want the defect loud let it propagate."""


class ShallowRepositoryRefusal(TelemetryError):
    """Constraint 1: a git-history-derived metric was asked for on a shallow (or
    unverifiable) clone, so nothing was emitted. Raised INSTEAD of writing a truncated
    number -- the memo's "wrong numbers worse than none" in enforceable form."""


def repo_root(start: str | os.PathLike[str] | None = None) -> Path | None:
    """The repository `start` (default: the CWD) is in -- `git rev-parse --show-toplevel`, asked
    at CALL time. `None` when the question cannot be answered (git absent, not a repository).

    `[#529]` leg 4, ruling R6(c). What this replaces is a module-level
    `_REPO_ROOT = Path(__file__).resolve().parent.parent` -- the LIBRARY's own location, frozen
    at import. That value answers "where does this file live", and every caller wanted "which
    repository is being gated". The two diverge whenever the library is imported from somewhere
    other than the tree under test: a linked worktree, a shared hooks dir, a deployed copy, a
    test sandbox. The store then lands outside the tree anything is watching, and NOTHING goes
    red -- the seam detaches silently, which is why all three live call sites
    (`audit._telemetry_db_path`, `block_ff_push.telemetry_db`,
    `block_commit_on_main.telemetry_db`) each hand-rolled their own root rather than trust the
    library. This makes the library's own answer correct; those three keep their explicit paths.

    HONEST LIMIT, stated because the ruling's own wording invites the question:
    `--show-toplevel` in a LINKED WORKTREE returns THAT WORKTREE, not the primary checkout. So
    two lanes running in two worktrees of one repo write two stores, one per tree, rather than
    sharing one. That is the ruled shape (R6(c) names `--show-toplevel` specifically); the
    alternative resolver, `--git-common-dir` as used by `fleet_analytics._git_common_dir`, would
    merge them into a single store. Nothing here quietly substitutes it. Correlating across the
    two trees is `run_id`'s job ([#565]), not the path's.

    The git-env scrub applies for the same reason it applies to the shallow probe: an inherited
    `GIT_DIR` overrides both cwd and `-C`, so without it this would answer about the PARENT
    repository while the caller believed it had asked about its own.
    """
    where = Path(start) if start is not None else Path.cwd()
    try:
        proc = subprocess.run(
            ["git", "-C", str(where), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=_gitenv.scrubbed_git_env(),
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    answer = proc.stdout.strip()
    return Path(answer) if answer else None


def new_run_id() -> str:
    """A fresh correlation id: `uuid.uuid4().hex`.

    uuid4 and not a counter, a pid or a timestamp, because `[#565]`'s distinctness requirement
    is across processes that share neither memory nor clock: two lanes in two worktrees start
    within the same millisecond often enough that a timestamp collides, and pids recycle.
    """
    return uuid.uuid4().hex


def current_run_id() -> str:
    """The id correlating every event emitted by ONE gate invocation. `[#565]`.

    Resolution order, and each step is load-bearing:

      1. `$DEV_KNOWLEDGE_TELEMETRY_RUN_ID` when set and non-blank -- an INHERITED id. This is
         how one runner's id reaches the processes it spawns, and how an outer wrapper widens
         the correlation window over a whole gate mesh.
      2. otherwise a fresh `new_run_id()`, cached for this process AND exported into
         `os.environ` so anything this process spawns inherits it.

    THE EXPORT IS THE MECHANISM, not a side effect, so it is stated rather than hidden: the
    gate mesh is multi-process (a runner spawns git, a hook spawns a validator), and an id that
    stopped at the process boundary would correlate one process rather than one invocation.

    HONEST LIMIT, and it bounds what a read path may claim. The export reaches this process's
    DESCENDANTS. It does NOT reach its SIBLINGS: `pre-commit` spawns each hook as its own child,
    so hook A setting the variable in its own environment cannot be seen by hook B. One
    `git commit` therefore yields one run_id per emitting hook, not one for the commit --
    unless something outside sets `RUN_ID_ENV` before pre-commit starts, which is exactly the
    seam step 1 leaves open. A reader grouping by run_id is grouping RUNNER INVOCATIONS.
    """
    global _RUN_ID
    inherited = os.environ.get(RUN_ID_ENV, "").strip()
    if inherited:
        return inherited
    if _RUN_ID is None:
        # LOCKED, double-checked. Terra P1, 2026-08-21: two threads reaching an unset `_RUN_ID`
        # together each mint a uuid and each overwrite the cache, so ONE gate invocation emits
        # events under TWO ids -- the exact thing this field exists to prevent. Not hypothetical:
        # `audit.run_checks` runs checks in a ThreadPoolExecutor and its error path emits from
        # inside the worker, so a fresh process whose first two emits are concurrent failures hits
        # precisely this window.
        with _RUN_ID_LOCK:
            if _RUN_ID is None:
                _RUN_ID = new_run_id()
    os.environ[RUN_ID_ENV] = _RUN_ID
    return _RUN_ID


def is_shallow_repository(repo_path: str | os.PathLike[str] | None = None) -> bool | None:
    """`git rev-parse --is-shallow-repository`, as a tri-state.

    `False` -> full history. `True` -> shallow. `None` -> could not be determined (git
    absent, not a repository, git errored). The third state is separate on purpose: callers
    must not read "could not ask" as "answered no", which is how an unverified provenance
    claim becomes a verified-looking one.
    """
    root = Path(repo_path) if repo_path is not None else Path.cwd()
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-shallow-repository"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=_gitenv.scrubbed_git_env(),
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    answer = proc.stdout.strip().lower()
    if answer == "false":
        return False
    if answer == "true":
        return True
    return None


def assert_not_shallow(repo_path: str | os.PathLike[str] | None = None) -> None:
    """Constraint 1's gate. Passes only on a verified-full history; raises otherwise."""
    shallow = is_shallow_repository(repo_path)
    if shallow is False:
        return
    if shallow is True:
        raise ShallowRepositoryRefusal(
            "refusing to emit a git-history-derived metric: "
            "`git rev-parse --is-shallow-repository` reports true, so the history is truncated"
        )
    raise ShallowRepositoryRefusal(
        "refusing to emit a git-history-derived metric: "
        "`git rev-parse --is-shallow-repository` could not be answered, so the history is unverified"
    )


def capability_vector() -> dict[str, bool]:
    """Constraint 3's host vector: presence of git / grep / pre-commit / powershell / pandas.

    Probed live per call, never cached -- a cached vector outlives the host state it
    describes, and the whole point of shipping it beside a skip count is that it is true of
    the run that produced the count. `powershell` is satisfied by either `pwsh` (7+) or
    `powershell` (Windows PowerShell), because a host with either can run a `.ps1` organ.
    """
    return {
        "git": shutil.which("git") is not None,
        "grep": shutil.which("grep") is not None,
        "pre-commit": shutil.which("pre-commit") is not None,
        "powershell": shutil.which("pwsh") is not None or shutil.which("powershell") is not None,
        "pandas": importlib.util.find_spec("pandas") is not None,
    }


def coverage_value(resolved: int | None) -> int | str:
    """Constraint 2's normalizer: `None` -> `"unknown"`, an int -> itself.

    `0` passes through untouched and means a MEASURED zero. The distinction this preserves is
    the finding: a signal whose only evidence is a non-call reference has NOT been measured at
    zero, it has not been measured.
    """
    if resolved is None:
        return UNKNOWN
    if not isinstance(resolved, int) or isinstance(resolved, bool):
        raise TelemetryError(f"coverage must be an int or None, got {type(resolved).__name__}")
    return resolved


def default_db_path() -> Path:
    """The store location: `$DEV_KNOWLEDGE_TELEMETRY_DB` if set, else `<repo>/logs/TELEMETRY.db`
    where `<repo>` is `repo_root()` -- the CALLER's repository, resolved at call time.

    Resolved per call, never cached at import, so a test or a sandbox can set the env var
    after this module is already imported.

    REFUSES (rather than guessing) when neither the override nor a repository answers. The
    alternatives are both worse than a loud stop: falling back to the library's own directory
    is the R6(c) defect this function was just fixed for, and falling back to the CWD scatters
    a `logs/TELEMETRY.db` into whatever directory a process happened to start in. A gate always
    runs inside a repository, so this path is a wiring defect, and `TelemetryError` is the class
    `safe_emit` deliberately does not swallow for exactly that reason.
    """
    override = os.environ.get(DB_PATH_ENV)
    if override:
        return Path(override)
    root = repo_root()
    if root is None:
        raise TelemetryError(
            f"cannot resolve the telemetry store: `git rev-parse --show-toplevel` did not answer "
            f"from {Path.cwd()}. Set ${DB_PATH_ENV} to an explicit path, pass `db_path=`, or run "
            f"inside a repository"
        )
    return root / DEFAULT_DB_RELPATH


def _migrate(conn: sqlite3.Connection) -> None:
    """Add any column `_MIGRATIONS` declares and the live table lacks. Idempotent.

    `CREATE TABLE IF NOT EXISTS` is a no-op against a store that already exists, so a schema
    that GREW cannot reach an older file through it -- the file keeps its original columns and
    the first insert fails on the missing one. Asking `PRAGMA table_info` and adding what is
    absent is the smallest thing that makes an existing store correct, and it never rewrites a
    row: the column arrives with its default and the append-only discipline is intact.
    """
    have = {row[1] for row in conn.execute("PRAGMA table_info(events)")}
    for column, ddl in _MIGRATIONS:
        if column in have:
            continue
        try:
            conn.execute(ddl)
        except sqlite3.OperationalError as exc:
            # ANOTHER CONNECTION WON THE RACE, and that is success rather than failure. This store
            # is built for concurrent writers (WAL, parallel lanes, one shared hooks dir), so two
            # hooks opening a pre-run_id store at the same moment BOTH read the column as absent
            # before either alters. Whoever loses the write lock then hits `duplicate column
            # name`, which propagates as a `sqlite3.Error`, which `safe_emit` swallows -- so the
            # loser's event would be dropped SILENTLY. The post-condition here is "the column
            # exists", not "I am the one who added it".
            if "duplicate column" not in str(exc).lower():
                raise


@contextmanager
def connect(db_path: str | os.PathLike[str] | None = None):
    """Open the store with the memo's three pragmas applied and the schema ensured.

    Creates the parent directory if absent -- a hook firing in a fresh checkout must not need
    a provisioning step to emit. Commits on clean exit, rolls back on exception, always closes.
    """
    path = Path(db_path) if db_path is not None else default_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=5.0)
    try:
        for pragma, value in WAL_PRAGMAS:
            conn.execute(f"PRAGMA {pragma}={value}")
        conn.execute(SCHEMA)
        _migrate(conn)
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def _log_event(row: Mapping[str, Any]) -> None:
    """Mirror the event onto the structured-log side-channel (structlog, or stdlib JSON).

    Never raises: the durable record is the SQLite row, and a logging misconfiguration in a
    host process is not a reason to lose an event.

    The backend is asked ONCE per process (`logger_backend()`), not once per event. The previous
    shape put `try: import structlog` inside this function, and a FAILED import is not cached --
    `sys.modules` records successes only -- so on a host without structlog every single event
    re-walked `sys.path` looking for a module that was not there. Measured on this host
    (2026-08-21, `[#529]` leg 3 / R6(a)): 481 us per event, against 8.85 us for the JSON encode
    and 0.37 us for the stdlib log call it was wrapping. The absence detection cost 50x the work
    it was guarding.
    """
    try:
        if logger_backend() == "structlog":
            import structlog  # cached in sys.modules after the first successful import
            structlog.get_logger("telemetry").info(row["event_type"], **dict(row))
        else:
            logging.getLogger("telemetry").info(json.dumps(dict(row), sort_keys=True, default=str))
    except Exception:  # side-channel only -- the SQLite row is the durable record
        pass


def logger_backend() -> str:
    """`"structlog"` when structlog is importable here, else `"stdlib-logging"`.

    Exposed so a wiring site (or an operator) reads which backend is live instead of assuming
    the preferred one is installed. Resolved once and cached: what is being asked is which
    packages are installed, and that does not change under a running process. A test that needs
    the question asked again sets `telemetry_emit._LOGGER_BACKEND = None`.

    `find_spec` rather than a `try: import`: it answers the same question without executing the
    module, and it is the same probe `capability_vector()` already uses for pandas.
    """
    global _LOGGER_BACKEND
    if _LOGGER_BACKEND is None:
        _LOGGER_BACKEND = (
            "structlog" if importlib.util.find_spec("structlog") is not None else "stdlib-logging"
        )
    return _LOGGER_BACKEND


def emit_event(
    event_type: str,
    name: str,
    outcome: str | None = None,
    duration_ms: int | None = None,
    context: Mapping[str, Any] | None = None,
    db_path: str | os.PathLike[str] | None = None,
    ts: str | None = None,
    git_derived: bool = False,
    coverage: int | None = _UNSET,
    skipped: int | None = None,
    repo_path: str | os.PathLike[str] | None = None,
    run_id: str | None = None,
) -> int:
    """Append one event and return its row id.

    Refuses (raises `TelemetryError`) on an unknown `event_type` or `outcome`, on an empty
    `name`, and on a `context` that will not serialize -- all four are wiring defects, and a
    silently-dropped or silently-mangled event is the "plausible-but-false metric" this slice
    exists to avoid.

    The three binding constraints ride the last four parameters:

      * `git_derived=True` -- this event's number came from git history. Checked against
        `assert_not_shallow(repo_path)` BEFORE anything is written, so a refusal leaves no
        row. Stamps `context["git_derived"] = True` so a reader can tell which rows carry a
        history-derived number without re-deriving provenance.
      * `coverage=<int|None>` -- routed through `coverage_value()`. `None` stores `"unknown"`,
        `0` stores a measured zero. A raw `coverage` key in `context` is refused.
      * `skipped=<int>` -- stores the count AND `context["capabilities"]`, the live host
        vector. A raw skip key in `context` is refused.

    `run_id` ([#565]) defaults to `current_run_id()` -- one id for every event this invocation
    emits. Passing it explicitly is for a caller that owns a wider unit than this process (or a
    test staging two runs); an empty or blank string is REFUSED rather than stored, because a
    blank id is what a pre-`[#565]` row carries and a new event must not be indistinguishable
    from one written before correlation existed.
    """
    if event_type not in EVENT_TYPES:
        raise TelemetryError(f"unknown event_type {event_type!r}; expected one of {sorted(EVENT_TYPES)}")
    if outcome is not None and outcome not in OUTCOMES:
        raise TelemetryError(f"unknown outcome {outcome!r}; expected one of {sorted(OUTCOMES)}")
    if not name or not str(name).strip():
        raise TelemetryError("name is required -- an unnamed organ cannot be counted")
    if duration_ms is not None and (not isinstance(duration_ms, int) or isinstance(duration_ms, bool)):
        raise TelemetryError(f"duration_ms must be an int or None, got {type(duration_ms).__name__}")
    if run_id is not None and not str(run_id).strip():
        raise TelemetryError(
            "run_id must be a non-empty string -- a blank id is what rows written before [#565] "
            "carry, and a new event must not be indistinguishable from an uncorrelated one"
        )

    payload = dict(context or {})

    # Constraint 2 and 3 are refused at the RAW-CONTEXT door as well as offered as parameters.
    # Without this, a wiring site that spells the field by hand bypasses the normalizer and the
    # vector silently, and the constraint becomes a convention.
    if "coverage" in payload:
        raise TelemetryError(
            "pass coverage through the `coverage=` parameter, not raw context: a raw 0 cannot be "
            "told apart from an unresolved signal, which is the defect the constraint closes"
        )
    bare_skip = _SKIP_KEYS & payload.keys()
    if bare_skip:
        raise TelemetryError(
            f"pass skip counts through the `skipped=` parameter, not raw context ({sorted(bare_skip)}): "
            "a bare skip count carries no host capability vector and is unreadable later"
        )

    # Constraint 1 fires BEFORE the insert, so a refusal leaves no row behind.
    if git_derived:
        assert_not_shallow(repo_path)
        payload["git_derived"] = True

    if coverage is not _UNSET:
        payload["coverage"] = coverage_value(coverage)

    if skipped is not None:
        if not isinstance(skipped, int) or isinstance(skipped, bool):
            raise TelemetryError(f"skipped must be an int or None, got {type(skipped).__name__}")
        payload["skipped"] = skipped
        payload["capabilities"] = capability_vector()

    try:
        context_json = json.dumps(payload, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise TelemetryError(f"context is not JSON-serializable: {exc}") from exc

    row = {
        "ts": ts or _utc_now_iso(),
        "event_type": event_type,
        "name": str(name),
        "outcome": outcome,
        "duration_ms": duration_ms,
        "context_json": context_json,
        "run_id": str(run_id) if run_id is not None else current_run_id(),
    }
    with connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO events (ts, event_type, name, outcome, duration_ms, context_json, run_id)"
            " VALUES (:ts, :event_type, :name, :outcome, :duration_ms, :context_json, :run_id)",
            row,
        )
        row_id = int(cur.lastrowid)
    _log_event(row)
    return row_id


def emit_check_run(name: str, outcome: str, duration_ms: int | None = None, **kwargs: Any) -> int:
    """Memo line 82 -- `check_run`: each audit check fires, with `name`, `outcome`, `duration_ms`.

    Feeds "retire checks with fires>0/blocks=0; promote high-catch checks."
    """
    return emit_event("check_run", name, outcome=outcome, duration_ms=duration_ms, **kwargs)


def emit_hook_run(name: str, outcome: str, duration_ms: int | None = None, **kwargs: Any) -> int:
    """Memo line 83 -- `hook_run`: each git hook (pre-commit/pre-push) fires, with `name`, `outcome`.

    `duration_ms` is optional here because the memo's line for this event does not require it.
    Feeds "is a hook pure ceremony? Promote/demote."
    """
    return emit_event("hook_run", name, outcome=outcome, duration_ms=duration_ms, **kwargs)


def emit_blocker_fired(name: str, reason: str, **kwargs: Any) -> int:
    """Memo line 84 -- `blocker_fired`: any gate that REFUSES an action, with reason in `context`.

    `outcome` is fixed to `block` because that is what this event means; a gate that passed is
    a `check_run`/`hook_run` with `outcome="pass"`, not a blocker that fired. `reason` merges
    into `context` rather than replacing it, so a caller can add its own fields.
    """
    context = dict(kwargs.pop("context", None) or {})
    context["reason"] = reason
    return emit_event("blocker_fired", name, outcome="block", context=context, **kwargs)


def safe_emit(emitter: Callable[..., int], *args: Any, **kwargs: Any) -> int | None:
    """Call `emitter`, swallowing store/IO failure and returning `None` instead of raising.

    For wiring sites on a gate's critical path: a locked database or a read-only disk must not
    turn into a failed commit. `TelemetryError` is NOT swallowed -- that class is a wiring
    defect (bad event type, unserializable context, a raw coverage/skip key), and hiding it
    would ship a gate that silently records nothing. `ShallowRepositoryRefusal` propagates for
    the same reason: constraint 1 refusing is the mechanism working, and a swallowed refusal is
    indistinguishable from a metric that was never asked for.
    """
    try:
        return emitter(*args, **kwargs)
    except (sqlite3.Error, OSError):
        return None


# ===================================================================================
# CLI -- B2 lane 4 (hook-role review). The phase-3 wiring this module's docstring named
# as owed: a hook `entry` needs ONE call that runs the real check AND records a
# `hook_run` event, without a second `scripts/` file (BUILD MODE rule 7's counter
# requirement, paid without raising the mechanism count) and without a second
# `uv run --locked` per hook (this process already holds the synced venv; the wrapped
# command reuses `sys.executable` rather than re-invoking uv).
#
# Usage from a pre-commit `entry:` line:
#     uv run --locked python scripts/telemetry_emit.py wrap <hook-id> -- <script.py [args...]>
#     uv run --locked python scripts/telemetry_emit.py wrap <hook-id> -- -m <module> [args...]
# `pass_filenames: true` hooks are unaffected: pre-commit appends filenames after the
# whole entry, which lands after `--`, exactly where the wrapped command expects them.
# ===================================================================================

# `wrap` options, all BEFORE the `--`. Absent, `wrap` is exactly the hook wrapper above; present,
# it also writes one RECEIPT file (DECLARE-NIGHT N2: the receipt is the doit target, so a step's
# "done" is a file). `--value` options take the next token; the rest are flags.
_WRAP_VALUE_OPTS = {"--receipt": "receipt", "--input-hash": "input_hash", "--stdout-file": "stdout_file",
                    "--model-requested": "model_requested", "--model-reported": "model_reported",
                    "--skipped": "skipped"}
_WRAP_FLAGS = {"--exec": "literal"}
_RECEIPT_SCHEMA = 1


def _parse_wrap_opts(rest: list[str]) -> tuple[dict[str, Any], list[str]]:
    opts: dict[str, Any] = {}
    while rest and rest[0] in {*_WRAP_VALUE_OPTS, *_WRAP_FLAGS}:
        flag = rest[0]
        if flag in _WRAP_FLAGS:
            opts[_WRAP_FLAGS[flag]] = True
            rest = rest[1:]
        elif len(rest) < 2:
            raise ValueError(f"{flag} needs a value")
        else:
            opts[_WRAP_VALUE_OPTS[flag]] = rest[1]
            rest = rest[2:]
    if rest and rest[0] == "--":
        rest = rest[1:]
    return opts, rest


def _write_receipt(path: str, body: Mapping[str, Any]) -> None:
    """One receipt, written whole or not at all: a kill between the write and the rename leaves the
    previous receipt (or none), never a half-file that reads as "done"."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, target)


def _cli_wrap(argv: list[str]) -> int:
    """`wrap <id> [options] -- <python-args...>`: run `sys.executable <python-args...>` (or the argv
    itself with `--exec`), time it, record one `hook_run` event (outcome pass/block/error,
    `duration_ms`), optionally write a receipt file, and propagate the wrapped command's exit code
    unchanged -- a recording failure must never turn a passing hook into a failing one (`safe_emit`),
    and a wrapped-command failure must never be hidden (the hook's own exit code is what pre-commit
    sees).

    Receipt options (`--receipt PATH` turns the receipt on): `--input-hash`, `--stdout-file` (the
    wrapped stdout is kept there AND echoed), `--model-requested` / `--model-reported`, and
    `--skipped STATUS` (write the receipt with that status and run nothing).
    """
    usage = "usage: telemetry_emit.py wrap <id> [receipt options] -- <python-args...>"
    if len(argv) < 2 or argv[0] != "wrap":
        print(usage, file=sys.stderr)
        return 2
    hook_id = argv[1]
    try:
        opts, rest = _parse_wrap_opts(argv[2:])
    except ValueError as exc:
        print(f"telemetry_emit wrap: {exc}\n{usage}", file=sys.stderr)
        return 2
    if not hook_id or not rest:
        print(usage, file=sys.stderr)
        return 2

    def receipt(status: str, exit_code: int | None, duration_ms: int) -> None:
        if "receipt" not in opts:
            return
        out_name = Path(opts["stdout_file"]).name if opts.get("stdout_file") else None
        _write_receipt(opts["receipt"], {
            "schema": _RECEIPT_SCHEMA, "organ": hook_id, "status": status, "exit_code": exit_code,
            "duration_ms": duration_ms, "input_hash": opts.get("input_hash"),
            "model_requested": opts.get("model_requested"), "model_reported": opts.get("model_reported"),
            "command": rest, "output_file": out_name, "finished_at": _utc_now_iso()})

    if opts.get("skipped"):
        receipt(opts["skipped"], None, 0)
        return 0
    argv_run = rest if opts.get("literal") else [sys.executable, *rest]
    start = time.monotonic()
    capture = opts.get("stdout_file")
    try:
        proc = subprocess.run(argv_run, stdout=subprocess.PIPE if capture else None,
                              env={**os.environ, "PYTHONUTF8": "1"} if capture else None)
        rc = proc.returncode
    except OSError as exc:
        print(f"telemetry_emit wrap: failed to launch {rest!r}: {exc}", file=sys.stderr)
        duration_ms = int((time.monotonic() - start) * 1000)
        safe_emit(emit_hook_run, hook_id, "error", duration_ms=duration_ms)
        receipt("error", 2, duration_ms)
        return 2
    duration_ms = int((time.monotonic() - start) * 1000)
    if capture:
        Path(capture).parent.mkdir(parents=True, exist_ok=True)
        Path(capture).write_bytes(proc.stdout or b"")
        sys.stdout.flush()
        sys.stdout.buffer.write(proc.stdout or b"")
        sys.stdout.buffer.flush()
    outcome = "pass" if rc == 0 else "block"
    safe_emit(emit_hook_run, hook_id, outcome, duration_ms=duration_ms)
    receipt("ok" if rc == 0 else "failed", rc, duration_ms)
    return rc


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] == ["wrap"]:
        return _cli_wrap(args)
    print("usage: telemetry_emit.py wrap <id> [receipt options] -- <python-args...>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
