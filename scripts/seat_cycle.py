#!/usr/bin/env python
"""seat_cycle.py -- a seat hands over BY CODE at a threshold (R179).

THE SEQUENCE, IN ORDER, AND WHY THE ORDER IS THE POINT
  1. `check`: the seat's context (last assistant `message.usage` of its transcript) or age crossed
     the threshold in `ecosystem/seat-cycle.yaml`.
  2. write `HANDOVER-<seat>-cycle-<n>.md` (kind HANDOVER, `carried-by: OPEN`).
  3. launch the successor through `dispatch.successor_lane` -- the one launch path -- on the model
     the role table names (`provider_registry.anthropic_role_model("seat-<role>")`). A model is never
     typed here, never taken from a caller and never read out of the handover text.
  4. wait for the successor's BOUND line appended to the handover. No BOUND, no stop: the old seat
     keeps running.
  5. only then `claude stop <seat>`; never `claude rm`, never resume.
  6. VERIFY the stop: not listed, nothing queued, no surviving process. The LAST poll is the verdict;
     a seat that fails it is reported not replaced.

Production probes (`list_agents`, `read_job`, `find_processes`, `stop`) are injectable defaults;
tests drive fakes and an injected `sleep`/`clock`.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

import click
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "ecosystem" / "seat-cycle.yaml"
SECTIONS = ("State", "Next steps", "Open decisions", "Live children", "Seat bookkeeping",
            "First act (successor)")
_BOUND = re.compile(r"(?m)^BOUND seat=\S+ cycle=\S+ job=(\S+) model=(\S+)\s*$")


class SeatCycleRefused(Exception):
    pass


def _dispatch():
    try:
        import dispatch
    except ImportError as exc:
        raise SeatCycleRefused("the launch path is the hub's dispatch.py successor verb; "
                               "it is not carried here") from exc
    return dispatch


def _registry():
    try:
        import provider_registry
    except ImportError as exc:
        raise SeatCycleRefused("the role table is the hub's provider_registry; "
                               "it is not carried here") from exc
    return provider_registry


@dataclass(frozen=True)
class StopVerdict:
    verified: bool
    reasons: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Successor:
    job_id: str
    model: str
    slug: str


@dataclass(frozen=True)
class CycleResult:
    replaced: bool
    handover: Optional[Path] = None
    successor: Optional[Successor] = None
    bound: Optional[str] = None
    verdict: Optional[StopVerdict] = None


def load_config(path: Optional[Path] = None) -> dict[str, Any]:
    return yaml.safe_load(Path(path or CONFIG_PATH).read_text(encoding="utf-8"))


def context_tokens(transcript: Path) -> int:
    """Context in use = the last assistant usage record's input + cache-creation + cache-read tokens."""
    try:
        lines = Path(transcript).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return 0
    for line in reversed(lines):
        try:
            usage = (json.loads(line).get("message") or {}).get("usage")
        except (json.JSONDecodeError, AttributeError):
            continue
        if isinstance(usage, dict):
            return sum(int(usage.get(k) or 0) for k in
                       ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    return 0


def threshold_crossed(role: str, *, tokens: float, age_hours: float, config: dict[str, Any]) -> bool:
    limits = (config.get("threshold") or {}).get(role)
    if not limits:
        raise SeatCycleRefused(f"no threshold declared for role {role!r}")
    return tokens >= limits["context_tokens"] or age_hours >= limits["max_age_hours"]


# D9 puts the orchestrator SEAT on the seat-dispatcher row; seat-orchestrator is the lane-head row.
_ROLE_ROWS = {"orchestrator": "seat-dispatcher", "integrator": "seat-integrator"}


def successor_model(role: str, registry: Optional[Path] = None) -> str:
    row = _ROLE_ROWS.get(role)
    if row is None:
        raise SeatCycleRefused(f"no registry row for role {role!r}; known roles: {sorted(_ROLE_ROWS)}")
    reg = _registry()
    return reg.anthropic_role_model(row, registry) if registry else reg.anthropic_role_model(row)


def successor_name(role: str, batch: str, cycle_no: int) -> str:
    batch_slug = re.sub(r"[^a-z0-9]+", "-", batch.lower()).strip("-")
    return f"{role}-{batch_slug}-cycle-{cycle_no + 1}"


def _effort(role: str, config: dict[str, Any]) -> Optional[str]:
    """The injected config's effort; a config that declares none falls back to the repo's seat-cycle.yaml."""
    for source in (config, load_config()):
        effort = ((source.get("threshold") or {}).get(role) or {}).get("effort")
        if effort:
            return effort
    return None


# Free text is indented so no line of it can start a header, a `BOUND ` line or a `carried-by:`/`kind:` key.
def _indent(text: str) -> str:
    return "\n".join(f"  {ln}".rstrip() for ln in str(text).splitlines()) or "  "


def _indent_tail(text: str) -> str:
    lines = str(text).splitlines() or [""]
    return "\n".join([lines[0]] + [f"  {ln}".rstrip() for ln in lines[1:]])


def _shell_quote(value: str) -> str:
    # Double quotes are valid in both PowerShell and POSIX shells.
    return f'"{value}"' if re.search(r"\s", value) else value


def write_handover(path: Path, *, seat: str, role: str, cycle: int, state: str, next_steps: Sequence[str],
                   open_decisions: Sequence[str], live_children: Sequence[str], bookkeeping: str,
                   by: str, successor_slug: Optional[str] = None,
                   registry: Optional[Path] = None, config: Optional[dict[str, Any]] = None) -> Path:
    # The handover is the successor's contract, so the pre-launch model-per-role gate reads this row.
    config = config if config is not None else load_config()
    effort = _effort(role, config)
    if not effort:
        raise SeatCycleRefused(f"no effort declared for role {role!r} in seat-cycle.yaml")
    try:
        model = successor_model(role, registry)
    except SeatCycleRefused:
        raise
    except Exception as exc:
        raise SeatCycleRefused(f"no role-table model for role {role!r}: {exc}") from exc
    head_row = f"| Model | Mode | Effort |\n|---|---|---|\n| {model} | execute | {effort} |"
    steps = "\n".join(f"{i}. {_indent_tail(s)}" for i, s in enumerate(next_steps, 1))
    bullets = lambda items: "\n".join(f"- {_indent_tail(x)}" for x in items)   # noqa: E731
    state, bookkeeping = _indent(state), _indent(bookkeeping)
    path = Path(path)
    slug = successor_slug or f"{seat}-c{cycle + 1}"
    command = (f"uv run --locked python scripts/seat_cycle.py bound --handover {_shell_quote(str(path.resolve()))} "
               f"--name {_shell_quote(slug)} --seat {_shell_quote(seat)} --cycle {cycle}")
    summary = f"seat {seat} role={role} cycle={cycle} hands over to {slug}"
    text = (f"carried-by: OPEN\nkind: HANDOVER\nsummary: {summary}\nby: {by}\n\n"
            f"# Handover {seat} cycle {cycle}\n\n## Head row\n\n{head_row}\n\n## State\n\n{state}\n\n## Next steps\n\n{steps}\n\n"
            f"## Open decisions\n\n{bullets(open_decisions)}\n\n## Live children\n\n{bullets(live_children)}\n\n"
            f"## Seat bookkeeping\n\n{bookkeeping}\n\n"
            f"## First act (successor)\n\nFIRST read every section above. THEN, as the next action, run exactly:\n\n"
            f"```\n{command}\n```\n\nThe BOUND line it appends means the handover is consumed.\n")
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def lint_handover(text: str) -> list[str]:
    defects: list[str] = []
    lines = text.splitlines()
    if not lines or not lines[0].startswith("carried-by:"):
        defects.append("missing `carried-by:` header on line 1")
    if "kind: HANDOVER" not in lines[:3]:
        defects.append("missing `kind: HANDOVER` header")
    if not any(ln.startswith("summary:") and ln[8:].strip() for ln in lines[:5]):
        defects.append("missing `summary:` header")
    body = {m.group(1): m.group(2) for m in
            re.finditer(r"(?ms)^## (.+?)\s*$(.*?)(?=^## |\Z)", text)}
    for section in SECTIONS:
        if section not in body:
            defects.append(f"missing section: {section}")
    if "Head row" not in body:
        defects.append("missing section: Head row")
    else:
        try:
            _dispatch().parse_contract_model_effort(text)
        except SeatCycleRefused:
            pass
        except Exception as exc:
            defects.append(f"head row unparseable: {exc}")
    if "Next steps" in body and not re.search(r"(?m)^1\. \S", body["Next steps"]):
        defects.append("no next steps: the section carries no numbered item")
    return defects


def write_bound(handover: Path, *, job_id: str, served_model: str, seat: str, cycle: int) -> str:
    line = f"BOUND seat={seat} cycle={cycle} job={job_id} model={served_model}"
    text = Path(handover).read_text(encoding="utf-8")
    sep = "" if text.endswith("\n") else "\n"
    Path(handover).write_text(f"{text}{sep}\n{line}\n", encoding="utf-8", newline="\n")
    return line


def await_bound(handover: Path, *, job_id: str, timeout: float, interval: float = 1.0,
                sleep: Callable[[float], Any] = time.sleep,
                clock: Callable[[], float] = time.monotonic) -> str:
    start = clock()
    while True:
        for m in _BOUND.finditer(Path(handover).read_text(encoding="utf-8")):
            if _short(m.group(1)) == _short(job_id):
                return m.group(0).strip()
        if clock() - start >= timeout:
            raise SeatCycleRefused(f"successor job {job_id} never wrote a BOUND line to {handover}")
        sleep(interval)


def launch_successor(handover: Path, *, role: str, slug: str, batch: str, base: str, repo_root: Path,
                     model: Optional[str] = None, effort: Optional[str] = None,
                     successor_lane: Optional[Callable[..., Any]] = None,
                     config: Optional[dict[str, Any]] = None) -> Successor:
    if model is not None:
        raise SeatCycleRefused("the successor model comes from the role table; an override is refused")
    defects = lint_handover(Path(handover).read_text(encoding="utf-8"))
    if defects:
        raise SeatCycleRefused("handover refused: " + "; ".join(defects))
    dispatch = _dispatch()
    if effort is None:
        config = config if config is not None else load_config()
        effort = _effort(role, config)
        if not effort:
            raise SeatCycleRefused(f"no effort declared for role {role!r} in seat-cycle.yaml")
    successor_lane = successor_lane or dispatch.successor_lane
    chosen = successor_model(role)
    request = dispatch.SuccessorRequest(slug=slug, contract=Path(handover), base=base, batch=batch,
                                        model=chosen, effort=effort)
    spawned = successor_lane(request, repo_root=repo_root)
    found = dispatch._JOB_ID.search(dispatch._ANSI.sub("", spawned.stdout or ""))
    if spawned.returncode != 0 or not found:
        raise SeatCycleRefused(f"successor {slug} did not launch (rc={spawned.returncode}, no job id)")
    return Successor(job_id=found.group(1), model=chosen, slug=slug)


def _short(ident: str) -> str:
    return str(ident)[:8]


def verify_stop(job_id: str, worktree: str, *, list_agents: Optional[Callable[[], list]] = None,
                read_job: Optional[Callable[[str], Optional[dict]]] = None,
                find_processes: Optional[Callable[[Sequence[str]], list[str]]] = None,
                window: float, interval: float, sleep: Callable[[float], Any] = time.sleep,
                clock: Callable[[], float] = time.monotonic) -> StopVerdict:
    list_agents = list_agents or _list_agents
    read_job = read_job or _read_job
    find_processes = find_processes or _find_processes
    start = clock()
    while True:
        reasons: list[str] = []
        try:
            for entry in list_agents():
                if job_id in (entry.get("id"), entry.get("sessionId")) or \
                        _short(job_id) in (_short(entry.get("id") or ""), _short(entry.get("sessionId") or "")):
                    reasons.append(f"seat {job_id} is still listed by `claude agents`")
                    break
        except Exception as exc:
            reasons.append(f"probe failed: claude agents listing unavailable ({exc})")
        try:
            job = read_job(job_id)
        except Exception as exc:
            job = None
            reasons.append(f"job state unreadable (probe failed: {exc})")
        if job is not None:
            if job.get("state") not in ("stopped", "done"):
                reasons.append(f"job state is {job.get('state')!r}, not 'stopped' or 'done'")
            queued = int((job.get("inFlight") or {}).get("queued") or 0)
            if queued:
                reasons.append(f"{queued} message(s) still queued for the stopped seat")
        try:
            survivors = find_processes([job_id, worktree])
        except Exception as exc:
            survivors = []
            reasons.append(f"probe failed: process table unavailable ({exc})")
        if survivors:
            reasons.append(f"surviving process: {survivors[0]}" + (f" (+{len(survivors) - 1})" if len(survivors) > 1 else ""))
        if clock() - start + interval > window:
            return StopVerdict(verified=not reasons, reasons=reasons)
        sleep(interval)


def _list_agents() -> list:                                  # pragma: no cover -- production probe
    try:
        done = subprocess.run(["claude", "agents", "--json"], capture_output=True, text=True, check=False)
    except OSError as exc:
        raise SeatCycleRefused(f"`claude agents` could not run: {exc}") from exc
    if done.returncode != 0:
        raise SeatCycleRefused(f"`claude agents` exited {done.returncode}")
    try:
        data = json.loads(done.stdout or "")
    except json.JSONDecodeError as exc:
        raise SeatCycleRefused(f"`claude agents` output is not JSON: {exc}") from exc
    if isinstance(data, dict):
        data = data.get("agents", [])
    if not isinstance(data, list):
        raise SeatCycleRefused("`claude agents` output has no agent list")
    return [d for d in data if isinstance(d, dict)]


def _read_job(job_id: str) -> Optional[dict]:                # pragma: no cover -- production probe
    """None only when the job directory is gone; a directory without a readable state is a failed check."""
    job_dir = Path.home() / ".claude" / "jobs" / _short(job_id)
    if not job_dir.exists():
        return None
    try:
        data = json.loads((job_dir / "state.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SeatCycleRefused(f"job state unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise SeatCycleRefused("job state unreadable: not an object")
    return data


def _process_table() -> list[tuple[int, int, str]]:          # pragma: no cover -- production probe
    rows: list[tuple[int, int, str]] = []
    try:
        if os.name == "nt":
            done = subprocess.run(["powershell", "-NoProfile", "-Command",
                                   "Get-CimInstance Win32_Process | "
                                   "Select ProcessId,ParentProcessId,CommandLine | ConvertTo-Json"],
                                  capture_output=True, text=True, check=False)
        else:
            done = subprocess.run(["ps", "-eo", "pid,ppid,args"], capture_output=True, text=True, check=False)
    except OSError as exc:
        raise SeatCycleRefused(f"process table could not be read: {exc}") from exc
    if done.returncode != 0:
        raise SeatCycleRefused(f"process table probe exited {done.returncode}")
    if os.name == "nt":
        try:
            data = json.loads(done.stdout)
        except json.JSONDecodeError as exc:
            raise SeatCycleRefused(f"process table output is not JSON: {exc}") from exc
        for d in [data] if isinstance(data, dict) else data:
            rows.append((int(d.get("ProcessId") or 0), int(d.get("ParentProcessId") or 0),
                         d.get("CommandLine") or ""))
    else:
        for line in done.stdout.splitlines()[1:]:
            parts = line.split(None, 2)
            if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                rows.append((int(parts[0]), int(parts[1]), parts[2]))
    return rows


def needle_matches(cmdline: str, needle: str) -> bool:
    """True where `needle` sits on an identifier boundary: not followed by [A-Za-z0-9_-] (so a
    successor `<seat>-c2` is not the seat) and not preceded by [A-Za-z0-9_] (a `pty-<id>` prefix
    still names the id). A following path separator still matches."""
    return bool(needle) and re.search(rf"(?<![A-Za-z0-9_]){re.escape(needle)}(?![A-Za-z0-9_-])", cmdline,
                                      re.IGNORECASE) is not None


def _find_processes(needles: Sequence[str]) -> list[str]:    # pragma: no cover -- production probe
    needles = [n for n in needles if n]
    rows = _process_table()
    parent = {pid: ppid for pid, ppid, _ in rows}
    skip, cur = set(), os.getpid()
    while cur and cur not in skip:                           # this process and its ancestors carry the needles too
        skip.add(cur)
        cur = parent.get(cur, 0)
    return [f"{pid} {cmd}" for pid, _ppid, cmd in rows
            if pid not in skip and any(needle_matches(cmd, n) for n in needles)]


def _stop(seat: str) -> None:                                # pragma: no cover -- production probe
    subprocess.run(["claude", "stop", seat], check=False)


def cycle(seat: str, *, role: str, transcript: Path, bound_age_hours: float, config: dict[str, Any],
          handover_dir: Path, cycle_no: int, batch: str, base: str, repo_root: Path, state: str,
          next_steps: Sequence[str], open_decisions: Sequence[str], live_children: Sequence[str],
          bookkeeping: str, worktree: str = "",
          successor_lane: Optional[Callable[..., Any]] = None,
          stop: Callable[[str], Any] = _stop,
          verify: Optional[Callable[[str], StopVerdict]] = None,
          wait_bound: Optional[Callable[[Path, str], str]] = None) -> CycleResult:
    if not threshold_crossed(role, tokens=context_tokens(transcript), age_hours=bound_age_hours,
                             config=config):
        return CycleResult(replaced=False)
    poll = config.get("stop_poll") or {}
    wait = config.get("bound_wait") or {}
    verify = verify or (lambda s: verify_stop(s, worktree, window=poll["window_seconds"],
                                              interval=poll["interval_seconds"]))
    wait_bound = wait_bound or (lambda h, j: await_bound(h, job_id=j, timeout=wait["timeout_seconds"],
                                                         interval=wait["interval_seconds"]))
    slug = successor_name(role, batch, cycle_no)
    handover = write_handover(Path(handover_dir) / f"HANDOVER-{seat}-cycle-{cycle_no}.md", seat=seat,
                              role=role, cycle=cycle_no, state=state, next_steps=next_steps,
                              open_decisions=open_decisions, live_children=live_children,
                              bookkeeping=bookkeeping, by=seat, successor_slug=slug, config=config)
    successor = launch_successor(handover, role=role, slug=slug, batch=batch, base=base,
                                 repo_root=repo_root, successor_lane=successor_lane, config=config)
    bound = wait_bound(handover, successor.job_id)
    served = re.search(r"\bmodel=(\S+)", bound)
    if not served or served.group(1) != successor.model:
        raise SeatCycleRefused(f"successor served model {served.group(1) if served else None!r}, "
                               f"role table says {successor.model!r}; the seat is not stopped")
    stop(seat)
    verdict = verify(seat)
    return CycleResult(replaced=verdict.verified, handover=handover, successor=successor, bound=bound,
                       verdict=verdict)


# --- the Stop leg ([#1636]) -------------------------------------------------------------------------
# The Stop hook calls `stop_check` every turn. It only RECORDS: a CROSSED line in the seat's state file
# and receipt, read by the seat at its next wake (a no-merge point). It returns a string for the caller
# and prints nothing -- a Stop hook that asks the model to continue cost +45k tokens per start ([#1700]).

# registry role -> (cycle role, state-file suffix)
_STOP_ROLES = {"dispatcher": ("orchestrator", "-dispatcher"), "integrator": ("integrator", "")}


def transcript_stats(transcript: Path) -> tuple[int, int]:
    """(context tokens, compaction count) from ONE read of the transcript."""
    try:
        lines = Path(transcript).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return 0, 0
    tokens, compactions = 0, 0
    for line in lines:
        if '"isCompactSummary"' in line:
            try:
                if json.loads(line).get("isCompactSummary") is True:
                    compactions += 1
            except (json.JSONDecodeError, AttributeError):
                pass
    for line in reversed(lines):
        if '"usage"' not in line:
            continue
        try:
            usage = (json.loads(line).get("message") or {}).get("usage")
        except (json.JSONDecodeError, AttributeError):
            continue
        if isinstance(usage, dict):
            tokens = sum(int(usage.get(k) or 0) for k in
                         ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
            break
    return tokens, compactions


def _bound_seat(session_id: str, registry_path: Optional[Path]) -> Optional[dict]:
    """The session's LATEST bind row, unless an unbind followed it."""
    import seat_registry
    seat: Optional[dict] = None
    for row in seat_registry.read_rows(registry_path):
        if row.get("session_id") != session_id:
            continue
        if row.get("kind") == "bind":
            seat = row
        elif row.get("kind") == "unbind":
            seat = None
    return seat


def stop_check(payload: dict[str, Any], *, registry_path: Optional[Path] = None,
               repo_root: Optional[Path] = None, config: Optional[dict[str, Any]] = None,
               now: Optional[Any] = None) -> Optional[str]:
    """None for any seat that is not a bound orchestrator/integrator; else "OK" or "CROSSED"."""
    from datetime import datetime, timezone
    session = str(payload.get("session_id") or "")
    if not session:
        return None
    bound = _bound_seat(session, registry_path)
    mapped = _STOP_ROLES.get(str((bound or {}).get("role")))
    if not bound or not mapped:
        return None
    role, suffix = mapped
    root = Path(repo_root or payload.get("cwd") or Path.cwd())
    tokens, compactions = transcript_stats(Path(str(payload.get("transcript_path") or "")))
    moment = now or datetime.now(timezone.utc)
    age_hours = (moment - datetime.fromisoformat(str(bound["ts"]))).total_seconds() / 3600.0
    crossed = threshold_crossed(role, tokens=tokens, age_hours=age_hours,
                                config=config if config is not None else load_config())
    slug = re.sub(r"[^a-z0-9]+", "-", str(bound.get("batch") or "").lower()).strip("-")
    folder = root / "to-browser"
    line = None
    if crossed:
        line = (f"CROSSED seat={session} role={role} tokens={tokens} age_hours={age_hours:.2f} "
                f"ts={moment.isoformat(timespec='seconds')}")
    import seat_state
    seat_state.update_counters(folder / f"STATE-{slug}{suffix}.json", max_context=tokens,
                               compactions=compactions, crossed_line=line)
    if line:
        receipt = folder / f"SESSION-{bound['role']}-{slug}.md"
        # one CROSSED per seat session: the state file is the dedupe key when it exists, else the receipt
        seen = receipt.read_text(encoding="utf-8", errors="replace") if receipt.exists() else ""
        if f"CROSSED seat={session} " not in seen:
            folder.mkdir(parents=True, exist_ok=True)
            with receipt.open("a", encoding="utf-8", newline="\n") as fh:
                fh.write(("" if not seen or seen.endswith("\n") else "\n") + line + "\n")
    return "CROSSED" if crossed else "OK"


@click.group(help="Seat cycling (R179): hand a seat over to a fresh successor at a threshold.")
def cli() -> None:                                           # pragma: no cover -- click plumbing
    pass


@cli.command("check")
@click.option("--role", required=True, type=click.Choice(["orchestrator", "integrator"]))
@click.option("--transcript", required=True, type=click.Path(path_type=Path))
@click.option("--bound-age-hours", required=True, type=float)
def cmd_check(role: str, transcript: Path, bound_age_hours: float) -> None:
    crossed = threshold_crossed(role, tokens=context_tokens(transcript), age_hours=bound_age_hours,
                                config=load_config())
    click.echo("CROSSED" if crossed else "OK")


def _find_transcript(session_id: str) -> Optional[Path]:
    hits = sorted((Path.home() / ".claude" / "projects").glob(f"*/{session_id}.jsonl"))
    return hits[0] if hits else None


def served_model(transcript: Optional[Path]) -> str:
    """The `model` of the LAST assistant record of a transcript; "unknown" when unreadable."""
    if transcript is None:
        return "unknown"
    try:
        lines = Path(transcript).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return "unknown"
    for line in reversed(lines):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and rec.get("type") == "assistant":
            model = rec.get("model") or (rec.get("message") or {}).get("model")
            return str(model).replace(" ", "_") if model else "unknown"
    return "unknown"


def bind_successor(handover: Path, *, name: str, seat: str, cycle_no: int,
                   list_agents: Optional[Callable[[], list]] = None,
                   find_transcript: Optional[Callable[[str], Optional[Path]]] = None) -> str:
    matches = [a for a in (list_agents or _list_agents)() if a.get("name") == name]
    if len(matches) != 1:
        raise SeatCycleRefused(f"{len(matches)} listed agents are named {name!r}; expected exactly 1")
    job_id, session_id = matches[0].get("id"), matches[0].get("sessionId")
    if not job_id:
        raise SeatCycleRefused(f"agent {name!r} has no id")
    transcript = (find_transcript or _find_transcript)(session_id) if session_id else None
    return write_bound(handover, job_id=job_id, served_model=served_model(transcript), seat=seat,
                       cycle=cycle_no)


@cli.command("bound")
@click.option("--handover", required=True, type=click.Path(path_type=Path))
@click.option("--name", required=True, help="The successor's own agent name (its launch slug).")
@click.option("--seat", required=True)
@click.option("--cycle", "cycle_no", required=True, type=int)
def cmd_bound(handover: Path, name: str, seat: str, cycle_no: int,
              list_agents: Optional[Callable[[], list]] = None,
              find_transcript: Optional[Callable[[str], Optional[Path]]] = None) -> None:
    try:
        line = bind_successor(handover, name=name, seat=seat, cycle_no=cycle_no,
                              list_agents=list_agents, find_transcript=find_transcript)
    except SeatCycleRefused as exc:
        click.echo(str(exc), err=True)
        sys.exit(1)
    click.echo(line)


@cli.command("verify-stop")
@click.option("--job", required=True)
@click.option("--worktree", required=True)
def cmd_verify_stop(job: str, worktree: str) -> None:       # pragma: no cover -- click plumbing
    poll = load_config()["stop_poll"]
    verdict = verify_stop(job, worktree, window=poll["window_seconds"], interval=poll["interval_seconds"])
    for reason in verdict.reasons:
        click.echo(reason)
    if not verdict.verified:
        sys.exit(1)
    click.echo("VERIFIED")


@cli.command("run")
@click.option("--seat", required=True, help="The seat's job id (what `claude stop` takes).")
@click.option("--role", required=True, type=click.Choice(["orchestrator", "integrator"]))
@click.option("--transcript", required=True, type=click.Path(path_type=Path))
@click.option("--bound-age-hours", required=True, type=float)
@click.option("--handover-dir", required=True, type=click.Path(path_type=Path))
@click.option("--cycle-no", required=True, type=int)
@click.option("--batch", required=True)
@click.option("--base", default="main", show_default=True)
@click.option("--repo-root", type=click.Path(path_type=Path), default=Path.cwd)
@click.option("--worktree", required=True, help="The old seat's worktree path (a process-probe needle).")
@click.option("--state", required=True)
@click.option("--next-step", "next_steps", multiple=True, required=True)
@click.option("--open-decision", "open_decisions", multiple=True)
@click.option("--live-child", "live_children", multiple=True)
@click.option("--bookkeeping", required=True)
def cmd_run(seat, role, transcript, bound_age_hours, handover_dir, cycle_no, batch, base, repo_root,
            worktree, state, next_steps, open_decisions, live_children,
            bookkeeping) -> None:                            # pragma: no cover -- click plumbing
    try:
        r = cycle(seat, role=role, transcript=transcript, bound_age_hours=bound_age_hours,
                  config=load_config(), handover_dir=handover_dir, cycle_no=cycle_no, batch=batch,
                  base=base, repo_root=repo_root, state=state, next_steps=next_steps,
                  open_decisions=open_decisions or ["none"], live_children=live_children or ["none"],
                  bookkeeping=bookkeeping, worktree=worktree)
    except Exception as exc:
        if isinstance(exc, SeatCycleRefused) or type(exc).__name__ == "DispatchRefused":
            raise click.ClickException(str(exc)) from exc
        raise
    if r.handover is None:
        click.echo("OK: below threshold, nothing done")
        return
    click.echo(f"handover={r.handover} successor={r.successor.job_id} {r.bound}")
    for reason in r.verdict.reasons:
        click.echo(reason)
    if not r.replaced:
        raise click.ClickException("stop NOT verified: seat not replaced")
    click.echo("REPLACED")


if __name__ == "__main__":
    cli()
