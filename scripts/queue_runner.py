#!/usr/bin/env python
"""queue_runner.py -- code runs the queue on events (R130, [#1633]).

Three event sources, one fire per NEW event:

  HANDBACK  a flush-left `HANDBACK ` line in `<transport>/to-browser/SESSION-<slug>.md` or
            `SESSION-<slug>-repair-<n>.md` of a batch lane (a lane ended, a local slot freed)
            -> ONE `dispatch.py queue` pass over the batch's contracts (no --watch).
  MERGED /  a `STATE <lane> MERGED|FAILED <sha> <time> <min>` line in the integrator's receipt
  FAILED    -> ONE `dispatch.py queue` pass.
  REFUSED   `<transport>/to-browser/REFUSED-<slug>.md` carrying `from: the INTEGRATOR` and
            `repair N of 2` -> ONE `dispatch.py repair <slug> <contract> --model M --effort E
            --attempt N --batch B`, M and E read off the contract's head table row.

The seen-events ledger is `logs/receipts/QUEUE-RUNNER-<batch>.jsonl` (gitignored runtime state),
so a restart never refires. `--dry-run` READS the ledger and prints what it would fire; it never
writes the ledger and never fires, so a dry run can never suppress a later live event.

Every event is first run through the existing `P1DispatchLane` machine (`gen_process_diagrams`):
the lane's state comes from its ledger history (a lane with none is adopted at the precondition
state of its first event), the event's transitions are sent, and an event the machine does not
allow fires nothing and is recorded `machine-refused`. Every fire runs `dispatch.py` with
`DISPATCH_CALLER=queue_runner`, which `dispatch.py` writes into the LAUNCH receipt as `caller`.

USAGE:
    uv run --locked python scripts/queue_runner.py watch --batch E3.0 \\
        --state-file <integrator receipt> --transport <root> --contracts <LANE files...> \\
        [--interval 60] [--once] [--dry-run]

A `repair 3 of 2` REFUSED file is outside `dispatch.py repair`'s domain: it is the event that takes the lane,
through the machine, into `failed`, and it fires ONE `dispatch.py queue` pass (not a repair) so dependents are
held and the slot is released at the moment the lane fails. A later integrator `STATE <lane> FAILED` line for a
lane already `failed` is an event the machine does not allow, so it is refused and recorded with no fire; it
is never double-fired (dispatcher ruling 2026-11-01, option C). An existing ledger that cannot be read, or has a
malformed row, halts the runner (LedgerHalt, exit 1) rather than being read as empty and refiring.

`--contracts` takes several values, which click cannot do for one option, so this CLI is argparse.
Event order within one pass is fixed: handbacks (file name, then line order), state lines (file
order), refusals (file name).
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping, Optional, Sequence

from statemachine.exceptions import TransitionNotAllowed

try:  # one machine, one queue reader: reused, never copied. The bare names come first so a test (and a
    # script run as `python scripts/queue_runner.py`) sees the SAME class objects, not a `scripts.` twin.
    import dispatch as _dispatch
    import gen_process_diagrams as _gpd
except ImportError:  # pragma: no cover
    from scripts import dispatch as _dispatch
    from scripts import gen_process_diagrams as _gpd

logger = logging.getLogger("queue_runner")

REPO_ROOT = Path(__file__).resolve().parent.parent
MACHINE = _gpd.P1DispatchLane

CALLER_ENV = "DISPATCH_CALLER"
CALLER_VALUE = "queue_runner"
FIRE_TIMEOUT_S = 1800

KINDS = ("handback", "merged", "failed", "refused")
#: A lane the runner has never seen is adopted at the state its first event presupposes.
ADOPTED_STATE = {"handback": "running", "merged": "integrating", "failed": "integrating",
                 "refused": "integrating"}

STATUS_FIRED = "fired"
STATUS_FAILED = "FIRE-FAILED"      # a non-zero fire: recorded once, never retried (only a NEW event fires again)
STATUS_RECORDED = "recorded"            # an event that needs no fire (a lane failing, `repair 3 of 2`)
STATUS_MACHINE_REFUSED = "machine-refused"
STATUS_OBSERVED = "observed"            # a lane the queue pass reported FIRE for
_SEEN_STATUSES = (STATUS_FIRED, STATUS_RECORDED, STATUS_MACHINE_REFUSED, STATUS_OBSERVED, STATUS_FAILED)

_SESSION_FILE = re.compile(r"^SESSION-(?P<stem>.+)\.md$")
_REPAIR_SUFFIX = re.compile(r"^(?P<slug>.+)-repair-\d+$")
_REFUSED_FILE = re.compile(r"^REFUSED-(?P<slug>.+)\.md$")
_FROM_INTEGRATOR = re.compile(r"^from:[ \t]*the INTEGRATOR[ \t]*$", re.MULTILINE)
_REPAIR_N = re.compile(r"^repair[ \t]+(?P<n>\d+)[ \t]+of[ \t]+2[ \t]*$", re.MULTILINE)
_FENCE = re.compile(r"^(```|~~~)")
_FIRE_LINE = re.compile(r"\[queue\] FIRE (?P<slug>\S+?):")
_HEAD_ROW = re.compile(r"^\|[ \t]*Model[ \t]*\|[ \t]*Mode[ \t]*\|[ \t]*Effort[ \t]*\|[ \t]*$", re.MULTILINE)


@dataclass(frozen=True)
class Event:
    kind: str                   # handback | merged | failed | refused
    lane: str                   # the batch lane's slug
    key: str                    # unique id of this event; the ledger's idempotency key
    attempt: Optional[int]      # N of `repair N of 2` (refused only)
    source: str                 # the file name the event was read from
    text: str                   # the line (handback / state) or the REFUSED file's content


@dataclass(frozen=True)
class FireResult:
    returncode: int
    output: str


@dataclass(frozen=True)
class Fired:
    verb: str                   # queue | repair
    lane: str
    kind: str
    argv: list
    returncode: Optional[int] = None    # None: a dry run, nothing was fired


# --- reading the three event sources ---------------------------------------------------------------

def _read(path: Path) -> str:
    try:
        return Path(path).read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


def _flush_left_lines(text: str, prefix: str) -> list[str]:
    """Lines that START with `prefix`, outside any fenced block (an indented or quoted line is no event)."""
    out, fenced = [], False
    for line in text.splitlines():
        if _FENCE.match(line.lstrip()):
            fenced = not fenced
            continue
        if not fenced and line.startswith(prefix):
            out.append(line.rstrip())
    return out


def _session_lane(name: str, slugs: set) -> Optional[str]:
    match = _SESSION_FILE.match(name)
    if not match:
        return None
    stem = match.group("stem")
    if stem in slugs:
        return stem
    repair = _REPAIR_SUFFIX.match(stem)
    return repair.group("slug") if repair and repair.group("slug") in slugs else None


def _natural_name(path: Path) -> list:
    """File-name order with digit runs compared as numbers, so `-repair-2` sorts before `-repair-10`."""
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", path.name)]


def collect_events(*, transport: Path, state_file: Path, slugs: Sequence[str]) -> list[Event]:
    """Every event the three sources carry, in the fixed order; the ledger decides which are new."""
    known = set(slugs)
    events: list[Event] = []
    inbox = Path(transport) / "to-browser"
    try:
        files = sorted((p for p in inbox.iterdir() if p.is_file()), key=_natural_name) if inbox.is_dir() else []
    except OSError as exc:      # a Drive folder that vanishes mid-sync reads as empty this pass
        logger.warning("%s: unreadable this pass (%s)", inbox, exc)
        files = []

    for path in files:
        lane = _session_lane(path.name, known)
        if lane is None:
            continue
        for line in _flush_left_lines(_read(path), "HANDBACK "):
            events.append(Event("handback", lane, f"handback|{path.name}|{line}", None, path.name, line))

    for match in _dispatch._STATE_LINE_RE.finditer(_read(state_file)):
        state, lane = match.group("state"), match.group("slug")
        if state in ("MERGED", "FAILED") and lane in known:
            line = match.group(0).strip()
            events.append(Event(state.lower(), lane, f"state|{line}", None, Path(state_file).name, line))

    for path in files:
        named = _REFUSED_FILE.match(path.name)
        if not named or named.group("slug") not in known:
            continue
        text = _read(path)
        repairs = list(_REPAIR_N.finditer(text))
        repair = repairs[-1] if repairs else None   # the newest refusal is the last one a file names
        if not _FROM_INTEGRATOR.search(text) or not repair:
            continue
        attempt = int(repair.group("n"))
        events.append(Event("refused", named.group("slug"), f"refused|{path.name}|{attempt}",
                            attempt, path.name, text))
    return events


# --- the seen-events ledger ------------------------------------------------------------------------

class LedgerHalt(RuntimeError):
    """A ledger append failed AFTER a fire: the outcome exists only in memory, so a restart would
    refire it. The runner fires nothing more and exits 1 (dispatcher ruling 2026-11-01)."""


class Ledger:
    """`QUEUE-RUNNER-<batch>.jsonl`: one row per event outcome. `persist=False` keeps rows in memory
    only, which is what a dry run needs to walk a lane through several events without writing."""

    def __init__(self, path: Path, *, persist: bool = True):
        self.path, self.persist = Path(path), persist
        self.rows: list[dict] = []
        self.halted = False         # sticky: set when an append failed after a fire (see LedgerHalt)
        try:
            lines = self.path.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            lines = []              # no ledger yet: an empty one
        except (OSError, UnicodeDecodeError) as exc:
            # An existing ledger we cannot read may hold fired events: reading it as empty would refire them.
            raise LedgerHalt(f"ledger {self.path} exists but cannot be read ({exc}); nothing fires") from exc
        for number, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError as exc:
                raise LedgerHalt(f"ledger {self.path} line {number} is not valid JSON ({exc}); nothing fires") from exc
            if not isinstance(row, dict):
                raise LedgerHalt(f"ledger {self.path} line {number} is not a JSON object; nothing fires")
            self.rows.append(row)

    def writable(self) -> bool:
        """Can a row be appended right now? A live pass checks before it fires: a fire whose outcome
        cannot be made durable would be fired again by the next restart, so nothing fires instead."""
        if not self.persist:
            return True
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8", newline="\n"):
                pass
            return True
        except OSError as exc:
            logger.error("ledger %s is not writable (%s)", self.path, exc)
            return False

    def in_memory_copy(self) -> "Ledger":
        copy = Ledger.__new__(Ledger)
        copy.path, copy.persist, copy.rows = self.path, False, [dict(r) for r in self.rows]
        copy.halted = False
        return copy

    def failures(self, key: str) -> int:
        return sum(1 for r in self.rows if r.get("key") == key and r.get("status") == STATUS_FAILED)

    def seen(self, key: str) -> bool:
        return any(r.get("key") == key and r.get("status") in _SEEN_STATUSES for r in self.rows)

    def lane_state(self, slug: str) -> Optional[str]:
        for row in reversed(self.rows):
            if row.get("lane") == slug and row.get("state_after"):
                return row["state_after"]
        return None

    def record(self, event: Event, status: str, *, state_after: Optional[str] = None,
               detail: str = "") -> None:
        row = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "key": event.key,
               "kind": event.kind, "lane": event.lane, "status": status, "state_after": state_after,
               "detail": detail}
        self.rows.append(row)       # in memory first: this process never refires what it just fired
        if self.persist:
            try:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                with self.path.open("a", encoding="utf-8", newline="\n") as fh:
                    fh.write(json.dumps(row, sort_keys=True) + "\n")
            except OSError as exc:
                self.halted = True
                logger.error("ledger %s is not writable (%s): %s %s is held in memory only, so a "
                             "restart can refire it; halting", self.path, exc, event.kind, event.lane)
                raise LedgerHalt(f"ledger {self.path} could not record {event.kind} {event.lane}: {exc}") from exc


# --- the machine ------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Plan:
    state_after: str
    fire: bool                  # does the event fire dispatch.py at all
    refusal: str = ""           # non-empty: the machine does not allow the event


def _walk(state: str, facts, events: Sequence[str]) -> str:
    machine = MACHINE(facts, start_value=state)
    for event in events:
        machine.send(event)
    return machine.configuration[0].id


def plan_event(event: Event, state: str, substrate: str) -> Plan:
    """Send the event's transitions to a throwaway P1DispatchLane started at `state`."""
    if substrate not in ("local", "codespace"):   # `dispatch.SUBSTRATES`; a cloud lane has its own read-only path
        return Plan(state, False, refusal=f"substrate {substrate!r} has no handback path in this runner")
    handback_chain = ["handback", "to_integrator"] if substrate == "local" else ["box_done", "harvested"]
    if event.kind == "handback":
        facts = _gpd.LaneFacts(substrate=substrate)
        chain = handback_chain
        fire = True
    elif event.kind == "merged":
        facts, chain, fire = _gpd.LaneFacts(substrate=substrate, landed=True), ["merge"], True
    elif event.kind == "failed":
        facts = _gpd.LaneFacts(substrate=substrate, refusals=_gpd.REFUSAL_CAP)
        # from `running` the catch-up below lands the lane on `integrating` first, so `refusal` still leads
        chain, fire = (["refusal", "fail"] if state in ("integrating", "running") else ["fail"]), True
    else:  # refused: `repair N of 2` has N-1 refusals behind it
        attempt = event.attempt or 1
        facts = _gpd.LaneFacts(substrate=substrate, refusals=attempt - 1)
        if attempt > _gpd.REFUSAL_CAP:
            chain, fire = ["refusal", "fail"], True     # the event that fails the lane fires one queue pass
        else:
            chain, fire = ["refusal", "repair", "repaired"], True
    if state == "running" and event.kind != "handback":
        # The integrator can only write MERGED / FAILED / REFUSED for a lane that handed back. A lane the
        # ledger still holds `running` (its handback line not read yet, or a repair that was refused
        # again before the repair's own handback was seen) is caught up first, not dropped for good.
        chain = handback_chain + chain
    try:
        return Plan(_walk(state, facts, chain), fire)
    except TransitionNotAllowed as exc:
        return Plan(state, False, refusal=str(exc))


