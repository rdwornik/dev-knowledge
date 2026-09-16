#!/usr/bin/env python
"""id_allocator.py -- `[#804]` / `[#788]`: an id is RESERVED by a PUSH before a lane writes it.

THE DEFECT. Every lane allocated `max(local ids) + 1`. From a worktree, that maximum cannot
see a sibling branch that has not pushed. So every id surface in the tree agreed on an answer
that was wrong: the local row files, the generated manifest and the backlog view. Measured on
2026-09-15: lane aa-4's unpushed branch held 786 while every in-tree surface called 786 free.
It then happened four more times across batch AA (`279caaff`), and a third renumber came on
2026-09-16 (`e17c6200`). Re-checking does not help. The held id cannot be observed from the tree
at any moment, so a re-check only returns the same wrong answer.

THE MECHANISM -- a ref pushed create-only to the shared remote:

    reserve   git push --porcelain --force-with-lease=<ref>: <remote> <obj>:<ref>
    holder    git ls-remote <remote> <ref>  (+ a fetch of that one object to read its holder)

    <ref> = refs/reservations/<kind>/<value>, e.g. refs/reservations/task-id/815

The remote is the one substrate that two worktrees, two clones or two machines all share. It
decides the create atomically. `--force-with-lease=<ref>:` with an EMPTY expectation means
"this ref must not exist", and the RECEIVING side evaluates it, so a racer that has never
fetched is still refused. When two creates arrive TOGETHER, both pass the lease, and the
server's ref transaction refuses the second (measured; see `_CONTENTION_MARKERS`). This is
`single_flight`'s compare-and-swap. Its transport (`_git`, `_push_status`) and its contention
markers are imported from there, not copied: library-first inside the repo.

WHY THE VERDICT IS THE PORCELAIN FLAG AND NOT THE EXIT CODE. `single_flight` measured this
(git 2.55): a push of a value the remote ALREADY holds prints `= [up to date]` and exits 0 before
the lease decides anything. A reservation is WON only on `*` (new reference). The object pushed
here is also a PARENTLESS commit whose message carries the holder and a fresh nonce. Two holders
therefore never push the same value, and the `=` case cannot turn into a false win even in
principle.

THE LOCAL MAXIMUM IS NEVER CONSULTED, on any path. Candidates come ONLY from the block the
caller is granted (`--block 815-818`, the batch manifest's per-lane grant). Whether a candidate is
free is asked ONLY of the remote. This module reads no local id surface at all. That is not a
style choice: it is the whole fix. A lane whose tree carries rows far above the block gets the
same answer as a lane whose tree carries none.

EXIT CODES: 0 reserved / allocated / answered, 3 refused (held, or the block is exhausted),
2 internal error. FAIL CLOSED: an internal error is never read as "free". Only a rejection git
itself attributes to the lease counts as contention; every other failure exits 2.

HONEST LIMITS
  * NETWORK IS REQUIRED. There is no local-only mode, deliberately. A same-clone reservation is
    the visibility defect this module exists to end, so offering one would rebuild it behind a
    flag.
  * A reservation is permanent. An id is allocated once (ADR-107 6.3), so no release verb exists.
    A reservation for a row that is never filed is a gap in the numbering, not a collision.
    Gaps are cheap; collisions cost renumbers.
  * It guards what callers route through it. Nothing refuses a seat that writes a row file by
    hand without reserving. The duplicate-id refusal in the task-tree generator still fires at
    integration for that case, which is late, but it is no worse than before.
  * The block itself comes from the caller. Reading a manifest's per-lane block by machine is
    `[#804]` Done-when (2)'s remaining half. The batch AB manifest states its blocks in a prose
    table that no parser reads yet.
"""
from __future__ import annotations

import logging
import re
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path

import click

try:
    from scripts import single_flight as _sf  # type: ignore  # noqa: PLC0415
    from scripts.validate_branch_naming import BATCH_TOKEN  # type: ignore  # noqa: PLC0415
