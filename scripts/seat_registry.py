#!/usr/bin/env python
"""seat_registry.py -- the seat as a registered entity: ONE field, written by events ([#833]).

THE ABSENCE THIS FILLS. Wedged, absent and starved were filed four times as four symptoms
(`[#648]` dispatcher liveness, `[#805]` an integrator that sat 10.6 h waiting, `[#808]` a session
wedged by a hung hook, `[#682]` a paste addressed to a seat roster that does not exist). They are
three values of one field, and no organ held that field: `seat_refusals` refuses a seat's acts and
never records the seat; `resource_lifecycle` counts processes NAMED `claude` and knows neither
their session nor their role; `lane_cost` keys a seat by session id only to price it afterwards;
and `claude agents` reported a dead session "busy" (`[#803]`). The plan of 2026-09-16 priced the
absence at ~17 agent-hours in one week.

On 2026-09-17 it was demonstrated on the lane that built this: a second session was dispatched
onto lane ab-833 while its owner was live, and found the owner only by reading staged files and
scanning processes. Every value this module stores was available at that moment; none of it was
written anywhere a dispatcher reads.

THE FIELD, AND WHO MAY WRITE IT
-------------------------------
`state` in {live, wedged, absent, starved}. It is WRITTEN ONLY BY AN EVENT:

  * `record_event` takes a HOOK PAYLOAD. The writer sets `state` from the event kind
    (`EVENT_STATE`); a payload carrying its own `state` is REFUSED (`model-authored-state`), and a
    payload whose `hook_event_name` is not a known event is REFUSED (`not-an-event`). No verb on
    the CLI accepts a state.
  * the reader DISCARDS any row the writer could not have produced -- a row whose `state`
    disagrees with its event, or a row of an unknown kind. The write-time refusal alone would be
    decoration: anyone can append a line to a file.
  * `bind` records IDENTITY (role, batch) for a seat in the primary checkout, and never a state.
    Its CLI binds `CLAUDE_CODE_SESSION_ID` -- the id the RUNTIME set -- and offers no `--session`,
    so a seat cannot bind someone else.

`wedged` and `starved` are never written at all. They are READ, as a function of event timestamps
and one threshold each: a seat silent mid-turn past `WEDGED_AFTER_MIN` is wedged; a seat whose last
event was a `Stop` and which nothing has fed since, past `STARVED_AFTER_MIN`, is starved. The last
event is the newer of the registry's last hook row and the session TRANSCRIPT's last write -- the
transcript is appended by the harness, not by the model's prose, so its mtime is an event time.
`absent` is read from facts, not age: a dead recorded pid (`resource_lifecycle.pid_is_alive`, the
query-only probe), a lane worktree that no longer exists, or a `SessionEnd`.

WHERE IT LIVES: `~/.claude/seat-registry.jsonl`, append-only, for the three reasons
`resource_lifecycle.SAMPLE_LEDGER_PATH` records -- a hook writes it every session so it must never
dirty the tree it reports on; the fact is about THIS machine's processes; and an in-repo `.jsonl`
under `logs/` is the home `[#785]` shows two organs disagreeing over.

WHO WRITES EVENTS, with no new hook registration (`.claude/settings.json` is sequenced behind
ab-808 in the batch AB manifest): `resource_lifecycle.py session-start` (the SessionStart leg) and
`session_end_backpressure.py` (the Stop leg) each pass their hook payload to `record_hook_event`,
which is fail-soft in full. The READ side is `fleet_health.py`'s `[seats]` line and the two
STEP-0 refusals in `seat_refusals.py` (`no-live-integrator`, `lane-owned`), run by
`lane_boot.py preflight` and the dispatcher's boot.

HONEST LIMITS
  * A process that pipes a well-formed hook payload into `record_event` writes an event. The
    refusal stops a seat ASSERTING a state; it cannot stop a seat forging the event that implies
    one. Under `bypassPermissions` only a deny rule or a PreToolUse exit 2 could refuse the
    write itself, and neither is wired here.
  * No PreToolUse heartbeat. Between a SessionStart and a Stop the only activity signal is the
    transcript's mtime, which moves when a tool call RETURNS. A single call longer than
    `WEDGED_AFTER_MIN` -- or a seat supervising a background agent for that long -- reads wedged.
  * A `browser` seat has no hook surface. It can be bound; with no event yet it reads `live`
    (D23: a fresh bind is a seat that just started, not one that is gone -- it ages to `wedged`
    on the same `WEDGED_AFTER_MIN` threshold as any other silent seat if no event ever follows).
  * The dispatch verb (win-tooling `dispatch.ps1`) calls no hub script, so a seat that types
    `dispatch` without `/lane-boot` is not refused by anything here.
  * The registry is never compacted; every SessionStart reads it whole. Bounded today by one row
    per session start and stop on one machine.
"""
from __future__ import annotations

