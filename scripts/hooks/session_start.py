"""The ONE SessionStart entry: every former SessionStart reader, in ONE interpreter, bounded.

WHY ([#1001], batch BW lane `lane-bw-1001-sessionstart-one`, R96 D9 / package T5.4). Until this
file, `.claude/settings.json` registered NINE SessionStart commands, each its own
`uv run --locked python <reader>` -- nine interpreters per session start, and an injected
context of 10,126 bytes (median, measured). The measurement, per reader, is
`docs/audits/2026-10-13-technical-lane-bw-1001-sessionstart-measurement.md`. Now there is one
command, launched through the shared launcher (`scripts/hooks/hook_launcher.py`), and it runs
the readers below by IMPORT, each on its own thread, so the network-bound ones (gh, version
probes) overlap rather than queue.

WHAT IT KEEPS. Every reader still runs its own entry point unchanged, so every line it prints
is still printed: the refusal and advisory lines each reader's own tests pin are produced by the
same code as before. This file only CAPTURES each reader's stdout and stderr, and composes them
in the declared order -- never finish order, so the boot text reads the same every session.

WHAT IT BOUNDS. The composed stdout -- what Claude Code folds into the session's context -- is
held to `OUTPUT_CAP_BYTES`, each line to `LINE_CAP_BYTES`. A line over the line cap is shortened
in place. If the total is still over the cap, lines are cut from the END, but a line whose tag
is in `PROTECTED_TAGS` (a refusal, a warning, a failure this file reports itself) is never cut:
the cut costs digest detail, never a warning. The cut is announced in one line that says how
many lines went and how to read them all (`--full`, by hand).

WHAT IT DOES NOT DO. It does not refuse: a SessionStart hook cannot stop a session (measured,
recorded in `scripts/fleet_health.py`), so it always exits 0. A reader that exits non-zero, or
raises, is NAMED in one protected line rather than turning the whole entry's exit code -- under
Claude Code a SessionStart exit of 2 drops stdout from the context, so one reader's signal would
otherwise cost every other reader's lines. A reader still running at `DEADLINE_S` is named and
left behind (its thread is a daemon), never waited on.

STDLIB ONLY. This module imports nothing outside the standard library and spawns no process.
The readers keep their own imports (they ran under the same `uv run --locked` interpreter
before); they are imported lazily, inside the functions below, so a reader that cannot be
imported is reported as that reader's failure and costs nobody else's lines.
"""
from __future__ import annotations

import io
import logging
import sys
import threading
import time
from pathlib import Path
from typing import Callable, NamedTuple, Optional, Sequence

ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = ROOT / "scripts"
_HOOKS = _SCRIPTS / "hooks"

#: The byte cap on the injected stdout. Measured before this file: 10,126 bytes median across
#: the nine entries, 9,222 of them from `fleet_health.py` alone (most of it the `[hook-rate]` /
#: `[hook-BROKEN]` / `[hook-ADVISORY]` lines, several over 400 bytes each). Set under Claude
#: Code's own 10,000-character hook-output ceiling, with the line cap below doing most of the work.
OUTPUT_CAP_BYTES = 8192

#: The byte cap on one line. Long enough for every tag, id and verdict a line leads with; the
#: tail it trims is the prose remedy, which `--full` prints whole.
LINE_CAP_BYTES = 240

#: How long the entry waits for its readers, all together, before naming the stragglers. Under
#: the settings entry's own timeout (60 s) so the entry always gets to print what it has.
DEADLINE_S = 45.0

#: Lines that are never cut by the overflow rule: refusals, warnings and failures. The tag is a
#: line's leading `[...]` token.
PROTECTED_TAGS = frozenset({
    "[prompts]", "[prompts-guard]", "[billing]", "[gh]", "[self-arm]", "[asks]",
    "[hook-BROKEN]", "[hook-ADVISORY]", "[session-start]",
})

_FULL_FLAG = "--full"

log = logging.getLogger("session_start")


class Reader(NamedTuple):
    reader_id: str
    script: str  # repo-relative path of the reader's module, the file it used to be wired as
    entry: Callable[[], Optional[int]]


# --- the readers ------------------------------------------------------------------------------
# Each is a plain `import` inside a function: lazy (a broken reader fails alone), and still a
# static import the file-purpose graph reads as this file's wiring edge to the reader.

def _ensure_paths() -> None:
    for p in (str(ROOT), str(_SCRIPTS), str(_HOOKS)):
        if p not in sys.path:
            sys.path.insert(0, p)


def _fleet_health() -> int:
    import fleet_health
    return fleet_health.main([])


def _billing_leak_sentinel() -> int:
    import billing_leak_sentinel
    return billing_leak_sentinel.main()


def _surface_triage() -> int:
    import surface_triage
    return surface_triage.main()


def _changelog_sentinel() -> int:
    import changelog_sentinel
    return changelog_sentinel.main()


def _arm_hooks() -> int:
    import arm_hooks
    return arm_hooks.main(ROOT)