except ImportError:
    _SCRIPTS_DIR = str(Path(__file__).resolve().parent)
    if _SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, _SCRIPTS_DIR)
    import single_flight as _sf  # noqa: E402
    from validate_branch_naming import BATCH_TOKEN  # noqa: E402

logger = logging.getLogger("id-allocator")

RESERVED = 0
INTERNAL_ERROR = 2
REFUSED = 3

RESERVATION_NAMESPACE = "refs/reservations/"

#: The identifier spaces this allocator reserves in, and the shape a value must have in each.
KIND_TASK_ID = "task-id"
#: `[#809]` Done-when (4): a batch token is allocated by the SAME mechanism as a task id, never
#: chosen by a seat. The shape is the enum's own token, imported rather than restated.
KIND_BATCH_TOKEN = "batch-token"
KINDS: dict[str, re.Pattern[str]] = {
    KIND_TASK_ID: re.compile(r"[1-9][0-9]{0,6}"),
    KIND_BATCH_TOKEN: re.compile(BATCH_TOKEN),
}

_HOLDER_FIELD = "holder: "
_NONCE_FIELD = "nonce: "

#: A fixed identity for the reservation object, on `single_flight`'s precedent: the object is a
#: machine artifact, and `commit-tree` must not fail on a checkout that has no `user.email`.
_IDENTITY = ("-c", "user.name=id-allocator", "-c", "user.email=id-allocator@localhost")

_BLOCK_RE = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")

#: `single_flight`'s contention markers PLUS the one a TRULY SIMULTANEOUS create produces.
#: MEASURED HERE, 2026-09-16, git 2.55.0.windows.3, six rounds of two threads racing one ref
#: through a local bare remote: the lease check passes for BOTH pushers, because both saw the
#: ref absent. The server's ref transaction then decides, and the loser gets
#: `! ... [remote rejected] (reference already exists)`. That is not one of `single_flight`'s
#: three markers, so a real race read through them alone exits 2 (fail closed, not a false win).
#: Recorded as a finding against `single_flight` in this lane's audit, and not edited there.
_CONTENTION_MARKERS = (*_sf._CONTENTION_MARKERS, "reference already exists")


class AllocatorError(RuntimeError):
    """Internal failure. Raised, never swallowed: the CLI turns it into exit 2."""


@dataclass(frozen=True)
class Reservation:
    """The outcome of one reservation attempt. `won` is False when someone else holds it."""
    kind: str
    value: int | str
    won: bool
    holder: str | None
    ref: str


def reservation_ref(kind: str, value: int | str) -> str:
    """`refs/reservations/<kind>/<value>`, after checking the value against its kind's shape."""
    pattern = KINDS.get(kind)
    if pattern is None:
        raise AllocatorError(f"unknown kind {kind!r}; expected one of {sorted(KINDS)}")
    text = str(value)
    if not pattern.fullmatch(text):
        raise AllocatorError(f"{kind} value {text!r} does not match {pattern.pattern}")
    return f"{RESERVATION_NAMESPACE}{kind}/{text}"


def _check_holder(holder: str) -> str:
    """The holder is written as one line of the object. `single_flight._SAFE_FIELD` refuses a
    value that could forge a second field."""
    if not holder or not _sf._SAFE_FIELD.fullmatch(holder):
        raise AllocatorError(f"unsafe holder {holder!r}: expected {_sf._SAFE_FIELD.pattern}")
    return holder


#: `single_flight`'s transport: bytes on the wire (no CRLF rewrite of stdin on Windows), git's
#: repo-local env vars scrubbed, `LC_ALL=C` so the contention markers match, no credential prompt.
_run = _sf._git


