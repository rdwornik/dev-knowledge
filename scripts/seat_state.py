#!/usr/bin/env python
"""seat_state.py -- the per-lane state an orchestrator seat hands to its own successor
(LANE-5B3-10-orchestrator-cycling, Done-contract item 1).

THE ABSENCE THIS FILLS. `DIGEST-WAVE5B-N2-2026-09-26.md` §5: a reboot left 5 records `running`
and the daemon respawned 20 jobs 1.5 h later; the integrator and dispatcher receipts that would
have told a fresh seat what was merged, in flight, queued, refused, failed or reported were two
free-text logs (59 KB and 70 KB by the batch's end) -- readable by a human at leisure, not
`--rebind`-able by a session that has just started and does not want to reread the whole night.
`DIGEST-WAVE5B-N2-2026-09-26.md` §5's own ask: "a resume path (integrator/dispatcher re-bind from
logs + receipts)". This module is that path: ONE small file, written after every state change,
that a fresh session reads instead of the log.

IT IS A SIDECAR, NOT A REPLACEMENT. `to-browser/SESSION-<role>-<batch>.md` stays the seat's
prose receipt -- the record a human (and `learning_distiller.py`) reads. This file is the same
facts, structured, so a program can answer "what is still open" without parsing prose. Losing it
loses nothing a fresh session could not eventually reconstruct by rereading the receipt; it only
loses the shortcut.

THE SIX STATES ARE A CLOSED ENUM (`LANE_STATES`), chosen to span both seats that write here:
  * `QUEUED`     -- the dispatcher has not fired it yet (a dependency, the cap or the RAM floor).
  * `IN-FLIGHT`  -- fired and building, held mid-repair, or picked up by the integrator and not
                    yet verified. The integrator's own receipt vocabulary calls this `WAITING`
                    (`templates/integrator-order-template.md`'s Receipt bullet); this schema uses
                    one name for the one state, and a writer maps `WAITING` to `IN-FLIGHT`.
  * `MERGED`, `REFUSED`, `FAILED`, `REPORTED` -- terminal, and spelled exactly as the integrator's
    receipt line and the dispatcher's cloud-lane log already spell them, because a schema that
    renamed a terminal state on the way in would make its own evidence pointer disagree with the
    receipt line it cites.

EVERY LANE ROW CARRIES EVIDENCE, NEVER A BARE STATE. `{session_file, receipt_line, sha}` --
the session file is the receipt a human would read to confirm the claim; `receipt_line` is that
receipt's own line, copied verbatim (not a line NUMBER, which a growing receipt would invalidate
by the next append); `sha` is the merge commit where one exists, `None` otherwise (`QUEUED` and
most `IN-FLIGHT` rows have none yet). A state with no evidence is not a fact this module accepts
-- see `_validate_lane`.

TORN AND STALE ARE BOTH REFUSED, AND THEY ARE DIFFERENT FAILURES. Torn is a file a reader cannot
parse as this schema at all -- truncated by a crash mid-write, or hand-edited into something
`from_dict` cannot rebuild. Stale is a file that parses perfectly and is simply too old to trust:
the cycle rule this file exists to serve (`templates/*-order-template.md`'s new Cycle section)
hands over "about every 2 h or at a context threshold", so a file nobody has touched in longer
than that is a sign the writing seat died or wedged mid-cycle without writing its successor a
fresh state -- exactly the N2 reboot's own failure shape, one layer down. Trusting it would let a
fresh session believe a lane is still `IN-FLIGHT` when the seat that could confirm that has been
gone for hours. `read_state`'s `max_age_min` makes that refusal a parameter, not a guess baked in.

WRITING IS ATOMIC (temp file + `os.replace`), which is the module's own defence against
producing a torn file in the first place -- a crash mid-`json.dump` leaves the OLD file in place,
never a half-written one. The torn-file test still exists because a reader has to survive a file
THIS module did not write (hand edit, disk corruption, a future writer with a bug); atomicity
narrows how a torn file can arise, it does not make the reader assume one never will.

HONEST LIMITS
  * `base_sha` is carried, never checked against git here. Whether it is still an ancestor of the
    current tip is the F2 check (`git merge-base --is-ancestor`) the batch's common rules already
    run at a lane's own first step; duplicating a git call in a module that also has to run
    inside a unit test with no repository fixture would make the common case (a test) pay for the
    rare one (a real staleness git can detect that time cannot).
  * Staleness is read from `written_ts` alone. A seat that writes the file, then wedges for two
    hours without writing again, reads exactly like a seat that died -- there is no heartbeat
    finer than the write this module records. That is `seat_registry.py`'s own honest limit
    (`WEDGED_AFTER_MIN`) one field over: a state that is "read", never "polled".
  * Nothing here enforces that a lane's states move only forward (`QUEUED` -> `IN-FLIGHT` ->
    terminal). A caller can write `MERGED` and then `QUEUED` for the same lane and this module
    will not refuse it -- the receipt line the caller cites is the audit trail for that, not this
    module's job to police.
"""
from __future__ import annotations