def _conductor() -> int:
    import conductor
    return conductor.main(["session-start"])


def _resource_lifecycle() -> None:
    import resource_lifecycle
    resource_lifecycle.cmd_session_start.callback()


def _codespace_regime() -> None:
    import codespace_regime
    codespace_regime.cmd_session_start.callback()


def _quota_daily() -> int:
    import quota_daily
    return quota_daily.main([])


#: The readers, in OUTPUT order. `fleet_health` leads because its prompts-dir banner and guard
#: preflight are documented to render first ("a boot banner nobody reaches is not a banner").
READERS: tuple[Reader, ...] = (
    Reader("fleet-health", "scripts/fleet_health.py", _fleet_health),
    Reader("billing-leak-sentinel", "scripts/billing_leak_sentinel.py", _billing_leak_sentinel),
    Reader("surface-triage", "scripts/surface_triage.py", _surface_triage),
    Reader("changelog-sentinel", "scripts/changelog_sentinel.py", _changelog_sentinel),
    Reader("arm-hooks", "scripts/arm_hooks.py", _arm_hooks),
    Reader("conductor-session-start", "scripts/conductor.py", _conductor),
    Reader("resource-lifecycle", "scripts/resource_lifecycle.py", _resource_lifecycle),
    Reader("codespace-regime", "scripts/codespace_regime.py", _codespace_regime),
    Reader("quota-daily", "scripts/hooks/quota_daily.py", _quota_daily),
)

#: Former SessionStart readers this entry does NOT run, each with why. Empty: all nine run.
DROPPED: tuple[tuple[str, str], ...] = ()


# --- capture ----------------------------------------------------------------------------------

class _ThreadRouter(io.TextIOBase):
    """A text stream that writes to the CALLING thread's buffer. A thread that was never bound
    (a reader's own helper thread) writes to the shared `stray` buffer, which is composed last."""

    def __init__(self, stray: io.StringIO) -> None:
        super().__init__()
        self._local = threading.local()
        self._stray = stray
        self._lock = threading.Lock()

    encoding = "utf-8"
    errors = "replace"

    def bind(self, buf: io.StringIO) -> None:
        self._local.buf = buf

    def writable(self) -> bool:
        return True

    def isatty(self) -> bool:
        return False

    def write(self, s: str) -> int:
        buf = getattr(self._local, "buf", None)
        if buf is None:
            with self._lock:
                self._stray.write(s)
        else:
            buf.write(s)
        return len(s)

    def flush(self) -> None:
        return None


class _Payload(io.TextIOBase):
    """The hook's stdin JSON, read ONCE by this entry and handed whole to the FIRST read on each
    thread -- a reader that reads stdin from its own helper thread still gets the payload, and a
    reader that reads until EOF gets EOF next, never the payload again."""

    def __init__(self, text: str) -> None:
        super().__init__()
        self._text = text
        self._local = threading.local()

    def readable(self) -> bool:
        return True

    def isatty(self) -> bool:
        return False

    def read(self, size: int = -1) -> str:
        if getattr(self._local, "consumed", False):
            return ""
        self._local.consumed = True
        return self._text

    def readline(self, size: int = -1) -> str:
        return self.read()


class _Sink(io.TextIOBase):
    """Where a straggler reader's late writes go once the entry has composed its output: a
    reader still running at the deadline must not print past the byte cap."""

    def writable(self) -> bool:
        return True

    def write(self, s: str) -> int:
        return len(s)


def read_payload(stream, timeout: float = 2.0) -> str:
    """The hook payload on `stream`, bounded: an unbounded stdin read is how a hook wedges."""
    if stream is None:
        return ""
    try:
        if stream.isatty():
            return ""
    except (AttributeError, ValueError, OSError):
        return ""
    box: list[str] = []
    reader = threading.Thread(target=lambda: box.append(stream.read()), daemon=True)
    reader.start()
    reader.join(timeout)
    return box[0] if box else ""


class _Result:
    __slots__ = ("out", "err", "rc", "raised", "seconds", "done")

    def __init__(self) -> None:
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.rc: Optional[int] = None
        self.raised: Optional[BaseException] = None
        self.seconds = 0.0
        self.done = threading.Event()


def _run_one(reader: Reader, result: _Result, out: _ThreadRouter, err: _ThreadRouter) -> None:
    out.bind(result.out)
    err.bind(result.err)
    t0 = time.perf_counter()
    try:
        rc = reader.entry()
        result.rc = rc if isinstance(rc, int) else 0
    except SystemExit as exc:
        code = exc.code
        result.rc = code if isinstance(code, int) else (0 if code is None else 1)
    except BaseException as exc:  # noqa: BLE001 -- a reader's failure is reported, never fatal
        result.raised = exc
    finally:
        result.seconds = time.perf_counter() - t0
        result.done.set()


# --- composition ------------------------------------------------------------------------------

def _tag(line: str) -> str:
    if line.startswith("["):
        end = line.find("]")
        if end > 0:
            return line[:end + 1]
    return ""