def reservation_object(repo: Path, kind: str, value: int | str, holder: str) -> str:
    """A PARENTLESS commit on the empty tree. Its message names the holder and a fresh nonce.

    Parentless, so a plain push of it can never fast-forward onto a sibling's reservation.
    Nonce-bearing, so two attempts never produce the same sha. The `= [up to date]` false win
    therefore has no input that could produce it.
    """
    tree = _run(repo, "mktree", stdin="")
    if tree.returncode != 0 or not tree.stdout.strip():
        raise AllocatorError(f"cannot build the empty tree: {tree.stderr.strip()}")
    message = (f"id reservation: {kind} {value}\n\n"
               f"{_HOLDER_FIELD}{_check_holder(holder)}\n{_NONCE_FIELD}{uuid.uuid4().hex}\n")
    obj = _run(repo, *_IDENTITY, "commit-tree", tree.stdout.strip(), "-m", message)
    sha = obj.stdout.strip()
    if obj.returncode != 0 or not sha:
        raise AllocatorError(f"cannot build the reservation object: {obj.stderr.strip()}")
    return sha


def _holder_of(repo: Path, sha: str) -> str | None:
    r = _run(repo, "cat-file", "commit", sha)
    if r.returncode != 0:
        return None
    for line in r.stdout.splitlines():
        if line.startswith(_HOLDER_FIELD):
            return line[len(_HOLDER_FIELD):].strip() or None
    return None


def remote_holder(repo: Path | str, kind: str, value: int | str,
                  remote: str = "origin") -> str | None:
    """Who holds `<kind>/<value>` on the remote: the holder's name, or None when it is free.

    A ref that exists but whose object cannot be read or names no holder raises, and is never
    reported as free. "Held by someone unreadable" is still held.
    """
    repo = Path(repo)
    ref = reservation_ref(kind, value)
    listed = _run(repo, "ls-remote", remote, ref)
    if listed.returncode != 0:
        raise AllocatorError(f"cannot read {remote} {ref}: {listed.stderr.strip()}")
    fields = listed.stdout.split()
    if not fields:
        return None
    sha = fields[0]
    holder = _holder_of(repo, sha)
    if holder is None:
        fetched = _run(repo, "fetch", "--quiet", "--no-write-fetch-head", remote, ref)
        if fetched.returncode != 0:
            raise AllocatorError(f"{ref} is held on {remote} at {sha[:8]}, and its object "
                                 f"could not be fetched: {fetched.stderr.strip()}")
        holder = _holder_of(repo, sha)
    if holder is None:
        raise AllocatorError(f"{ref} is held on {remote} at {sha[:8]} by an object that names "
                             f"no holder -- held, but not by this allocator's shape")
    return holder


def reserve(repo: Path | str, kind: str, value: int | str, holder: str,
            remote: str = "origin") -> Reservation:
    """Reserve one value by a create-only push. `won=False` names whoever already holds it."""
    repo = Path(repo)
    ref = reservation_ref(kind, value)
    sha = reservation_object(repo, kind, value, holder)
    push = _run(repo, "push", "--porcelain", f"--force-with-lease={ref}:", remote, f"{sha}:{ref}")
    flag, summary = _sf._push_status(push.stdout, ref)
    if push.returncode == 0 and flag == _sf._PUSH_NEW:
        logger.info("reserved %s for %s on %s", ref, holder, remote)
        return Reservation(kind, value, True, holder, ref)
    contended = flag == _sf._PUSH_UP_TO_DATE or (
        flag == _sf._PUSH_REJECTED
        and any(m in summary.lower() for m in _CONTENTION_MARKERS))
    if contended:
        return Reservation(kind, value, False, remote_holder(repo, kind, value, remote), ref)
    raise AllocatorError(f"push of {ref} to {remote} failed: "
                         f"{push.stderr.strip() or push.stdout.strip() or 'no output'}")


def parse_block(text: str) -> range:
    """`"815-818"` -> `range(815, 819)`. Inclusive at both ends, as the manifest writes it."""
    m = _BLOCK_RE.match(text or "")
    if not m or int(m.group(1)) < 1 or int(m.group(1)) > int(m.group(2)):
        raise AllocatorError(f"block {text!r} is not LO-HI with 1 <= LO <= HI")
    return range(int(m.group(1)), int(m.group(2)) + 1)


