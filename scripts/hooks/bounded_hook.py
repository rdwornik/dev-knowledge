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

THE WIRING IS HELD (operator ruling 2026-09-17, item 1). No hook in `.claude/settings.json` is
routed through `run`: the wrapper bounds only what it starts, and it adds an interpreter to every
hook, which makes the measured failure -- hook interpreters created suspended, never resumed --
likelier rather than less. Every `POSTURES` entry is therefore `wrapped=False`, and the surface
rides inside the SessionStart hook that already runs (`fleet_health.hook_bypass_lines`).

THE BYPASS RATE IS THE SIGNAL (same ruling, item 2). Fail-open-silently is the state that let the
guards time out unseen for days; fail-closed on a guard that cannot start wedges the box. So a
hook whose bypass rate exceeds `BROKEN_RATE` over `RATE_WINDOW_H`, on at least `BROKEN_MIN_RUNS`
runs, is DECLARED BROKEN: written to `HOOK-BYPASSES-BROKEN.json` beside the record with its
numbers and a draft row, printed at every SessionStart, and skipped by `run` without being started.
The rate reads two sources that never overlap: this wrapper's own run rows, and the transcripts'
hook attachments for every hook the wrapper did not run (`scan_transcripts`, incremental and
time-boxed). A declaration is sticky -- a disabled hook produces no runs, so a declaration that
lapsed with the rate would re-arm a broken guard by itself -- until `reinstate` clears it, and the
count restarts from the reinstatement.

WHAT THIS CANNOT DO, stated rather than implied. (1) The disable acts only through `run`, and the
wiring is held, so today no hook it declares is actually stopped by it: the declaration says so in
its own line. Claude Code offers no per-hook off switch outside the tracked settings file
(`settings.local.json` cannot cancel a project hook; `disableAllHooks` is all-or-nothing, measured
2026-09-15). (2) The row is DRAFTED, not filed: filing needs an id reservation, a branch and a
commit, and a SessionStart hook in the primary checkout may do none of those.

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
from datetime import datetime, timedelta, UTC
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
KILL_GRACE_S = 1.0

SURFACE_WINDOW_H = 72
SURFACE_TAIL_LINES = 50000

#: THE STATED FRACTION AND WINDOW (operator ruling 2026-09-17, item 2). A guard that is skipped on
#: more than one call in ten is not enforcing its rule; seven days spans a working week, so a bad
#: afternoon on a loaded box does not condemn a hook, and a hook that fails all week cannot hide.
#: Strictly GREATER than the fraction declares. Below `BROKEN_MIN_RUNS` runs the rate is printed
#: and called a thin sample, never declared.
BROKEN_RATE = 0.10
RATE_WINDOW_H = 168
BROKEN_MIN_RUNS = 20

#: Wall-clock the transcript scan may spend per SessionStart. The store is append-only JSONL
#: (1.4 GB, 1,036 files measured 2026-09-17; a cold full read took 11 s), so the scan resumes from
#: per-file byte offsets and a boot pays for new bytes only. A scan cut off by the budget is
#: PARTIAL and declares nothing. Two seconds, not more: the scan rides inside `fleet_health.py`'s
#: SessionStart hook, which itself timed out on 107 of 263 boots in the week measured (41%).
SCAN_BUDGET_S = 2.0
TRANSCRIPTS_ENV = "DEV_KNOWLEDGE_HOOK_TRANSCRIPTS"
TRANSCRIPT_GLOB = "*dev-knowledge*"

#: Reasons that are a skip of the hook's judgement. `pipe-held-after-exit` is surfaced as a skip
#: of the seat's TIME but the verdict stood, so it is a run and not a bypass in the rate;
#: `declared-broken` is neither -- it is the declaration acting, and must not feed itself.
BYPASS_REASONS = frozenset({"timeout"})
NOT_A_RUN = frozenset({"declared-broken"})

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