def _shorten(line: str, cap: int) -> str:
    raw = line.encode("utf-8")
    if len(raw) <= cap:
        return line
    marker = " ..."
    return raw[:cap - len(marker)].decode("utf-8", errors="ignore") + marker


def compose(lines: Sequence[str], cap: int = OUTPUT_CAP_BYTES,
            line_cap: int = LINE_CAP_BYTES) -> list[str]:
    """`lines` shortened to `line_cap` each and cut from the end to fit `cap`, never cutting a
    protected line; the cut, if any, announced in one last protected line."""
    kept = [_shorten(line, line_cap) for line in lines]

    def size(ls: Sequence[str]) -> int:
        return sum(len(s.encode("utf-8")) + 1 for s in ls)

    if size(kept) <= cap:
        return kept
    dropped = 0
    total = size(kept)
    budget = cap - 160  # room for the notice line below
    i = len(kept) - 1
    while i >= 0 and total > budget:
        if _tag(kept[i]) not in PROTECTED_TAGS:
            total -= len(kept[i].encode("utf-8")) + 1
            del kept[i]
            dropped += 1
        i -= 1
    kept.append(f"[session-start] cut {dropped} line(s) at the {cap}-byte cap -- full text: "
                f"uv run --locked python scripts/hooks/session_start.py {_FULL_FLAG}")
    # Protected lines alone can still exceed the cap; shorten them further rather than drop one.
    while size(kept) > cap and line_cap > 60:
        line_cap -= 20
        kept = [_shorten(line, line_cap) for line in kept[:-1]] + kept[-1:]
    return kept


def run(readers: Sequence[Reader] = READERS, *, payload: str = "",
        deadline_s: float = DEADLINE_S, bounded: bool = True,
        silence_stragglers: bool = False) -> tuple[str, str]:
    """Run `readers` in this interpreter, one thread each; return (stdout, stderr) composed.

    With `silence_stragglers` (the hook's own call), a reader still running at the deadline
    leaves `sys.stdout` / `sys.stderr` pointed at a sink rather than the real streams, so its
    late lines cannot reach the context past the cap; the caller writes to the streams it saved."""
    _ensure_paths()
    stray_out, stray_err = io.StringIO(), io.StringIO()
    out_router, err_router = _ThreadRouter(stray_out), _ThreadRouter(stray_err)
    saved = (sys.stdout, sys.stderr, sys.stdin)
    results = [_Result() for _ in readers]
    sys.stdout, sys.stderr, sys.stdin = out_router, err_router, _Payload(payload)
    try:
        threads = [threading.Thread(target=_run_one, args=(r, res, out_router, err_router),
                                    name=f"session-start:{r.reader_id}", daemon=True)
                   for r, res in zip(readers, results)]
        for t in threads:
            t.start()
        end = time.monotonic() + deadline_s
        for res in results:
            res.done.wait(max(0.0, end - time.monotonic()))
    finally:
        sys.stdout, sys.stderr, sys.stdin = saved
        if silence_stragglers and not all(res.done.is_set() for res in results):
            sys.stdout, sys.stderr = _Sink(), _Sink()

    out_lines: list[str] = []
    err_parts: list[str] = []
    for reader, res in zip(readers, results):
        if not res.done.is_set():
            out_lines.append(f"[session-start] {reader.reader_id} still running after "
                             f"{deadline_s:g} s -- its lines are not in this digest")
            log.warning("%s still running after %g s", reader.reader_id, deadline_s)
            continue
        out_lines.extend(res.out.getvalue().splitlines())
        err_parts.append(res.err.getvalue())
        if res.raised is not None:
            out_lines.append(f"[session-start] {reader.reader_id} raised "
                             f"{type(res.raised).__name__}: {res.raised}")
        elif res.rc:
            out_lines.append(f"[session-start] {reader.reader_id} exited {res.rc}")
        log.debug("%s rc=%s %.2fs", reader.reader_id, res.rc, res.seconds)
    out_lines.extend(stray_out.getvalue().splitlines())
    err_parts.append(stray_err.getvalue())

    err_text = "".join(err_parts)
    if bounded:
        out_lines = compose(out_lines)
        err_text = "\n".join(compose(err_text.splitlines())) + ("\n" if err_text else "")
    out_text = "\n".join(out_lines) + ("\n" if out_lines else "")
    return out_text, err_text


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    payload = read_payload(sys.stdin)
    real_out, real_err = sys.stdout, sys.stderr
    out, err = run(payload=payload, bounded=_FULL_FLAG not in args, silence_stragglers=True)
    for stream, text in ((real_out, out), (real_err, err)):
        try:
            stream.reconfigure(errors="replace")  # a reader's non-ASCII never costs the digest
        except (AttributeError, ValueError):
            pass
        try:
            stream.write(text)
            stream.flush()
        except (OSError, ValueError, UnicodeError):  # a closed or narrow console never fails boot
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
