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
_BOUND = re.compile(r"(?m)^BOUND seat=\S+ cycle=\S+ job=(\S+) model=\S+\s*$")


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


def successor_model(role: str, registry: Optional[Path] = None) -> str:
    reg = _registry()
    return reg.anthropic_role_model(f"seat-{role}", registry) if registry else \
        reg.anthropic_role_model(f"seat-{role}")


def write_handover(path: Path, *, seat: str, role: str, cycle: int, state: str, next_steps: Sequence[str],
                   open_decisions: Sequence[str], live_children: Sequence[str], bookkeeping: str,
                   by: str, successor_slug: Optional[str] = None,
                   registry: Optional[Path] = None) -> Path:
    # The handover is the successor's contract, so the pre-launch model-per-role gate reads this row.
    effort = ((load_config().get("threshold") or {}).get(role) or {}).get("effort")
    if not effort:
        raise SeatCycleRefused(f"no effort declared for role {role!r} in seat-cycle.yaml")
    try:
        model = successor_model(role, registry)
    except SeatCycleRefused:
        raise
    except Exception as exc:
        raise SeatCycleRefused(f"no role-table model for role {role!r}: {exc}") from exc
    head_row = f"| Model | Mode | Effort |\n|---|---|---|\n| {model} | execute | {effort} |"
    steps = "\n".join(f"{i}. {s}" for i, s in enumerate(next_steps, 1))
    bullets = lambda items: "\n".join(f"- {x}" for x in items)   # noqa: E731
    path = Path(path)
    slug = successor_slug or f"{seat}-c{cycle + 1}"
    command = (f"uv run --locked python scripts/seat_cycle.py bound --handover {path.resolve()} "
               f"--name {slug} --seat {seat} --cycle {cycle}")
    text = (f"carried-by: OPEN\nkind: HANDOVER\nseat: {seat} role={role} cycle={cycle}\nby: {by}\n\n"
            f"# Handover {seat} cycle {cycle}\n\n## Head row\n\n{head_row}\n\n## State\n\n{state}\n\n## Next steps\n\n{steps}\n\n"
            f"## Open decisions\n\n{bullets(open_decisions)}\n\n## Live children\n\n{bullets(live_children)}\n\n"
            f"## Seat bookkeeping\n\n{bookkeeping}\n\n"
            f"## First act (successor)\n\nAs your FIRST action, before anything else, run exactly:\n\n"
            f"```\n{command}\n```\n\nThen read the sections above.\n")
    path.write_text(text, encoding="utf-8")
    return path


def lint_handover(text: str) -> list[str]:
    defects: list[str] = []
    lines = text.splitlines()
    if not lines or not lines[0].startswith("carried-by:"):
        defects.append("missing `carried-by:` header on line 1")
    if "kind: HANDOVER" not in lines[:3]:
        defects.append("missing `kind: HANDOVER` header")
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
    Path(handover).write_text(f"{text}{sep}\n{line}\n", encoding="utf-8")
    return line


def await_bound(handover: Path, *, job_id: str, timeout: float, interval: float = 1.0,
                sleep: Callable[[float], Any] = time.sleep,
                clock: Callable[[], float] = time.monotonic) -> str:
    start = clock()
    while True:
        for m in _BOUND.finditer(Path(handover).read_text(encoding="utf-8")):
            if m.group(1) == job_id:
                return m.group(0).strip()
        if clock() - start >= timeout:
            raise SeatCycleRefused(f"successor job {job_id} never wrote a BOUND line to {handover}")
        sleep(interval)


