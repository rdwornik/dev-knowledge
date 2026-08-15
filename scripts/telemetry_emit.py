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
`uv.lock`), and this module's owned-files manifest does not include `pyproject.toml`. So the
structured-log side-channel binds structlog WHEN IMPORTABLE and otherwise falls back to the
option the memo itself names as the least-deps fallback on the same line: stdlib `logging`
emitting one JSON object per event. `logger_backend()` reports which is live, so a caller
never has to guess. Adding structlog as a real dependency remains an open, separate decision;
the durable record is the SQLite row either way, and no event is lost by the fallback.

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
from collections.abc import Callable, Mapping
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent

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
#: context_json)". Append-only by discipline -- there is no UPDATE or DELETE path in this
#: module (retention pruning is the memo's separate maintenance check, line 93).
SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    ts           TEXT    NOT NULL,
    event_type   TEXT    NOT NULL,
    name         TEXT    NOT NULL,
    outcome      TEXT,
    duration_ms  INTEGER,
    context_json TEXT    NOT NULL DEFAULT '{}'
)
"""


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


class TelemetryError(Exception):
    """Base for every refusal this module raises. Callers that must not break their host
    catch this (or use `safe_emit`); callers that want the defect loud let it propagate."""


class ShallowRepositoryRefusal(TelemetryError):
    """Constraint 1: a git-history-derived metric was asked for on a shallow (or
    unverifiable) clone, so nothing was emitted. Raised INSTEAD of writing a truncated
    number -- the memo's "wrong numbers worse than none" in enforceable form."""


def is_shallow_repository(repo_path: str | os.PathLike[str] | None = None) -> bool | None:
    """`git rev-parse --is-shallow-repository`, as a tri-state.

    `False` -> full history. `True` -> shallow. `None` -> could not be determined (git
    absent, not a repository, git errored). The third state is separate on purpose: callers
    must not read "could not ask" as "answered no", which is how an unverified provenance
    claim becomes a verified-looking one.
    """
    root = Path(repo_path) if repo_path is not None else _REPO_ROOT
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
    """The store location: `$DEV_KNOWLEDGE_TELEMETRY_DB` if set, else `<repo>/logs/TELEMETRY.db`.

    Resolved per call, never cached at import, so a test or a sandbox can set the env var
    after this module is already imported.
    """
    override = os.environ.get(DB_PATH_ENV)
    if override:
        return Path(override)
    return _REPO_ROOT / DEFAULT_DB_RELPATH


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
    """
    try:
        try:
            import structlog
        except ModuleNotFoundError:
            logging.getLogger("telemetry").info(json.dumps(dict(row), sort_keys=True, default=str))
        else:
            structlog.get_logger("telemetry").info(row["event_type"], **dict(row))
    except Exception:  # side-channel only -- the SQLite row is the durable record
        pass


def logger_backend() -> str:
    """`"structlog"` when structlog is importable here, else `"stdlib-logging"`.

    Exposed so a wiring site (or an operator) reads which backend is live instead of assuming
    the preferred one is installed.
    """
    try:
        import structlog  # noqa: F401
    except ModuleNotFoundError:
        return "stdlib-logging"
    return "structlog"


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
    """
    if event_type not in EVENT_TYPES:
        raise TelemetryError(f"unknown event_type {event_type!r}; expected one of {sorted(EVENT_TYPES)}")
    if outcome is not None and outcome not in OUTCOMES:
        raise TelemetryError(f"unknown outcome {outcome!r}; expected one of {sorted(OUTCOMES)}")
    if not name or not str(name).strip():
        raise TelemetryError("name is required -- an unnamed organ cannot be counted")
    if duration_ms is not None and (not isinstance(duration_ms, int) or isinstance(duration_ms, bool)):
        raise TelemetryError(f"duration_ms must be an int or None, got {type(duration_ms).__name__}")

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
    }
    with connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO events (ts, event_type, name, outcome, duration_ms, context_json)"
            " VALUES (:ts, :event_type, :name, :outcome, :duration_ms, :context_json)",
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
