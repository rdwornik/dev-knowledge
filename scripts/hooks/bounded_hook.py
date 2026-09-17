#!/usr/bin/env python
"""bounded_hook.py -- a Claude Code hook runs inside a bound it cannot outlive, and a bypass is
RECORDED ([#808]).

WHAT THE HARNESS ALREADY DOES, MEASURED (lane ab-808 step 1,
`docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md`). A hook's `timeout` field is
real while the hook's TOP process is alive: at the bound Claude Code kills that process tree,
writes a `hook_cancelled` attachment into the transcript, and FAILS OPEN -- the tool call runs.
With no `timeout` field the bound is 600 s. What the field does NOT bound is a hook whose top
process has EXITED while a descendant still holds the inherited stdout/stderr pipe: the harness
waits for that pipe to close, past the bound, and writes nothing. Both multi-hour wedges found in
the transcripts carry that signature.

WHAT THIS MODULE ADDS -- and why it is not a rival timer. `run` starts the wrapped command with
pipes of ITS OWN, so no descendant can ever hold the harness's pipe; it drains them itself and
stops waiting at `--bound` whatever the descendants do. Past the bound it kills the tree,
appends one line to the bypass record, tells the seat in-band which guard was skipped, and exits
by the declared posture. Within the bound it is invisible: exit code and both streams are relayed
byte-for-byte, so a refusal stays a refusal.

THE RECORD IS ONE NAMED SURFACE: `logs/HOOK-BYPASSES.jsonl` under the PRIMARY checkout (gitignored,
the `logs/PARITY-EVENTS.jsonl` class). A lane's worktree is torn down at integration, so a bypass
recorded inside it would die with it -- `primary_root` follows a worktree's `.git` file back to the
checkout that owns it. `$DEV_KNOWLEDGE_HOOK_BYPASS_LOG` overrides the path (tests use it). Each
line carries hook id, bound, elapsed time, session id, event, tool, reason and posture.

`surface` prints the record at SessionStart, so a guard that keeps timing out reads as DISARMED
rather than merely slow. `check` refuses a hook registration with no explicit bound, a wrapper
bound the harness timeout does not cover, or a hook with no stated posture.

THE POSTURE IS STATED PER HOOK, in `POSTURES`, each with its reason. A hook whose ruling says it
must fail CLOSED is named `escalated` and is NOT routed through this wrapper: wrapping it
fail-open would decide a question [#808] Done 4 reserves for a ruling. `--posture closed` exists
so that either answer is one flag; nothing is wired closed.

Stdlib only, run on the system interpreter -- the same reason the ADR-77 guard is: a stale
lockfile must never be able to stop a hook from being bounded.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple

LOG = logging.getLogger("bounded_hook")

RECORD_ENV = "DEV_KNOWLEDGE_HOOK_BYPASS_LOG"
RECORD_RELPATH = Path("logs") / "HOOK-BYPASSES.jsonl"

#: Headroom the harness `timeout` must leave over a wrapper's `--bound`. The wrapper's bound
#: runs from the wrapper's OWN start; interpreter start on a loaded box was measured at up to
#: ~20 s (step 1: hook start logged 18-22 s after launch). A harness timeout with less headroom
#: cancels the wrapper before it can write the record -- a silent bypass again.
HARNESS_HEADROOM_S = 20

#: How long to wait for a killed tree's pipes to close before abandoning them.
KILL_GRACE_S = 2.0

SURFACE_WINDOW_H = 72
SURFACE_TAIL_LINES = 5000

_WRAPPED_RE = re.compile(
    r"bounded_hook\.py\"?\s+run\s+--id\s+(?P<id>\S+)\s+--bound\s+(?P<bound>\d+(?:\.\d+)?)"
    r"(?:\s+--posture\s+(?P<posture>\S+))?\s+--\s")

_REPO_ROOT = Path(__file__).resolve().parents[2]


class Posture(NamedTuple):
    hook_id: str
    match: str
    posture: str  # "fail-open" | "escalated"
    wrapped: bool
    reason: str


#: One entry per hook registered in `.claude/settings.json`, first match wins. `match` is a
#: substring of the registered command; `check` refuses a hook no entry matches.
POSTURES: tuple[Posture, ...] = (
    Posture("prompts-guard", "--prompts-guard", "escalated", False,
            "AX15-1 rules this guard FAIL-CLOSED on any inability to evaluate, and a timeout is "
            "one. Measured: the harness already fails it OPEN at its bound, silently, on 477 of "
            "573 recorded calls (83%). Which way it goes past its bound is a class (b) ruling, "
            "not a wrapper default -- so it is left byte-identical and escalated."),
    Posture("immutable-edits-guard", "block_immutable_edits.py", "escalated", False,
            "ADR-77 transcript-immutability guard, fail-CLOSED in-zone by design. It carried no "
            "timeout, so the measured 600 s harness default applied; the explicit bound written "
            "now is that same 600 s, which changes no behaviour. Whether it may fail open sooner "
            "is a class (b) ruling."),
    Posture("hook-bypass-surface", "bounded_hook.py\" surface", "fail-open", False,
            "It IS the surface: reads one local file and spawns nothing, so the held-pipe gap "
            "cannot arise and the harness timeout bounds it fully. Wrapping it would record a "
            "bypass of the reader of bypasses."),
    Posture("session-end-backpressure", "session_end_backpressure.py", "fail-open", True,
            "Advisory in full since the ADR-85 amendment A5: it cannot block a turn, so skipping "
            "it past its bound loses a nudge, never a gate."),
    Posture("fleet-health-session-start", "fleet_health.py\"", "fail-open", True,
            "SessionStart surfacing: a SessionStart hook cannot refuse (measured 2026-09-06), so "
            "a bypass loses a digest line, never a gate. The per-call prompts guard is separate."),
    Posture("surface-triage", "surface_triage.ps1", "fail-open", True,
            "SessionStart surfacing only; cannot refuse."),
    Posture("billing-leak-sentinel", "billing_leak_sentinel.ps1", "fail-open", True,
            "SessionStart sentinel; cannot refuse. A bypass loses one warning for one session."),
    Posture("changelog-sentinel", "changelog_sentinel.py", "fail-open", True,
            "SessionStart nudge, local and fail-soft by its own design."),
    Posture("arm-hooks", "arm_hooks.py", "fail-open", True,
            "Idempotent self-arm; the git hooks it arms stay armed from the previous session, and "
            "audit.py check_hooks_armed is the backstop."),
    Posture("conductor-session-start", "conductor.py\" session-start", "fail-open", True,
            "SessionStart surfacing of the conductor; cannot refuse."),
    Posture("logs-retention", "logs_retention.py", "fail-open", True,
            "Relocation housekeeping; the next session repeats it."),
    Posture("resource-lifecycle", "resource_lifecycle.py\" session-start", "fail-open", True,
            "SessionStart surfacing of seat/memory state; admission itself is a separate act."),
    Posture("codespace-regime", "codespace_regime.py\" session-start", "fail-open", True,
            "SessionStart surfacing; cannot refuse."),
)


def posture_for(command: str) -> Posture | None:
    for posture in POSTURES:
        if posture.match in command:
            return posture
    return None


# --- the record ---------------------------------------------------------------------------

def primary_root(path: Path) -> Path:
    """The checkout that owns `path`: a worktree's `.git` FILE points into
    `<primary>/.git/worktrees/<name>`; a primary's `.git` is a directory."""
    dot_git = path / ".git"
    if not dot_git.is_file():
        return path
    try:
        text = dot_git.read_text(encoding="utf-8").strip()
    except OSError:
        return path
    if not text.startswith("gitdir:"):
        return path
    gitdir = Path(text[len("gitdir:"):].strip())
    if not gitdir.is_absolute():
        gitdir = (path / gitdir).resolve()
    if gitdir.parent.name == "worktrees" and gitdir.parent.parent.name == ".git":
        return gitdir.parent.parent.parent
    return path


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
    except OSError as exc:
        LOG.warning("[hook-bypass] could not write the record at %s: %r", path, exc)
        return None
    return path