import json
import os
import sys
import threading
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path, PurePath
from collections.abc import Callable, Iterable, Mapping

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

try:
    from seat_refusals import SeatRefusal
    from validate_branch_naming import validate_lane_worktree_name
except ImportError:                                  # imported as `scripts.seat_registry`
    from scripts.seat_refusals import SeatRefusal  # type: ignore[no-redef]
    from scripts.validate_branch_naming import validate_lane_worktree_name  # type: ignore[no-redef]

SCHEMA = "dev-knowledge-seat-registry/1"

#: The append-only store. Machine-local, outside the tree -- see the module docstring.
REGISTRY_PATH = Path.home() / ".claude" / "seat-registry.jsonl"

ROLES: tuple[str, ...] = ("dispatcher", "integrator", "lane", "browser")
STATES: tuple[str, ...] = ("live", "wedged", "absent", "starved")

#: The ONLY route from an event to a written `state`. A hook event not named here is not an event
#: this registry records, and the value a row carries must equal this map's -- the reader checks.
#: `Stop` is `live`: a seat that ended its turn is alive and waiting; whether it is STARVED is a
#: question of how long it has waited, which is read, never written.
EVENT_STATE: dict[str, str] = {
    "SessionStart": "live",
    "UserPromptSubmit": "live",
    "Stop": "live",
    "SessionEnd": "absent",
}

# ================================================================================ the thresholds

#: A seat silent MID-TURN for longer than this reads `wedged`.
WEDGED_AFTER_MIN = 45.0
#: A seat that ended its turn and has not been fed for longer than this reads `starved`.
STARVED_AFTER_MIN = 60.0
#: The `[seats]` line reports seats whose last event falls inside this window.
SURFACE_LOOKBACK_HOURS = 24.0

#: EVERY threshold above, with the measurement behind it or the admission that there is none.
THRESHOLD_PROVENANCE: dict[str, str] = {
    "WEDGED_AFTER_MIN": (
        "A CHOSEN MARGIN OVER MEASURED MAXIMA, not itself a measurement. The longest legitimate "
        "silent stretch on record is one merge: `[#805]` measured four batch-AA merges at "
        "5.8-22.6 min of wall time each (pre-commit hooks 1.3-6.3 min), and lane ab-833's own "
        "step-1 commit ran its pre-commit hooks for more than 600 s on 2026-09-17 -- a tool call "
        "writes to the transcript only when it returns. 45 min is about twice the longest measured "
        "merge. The wedges it exists to catch were 8 h (a lane), ~6 h (the integrator, twice) and "
        "12 h 43 min (lane ab-833's first boot, a SessionStart hook created suspended): each is "
        "caught in 45 min instead of being found by a human hours later."
    ),
    "STARVED_AFTER_MIN": (
        "CHOSEN, and labelled so. No measurement of how long a healthy seat waits for its next "
        "input exists in this repo. What is measured is the failure: `[#805]`'s integrator sat "
        "10.6 h between its last tool call (2026-09-15 21:43) and the operator's rulings "
        "(2026-09-16 08:17), and the plan of 2026-09-16 priced starved subagents at 10.7 h in "
        "one week. 60 min sits two orders of magnitude below the witnessed starvation and above a "
        "short break at the keyboard. Replace it with a derived figure once the registry holds "
        "enough Stop -> next-event gaps to show the healthy distribution."
    ),
    "SURFACE_LOOKBACK_HOURS": (
        "DERIVED from `resource_lifecycle.THRESHOLD_PROVENANCE['LIFETIME_HOURS']`'s measured "
        "session spans: median 88.0 min, p90 477.3 min (7.96 h). 24 h is three times the p90, "
        "so a seat inside it is plausibly still someone's concern and one outside it is history. "
        "Every witnessed stall this week -- 8 h, 10.6 h, 12 h 43 min -- falls inside it, so none "
        "of them would have aged out of the line before anyone read it."
    ),
}