import contextlib
import json
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Optional, Sequence

import click

SCHEMA = "dev-knowledge-seat-state/1"

#: The two seats that cycle under this contract (`templates/*-order-template.md`'s new Cycle
#: section). `seat_registry.ROLES` also lists `lane` and `browser`; neither hands over to a fresh
#: session of itself mid-batch, so neither writes this file.
ROLES: tuple[str, ...] = ("integrator", "dispatcher")

#: The closed enum a lane row's `state` must be one of. See the module docstring for what each
#: means and which seat writes it.
LANE_STATES: tuple[str, ...] = ("QUEUED", "IN-FLIGHT", "MERGED", "REFUSED", "FAILED", "REPORTED")

#: The integrator receipt's own word for `IN-FLIGHT` (`templates/integrator-order-template.md`'s
#: Receipt bullet: `STATE <lane> MERGED|REFUSED|WAITING|FAILED ...`). A writer building rows from
#: that receipt maps it here rather than teaching the receipt a second vocabulary.
WAITING_ALIAS = "WAITING"


class SeatStateError(RuntimeError):
    """A state file that cannot be trusted -- torn, stale, or built from an invalid lane row.
    Raised rather than degraded: a fresh session that silently got an empty state back would
    believe the batch had nothing open, which is the one belief this module must never hand out
    by accident."""


@dataclass(frozen=True)
class LaneEvidence:
    session_file: str
    receipt_line: Optional[str] = None
    sha: Optional[str] = None

    def to_dict(self) -> dict:
        return {"session_file": self.session_file, "receipt_line": self.receipt_line,
                "sha": self.sha}

    @classmethod
    def from_dict(cls, data: Mapping) -> "LaneEvidence":
        return cls(session_file=str(data.get("session_file") or ""),
                   receipt_line=data.get("receipt_line"), sha=data.get("sha"))


@dataclass(frozen=True)
class LaneRow:
    state: str
    evidence: LaneEvidence
    ts: str
    sha: Optional[str] = None

    def to_dict(self) -> dict:
        return {"state": self.state, "sha": self.sha, "ts": self.ts,
                "evidence": self.evidence.to_dict()}

    @classmethod
    def from_dict(cls, data: Mapping) -> "LaneRow":
        return cls(state=str(data.get("state") or ""), sha=data.get("sha"),
                   ts=str(data.get("ts") or ""),
                   evidence=LaneEvidence.from_dict(data.get("evidence") or {}))