#: One entry per hook registered in `.claude/settings.json`, plus the guards held off it pending
#: their conditions, first match wins. `match` is a substring of the registered command; `check`
#: refuses a hook no entry matches. The fail-open reasons state the posture the hook takes IF
#: wrapped; every entry is `wrapped=False` while the wiring is held.
POSTURES: tuple[Posture, ...] = (
    Posture("prompts-guard", "--prompts-guard", "escalated", False,
            "AX15-1 rules this guard FAIL-CLOSED on any inability to evaluate, and a timeout is "
            "one. Measured: the harness fails it OPEN at its bound, silently -- 1,066 timeouts "
            "in the week to 2026-09-17, 6% of the calls it matched across every session -- the "
            "event-fired denominator (X-3, operator ruling 2026-09-17; a recorded-only one reads "
            "13% and is the bias behind the retracted 83%). Which way it goes past its bound is a class "
            "(b) ruling, not a wrapper default -- so it is escalated. Removed from the settings "
            "file by the 2026-09-17 emergency order."),
    Posture("immutable-edits-guard", "block_immutable_edits.py", "escalated", False,
            "ADR-77 transcript-immutability guard, fail-CLOSED in-zone by design. It carried no "
            "timeout, so the measured 600 s harness default applied. Whether it may fail open "
            "sooner is a class (b) ruling. Removed from the settings file by the 2026-09-17 "
            "emergency order."),
    Posture("deny-and-point", "deny_and_point.py", "fail-open", False,
            "[#727] nudge, fail-OPEN by its own design. Held OFF the settings file since "
            "2026-09-15; 182 timeouts in the week to 2026-09-17, 2% of the calls it matched. "
            "Named here so its transcript rate is read under a stable id."),
    Posture("session-end-backpressure", "session_end_backpressure.py", "fail-open", False,
            "Advisory in full since the ADR-85 amendment A5: it cannot block a turn, so skipping "
            "it past its bound loses a nudge, never a gate."),
    Posture("fleet-health-session-start", "fleet_health.py\"", "fail-open", False,
            "SessionStart surfacing: a SessionStart hook cannot refuse (measured 2026-09-06), so "
            "a bypass loses a digest line, never a gate. The per-call prompts guard is separate."),
    Posture("surface-triage", "surface_triage.ps1", "fail-open", False,
            "SessionStart surfacing only; cannot refuse."),
    Posture("billing-leak-sentinel", "billing_leak_sentinel.ps1", "fail-open", False,
            "SessionStart sentinel; cannot refuse. A bypass loses one warning for one session."),
    Posture("changelog-sentinel", "changelog_sentinel.py", "fail-open", False,
            "SessionStart nudge, local and fail-soft by its own design."),
    Posture("arm-hooks", "arm_hooks.py", "fail-open", False,
            "Idempotent self-arm; the git hooks it arms stay armed from the previous session, and "
            "audit.py check_hooks_armed is the backstop."),
    Posture("conductor-session-start", "conductor.py\" session-start", "fail-open", False,
            "SessionStart surfacing of the conductor; cannot refuse."),
    Posture("logs-retention", "logs_retention.py", "fail-open", False,
            "Relocation housekeeping; the next session repeats it."),
    Posture("resource-lifecycle", "resource_lifecycle.py\" session-start", "fail-open", False,
            "SessionStart surfacing of seat/memory state; admission itself is a separate act."),
    Posture("codespace-regime", "codespace_regime.py\" session-start", "fail-open", False,
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
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


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
        # FIRED, NOT AWAITED. `taskkill /T` was measured taking >10 s on a loaded box, and a
        # wrapper that waits on its own kill has moved the unbounded wait one level down.
        # taskkill runs on after this process exits; its std handles are DEVNULL, so it holds
        # no pipe of ours or the harness's.
        try:
            subprocess.Popen(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        except OSError:
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


def _row(hook_id: str, bound_s: float, elapsed: float, fields: dict, reason: str,
         stated: str) -> dict:
    return {"ts": _utc_now(), "hook_id": hook_id, "bound_s": bound_s, "elapsed_s": elapsed,
            "session_id": fields.get("session_id") or "unknown",
            "event": fields.get("hook_event_name") or "unknown",
            "tool": fields.get("tool_name"), "reason": reason, "posture": stated,
            "cwd": fields.get("cwd") or os.getcwd()}


def run(hook_id: str, bound_s: float, posture: str, argv: list[str]) -> None:
    started = time.monotonic()
    payload = _read_stdin(min(bound_s, 5.0))
    fields = _payload_fields(payload)
    stated = "fail-closed" if posture == "closed" else "fail-open"

    broken = load_declarations()["broken"].get(hook_id)
    if broken:
        # DISABLED AUTOMATICALLY (operator ruling 2026-09-17, item 2): not started at all. Open
        # whatever the posture -- a guard declared broken is not enforcing anything, and refusing
        # in its name would wedge the seat for a check that does not happen.
        append_record(_row(hook_id, bound_s, 0.0, fields, "declared-broken", stated))
        message = (f"[hook-bypass] {hook_id} is DECLARED BROKEN ({broken.get('bypasses')}/"
                   f"{broken.get('runs')} runs bypassed over {broken.get('window_h')} h, declared "
                   f"{broken.get('declared_at')}) and was NOT RUN. Reinstate once fixed: "
                   f"bounded_hook.py reinstate --id {hook_id}")
        _finish(0, (json.dumps({"systemMessage": message}) + "\n").encode("utf-8"))

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

    elapsed = round(time.monotonic() - started, 3)
    if reason is None:
        # A RUN row: the rate's denominator. A rate with no denominator is a count of failures
        # that cannot say whether the hook is mostly working.
        append_record(_row(hook_id, bound_s, elapsed, fields, "ok", stated))
        _finish(proc.returncode, bytes(out), bytes(err))

    where = append_record(_row(hook_id, bound_s, elapsed, fields, reason, stated))
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


# --- the rate: declarations ------------------------------------------------------------------

def declarations_path() -> Path:
    return record_path().with_name("HOOK-BYPASSES-BROKEN.json")


def scan_cache_path() -> Path:
    return record_path().with_name("HOOK-BYPASSES-SCAN-CACHE.json")


def _read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_json(path: Path, data: dict) -> bool:
    """Whole-file replace through a temp file: two seats booting together each write a complete
    state, and the last one wins -- a lost increment, never a torn file or a double count."""
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, path)
    except OSError as exc:
        LOG.warning("[hook-rate] could not write %s: %r", path, exc)
        try:
            tmp.unlink()
        except OSError:
            pass
        return False
    return True


def load_declarations() -> dict:
    data = _read_json(declarations_path())
    return {"broken": dict(data.get("broken") or {}),
            "reinstated": dict(data.get("reinstated") or {})}


def reinstate(hook_id: str) -> int:
    data = load_declarations()
    was = data["broken"].pop(hook_id, None)
    data["reinstated"][hook_id] = _utc_now()
    if not _write_json(declarations_path(), data):
        return 1
    sys.stdout.write(f"[hook-rate] {hook_id} reinstated at {data['reinstated'][hook_id]}"
                     f"{'' if was else ' (it was not declared broken)'}; its rate counts from "
                     "now.\n")
    return 0


# --- the rate: sources -----------------------------------------------------------------------

def _hour(ts: str) -> str:
    return ts[:13]  # "2026-09-17T10" -- ISO, UTC, sortable as a string


def _record_rows() -> list[dict]:
    try:
        lines = record_path().read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    rows = []
    for line in lines[-SURFACE_TAIL_LINES:]:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and isinstance(row.get("ts"), str) and row.get("hook_id"):
            rows.append(row)
    return rows


def transcripts_root() -> Path:
    override = os.environ.get(TRANSCRIPTS_ENV, "").strip()
    return Path(override) if override else Path.home() / ".claude" / "projects"


_SCRIPT_RE = re.compile(r"([\w.-]+\.(?:py|ps1|sh|js|cmd|bat))\b")


def _transcript_hook_id(command: str) -> str:
    """A `POSTURES` id for a hook this repo states; otherwise `cmd:<script>` -- the script's
    basename, which survives a path or interpreter change that a truncated command would not."""
    posture = posture_for(command)
    if posture:
        return posture.hook_id
    scripts = _SCRIPT_RE.findall(command)
    return "cmd:" + (scripts[-1] if scripts else " ".join(command.split())[:80])


#: The SessionStart hook this report prints from. It is held to the same bar as every other hook
#: and is NOT exempted (operator ruling 2026-09-17, X-4): a measurement organ that is broken must
#: say so, in its own output. It is named here only so the report can state its own status.
HOST_HOOK_ID = "fleet-health-session-start"


def _scope(hook_id: str) -> str:
    """`repo` for a hook this repo states a posture for; `advisory` for one it cannot stop --
    user-level or plugin-registered (operator ruling 2026-09-17, X-5)."""
    return "repo" if any(p.hook_id == hook_id for p in POSTURES) else "advisory"


def _disabled_text(hook_id: str) -> str:
    """What a declaration can actually do, stated -- never implied (X-1). While the wiring is held
    every repo declaration says NO, and that is correct: the declaration is a SIGNAL until the
    suspended-start cause is fixed upstream."""
    posture = next((p for p in POSTURES if p.hook_id == hook_id), None)
    if posture is None:
        return ("NO -- ADVISORY: registered outside this repo (user-level or a plugin); this repo "
                "observes it and cannot stop it, so it belongs to the user-level disable")
    if posture.wrapped:
        return "yes -- `bounded_hook.py run` no longer starts it"
    return ("NO -- not routed through `bounded_hook.py run` (wiring held by operator ruling "
            "2026-09-17), so it still runs wherever it is registered")


def _ingest(raw: bytes, state: dict, last_firing: dict) -> None:
    """Fold one transcript line into hour buckets: hook attachments, event firings, tool calls.

    ATTACHMENTS ARE NOT RUNS. A hook that passes silently writes no attachment on any event
    (measured 2026-09-17: 8,046 prompts-guard-matched calls carried 1,112 attachments; a quiet
    SessionStart hook attached in 109 of 263 firings). So FIRINGS are counted separately -- one per
    distinct `toolUseID` of a SessionStart/Stop event, one per `tool_use` for PreToolUse -- and they
    are the denominator `compute_rates` uses."""
    if b'"hook_' not in raw and b'"tool_use"' not in raw:
        return
    try:
        entry = json.loads(raw)
    except ValueError:
        return
    if not isinstance(entry, dict):
        return
    ts = entry.get("timestamp")
    if not isinstance(ts, str):
        return
    hour = _hour(ts)
    attachment = entry.get("attachment")
    if isinstance(attachment, dict) and str(attachment.get("type", "")).startswith("hook_"):
        event = str(attachment.get("hookEvent") or "")
        firing = attachment.get("toolUseID")
        if event != "PreToolUse" and firing and last_firing.get(event) != firing:
            last_firing[event] = firing
            key = f"{hour}\t{event}"
            state["firings"][key] = state["firings"].get(key, 0) + 1
        command = attachment.get("command")
        # Only an attachment naming its command is one run of that command. A wrapped command
        # is the wrapper record's to count; reading it here too would count it twice.
        if not isinstance(command, str) or re.search(r"bounded_hook\.py\"?\s+run\s", command):
            return
        key = "\t".join((hour, _transcript_hook_id(command), event))
        cell = state["hooks"].setdefault(key, [0, 0, []])
        cell[0] += 1
        cell[1] += attachment.get("timedOut") is True
        name = str(attachment.get("hookName") or "")
        tool = name.split(":", 1)[1] if event == "PreToolUse" and ":" in name else None
        if tool and tool not in cell[2]:
            cell[2].append(tool)
        return
    message = entry.get("message")
    if entry.get("type") == "assistant" and isinstance(message, dict) \
            and isinstance(message.get("content"), list):
        for block in message["content"]:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                key = f"{hour}\t{block.get('name')}"
                state["tools"][key] = state["tools"].get(key, 0) + 1


_TABLES = ("hooks", "firings", "tools")


def scan_transcripts(root: Path, cutoff_hour: str, budget_s: float) -> tuple[dict, bool]:
    """Read new bytes of every transcript into hour-bucketed counts; return (state, complete).

    INCREMENTAL: per-file byte offsets live in the cache, and only whole lines are consumed, so a
    line still being written is read next time. A file last modified before the window cannot
    hold a line inside it and is skipped unread. TIME-BOXED: past `budget_s` the scan stops where
    it is and says so; the next boot resumes."""
    started = time.monotonic()
    cache = _read_json(scan_cache_path())
    if cache.get("version") != 2:
        cache = {}  # an older cache counted differently; rebuild rather than mix estimators
    state = {"version": 2, "files": dict(cache.get("files") or {}),
             **{table: dict(cache.get(table) or {}) for table in _TABLES}}
    cutoff_epoch = datetime.strptime(cutoff_hour, "%Y-%m-%dT%H").replace(
        tzinfo=UTC).timestamp()
    try:
        files = sorted(root.glob(f"{TRANSCRIPT_GLOB}/*.jsonl"),
                       key=lambda f: f.stat().st_mtime, reverse=True)
    except OSError:
        files = []
    complete = True
    for path in files:
        try:
            stat = path.stat()
        except OSError:
            continue
        seen = state["files"].get(str(path)) or {}
        offset = int(seen.get("offset") or 0)
        last_firing = dict(seen.get("last_firing") or {})
        if offset > stat.st_size:
            offset, last_firing = 0, {}  # rewritten, not appended: read it again
        if offset == stat.st_size:
            continue
        if stat.st_mtime < cutoff_epoch:
            state["files"][str(path)] = {"offset": stat.st_size}
            continue
        if time.monotonic() - started >= budget_s:
            complete = False
            break
        try:
            with open(path, "rb") as fh:
                fh.seek(offset)
                while time.monotonic() - started < budget_s:
                    chunk = fh.read(8 << 20)
                    if not chunk:
                        break
                    whole = chunk.rfind(b"\n") + 1
                    if whole == 0:
                        break  # a single unfinished line: leave it for the next boot
                    for raw in chunk[:whole].splitlines():
                        _ingest(raw, state, last_firing)
                    offset += whole
                    fh.seek(offset)
        except OSError:
            continue
        state["files"][str(path)] = {"offset": offset, "last_firing": last_firing}
        if offset < stat.st_size and time.monotonic() - started >= budget_s:
            complete = False
            break
    for table in _TABLES:
        state[table] = {k: v for k, v in state[table].items() if k[:13] >= cutoff_hour}
    _write_json(scan_cache_path(), state)
    return state, complete


def compute_rates(now: datetime, budget_s: float = SCAN_BUDGET_S) -> tuple[dict, bool]:
    """Per hook id over `RATE_WINDOW_H`: {"runs", "bypasses", "sources"}; and whether complete.

    TRANSCRIPT RUNS ARE ESTIMATED, and the estimate is stated. Between the first and last hour a
    hook left any attachment, every firing of its event is taken as one run of it -- a hook
    registered for that span runs at every firing, silent or not. For PreToolUse the firings are
    the calls of the tools it was seen matching in the window. The attachment count is the floor.
    What this cannot see: a firing in a checkout whose settings did not register the hook (an
    older worktree), which counts as a run and so can only LOWER the rate -- never declare.

    ACROSS ALL SESSIONS, BY RULING (X-3, operator 2026-09-17). Restricting the count to the
    sessions that left a record is the recorded-only denominator -- precisely the bias that produced
    the retracted 83% -- so it is not an option here, however much higher a rate it reads."""
    cutoff = now - timedelta(hours=RATE_WINDOW_H)
    cutoff_ts = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")
    reinstated = load_declarations()["reinstated"]
    rates: dict[str, dict] = {}

    def cell(hook_id: str, source: str) -> dict:
        found = rates.setdefault(hook_id, {"runs": 0, "bypasses": 0, "sources": []})
        if source not in found["sources"]:
            found["sources"].append(source)
        return found

    for row in _record_rows():
        hook_id, reason, ts = str(row["hook_id"]), row.get("reason"), row["ts"]
        if ts < cutoff_ts or reason in NOT_A_RUN or ts <= reinstated.get(hook_id, ""):
            continue
        found = cell(hook_id, "wrapper record")
        found["runs"] += 1
        found["bypasses"] += reason in BYPASS_REASONS

    state, complete = scan_transcripts(transcripts_root(), cutoff.strftime("%Y-%m-%dT%H"),
                                       budget_s)
    seen: dict[tuple[str, str], dict] = {}
    for key, (attachments, bypasses, tools) in state["hooks"].items():
        hour, hook_id, event = key.split("\t")
        since = reinstated.get(hook_id)
        if since and hour <= _hour(since):
            continue
        agg = seen.setdefault((hook_id, event), {"att": 0, "bypasses": 0, "tools": set(),
                                                 "first": hour, "last": hour})
        agg["att"] += attachments
        agg["bypasses"] += bypasses
        agg["tools"].update(tools)
        agg["first"], agg["last"] = min(agg["first"], hour), max(agg["last"], hour)
    for (hook_id, event), agg in seen.items():
        if event == "PreToolUse":
            firings = sum(count for key, count in state["tools"].items()
                          if agg["first"] <= key[:13] <= agg["last"]
                          and key[14:] in agg["tools"])
        else:
            firings = sum(count for key, count in state["firings"].items()
                          if agg["first"] <= key[:13] <= agg["last"] and key[14:] == event)
        found = cell(hook_id, "transcripts")
        found["runs"] += max(agg["att"], firings)
        found["bypasses"] += agg["bypasses"]
    return rates, complete


# --- the rate: the declaration ----------------------------------------------------------------

def _draft_row(hook_id: str, decl: dict) -> str:
    """A DRAFT, written beside the record. A hook never files a row: filing needs an id, a branch
    and a commit, and cross-cutting writes from a hook are how a retention mover once wrote into a
    tree nobody could commit. The integrator files drafted rows at batch close (X-2)."""
    disabled = _disabled_text(hook_id)
    label = "DECLARED BROKEN (ADVISORY)" if decl["scope"] == "advisory" else "DECLARED BROKEN"
    return (f"- [#NNN] [P1][S] **Hook `{hook_id}` is {label}: {decl['bypasses']} of "
            f"{decl['runs']} runs bypassed ({decl['rate']:.0%}) over {decl['window_h']} h** - "
            f"Declared automatically by `scripts/hooks/bounded_hook.py` at {decl['declared_at']} "
            f"against the stated bar: more than {decl['threshold']:.0%} over {decl['window_h']} h "
            f"on at least {decl['min_runs']} runs (operator ruling 2026-09-17). Source: "
            f"{', '.join(decl['sources'])}. Disabled: {disabled}. · Done when: the hook is fixed "
            f"and reinstated (`bounded_hook.py reinstate --id {hook_id}`) and runs a full "
            f"{decl['window_h']} h window at or under the bar, or it is removed from every "
            "settings file that registers it")


def declare(rates: dict, complete: bool, now: datetime) -> list[str]:
    """Write a declaration for every hook over the bar; return the ids newly declared."""
    if not complete:
        return []
    data = load_declarations()
    fresh = []
    for hook_id, found in sorted(rates.items()):
        runs, bypasses = found["runs"], found["bypasses"]
        if hook_id in data["broken"] or runs < BROKEN_MIN_RUNS or bypasses / runs <= BROKEN_RATE:
            continue
        decl = {"declared_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "runs": runs,
                "bypasses": bypasses, "rate": round(bypasses / runs, 4),
                "threshold": BROKEN_RATE, "window_h": RATE_WINDOW_H,
                "min_runs": BROKEN_MIN_RUNS, "sources": found["sources"],
                "scope": _scope(hook_id)}
        decl["draft_row"] = _draft_row(hook_id, decl)
        data["broken"][hook_id] = decl
        fresh.append(hook_id)
    if fresh:
        _write_json(declarations_path(), data)
    return fresh


# --- surface ----------------------------------------------------------------------------------

def surface_lines(window_h: float = SURFACE_WINDOW_H, budget_s: float = SCAN_BUDGET_S,
                  now: datetime | None = None) -> list[str]:
    now = now or datetime.now(UTC)
    report: list[str] = []

    cutoff = (now - timedelta(hours=window_h)).strftime("%Y-%m-%dT%H:%M:%SZ")
    by_hook: dict[str, list[dict]] = {}
    for row in _record_rows():
        if row["ts"] >= cutoff and row.get("reason") not in ("ok", *NOT_A_RUN):
            by_hook.setdefault(str(row["hook_id"]), []).append(row)
    if by_hook:
        total = sum(len(rows) for rows in by_hook.values())
        report.append(f"[hook-bypass] {total} bypass(es) across {len(by_hook)} hook(s) in the "
                      f"last {window_h:g} h -- a hook that keeps timing out is DISARMED, not "
                      f"slow. Record: {record_path()}")
        for hook_id, rows in sorted(by_hook.items(), key=lambda kv: -len(kv[1])):
            reasons = ", ".join(sorted({str(r.get("reason")) for r in rows}))
            report.append(f"[hook-bypass]   {hook_id}: {len(rows)}x ({reasons}), bound "
                          f"{rows[-1].get('bound_s')} s, max elapsed "
                          f"{max(float(r.get('elapsed_s') or 0) for r in rows):g} s, "
                          f"last {rows[-1].get('ts')}")

    rates, complete = compute_rates(now, budget_s)
    declare(rates, complete, now)
    shown = {k: v for k, v in rates.items() if v["bypasses"]}
    if shown or not complete:
        report.append(f"[hook-rate] bypass rate over {RATE_WINDOW_H} h -- DECLARED BROKEN above "
                      f"{BROKEN_RATE:.0%} on >= {BROKEN_MIN_RUNS} runs"
                      + ("" if complete else "; transcript scan PARTIAL (time budget), resumes "
                         "next boot -- nothing is declared from a partial scan"))
    for hook_id, found in sorted(shown.items(), key=lambda kv: -kv[1]["bypasses"] / kv[1]["runs"]):
        runs, bypasses = found["runs"], found["bypasses"]
        verdict = ("thin sample" if runs < BROKEN_MIN_RUNS
                   else "OVER THE BAR" if bypasses / runs > BROKEN_RATE else "within the bar")
        report.append(f"[hook-rate]   {hook_id}: {bypasses}/{runs} bypassed "
                      f"({bypasses / runs:.0%}) -- {verdict} [{', '.join(found['sources'])}]")

    broken = load_declarations()["broken"]
    host = broken.get(HOST_HOOK_ID)
    if host:
        report.append(f"[hook-BROKEN] this report's own host ({HOST_HOOK_ID}) is DECLARED BROKEN: "
                      f"{host.get('bypasses')}/{host.get('runs')} runs bypassed over "
                      f"{host.get('window_h')} h -- on the boots it times out, this report is not "
                      "seen at all")
    for hook_id, decl in sorted(broken.items()):
        scope = decl.get("scope") or _scope(hook_id)
        tag = "[hook-ADVISORY]" if scope == "advisory" else "[hook-BROKEN]"
        report.append(f"{tag} {hook_id} DECLARED BROKEN {decl.get('declared_at')}: "
                      f"{decl.get('bypasses')}/{decl.get('runs')} runs bypassed over "
                      f"{decl.get('window_h')} h. Disabled: {_disabled_text(hook_id)}. "
                      f"Row NOT filed -- drafted to {declarations_path()}; the integrator files "
                      f"drafted rows at batch close. Reinstate: bounded_hook.py reinstate --id "
                      f"{hook_id}")
    return report


def surface(window_h: float = SURFACE_WINDOW_H, budget_s: float = SCAN_BUDGET_S) -> int:
    lines = surface_lines(window_h, budget_s)
    if lines:
        sys.stdout.write("\n".join(lines) + "\n")
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
    p_surface.add_argument("--scan-budget", type=float, default=SCAN_BUDGET_S)
    p_reinstate = sub.add_parser("reinstate", help="clear a DECLARED BROKEN hook; its rate "
                                                   "counts from now")
    p_reinstate.add_argument("--id", required=True, dest="hook_id")
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
        return surface(args.hours, args.scan_budget)
    if args.verb == "reinstate":
        return reinstate(args.hook_id)
    violations = check(args.settings)
    for violation in violations:
        sys.stdout.write(f"[hook-bound] REFUSED {violation}\n")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