def allocate(repo: Path | str, block: range, holder: str, kind: str = KIND_TASK_ID,
             remote: str = "origin") -> Reservation:
    """The lowest value in `block` whose reservation this call WINS.

    It tries each candidate in order, and contention simply moves it to the next one. So two
    concurrent callers on one block get distinct values, and a value a sibling pushed earlier is
    skipped. When the whole block is held, the result is `won=False` with `value` set to the
    block's last value. The block is the caller's grant, and nothing past it is tried.
    """
    last: Reservation | None = None
    for value in block:
        last = reserve(repo, kind, value, holder, remote)
        if last.won:
            return last
        logger.info("%s %s is held by %s; trying the next id in the block",
                    kind, value, last.holder)
    if last is None:
        raise AllocatorError("empty block")
    return last


# --- CLI ------------------------------------------------------------------------------------

def _fail(exc: Exception) -> None:
    logger.error("internal error -- %s. Refusing to report a reservation state that was never "
                 "established.", exc)
    sys.exit(INTERNAL_ERROR)


@click.group(help="Reserve ids by a create-only push to the shared remote ([#804]/[#788]). "
                  "Exit 0 ok, 3 refused, 2 internal error.")
def cli() -> None:
    logging.basicConfig(format="id_allocator: %(message)s", level=logging.INFO, stream=sys.stderr)


@cli.command("reserve")
@click.argument("kind", type=click.Choice(sorted(KINDS)))
@click.argument("value")
@click.option("--holder", required=True, help="the lane that will use the id, e.g. its slug")
@click.option("--repo", default=".", type=click.Path(file_okay=False), show_default=True)
@click.option("--remote", default="origin", show_default=True)
def cmd_reserve(kind: str, value: str, holder: str, repo: str, remote: str) -> None:
    """Reserve exactly VALUE, or be refused with the name of whoever holds it."""
    try:
        got = reserve(Path(repo), kind, value, holder, remote)
    except (AllocatorError, _sf.SingleFlightError, OSError) as exc:
        _fail(exc)
    if not got.won:
        logger.error("REFUSED: %s is already held by %s on %s. Take another id from your block.",
                     got.ref, got.holder, remote)
        sys.exit(REFUSED)
    click.echo(str(got.value))


@cli.command("allocate")
@click.option("--block", "block_text", required=True, help="the granted block, LO-HI (inclusive)")
@click.option("--holder", required=True, help="the lane that will use the id, e.g. its slug")
@click.option("--kind", default=KIND_TASK_ID, type=click.Choice(sorted(KINDS)), show_default=True)
@click.option("--repo", default=".", type=click.Path(file_okay=False), show_default=True)
@click.option("--remote", default="origin", show_default=True)
def cmd_allocate(block_text: str, holder: str, kind: str, repo: str, remote: str) -> None:
    """Reserve the lowest free id in the block, and print it."""
    try:
        got = allocate(Path(repo), parse_block(block_text), holder, kind, remote)
    except (AllocatorError, _sf.SingleFlightError, OSError) as exc:
        _fail(exc)
    if not got.won:
        logger.error("REFUSED: every id in block %s is held (the last, %s, by %s). A block is a "
                     "grant; ask for a new one rather than reaching past it.",
                     block_text, got.value, got.holder)
        sys.exit(REFUSED)
    click.echo(str(got.value))


@cli.command("holder")
@click.argument("kind", type=click.Choice(sorted(KINDS)))
@click.argument("value")
@click.option("--repo", default=".", type=click.Path(file_okay=False), show_default=True)
@click.option("--remote", default="origin", show_default=True)
def cmd_holder(kind: str, value: str, repo: str, remote: str) -> None:
    """Print who holds VALUE on the remote, or FREE. Does not contend."""
    try:
        who = remote_holder(Path(repo), kind, value, remote)
    except (AllocatorError, _sf.SingleFlightError, OSError) as exc:
        _fail(exc)
    click.echo(f"{reservation_ref(kind, value)} {'FREE' if who is None else f'HELD by {who}'}")


if __name__ == "__main__":
    cli()