@dataclass
class SeatStateFile:
    """One seat's whole state file, as read back. See the module docstring for the schema."""
    role: str
    batch: str
    base_sha: str
    written_ts: str
    written_by: str
    lanes: dict[str, LaneRow] = field(default_factory=dict)
    #: Cycle bookkeeping ([#1636]), written by the Stop hook through `seat_cycle.stop_check`:
    #: threshold crossings, the highest context seen, `isCompactSummary` records (target 0), and
    #: the CROSSED lines themselves. Absent in a file written before the fields existed -> 0.
    cycles: int = 0
    max_context: int = 0
    compactions: int = 0
    crossed: list[str] = field(default_factory=list)
    #: compactions seen per seat session; `compactions` is their SUM, so a successor's do not mask a predecessor's
    compaction_sessions: dict[str, int] = field(default_factory=dict)

    def in_flight(self) -> list[str]:
        """The lanes a fresh session still has to act on -- `QUEUED` or `IN-FLIGHT` -- sorted so
        two readers of the same file agree on order without a second comparison."""
        return sorted(lane for lane, row in self.lanes.items()
                     if row.state in ("QUEUED", "IN-FLIGHT"))

    def by_state(self, state: str) -> list[str]:
        return sorted(lane for lane, row in self.lanes.items() if row.state == state)

    def to_dict(self) -> dict:
        return {"schema": SCHEMA, "role": self.role, "batch": self.batch,
                "base_sha": self.base_sha, "written_ts": self.written_ts,
                "written_by": self.written_by,
                "lanes": {lane: row.to_dict() for lane, row in self.lanes.items()},
                "cycles": self.cycles, "max_context": self.max_context,
                "compactions": self.compactions, "crossed": list(self.crossed),
                "compaction_sessions": dict(self.compaction_sessions)}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _normalize_state(state: str) -> str:
    return WAITING_ALIAS if state == WAITING_ALIAS else state


def _validate_lane(lane: str, row: object) -> LaneRow:
    if not isinstance(row, Mapping):
        raise SeatStateError(
            f"lane {lane!r}: row is a {type(row).__name__}, not an object -- torn, refused "
            f"rather than read as though it were a state")
    state = _normalize_state(str(row.get("state") or ""))
    if state == WAITING_ALIAS:
        state = "IN-FLIGHT"
    if state not in LANE_STATES:
        raise SeatStateError(
            f"lane {lane!r}: state {row.get('state')!r} is outside "
            f"{{{', '.join(LANE_STATES)}}} (or {WAITING_ALIAS!r}, mapped to IN-FLIGHT)")
    evidence = row.get("evidence")
    if not isinstance(evidence, Mapping) or not evidence.get("session_file"):
        raise SeatStateError(
            f"lane {lane!r}: no evidence.session_file -- a state with nothing a reader could "
            f"confirm it against is not a fact this module accepts")
    return LaneRow(state=state, sha=row.get("sha"), ts=str(row.get("ts") or _now()),
                  evidence=LaneEvidence.from_dict(evidence))


def build_state(*, role: str, batch: str, base_sha: str, lanes: Mapping[str, Mapping],
                written_by: str = "", now: Optional[str] = None, cycles: int = 0,
                max_context: int = 0, compactions: int = 0,
                crossed: Sequence[str] = (),
                compaction_sessions: Optional[Mapping[str, int]] = None) -> SeatStateFile:
    """Validate inputs and assemble a `SeatStateFile`, without touching disk. Split out of
    `write_state` so a caller (and a test) can build one in memory."""
    if role not in ROLES:
        raise SeatStateError(f"role {role!r} is outside {{{', '.join(ROLES)}}}")
    if not batch:
        raise SeatStateError("a state file names no batch")
    if not base_sha:
        raise SeatStateError("a state file names no base_sha")
    validated = {lane: _validate_lane(lane, row) for lane, row in lanes.items()}
    return SeatStateFile(role=role, batch=str(batch).upper(), base_sha=base_sha,
                         written_ts=now or _now(), written_by=written_by, lanes=validated,
                         cycles=cycles, max_context=max_context, compactions=compactions,
                         crossed=list(crossed),
                         compaction_sessions=dict(compaction_sessions or {}))


def _primary_checkout(root: Path) -> Optional[Path]:
    """The primary checkout of a linked worktree (its `.git` is a `gitdir: <primary>/.git/worktrees/x` file)."""
    marker = Path(root) / ".git"
    if not marker.is_file():
        return None
    try:
        gitdir = marker.read_text(encoding="utf-8").split("gitdir:", 1)[1].strip()
    except (OSError, IndexError):
        return None
    for parent in Path(gitdir).parents:
        if parent.name == ".git":
            return parent.parent
    return None


