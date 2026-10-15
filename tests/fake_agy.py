"""A fake `agy` box and a fake clock for the Codespace launcher's agy sign-in tests ([#1537]).

`FakeAgy` answers the four helper verbs of `dispatch._credential_tools_script` the way a Codespace
would -- `agy-signin-start`, `agy-signin-code` (the code on STDIN), `agy-probe <nonce>`,
`agy-signin-stop` and `agy-signin-diag` -- so a test drives the whole operator-link flow with no
network, no `gh`, no `agy` and no real credential. Every value is fake: the URL ends in `.invalid`
and the code is a sentinel the tests compare against, never print.

Run as a script, `python tests/fake_agy.py menu [pidfile]` is a fake `agy` PROCESS for the helper's
login-menu test: it draws agy 1.3.5's "Select login method" menu, waits for a carriage return or a
newline on stdin, and only then prints the (fake) authorization URL -- the live behaviour of 2026-10-15.

`FakeClock` stands in for the `sleep` and `clock` seams: `sleep(s)` advances time instead of waiting,
and `at(offset, action)` schedules the "operator" -- an action (typically writing the channel file)
that fires the first time the clock has passed `start + offset`.
"""
from __future__ import annotations

import os
import select
import sys
import time
from typing import Callable, Optional, Sequence

try:  # absent when this file runs as a script (`python tests/fake_agy.py menu`): then only `_menu_main` is used
    import dispatch as d
except ImportError:  # pragma: no cover - script mode
    d = None  # type: ignore[assignment]

FAKE_URL = "https://agy.invalid/signin?state=fake-not-real"
FAKE_CODE = "SENTINEL-AGY-CODE-4f9a2c7e1b"

#: What `agy-signin-diag` prints: `name=yes|no` facts, a byte count, then sanitized output lines
#: (every URL already replaced by `<url>`).
FAKE_DIAG_LINES = ("SSH_CONNECTION=no", "SSH_TTY=no", "BROWSER=no", "DISPLAY=no",
                   "DBUS_SESSION_BUS_ADDRESS=no", "agy_alive=no", "out_bytes=0",
                   "Sign in at <url> and paste the code")

VERBS = ("agy-signin-start", "agy-signin-code", "agy-probe", "agy-signin-stop", "agy-signin-diag")


class FakeAgy:
    """The box side of an agy sign-in. `url=None` is an agy that prints no authorization URL."""

    def __init__(self, *, url: Optional[str] = FAKE_URL, expected_code: str = FAKE_CODE,
                 echo_code: bool = False, diag_lines: Sequence[str] = FAKE_DIAG_LINES) -> None:
        self.url = url
        self.expected_code = expected_code
        self.echo_code = echo_code          # a box that (wrongly) answers with the code it was given
        self.diag_lines = tuple(diag_lines)
        self.started = 0
        self.stopped = 0
        self.diag_calls = 0
        self.signed_in = False
        self.code_stdin: list[bytes] = []   # the exact bytes each `agy-signin-code` received
        self.probes: list[str] = []         # the nonce of each `agy-probe`
        self.verbs: list[str] = []          # every verb, in call order

    def handle(self, tail: Sequence[str], input_bytes: Optional[bytes] = None) -> "d.GhResult":
        """Answer one helper call; `tail` is the argv after the helper path (verb first)."""
        verb = tail[0]
        self.verbs.append(verb)
        if verb == "agy-signin-start":
            self.started += 1
            if self.url:
                return d.GhResult(True, 0, self.url + "\n")
            return d.GhResult(False, 70, "")
        if verb == "agy-signin-code":
            if input_bytes is None or not self.started or not self.url:
                return d.GhResult(False, 67, "", "no agy sign-in is waiting\n")
            self.code_stdin.append(input_bytes)
            self.signed_in = input_bytes.decode("utf-8", "replace").strip() == self.expected_code
            return d.GhResult(True, 0, (self.expected_code + "\n") if self.echo_code else "")
        if verb == "agy-probe":
            nonce = tail[1] if len(tail) > 1 else ""
            self.probes.append(nonce)
            if self.signed_in:
                return d.GhResult(True, 0, nonce + "\n")
            return d.GhResult(False, 1, "Please sign in to continue\n")
        if verb == "agy-signin-stop":
            self.stopped += 1
            self.signed_in = False
            return d.GhResult(True, 0, "")
        if verb == "agy-signin-diag":
            self.diag_calls += 1
            return d.GhResult(True, 0, "\n".join(self.diag_lines) + "\n")
        raise AssertionError(f"FakeAgy was asked for an unknown verb: {tail}")


class FakeClock:
    """Time that only moves when something sleeps. `now` is the `clock` seam, `sleep` the `sleep` seam."""

    RUNAWAY_SLEEPS = 5000

    def __init__(self, start: float = 1000.0) -> None:
        self.start = start
        self.t = start
        self.sleeps: list[float] = []
        self._events: list[tuple[float, Callable[[], None]]] = []

    def now(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        if len(self.sleeps) >= self.RUNAWAY_SLEEPS:
            raise AssertionError("FakeClock: runaway wait loop (the wait never ended)")
        self.sleeps.append(seconds)
        self.t += seconds
        due = [e for e in self._events if self.t >= self.start + e[0]]
        self._events = [e for e in self._events if e not in due]
        for _offset, action in due:
            action()

    def at(self, offset_s: float, action: Callable[[], None]) -> None:
        """Run `action` the first time the clock has passed `start + offset_s` -- the operator."""
        self._events.append((offset_s, action))


MENU_TEXT = (
    " Welcome to the Antigravity CLI. You are currently not signed in.\n"
    " Select login method:\n"
    " > 1. Google OAuth\n"
    "   2. Use a Google Cloud project\n"
    "   ↑/↓ Navigate · enter Select\n"
)
MENU_URL = "https://agy.invalid/oauth?state=fake-not-real"


def _menu_main(argv: Sequence[str]) -> int:
    """A fake agy that shows the login menu and prints the URL only after Enter (CR or LF) arrives."""
    if len(argv) > 1:
        with open(argv[1], "w", encoding="utf-8") as fh:
            fh.write(str(os.getpid()))
    sys.stdout.buffer.write(MENU_TEXT.encode("utf-8"))   # bytes: the box is UTF-8 whatever the locale
    sys.stdout.buffer.flush()
    fd = sys.stdin.fileno()
    seen = b""
    while b"\r" not in seen and b"\n" not in seen:
        chunk = os.read(fd, 64)
        if not chunk:
            return 1                      # stdin closed before anyone chose a method
        seen += chunk
    sys.stdout.write(f"Open this URL to sign in: {MENU_URL}\n")
    sys.stdout.flush()
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:    # wait for the pasted code, as the real agy would
        try:
            ready, _, _ = select.select([fd], [], [], 1.0)
        except OSError:                   # select() on a pipe is POSIX-only; the helper test runs on Linux
            time.sleep(1.0)
            continue
        if ready and not os.read(fd, 64):
            break
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "menu":
        sys.exit(_menu_main(sys.argv[1:]))
    sys.exit("usage: fake_agy.py menu [pidfile]")