# --- run ------------------------------------------------------------------------------------

def _read_stdin(limit_s: float) -> bytes:
    box: list[bytes] = []
    reader = threading.Thread(target=lambda: box.append(sys.stdin.buffer.read()), daemon=True)
    reader.start()
    reader.join(limit_s)
    return box[0] if box else b""


def _drain(stream, sink: bytearray) -> None:
    try:
        for chunk in iter(lambda: stream.read(65536), b""):
            sink.extend(chunk)
    except (OSError, ValueError):
        pass


def _feed(stream, payload: bytes) -> None:
    try:
        stream.write(payload)
    except OSError:
        pass
    finally:
        try:
            stream.close()
        except OSError:
            pass


def _kill_tree(proc: subprocess.Popen) -> None:
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        except (OSError, subprocess.SubprocessError):
            pass
    else:
        try:
            os.killpg(proc.pid, 9)
        except OSError:
            pass
    try:
        proc.kill()
    except OSError:
        pass


def _payload_fields(payload: bytes) -> dict:
    try:
        data = json.loads(payload.decode("utf-8", "replace") or "{}")
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def _finish(code: int, out: bytes = b"", err: bytes = b"") -> None:
    sys.stdout.buffer.write(out)
    sys.stderr.buffer.write(err)
    sys.stdout.flush()
    sys.stderr.flush()
    # os._exit, not sys.exit: a reader thread still blocked on a pipe a descendant holds must
    # not be able to delay interpreter shutdown -- that would rebuild the wedge one level down.
    os._exit(code)