def state_folders(repo_root: Path) -> list[Path]:
    """Where seat state files live, in PRECEDENCE order: the transport's (`$CLAUDE_PROMPTS_DIR/to-browser`,
    which is what the seat templates' `to-browser/` names), then the checkout's, then -- for a linked
    worktree -- the primary checkout's. Existing folders only, de-duplicated by where they resolve."""
    out: list[Path] = []
    prompts = os.environ.get("CLAUDE_PROMPTS_DIR", "").strip()
    primary = _primary_checkout(repo_root)
    for cand in (Path(prompts) / "to-browser" if prompts else None, Path(repo_root) / "to-browser",
                 primary / "to-browser" if primary else None):
        if cand is not None and cand.is_dir() and all(cand.resolve() != o.resolve() for o in out):
            out.append(cand)
    return out


def is_state_file(path: Path) -> bool:
    """True when `path` parses as this module's schema (the precondition of any counter update)."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(data, dict) and data.get("schema") == SCHEMA


LOCK_TIMEOUT_S = 2.0   # a Stop hook must not stall a turn ending on a stale lock file


@contextlib.contextmanager
def locked(path: Path):
    """The read-merge-write of a state file as ONE step: `transport.py`'s per-destination
    `O_EXCL` lock (library-first -- the idiom this repo already has), so the hook's counter update
    and a by-hand `write_state` never interleave and lose one another's fields."""
    try:
        from transport import _DestinationLock  # noqa: PLC0415
    except ImportError:
        from scripts.transport import _DestinationLock  # type: ignore[no-redef]  # noqa: PLC0415
    path.parent.mkdir(parents=True, exist_ok=True)
    with _DestinationLock(path, LOCK_TIMEOUT_S):
        yield


def write_state(path: Path, *, role: str, batch: str, base_sha: str, lanes: Mapping[str, Mapping],
                written_by: str = "", now: Optional[str] = None, cycles: Optional[int] = None,
                max_context: Optional[int] = None, compactions: Optional[int] = None,
                crossed: Optional[Sequence[str]] = None) -> SeatStateFile:
    """Build and write the state file, ATOMICALLY: a temp file in the same directory, then
    `os.replace` -- a crash mid-write leaves the previous file intact rather than a half-written
    one, which is the module's own defence against manufacturing the torn file `read_state`
    exists to refuse."""
    path = Path(path)
    with locked(path):
        kept = _read_counters(path)           # a by-hand rewrite must not erase the hook's bookkeeping
        state = build_state(role=role, batch=batch, base_sha=base_sha, lanes=lanes,
                            written_by=written_by, now=now,
                            cycles=kept["cycles"] if cycles is None else cycles,
                            max_context=kept["max_context"] if max_context is None else max_context,
                            compactions=kept["compactions"] if compactions is None else compactions,
                            crossed=kept["crossed"] if crossed is None else crossed,
                            compaction_sessions=kept["compaction_sessions"])
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(state.to_dict(), fh, indent=2, sort_keys=True)
                fh.write("\n")
            os.replace(tmp_name, path)
        finally:
            Path(tmp_name).unlink(missing_ok=True)
    return state


def _read_counters(path: Path) -> dict:
    """The cycle fields of an existing file, tolerant: unreadable, torn or old -> zeros. Staleness is
    deliberately not checked -- these are history, not a belief about what is open."""
    out: dict = {"cycles": 0, "max_context": 0, "compactions": 0, "crossed": [],
                 "compaction_sessions": {}}
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return out
    if not isinstance(data, Mapping):
        return out
    for key in ("cycles", "max_context", "compactions"):
        try:
            out[key] = int(data.get(key) or 0)
        except (TypeError, ValueError):
            pass
    per_session = data.get("compaction_sessions")
    if isinstance(per_session, Mapping):
        try:
            out["compaction_sessions"] = {str(k): int(v) for k, v in per_session.items()}
        except (TypeError, ValueError):
            pass
    crossed = data.get("crossed")
    if isinstance(crossed, list):
        out["crossed"] = [str(x) for x in crossed]
    return out