def _observe_fired_lanes(ledger: Ledger, event: Event, output: str, by_slug: Mapping) -> None:
    """A lane the queue pass FIRED is `running` from now on, so its handback is a legal event."""
    for slug in dict.fromkeys(m.group("slug") for m in _FIRE_LINE.finditer(output)):
        if slug not in by_slug or ledger.lane_state(slug) not in (None, "queued"):
            continue
        facts = _gpd.LaneFacts(substrate=by_slug[slug].substrate)
        chain = ["evaluate", "prelaunch_passed", "spawned"]
        try:
            after = _walk("queued", facts, chain)
        except TransitionNotAllowed:
            continue
        ledger.record(Event("fire", slug, f"fire|{event.key}|{slug}", None, event.source, ""),
                      STATUS_OBSERVED, state_after=after, detail="reported FIRE by the queue pass")


# --- the contracts' head row ------------------------------------------------------------------------

def head_row(contract: Path) -> tuple[str, str]:
    """(model, effort) from the contract's `| Model | Mode | Effort |` table data row."""
    text = Path(contract).read_text(encoding="utf-8-sig", errors="replace")   # an OSError is transient: it propagates
    head = _HEAD_ROW.search(text)
    if head:
        for line in text[head.end():].splitlines():
            cells = [c.strip().strip("`*") for c in line.strip().strip("|").split("|")]
            if line.strip().startswith("|") and len(cells) >= 3 and not set(cells[0]) <= set("-: "):
                return cells[0], cells[2]
    raise ValueError(f"{contract}: no `| Model | Mode | Effort |` head row to read a repair's model/effort from")