def run(hook_id: str, bound_s: float, posture: str, argv: list[str]) -> None:
    started = time.monotonic()
    payload = _read_stdin(min(bound_s, 5.0))
    fields = _payload_fields(payload)

    program = shutil.which(argv[0]) or argv[0]
    kwargs: dict = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    try:
        proc = subprocess.Popen([program, *argv[1:]], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    except OSError as exc:
        # Not a bypass: the hook never started. Exit 1 is a non-blocking error for every event,
        # so a missing program cannot turn into a refusal.
        LOG.warning("[hook-bypass] %s could not start %r: %r", hook_id, argv[0], exc)
        _finish(1)

    out, err = bytearray(), bytearray()
    threads = [threading.Thread(target=_drain, args=(proc.stdout, out), daemon=True),
               threading.Thread(target=_drain, args=(proc.stderr, err), daemon=True),
               threading.Thread(target=_feed, args=(proc.stdin, payload), daemon=True)]
    for thread in threads:
        thread.start()

    reason = None
    try:
        proc.wait(timeout=max(0.0, bound_s - (time.monotonic() - started)))
    except subprocess.TimeoutExpired:
        reason = "timeout"
        _kill_tree(proc)
        for thread in threads[:2]:
            thread.join(KILL_GRACE_S)
    else:
        for thread in threads[:2]:
            thread.join(max(0.0, bound_s - (time.monotonic() - started)))
        if any(thread.is_alive() for thread in threads[:2]):
            reason = "pipe-held-after-exit"

    if reason is None:
        _finish(proc.returncode, bytes(out), bytes(err))

    elapsed = round(time.monotonic() - started, 3)
    stated = "fail-closed" if posture == "closed" else "fail-open"
    row = {"ts": _utc_now(), "hook_id": hook_id, "bound_s": bound_s, "elapsed_s": elapsed,
           "session_id": fields.get("session_id") or "unknown",
           "event": fields.get("hook_event_name") or "unknown",
           "tool": fields.get("tool_name"), "reason": reason, "posture": stated,
           "cwd": fields.get("cwd") or os.getcwd()}
    where = append_record(row)
    message = (f"[hook-bypass] {hook_id} did not finish inside its {bound_s:g} s bound "
               f"({reason}, {elapsed:g} s) and was SKIPPED ({stated}). Recorded to "
               f"{where or 'NOWHERE -- the record could not be written'}.")

    if reason == "pipe-held-after-exit":
        # The command DID reach a verdict; only a descendant lingers. Relay the verdict.
        LOG.warning("%s The command exited %s; its verdict stands.", message, proc.returncode)
        _finish(proc.returncode, bytes(out), bytes(err))
    if stated == "fail-closed":
        _finish(2, b"", (message + " This hook's posture is fail-closed, so the call is "
                         "REFUSED. Fix: find why it is slow; the record names every "
                         "occurrence.\n").encode("utf-8"))
    LOG.warning("%s", message)
    _finish(0, (json.dumps({"systemMessage": message}) + "\n").encode("utf-8"))


# --- surface ----------------------------------------------------------------------------------

def surface(window_h: float = SURFACE_WINDOW_H) -> int:
    path = record_path()
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-SURFACE_TAIL_LINES:]
    except OSError:
        return 0
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_h)
    by_hook: dict[str, list[dict]] = {}
    for line in lines:
        try:
            row = json.loads(line)
            ts = datetime.strptime(row["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except (ValueError, KeyError, TypeError):
            continue
        if ts >= cutoff:
            by_hook.setdefault(str(row.get("hook_id")), []).append(row)
    if not by_hook:
        return 0
    total = sum(len(rows) for rows in by_hook.values())
    report = [f"[hook-bypass] {total} bypass(es) across {len(by_hook)} hook(s) in the last "
              f"{window_h:g} h -- a hook that keeps timing out is DISARMED, not slow. "
              f"Record: {path}"]
    for hook_id, rows in sorted(by_hook.items(), key=lambda kv: -len(kv[1])):
        reasons = ", ".join(sorted({str(r.get("reason")) for r in rows}))
        report.append(f"[hook-bypass]   {hook_id}: {len(rows)}x ({reasons}), bound "
                      f"{rows[-1].get('bound_s')} s, max elapsed "
                      f"{max(float(r.get('elapsed_s') or 0) for r in rows):g} s, "
                      f"last {rows[-1].get('ts')}")
    sys.stdout.write("\n".join(report) + "\n")
    return 0


# --- check ------------------------------------------------------------------------------------

def check(settings_path: Path) -> list[str]:
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"{settings_path}: unreadable ({exc!r})"]
    violations: list[str] = []
    for event, blocks in (settings.get("hooks") or {}).items():
        for block in blocks:
            for hook in block.get("hooks", []):
                command = str(hook.get("command", ""))
                label = f"{event}: {command[:120]}"
                timeout = hook.get("timeout")
                if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0:
                    violations.append(f"{label} -- no explicit `timeout`; every hook carries a "
                                      "bound (the harness default is 600 s per call)")
                wrapped = _WRAPPED_RE.search(command)
                if wrapped and isinstance(timeout, (int, float)):
                    bound = float(wrapped.group("bound"))
                    if timeout < bound + HARNESS_HEADROOM_S:
                        violations.append(
                            f"{event}: {wrapped.group('id')} -- harness timeout {timeout} s leaves "
                            f"less than {HARNESS_HEADROOM_S} s over its --bound {bound:g} s, so "
                            "the harness can cancel the wrapper before it records the bypass")
                posture = posture_for(command)
                if posture is None:
                    violations.append(f"{label} -- no stated posture in bounded_hook.POSTURES")
                    continue
                if posture.posture == "escalated" and wrapped:
                    violations.append(f"{event}: {posture.hook_id} -- escalated (class b) but "
                                      "routed through the wrapper, which decides its posture")
                if posture.wrapped and (not wrapped or wrapped.group("id") != posture.hook_id):
                    violations.append(f"{event}: {posture.hook_id} -- stated as wrapped but not "
                                      f"registered as `bounded_hook.py run --id {posture.hook_id}`")
    return violations


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="verb", required=True)
    p_run = sub.add_parser("run", help="run a hook command inside a bound")
    p_run.add_argument("--id", required=True, dest="hook_id")
    p_run.add_argument("--bound", required=True, type=float)
    p_run.add_argument("--posture", choices=("open", "closed"), default="open")
    p_run.add_argument("command", nargs=argparse.REMAINDER)
    p_surface = sub.add_parser("surface", help="print recent bypasses (SessionStart)")
    p_surface.add_argument("--hours", type=float, default=SURFACE_WINDOW_H)
    p_check = sub.add_parser("check", help="refuse unbounded or posture-less registrations")
    p_check.add_argument("--settings", type=Path, default=_REPO_ROOT / ".claude" / "settings.json")
    args = parser.parse_args(argv)

    if args.verb == "run":
        command = args.command[1:] if args.command[:1] == ["--"] else args.command
        if not command:
            parser.error("run needs a command after --")
        run(args.hook_id, args.bound, args.posture, command)
        return 0  # unreachable: run() always exits through _finish
    if args.verb == "surface":
        return surface(args.hours)
    violations = check(args.settings)
    for violation in violations:
        sys.stdout.write(f"[hook-bound] REFUSED {violation}\n")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