def load_counters(path: Path) -> SeatStateFile:
    """A state file for REPORTING (the batch-close digest): identity plus the counters, with no
    staleness refusal -- a closed batch's file is old by definition. Lanes are not validated."""
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SeatStateError(f"no readable state file at {path}: {exc!r}") from exc
    if not isinstance(data, Mapping) or data.get("schema") != SCHEMA:
        raise SeatStateError(f"{path} is not a {SCHEMA} file")
    return SeatStateFile(role=str(data.get("role") or ""), batch=str(data.get("batch") or ""),
                         base_sha=str(data.get("base_sha") or ""),
                         written_ts=str(data.get("written_ts") or ""),
                         written_by=str(data.get("written_by") or ""), **_read_counters(path))


def update_counters(path: Path, *, max_context: int = 0, compactions: int = 0,
                    crossed_line: Optional[str] = None, session: Optional[str] = None) -> bool:
    """The Stop hook's write ([#1636]): raise `max_context`/`compactions` to the observed values and,
    given a CROSSED line not yet recorded, append it and bump `cycles`. Touches ONLY the cycle
    fields of an EXISTING file (never fabricates a state, never moves `written_ts`, the staleness
    clock of the lane rows). Atomic. True when the file changed."""
    path = Path(path)
    if not path.is_file():
        return False                       # never fabricate a state (or its folder)
    with locked(path):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        if not isinstance(data, dict) or data.get("schema") != SCHEMA:
            return False
        kept = _read_counters(path)
        new = dict(kept)
        new["max_context"] = max(kept["max_context"], int(max_context))
        if session:       # per-session maxima, summed: a successor session's compactions ADD
            per = dict(kept["compaction_sessions"])
            per[session] = max(per.get(session, 0), int(compactions))
            new["compaction_sessions"] = per
            new["compactions"] = sum(per.values())
        else:
            new["compactions"] = max(kept["compactions"], int(compactions))
        # one CROSSED per seat session: the line's `seat=<id>` prefix is the dedupe key (tokens/age vary)
        key = " ".join(crossed_line.split()[:2]) + " " if crossed_line else None
        if crossed_line and not any(x.startswith(key) for x in kept["crossed"]):
            new["crossed"] = kept["crossed"] + [crossed_line]
            new["cycles"] = kept["cycles"] + 1
        if new == kept:
            return False
        data.update(new)
        fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(data, fh, indent=2, sort_keys=True)
                fh.write("\n")
            os.replace(tmp_name, path)
        finally:
            Path(tmp_name).unlink(missing_ok=True)
    return True


#: A file nobody has written to for longer than this is STALE, not merely old. Chosen as a margin
#: OVER the cycle rule's own ~2 h handover interval (`templates/*-order-template.md`'s Cycle
#: section) -- a healthy seat rewrites this file at every state change, several times inside 2 h,
#: so a gap this long means the writing seat is gone, not merely between changes.
STALE_AFTER_MIN = 180.0


