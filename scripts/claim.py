#!/usr/bin/env python
"""claim.py -- the claim marker as code (`lane-claim-marker`, BATCH-WAVE5B-N4 row 2).

WHAT THIS REFUSES. Two sessions once executed the same order and overwrote each other's files
(the CI/OS decision run, seat 71020de7 vs d4eded38, 2026-09-26). The rule "claim before work" is
prose today: every seat types `to-cc/<name>.CLAIMED-<session>` by hand, and a hand-typed check has
the same TOCTOU gap the rule exists to close -- two sessions can each see no marker, then each
create their own, and both proceed. This module makes the check-then-create ATOMIC instead of
advisory, and gives every template one command to call.

WHY THIS IS NOT `single_flight.py`. That module arbitrates two GIT CLONES that may never have
fetched each other's ref -- its mechanism (a git-ref compare-and-swap against a REMOTE) exists
because the racers it guards share no filesystem. Here the racers share exactly one filesystem:
the operator's `CLAUDE_PROMPTS_DIR` (a Drive-mounted folder every session mounts at the same local
path). The arbiter is therefore the filesystem itself, not git, and the primitive is an OS-level
exclusive file create -- `os.open(path, O_CREAT | O_EXCL)`, which git's own `update-ref --stdin
create` (single_flight's "local fast leg") already stands on the same guarantee for.

THE MECHANISM -- two layers, because the marker's OWN name varies (it carries the session id) and
an exclusive create only refuses a SECOND create of the SAME name:

  1. `to-cc/.<name>.claim.lock` -- a per-NAME sentinel, session-id-free, taken with
     `O_CREAT|O_EXCL|O_WRONLY`. This is the actual mutex: two sessions claiming the SAME `<name>`
     always race on the SAME sentinel path, so exactly one `open()` call wins regardless of what
     session id either one carries. A loser retries with bounded backoff (mirrors
     `transport._DestinationLock`) rather than refusing on a one-shot check, so a few-millisecond
     overlap -- the realistic case, not a dead holder -- resolves itself instead of double-refusing.
  2. Under the sentinel: glob `to-cc/<name>.CLAIMED-*`. Non-empty (a hand-made marker, per
     `BATCH-DECISION-OWN-TOOLS-2026-09-26.CLAIMED-7552b559`'s shape, counts the same as one this
     module wrote) -> refuse, write nothing. Empty -> create `to-cc/<name>.CLAIMED-<session>`
     with `open(..., "x")` -- exclusive even though the sentinel already serializes this, because a
     silent overwrite is worse than a redundant refusal if the two ever disagree.

  The sentinel is held only across step 2 (microseconds on a local mount; the transport adds
  network latency but still no I/O beyond one glob and one create), then removed in every case --
  claimed, refused, or erroring -- so a live claim never leaves it standing for the next caller.

WHY THE MARKER KEEPS THE SESSION SUFFIX rather than becoming `to-cc/<name>.CLAIMED` outright: the
existing markers on the live transport (dispatcher, integrator and every lane, both hand-made and
this module's own) are named `<name>.CLAIMED-<session>`, and changing the shape would silently
stop `no_leftovers.py`'s new check (below) and every human `ls to-cc/*.CLAIMED-*` from recognising
this module's own output as the same kind of file.

STALE-LOCK RESIDUAL, stated not hidden (same posture as `single_flight.py`). A process killed
inside the sentinel's held window leaves `.{name}.claim.lock` on the transport forever -- the
filesystem has no lock TTL. `claim` retries for `_LOCK_TIMEOUT_S` and then refuses with the exact
command to remove it by hand; nothing here auto-expires a lock, because a guard that decides for
itself that a lock is "old enough to be dead" can be wrong in the one case that matters.

RELEASE REQUIRES THE SESSION THAT CLAIMED (Do-not: never remove or rewrite another session's
marker, hand-made or not). `release <name> --session <s>` removes only the exact file
`to-cc/<name>.CLAIMED-<s>`; a marker present under a DIFFERENT session is left standing and
reported `NOT_OURS`. Releasing an already-absent marker is an idempotent success, matching
`single_flight.release`'s own re-runnability contract.

EXIT CODES: `claim`: **0** claimed | **3** already in flight (a marker exists, or the sentinel is
held past its retry window) | **2** internal error (transport unreadable, bad name/session).
`release`: **0** free (removed, or already absent) | **4** held by a different session, left
standing | **2** internal error. `inspect` answers 0/2 only -- it does not contend.

FAIL CLOSED, same posture as `single_flight.py` and `block_ff_push`: an unreadable transport is an
internal error (exit 2), never a silent "nothing was claimed, so proceed".

HONEST LIMITS:
  * This is an ADVISORY library + CLI. It refuses nothing by existing; a caller that never invokes
    it is not stopped.
  * The sentinel's atomicity is only as good as the mounted filesystem's own `O_CREAT|O_EXCL`
    guarantee. Verified here against a local directory (every test) and against the live
    `CLAUDE_PROMPTS_DIR` mount (this lane's own wire-before-build evidence, session file) -- not
    against every possible network-drive implementation.
  * Two DIFFERENT `<name>`s never contend -- one sentinel per name is the intended grain, same as
    `single_flight`'s one ref per contract id.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import transport_report as _tr  # noqa: E402 -- reused only for windows_user_env's registry read

CLAIMED = 0
INTERNAL_ERROR = 2
IN_FLIGHT = 3
#: `release` refusing because the marker belongs to a DIFFERENT session -- a policy refusal, not a
#: crash, distinct from 2 for the same reason `single_flight.NOT_OURS` is (this module's own
#: docstring on `single_flight`'s discrimination applies here unchanged).
NOT_OURS = 4

_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_SESSION_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
_TO_CC = "to-cc"
_MARKER_INFIX = ".CLAIMED-"
_LOCK_POLL_S = 0.05
_LOCK_TIMEOUT_S = 10.0


class ClaimError(RuntimeError):
    """Internal failure. Raised, never swallowed -- `main` turns it into exit 2."""


def _validate(value: str, pattern: re.Pattern[str], label: str) -> str:
    if not value or not pattern.fullmatch(value):
        raise ClaimError(f"refusing {label} {value!r}: expected a non-empty identifier matching "
                         f"{pattern.pattern}")
    return value


def _default_session() -> str:
    """The first 8 characters of `$CLAUDE_CODE_SESSION_ID` -- the convention every hand-made
    marker on the live transport already carries. An EXPLICIT `--session` is used verbatim
    instead (never sliced), because the dispatcher composes longer suffixes itself
    (`<id>-codespace`, `-resume-<n>`) that an 8-char slice would truncate wrongly."""
    raw = os.environ.get("CLAUDE_CODE_SESSION_ID", "").strip()
    if not raw:
        raise ClaimError("no --session given and $CLAUDE_CODE_SESSION_ID is not set")
    return raw[:8]


def _to_cc_root(explicit: Optional[str] = None) -> Path:
    """The transport's `to-cc/` folder. UNSET OR UNMOUNTED IS A REFUSAL -- never a fallback
    folder, and a missing `to-cc/` is never created to make a claim succeed (same posture as
    `transport_report.resolve_transport`, which this mirrors for the agent-bound folder instead
    of the browser-bound one)."""
    raw = (explicit or "").strip() or (_tr.windows_user_env("CLAUDE_PROMPTS_DIR") or "").strip() \
        or os.environ.get("CLAUDE_PROMPTS_DIR", "").strip()
    if not raw:
        raise ClaimError("CLAUDE_PROMPTS_DIR is not set; no transport to claim on")
    base = Path(raw)
    if not base.is_dir():
        raise ClaimError(f"transport root {base} is not mounted or does not exist")
    dest = base / _TO_CC
    if not dest.is_dir():
        raise ClaimError(f"{dest} does not exist; refusing to create it")
    return dest


def _lock_path(to_cc: Path, name: str) -> Path:
    return to_cc / f".{name}.claim.lock"


def _marker_glob(name: str) -> str:
    return f"{name}{_MARKER_INFIX}*"


def _marker_path(to_cc: Path, name: str, session: str) -> Path:
    return to_cc / f"{name}{_MARKER_INFIX}{session}"


class _Sentinel:
    """The per-`name` mutex: `O_CREAT|O_EXCL` on a session-id-free path, bounded retry on
    contention (mirrors `transport._DestinationLock`), released in `finally` on every exit.

    A loser here has NOT been told the contract is claimed -- only that another claimant (or a
    dead one) currently holds the sentinel. `claim()` retries rather than refusing on the first
    miss, because the sentinel is held for microseconds in the honest case; only a hold that
    outlives `_LOCK_TIMEOUT_S` is reported to the caller, and it is reported as contention with
    the exact command to clear it, never silently retried forever.
    """

    def __init__(self, path: Path, timeout_s: float = _LOCK_TIMEOUT_S):
        self._path = path
        self._timeout_s = timeout_s
        self._fd: Optional[int] = None

    def __enter__(self) -> "_Sentinel":
        deadline = time.monotonic() + self._timeout_s
        while True:
            try:
                self._fd = os.open(str(self._path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(_LOCK_POLL_S)

    def __exit__(self, *exc_info: object) -> None:
        if self._fd is not None:
            os.close(self._fd)
        try:
            self._path.unlink()
        except OSError as exc:
            # Codex terra HIGH, this lane's own review: a swallowed cleanup failure left the
            # sentinel behind while the caller still saw a successful claim -- the NEXT claim of
            # this name then blocks for the full retry window and refuses, with nothing in ITS
            # own output pointing at the real cause. Surfaced here, at the one place that still
            # knows which sentinel failed to clear, rather than left for a stranger to diagnose.
            print(f"claim: WARNING -- could not clear the sentinel {self._path}: {exc} (the next "
                  f"claim of this name will wait out the retry window and then report it; clear "
                  f"it by hand: del {self._path})", file=sys.stderr)


def _refusal(name: str, holder: str) -> None:
    print(f"CLAIM REFUSAL: {name} is already claimed by {holder!r} -- this contract is already in "
          f"flight.\n"
          f"  A resume or repair session claims a DIFFERENT name instead (`<name>-resume-<n>` / "
          f"`<name>-repair-<n>`), not this one.", file=sys.stderr)


def claim(name: str, session: Optional[str] = None, root: Optional[str] = None) -> tuple[int, Optional[Path]]:
    """Claim `name`, returning `(exit_code, marker_path)`. `marker_path` is set only when WON."""
    name = _validate(name, _NAME_RE, "name")
    session = _validate(session, _SESSION_RE, "session") if session else _default_session()
    to_cc = _to_cc_root(root)
    lock = _lock_path(to_cc, name)
    try:
        with _Sentinel(lock, timeout_s=_LOCK_TIMEOUT_S):
            existing = sorted(to_cc.glob(_marker_glob(name)))
            if existing:
                _refusal(name, existing[0].name)
                return IN_FLIGHT, None
            marker = _marker_path(to_cc, name, session)
            stamp = datetime.now().astimezone().isoformat()
            job = os.environ.get("CLAUDE_JOB_DIR", "-")
            body = f"claimed-by: CC session {session} (job {job}), {stamp}\n"
            try:
                with open(marker, "x", encoding="utf-8", newline="\n") as fh:
                    fh.write(body)
            except FileExistsError:
                # Defense in depth: the sentinel already made this unreachable in the honest case.
                _refusal(name, marker.name)
                return IN_FLIGHT, None
            print(f"claim: claimed {marker}")
            return CLAIMED, marker
    except FileExistsError:
        print(f"CLAIM REFUSAL: {lock} is held past {_LOCK_TIMEOUT_S}s -- either a concurrent claim "
              f"of {name} is genuinely still in flight, or a prior session died mid-claim and left "
              f"the sentinel standing (the filesystem has no lock TTL).\n"
              f"  inspect: dir {lock}\n"
              f"  clear (only once you have established the holder is dead): del {lock}",
              file=sys.stderr)
        return IN_FLIGHT, None


def release(name: str, session: Optional[str] = None, root: Optional[str] = None) -> int:
    """Release the marker THIS session claimed. 0 = free (removed or already absent) | 4 = a
    marker exists under a different session, left standing | raises on internal error."""
    name = _validate(name, _NAME_RE, "name")
    session = _validate(session, _SESSION_RE, "session") if session else _default_session()
    to_cc = _to_cc_root(root)
    marker = _marker_path(to_cc, name, session)
    if not marker.exists():
        others = sorted(p for p in to_cc.glob(_marker_glob(name)) if p != marker)
        if others:
            print(f"CLAIM REFUSAL: not releasing {name} -- no marker under session {session!r}, "
                  f"but {others[0].name!r} exists under a different session; left standing "
                  f"(Do-not: never remove another session's marker).", file=sys.stderr)
            return NOT_OURS
        print(f"claim: {name} is already free (no marker under session {session!r})")
        return CLAIMED
    try:
        marker.unlink()
    except FileNotFoundError:
        # Codex terra HIGH, this lane's own review: the `marker.exists()` check above and this
        # unlink are two separate syscalls, so a concurrent release of the SAME session's marker
        # (a repair session re-running teardown after a timeout, say) can see it vanish in
        # between. The goal state -- no marker -- is reached either way, so this is the same
        # idempotent success as the already-absent case above, not an internal error.
        print(f"claim: {name} is already free (marker under session {session!r} was removed "
              f"concurrently)")
        return CLAIMED
    except OSError as exc:
        raise ClaimError(f"could not remove {marker}: {exc}") from exc
    print(f"claim: released {marker}")
    return CLAIMED


def inspect(name: str, root: Optional[str] = None) -> int:
    """Report holders without contending for the sentinel. Always exits 0 (or 2 on an unreadable
    transport) -- the answer is the printed line, not the code."""
    name = _validate(name, _NAME_RE, "name")
    to_cc = _to_cc_root(root)
    holders = sorted(p.name for p in to_cc.glob(_marker_glob(name)))
    if not holders:
        print(f"claim: {name} is FREE")
    else:
        print(f"claim: {name} is HELD by: {', '.join(holders)}")
    return CLAIMED


_VERBS = {"claim": claim, "release": release, "inspect": inspect}


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="claim.py",
        description="the claim marker as code -- claim/release/inspect to-cc/<name>.CLAIMED-<session>.")
    parser.add_argument("verb", choices=sorted(_VERBS))
    parser.add_argument("name", help="the order or contract file name, without .md")
    parser.add_argument("--session", default=None,
                        help="the claimant's identity (default: the first 8 chars of "
                             "$CLAUDE_CODE_SESSION_ID). Used verbatim when given explicitly -- "
                             "a resume/repair/codespace suffix is the caller's to compose.")
    parser.add_argument("--transport-root", default=None,
                        help="the transport root (default: $CLAUDE_PROMPTS_DIR)")
    args = parser.parse_args(argv)
    try:
        if args.verb == "claim":
            return claim(args.name, session=args.session, root=args.transport_root)[0]
        if args.verb == "release":
            return release(args.name, session=args.session, root=args.transport_root)
        return inspect(args.name, root=args.transport_root)
    except ClaimError as exc:
        print(f"claim: internal error -- {exc}", file=sys.stderr)
        return INTERNAL_ERROR
    except OSError as exc:
        print(f"claim: internal error -- {exc}", file=sys.stderr)
        return INTERNAL_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