def launch_successor(handover: Path, *, role: str, slug: str, batch: str, base: str, repo_root: Path,
                     model: Optional[str] = None, effort: Optional[str] = None,
                                          successor_lane: Optional[Callable[..., Any]] = None) -> Successor:
    if model is not None:
        raise SeatCycleRefused("the successor model comes from the role table; an override is refused")
    defects = lint_handover(Path(handover).read_text(encoding="utf-8"))
    if defects:
        raise SeatCycleRefused("handover refused: " + "; ".join(defects))
    dispatch = _dispatch()
    if effort is None:
        effort = ((load_config().get("threshold") or {}).get(role) or {}).get("effort")
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
        for entry in list_agents():
            if job_id in (entry.get("id"), entry.get("sessionId")) or \
                    _short(job_id) in (_short(entry.get("id") or ""), _short(entry.get("sessionId") or "")):
                reasons.append(f"seat {job_id} is still listed by `claude agents`")
                break
        job = read_job(job_id)
        if job is not None:
            if job.get("state") not in ("stopped", "done"):
                reasons.append(f"job state is {job.get('state')!r}, not 'stopped' or 'done'")
            queued = int((job.get("inFlight") or {}).get("queued") or 0)
            if queued:
                reasons.append(f"{queued} message(s) still queued for the stopped seat")
        survivors = find_processes([job_id, worktree])
        if survivors:
            reasons.append(f"surviving process: {survivors[0]}" + (f" (+{len(survivors) - 1})" if len(survivors) > 1 else ""))
        if clock() - start + interval > window:
            return StopVerdict(verified=not reasons, reasons=reasons)
        sleep(interval)


def _list_agents() -> list:                                  # pragma: no cover -- production probe
    out = subprocess.run(["claude", "agents", "--json"], capture_output=True, text=True, check=False).stdout
    try:
        data = json.loads(out or "[]")
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        data = data.get("agents", [])
    return [d for d in data if isinstance(d, dict)]


def _read_job(job_id: str) -> Optional[dict]:                # pragma: no cover -- production probe
    path = Path.home() / ".claude" / "jobs" / _short(job_id) / "state.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _process_table() -> list[tuple[int, int, str]]:          # pragma: no cover -- production probe
    rows: list[tuple[int, int, str]] = []
    if os.name == "nt":
        out = subprocess.run(["powershell", "-NoProfile", "-Command",
                              "Get-CimInstance Win32_Process | "
                              "Select ProcessId,ParentProcessId,CommandLine | ConvertTo-Json"],
                             capture_output=True, text=True, check=False).stdout
        try:
            data = json.loads(out or "[]")
        except json.JSONDecodeError:
            return rows
        for d in [data] if isinstance(data, dict) else data:
            rows.append((int(d.get("ProcessId") or 0), int(d.get("ParentProcessId") or 0),
                         d.get("CommandLine") or ""))
    else:
        out = subprocess.run(["ps", "-eo", "pid,ppid,args"], capture_output=True, text=True, check=False).stdout
        for line in out.splitlines()[1:]:
            parts = line.split(None, 2)
            if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                rows.append((int(parts[0]), int(parts[1]), parts[2]))
    return rows


def needle_matches(cmdline: str, needle: str) -> bool:
    """True where `needle` sits on an identifier boundary: not followed by [A-Za-z0-9_-] (so a
    successor `<seat>-c2` is not the seat) and not preceded by [A-Za-z0-9_] (a `pty-<id>` prefix
    still names the id). A following path separator still matches."""
    return bool(needle) and re.search(rf"(?<![A-Za-z0-9_]){re.escape(needle)}(?![A-Za-z0-9_-])", cmdline) is not None


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
    slug = f"{seat}-c{cycle_no + 1}"
    handover = write_handover(Path(handover_dir) / f"HANDOVER-{seat}-cycle-{cycle_no}.md", seat=seat,
                              role=role, cycle=cycle_no, state=state, next_steps=next_steps,
                              open_decisions=open_decisions, live_children=live_children,
                              bookkeeping=bookkeeping, by=seat, successor_slug=slug)
    successor = launch_successor(handover, role=role, slug=slug, batch=batch,
                                 base=base, repo_root=repo_root, successor_lane=successor_lane)
    bound = wait_bound(handover, successor.job_id)
    stop(seat)
    verdict = verify(seat)
    return CycleResult(replaced=verdict.verified, handover=handover, successor=successor, bound=bound,
                       verdict=verdict)


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
@click.option("--worktree", default="", help="The old seat's worktree path (a process-probe needle).")
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