def read_state(path: Path, *, now: Optional[datetime] = None,
              max_age_min: float = STALE_AFTER_MIN) -> SeatStateFile:
    """Read and validate a state file. Refuses (`SeatStateError`) a file that is TORN (not this
    schema at all) or STALE (too old to trust) rather than handing back a partial or outdated
    belief -- see the module docstring for why both are refusals, not warnings."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SeatStateError(f"no state file at {path}: {exc!r}") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SeatStateError(f"{path} is torn -- not readable JSON: {exc}") from exc
    if not isinstance(data, Mapping) or data.get("schema") != SCHEMA:
        raise SeatStateError(
            f"{path} is torn -- schema {data.get('schema') if isinstance(data, Mapping) else None!r} "
            f"!= {SCHEMA!r}")
    role, batch = data.get("role"), data.get("batch")
    base_sha, written_ts = data.get("base_sha"), data.get("written_ts")
    if role not in ROLES or not batch or not base_sha or not written_ts:
        raise SeatStateError(
            f"{path} is torn -- missing or invalid required field(s) among "
            f"role/batch/base_sha/written_ts")
    try:
        written_at = datetime.fromisoformat(str(written_ts))
    except ValueError as exc:
        raise SeatStateError(f"{path} is torn -- written_ts {written_ts!r} does not parse") from exc
    if written_at.tzinfo is None:
        raise SeatStateError(
            f"{path} is torn -- written_ts {written_ts!r} carries no UTC offset, so its age "
            f"cannot be measured against an aware clock without guessing a timezone")
    moment = now or datetime.now(timezone.utc)
    age_min = (moment - written_at).total_seconds() / 60.0
    if age_min > max_age_min:
        raise SeatStateError(
            f"{path} is STALE -- written {age_min:.0f} min ago, over the {max_age_min:.0f} min "
            f"bound (a margin over the ~2 h cycle rule); the writing seat is presumed gone, not "
            f"merely between changes. Refused rather than trusted: bind a fresh seat and rebuild "
            f"this file from the receipt instead of acting on it")
    raw_lanes = data.get("lanes")
    if not isinstance(raw_lanes, Mapping):
        raise SeatStateError(f"{path} is torn -- 'lanes' is not an object")
    lanes = {lane: _validate_lane(lane, row) for lane, row in raw_lanes.items()}
    return SeatStateFile(role=str(role), batch=str(batch), base_sha=str(base_sha),
                         written_ts=str(written_ts), written_by=str(data.get("written_by") or ""),
                         lanes=lanes, **_read_counters(path))


# ============================================================================================ CLI

def _load_lanes_json(raw: str) -> dict:
    text = Path(raw[1:]).read_text(encoding="utf-8") if raw.startswith("@") else raw
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"--lanes-json is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise click.ClickException("--lanes-json must decode to a JSON object of lane -> row")
    return data


@click.group(help="The orchestrator-seat state file ([#833]'s sibling for the cycling seats): "
                  "what is merged, in flight, queued, refused, failed or reported, for a fresh "
                  "session of the same role to rebind from.")
def cli() -> None:                                           # pragma: no cover -- click plumbing
    pass


@cli.command("write")
@click.option("--path", required=True, type=click.Path(path_type=Path))
@click.option("--role", required=True, type=click.Choice(ROLES))
@click.option("--batch", required=True)
@click.option("--base-sha", required=True)
@click.option("--written-by", default="")
@click.option("--lanes-json", required=True,
             help="A JSON object {lane: {state, sha, evidence: {session_file, receipt_line}}}, "
                  "or @path to a file holding one.")
def cmd_write(path: Path, role: str, batch: str, base_sha: str, written_by: str,
             lanes_json: str) -> None:
    try:
        state = write_state(path, role=role, batch=batch, base_sha=base_sha,
                            lanes=_load_lanes_json(lanes_json), written_by=written_by)
    except SeatStateError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(f"wrote {path}: {len(state.lanes)} lane(s), in-flight = "
              f"{state.in_flight() or '[]'}")


@cli.command("read")
@click.option("--path", required=True, type=click.Path(path_type=Path))
@click.option("--max-age-min", default=STALE_AFTER_MIN, show_default=True)
def cmd_read(path: Path, max_age_min: float) -> None:
    try:
        state = read_state(path, max_age_min=max_age_min)
    except SeatStateError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(f"role={state.role} batch={state.batch} base_sha={state.base_sha} "
              f"written_ts={state.written_ts} written_by={state.written_by or '-'}")
    click.echo(f"in-flight ({len(state.in_flight())}): {state.in_flight() or '[]'}")
    for lane_state in LANE_STATES:
        lanes = state.by_state(lane_state)
        if lanes:
            click.echo(f"{lane_state}: {lanes}")


if __name__ == "__main__":
    cli()