# ============================================================================ writing: events only

def _now() -> datetime:
    return datetime.now(UTC)


def _append(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def lane_of(cwd: str) -> str | None:
    """The lane worktree name `cwd` sits in, or None. Read off the path's own segments against
    the ruled grammar (`validate_lane_worktree_name`), so this module compiles no regex."""
    parts = PurePath(str(cwd).replace("\\", "/")).parts
    for index, part in enumerate(parts[:-1]):
        if part == "worktrees" and index and parts[index - 1] == ".claude":
            name = parts[index + 1]
            return name if validate_lane_worktree_name(name) is None else None
    return None


def _batch_of(lane: str) -> str:
    return lane.split("-")[1].upper()


def record_event(payload: Mapping, *, path: Path | None = None,
                 now: datetime | None = None, env: Mapping[str, str] | None = None) -> dict:
    """Append ONE event row built from a hook payload. Raise `SeatRefusal` on anything else."""
    if not isinstance(payload, Mapping):
        raise SeatRefusal("not-an-event", f"payload is a {type(payload).__name__}, not a hook "
                          "payload", remedy="pass the hook's stdin JSON object")
    if "state" in payload:
        raise SeatRefusal(
            "model-authored-state",
            f"the payload carries its own state ({payload.get('state')!r}); a seat's state is "
            "written by the event that happened, never asserted by the writer",
            remedy="send the hook event (SessionStart / Stop / SessionEnd) and let the registry "
                   "derive the state; wedged and starved are read, never written")
    event = payload.get("hook_event_name")
    if event not in EVENT_STATE:
        raise SeatRefusal("not-an-event",
                          f"{event!r} is not a recorded hook event ({', '.join(EVENT_STATE)})",
                          remedy="record only a real hook payload")
    environ = os.environ if env is None else env
    session = str(payload.get("session_id") or environ.get("CLAUDE_CODE_SESSION_ID") or "")
    if not session:
        raise SeatRefusal("not-an-event", f"{event} payload names no session",
                          remedy="a hook payload always carries session_id")
    cwd = str(payload.get("cwd") or "")
    row = {"schema": SCHEMA, "kind": "event", "event": event, "state": EVENT_STATE[event],
           "session_id": session, "ts": (now or _now()).isoformat(), "cwd": cwd,
           "pid": str(environ.get("CLAUDE_PID") or ""),
           "transcript_path": str(payload.get("transcript_path") or "")}
    lane = lane_of(cwd)
    if lane:
        row.update(role="lane", lane=lane, batch=_batch_of(lane))
    _append(Path(path) if path else REGISTRY_PATH, row)
    return row


def bind(role: str, batch: str, *, session_id: str, path: Path | None = None,
         now: datetime | None = None) -> dict:
    """Record a seat's IDENTITY. Never a state -- there is no parameter to carry one."""
    if role not in ROLES:
        raise SeatRefusal("unknown-role", f"{role!r} is not a seat role ({', '.join(ROLES)})",
                          remedy="bind one of the four roles")
    if not session_id:
        raise SeatRefusal("unknown-role", "no session id to bind",
                          remedy="bind from inside the seat's own Claude Code session")
    row = {"schema": SCHEMA, "kind": "bind", "role": role, "batch": str(batch).upper(),
           "session_id": session_id, "ts": (now or _now()).isoformat()}
    _append(Path(path) if path else REGISTRY_PATH, row)
    return row


def read_hook_stdin(timeout: float = 2.0) -> dict:
    """The hook's stdin JSON, or {} -- BOUNDED, because an unbounded read is how a hook wedges."""
    if sys.stdin is None or sys.stdin.isatty():
        return {}
    box: list[str] = []
    reader = threading.Thread(target=lambda: box.append(sys.stdin.read()), daemon=True)
    reader.start()
    reader.join(timeout)
    if not box or not box[0].strip():
        return {}
    try:
        data = json.loads(box[0])
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def record_hook_event(payload: Mapping) -> dict | None:
    """The hook legs' entry point. FAIL-SOFT IN FULL: a reporter never blocks a session.

    A payload with no session_id of its own writes NOTHING -- it is not a hook payload, and
    falling back to the environment here would let any test or shell that happens to run inside a
    Claude Code session write that session's events into the real registry.
    """
    if not isinstance(payload, Mapping) or not payload.get("session_id"):
        return None
    try:
        return record_event(payload)
    except Exception:  # noqa: BLE001 -- a refused or unwritable event is dropped, never raised
        return None


# ===================================================================================== reading

@dataclass(frozen=True)
class Seat:
    session_id: str
    role: str | None
    batch: str | None
    lane: str | None
    state: str
    last_event: datetime
    last_kind: str
    minutes_since: float


def _valid(row: object) -> bool:
    """A row the writer could have produced. Anything else is discarded, never believed."""
    if not isinstance(row, dict) or row.get("schema") != SCHEMA or not row.get("session_id"):
        return False
    try:
        datetime.fromisoformat(str(row.get("ts")))
    except ValueError:
        return False
    if row.get("kind") == "event":
        return row.get("event") in EVENT_STATE and row.get("state") == EVENT_STATE[row["event"]]
    if row.get("kind") == "bind":
        return row.get("role") in ROLES and "state" not in row
    return False


def read_rows(path: Path | None = None) -> list[dict]:
    try:
        text = Path(path or REGISTRY_PATH).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    rows = []
    for line in text.splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if _valid(row):
            rows.append(row)
    return rows


def _default_pid_alive(pid: int) -> bool:
    try:
        from resource_lifecycle import pid_is_alive  # noqa: PLC0415 -- lazy: a hook leg's import
    except ImportError:
        from scripts.resource_lifecycle import pid_is_alive  # type: ignore[no-redef]  # noqa: PLC0415
    return pid_is_alive(pid)


def _default_transcript_mtime(path: str) -> datetime | None:
    try:
        return datetime.fromtimestamp(Path(path).stat().st_mtime, tz=UTC)
    except (OSError, ValueError):
        return None


def _derive(events: list[dict], lane: str | None, now: datetime, *,
            pid_alive: Callable[[int], bool], path_exists: Callable[[str], bool],
            transcript_mtime: Callable[[str], datetime | None]) -> tuple[str, datetime, str]:
    """(state, last activity, last hook event kind) -- a pure function of event timestamps."""
    last = events[-1]
    hook_ts = datetime.fromisoformat(last["ts"])
    kind = last["event"]
    if kind == "SessionEnd":
        return "absent", hook_ts, kind
    pid = str(last.get("pid") or "")
    if pid.isdigit() and not pid_alive(int(pid)):
        return "absent", hook_ts, kind
    if lane and last.get("cwd") and not path_exists(last["cwd"]):
        return "absent", hook_ts, kind
    written = transcript_mtime(last["transcript_path"]) if last.get("transcript_path") else None
    fed_since = written is not None and written > hook_ts
    activity = max(hook_ts, written) if written else hook_ts
    idle_min = (now - activity).total_seconds() / 60.0
    if kind == "Stop" and not fed_since:
        return ("starved" if idle_min > STARVED_AFTER_MIN else "live"), activity, kind
    return ("wedged" if idle_min > WEDGED_AFTER_MIN else "live"), activity, kind


def seats(path: Path | None = None, *, now: datetime | None = None,
          pid_alive: Callable[[int], bool] = _default_pid_alive,
          path_exists: Callable[[str], bool] = lambda p: Path(p).exists(),
          transcript_mtime: Callable[[str], datetime | None] = _default_transcript_mtime,
          ) -> list[Seat]:
    """Every session the registry has seen, each with its READ state."""
    moment = now or _now()
    events: dict[str, list[dict]] = {}
    binds: dict[str, dict] = {}
    for row in read_rows(path):
        if row["kind"] == "bind":
            binds[row["session_id"]] = row
        else:
            events.setdefault(row["session_id"], []).append(row)
    out: list[Seat] = []
    for session in sorted(set(events) | set(binds)):
        rows = sorted(events.get(session, []), key=lambda r: r["ts"])
        lane = next((r["lane"] for r in reversed(rows) if r.get("lane")), None)
        bound = binds.get(session)
        role = bound["role"] if bound else ("lane" if lane else None)
        batch = bound["batch"] if bound else (_batch_of(lane) if lane else None)
        if not rows:
            # D23: a fresh bind used to read `absent` until this session's first hook event --
            # long enough that a dispatcher checking occupancy right after a bind saw a seat
            # that looked gone (SESSION-integrator-wave4b-2026-09-22.md s1: two pre-launch
            # refusals while the seat read absent). A bind with no event YET is a seat that just
            # started; it ages on the same wedge threshold as any other silent seat, so a bind
            # that never gets a first event still eventually reads as stalled.
            ts = datetime.fromisoformat(bound["ts"])  # type: ignore[index]
            idle_min = (moment - ts).total_seconds() / 60.0
            state = "wedged" if idle_min > WEDGED_AFTER_MIN else "live"
            activity, kind = ts, "bind"
        else:
            state, activity, kind = _derive(rows, lane, moment, pid_alive=pid_alive,
                                            path_exists=path_exists,
                                            transcript_mtime=transcript_mtime)
        out.append(Seat(session, role, batch, lane, state, activity, kind,
                        round((moment - activity).total_seconds() / 60.0, 1)))
    return out


def _label(seat: Seat) -> str:
    who = seat.lane if seat.role == "lane" and seat.lane else f"{seat.role} {seat.batch or '-'}"
    return f"{who} {seat.session_id[:8]} ({seat.minutes_since:.0f} min since last event)"


def seat_health_line(path: Path | None = None, *, now: datetime | None = None,
                     open_batches: Iterable[str] = (), **probes) -> str | None:
    """The SessionStart `[seats]` line: stalled seats named WITHOUT anyone asking.

    SILENT over an empty registry -- no events is no measurement, and a `0 live` would be
    believed. Only ROLED seats count (a lane, or a bound primary-checkout seat); an unbound
    session is counted, not named. An open batch with no live integrator is named too: the
    half-day with no integrator was a batch nobody could see was unreceived.
    """
    moment = now or _now()
    horizon = SURFACE_LOOKBACK_HOURS * 60.0
    recent = [s for s in seats(path, now=moment, **probes) if s.minutes_since <= horizon]
    if not recent:
        return None
    roled = [s for s in recent if s.role]
    counts = {state: sum(1 for s in roled if s.state == state) for state in STATES}
    line = ("[seats] " + " / ".join(f"{counts[s]} {s}" for s in STATES)
            + f" (last {SURFACE_LOOKBACK_HOURS:.0f} h; {len(recent) - len(roled)} unbound)")
    for state in ("wedged", "starved"):
        named = [_label(s) for s in roled if s.state == state]
        if named:
            line += f" / {state.upper()}: " + "; ".join(named)
    unreceived = [b.upper() for b in open_batches
                  if not any(s.role == "integrator" and s.batch == b.upper()
                             and s.state == "live" for s in roled)]
    if unreceived:
        line += (" / NO LIVE INTEGRATOR for batch " + ", ".join(sorted(set(unreceived)))
                 + " -- bind one: `seat_registry.py bind --role integrator --batch <B>`")
    return line


# ============================================================================================ CLI

@click.group(help="The seat registry ([#833]). State is written by hook events only.")
def cli() -> None:                                           # pragma: no cover -- click plumbing
    pass


@cli.command("bind")
@click.option("--role", required=True, type=click.Choice(ROLES))
@click.option("--batch", required=True)
def cmd_bind(role: str, batch: str) -> None:
    """Bind THIS session (CLAUDE_CODE_SESSION_ID) to a role and batch. Writes no state."""
    session = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    if not session:
        click.echo("REFUSED [unknown-role]: CLAUDE_CODE_SESSION_ID is unset -- bind from inside "
                   "the seat's own Claude Code session; a typed session id is not accepted")
        raise SystemExit(1)
    try:
        row = bind(role, batch, session_id=session)
    except SeatRefusal as exc:
        click.echo(str(exc))
        raise SystemExit(1) from exc
    click.echo(f"bound {row['session_id']} as {row['role']} for batch {row['batch']}")


@cli.command("show")
def cmd_show() -> None:
    """Print every seat seen in the lookback window, with its read state."""
    horizon = SURFACE_LOOKBACK_HOURS * 60.0
    for seat in seats():
        if seat.minutes_since <= horizon:
            click.echo(f"{seat.state:8} {seat.role or 'unbound':10} {seat.batch or '-':4} "
                       f"{seat.session_id} {seat.lane or ''} last={seat.last_kind} "
                       f"{seat.minutes_since:.0f} min")


if __name__ == "__main__":
    cli()