# --- one pass ---------------------------------------------------------------------------------------

def subprocess_fire(argv: list, env: Mapping) -> FireResult:
    """Run `scripts/dispatch.py <argv>` with `env`; the real fire."""
    cmd = [sys.executable, str(REPO_ROOT / "scripts" / "dispatch.py"), *argv]
    try:
        proc = subprocess.run(cmd, env=dict(env), cwd=REPO_ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=FIRE_TIMEOUT_S, check=False)
    except subprocess.TimeoutExpired:
        return FireResult(124, f"dispatch.py {argv[0]} timed out after {FIRE_TIMEOUT_S}s")
    except OSError as exc:      # the child never started: a failed fire like any other, recorded once
        return FireResult(127, f"dispatch.py {argv[0]} did not start: {exc}")
    return FireResult(proc.returncode, (proc.stdout or "") + (proc.stderr or ""))


def _default_echo(line: str) -> None:
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


def run_once(*, batch: str, state_file: Path, transport: Path, contracts: Sequence[Path],
             ledger_path: Path, fire: Callable[[list, dict], FireResult] = subprocess_fire,
             dry_run: bool = False, echo: Optional[Callable[[str], None]] = None,
             ledger: Optional[Ledger] = None) -> list[Fired]:
    """One pass over the three sources: fire once per NEW event. Returns the fires attempted
    (a dry run: the fires it would make). The watch loop passes ONE `ledger` for its whole life, so a
    ledger file that cannot be written still stops this process refiring on every pass."""
    echo = echo or _default_echo
    lanes = _dispatch.load_queue(list(contracts))
    by_slug = {lane.slug: lane for lane in lanes}
    if ledger is None:
        ledger = Ledger(ledger_path, persist=not dry_run)
    elif dry_run:
        ledger = ledger.in_memory_copy()    # a dry run never writes, whichever ledger it is handed
    if ledger.halted:
        raise LedgerHalt(f"ledger {ledger.path} halted the runner earlier; nothing fires")
    env = {**os.environ, CALLER_ENV: CALLER_VALUE}
    queue_argv = ["queue", "--batch", batch, "--state-file", str(state_file),
                  *[str(c) for c in contracts]]
    fired: list[Fired] = []
    warned = _WARNED_KEYS

    def handle(event: Event) -> None:
        if ledger.seen(event.key):
            return
        lane = by_slug[event.lane]
        state = ledger.lane_state(event.lane) or ADOPTED_STATE[event.kind]
        plan = plan_event(event, state, lane.substrate)
        if plan.refusal:
            logger.warning("%s %s: refused by the machine at %s (%s)", event.kind, event.lane, state,
                           plan.refusal)
            ledger.record(event, STATUS_MACHINE_REFUSED, detail=plan.refusal)
            return
        if not plan.fire:
            ledger.record(event, STATUS_RECORDED, state_after=plan.state_after,
                          detail=f"{event.kind}: no dispatch.py call")
            return

        if event.kind == "refused" and (event.attempt or 1) <= _gpd.REFUSAL_CAP:
            try:
                model, effort = head_row(lane.contract)
            except OSError as exc:      # a contract mid-sync is not a failed fire: retried next pass, uncounted
                logger.warning("%s: unreadable this pass (%s)", lane.contract, exc)
                return
            except ValueError as exc:   # no head row: nothing was fired, so it costs no attempt and is
                if event.key not in warned:     # retried once the contract is fixed; logged once per event
                    warned.add(event.key)
                    logger.error("%s", exc)
                return
            verb = "repair"
            argv = ["repair", event.lane, str(lane.contract), "--model", model, "--effort", effort,
                    "--attempt", str(event.attempt), "--batch", batch]
        else:
            verb, argv = "queue", list(queue_argv)

        if dry_run:
            detail = f"(attempt {event.attempt})" if verb == "repair" else f"({event.kind})"
            echo(f"[queue-runner] would-fire {verb} {event.lane} {detail}")
            fired.append(Fired(verb, event.lane, event.kind, argv))
            ledger.record(event, STATUS_FIRED, state_after=plan.state_after)
            return

        if not ledger.writable():       # fail closed: an outcome that cannot be recorded is not fired
            return
        try:
            result = fire(argv, env)
        except Exception as exc:    # an injected or custom fire that raises counts as a failed fire
            logger.exception("fire raised for %s %s", event.kind, event.lane)
            result = FireResult(125, f"fire raised {type(exc).__name__}: {exc}")
        fired.append(Fired(verb, event.lane, event.kind, argv, result.returncode))
        if result.returncode == 0:
            logger.info("fired dispatch.py %s for %s %s", verb, event.kind, event.lane)
            ledger.record(event, STATUS_FIRED, state_after=plan.state_after)
            if verb == "queue":
                _observe_fired_lanes(ledger, event, result.output, by_slug)
        else:
            logger.error("dispatch.py %s for %s %s exited %s: %s", verb, event.kind, event.lane,
                         result.returncode, result.output.strip()[-400:])
            tail = result.output.strip()[-400:].replace("\n", " | ")
            ledger.record(event, STATUS_FAILED, detail=f"exit {result.returncode}: {tail}")

    for event in collect_events(transport=transport, state_file=state_file, slugs=list(by_slug)):
        try:
            handle(event)
        except LedgerHalt:
            raise
        except Exception:  # one bad event must not end the watch: it is logged and the next one runs
            logger.exception("%s %s: unhandled error; the event stays unrecorded and is retried next pass",
                             event.kind, event.lane)
    return fired


# --- one runner per batch ---------------------------------------------------------------------------

_WARNED_KEYS: set = set()    # events whose contract could not be parsed, so the log says it once, not every pass
_HELD_LOCKS: list = []       # the open lock files; a handle that is garbage collected would drop its lock


class RunnerAlreadyRunning(RuntimeError):
    """Another process holds the batch's runner lock."""


def acquire_single_instance(lock_path: Path):
    """Hold an exclusive OS lock on `lock_path` for the life of the returned file object (released by
    the OS when the process dies, so there is no stale lock to clean). Two watchers on one ledger would
    each see an unseen event and each fire it."""
    Path(lock_path).parent.mkdir(parents=True, exist_ok=True)
    handle = open(lock_path, "a+b")
    try:
        if os.name == "nt":
            import msvcrt
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        handle.close()
        raise RunnerAlreadyRunning(f"{lock_path} is held by another queue runner") from exc
    return handle


# --- the CLI ------------------------------------------------------------------------------------------

def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="queue_runner.py", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    watch = sub.add_parser("watch", help="read the three event sources and fire dispatch.py once per new event")
    watch.add_argument("--batch", required=True, help="the batch id, E<major>.<minor>")
    watch.add_argument("--state-file", required=True, type=Path, help="the integrator's own session receipt")
    watch.add_argument("--transport", required=True, type=Path, help="the transport root (holds to-browser/)")
    watch.add_argument("--contracts", required=True, nargs="+", type=Path, help="the batch's LANE contracts")
    watch.add_argument("--interval", type=float, default=60.0, help="seconds between passes (default 60)")
    watch.add_argument("--once", action="store_true", help="one pass, then exit")
    watch.add_argument("--dry-run", action="store_true",
                       help="one pass; print what would fire; write nothing and fire nothing")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.batch):
        parser.error(f"--batch {args.batch!r} is not a plain batch id (E<major>.<minor>)")
    if args.interval < 1:
        parser.error("--interval must be at least 1 second")
    # Absolute paths: the fired `dispatch.py` runs with the hub as its cwd, this process wherever it started.
    state_file, transport = args.state_file.resolve(), args.transport.resolve()
    contracts = [c.resolve() for c in args.contracts]
    ledger_path = _dispatch.receipts_dir() / f"QUEUE-RUNNER-{args.batch}.jsonl"
    once = args.once or args.dry_run
    failed = False
    if not args.dry_run:        # a dry run writes nothing, so any number may run beside a live watch
        try:
            _HELD_LOCKS.append(acquire_single_instance(ledger_path.with_suffix(".lock")))
        except RunnerAlreadyRunning as exc:
            logger.error("%s", exc)
            return 3
    try:
        ledger = Ledger(ledger_path, persist=not args.dry_run)
    except LedgerHalt as exc:       # an existing ledger that cannot be trusted: fire nothing
        logger.error("%s", exc)
        return 1
    while True:
        try:
            fired = run_once(batch=args.batch, state_file=state_file, transport=transport,
                             contracts=contracts, ledger_path=ledger_path, dry_run=args.dry_run,
                             ledger=ledger)
            failed = failed or any(f.returncode not in (None, 0) for f in fired)
        except KeyboardInterrupt:
            return 0
        except LedgerHalt as exc:   # an outcome that could not be made durable: fire nothing more
            logger.error("%s", exc)
            return 1
        except Exception:  # a pass that cannot run (a contract unreadable mid-sync) is logged, not fatal
            logger.exception("pass failed; the watch goes on")
            failed = True
        if once:
            return 1 if failed else 0
        try:
            time.sleep(args.interval)
        except KeyboardInterrupt:
            return 0


if __name__ == "__main__":
    logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
    sys.exit(main())
