"""go_reader.py -- is there a GO for this batch? (R-W3-7, `moment:merge`).

ONE QUESTION, ONE ANSWER. The operator's GO is a file, `to-cc/GO-<batch>.md`, on the transport
drive. Nothing read it: a merge could proceed with no GO, or wait on one that was already given.
This organ reads that one path for one batch and answers PRESENT or ABSENT. ABSENT is a REFUSAL --
a receipt on stdout and a non-zero exit -- because a check that could not find its ground truth
must not read as a pass to anything shelling out to it (register ruling Z-G4).

IT READS; IT WRITES NOTHING. Not a GO, not a marker, not a cache: a reader that could create the
file it looks for would answer yes to its own question. One GO per batch (AH-B2), so presence is
the whole predicate -- what the file says is the operator's, and is not judged here.

WHERE `to-cc/` IS. The transport is a machine-level surface (`CLAUDE_PROMPTS_DIR`), not a tracked
tree, and two live values of it exist on the operator's machine (E-29): the User scope is the
Drive channel, a long-lived process may inherit `~/Downloads`. So the directory searched is
PRINTED in every receipt, and `--transport` overrides the resolution. An unresolvable transport
is a refusal, never a pass and never a silent fallback to the working directory.

THE BATCH IS A FILENAME. It is validated as one token -- no separator, no `..` -- before it is
joined to the inbox, so a batch name can only ever name a file inside `to-cc/`.

HONEST LIMIT: presence, not authority. A file named `GO-<batch>.md` that anyone dropped in the
inbox reads as a GO. The transport's write access is the control, not this reader.
"""
from __future__ import annotations

import json
import logging
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

logger = logging.getLogger("go-reader")

#: The inbox on the transport, and how one batch's GO is named inside it.
INBOX = "to-cc"
GO_NAME = "GO-{batch}.md"

VERDICT_GO = "GO"
VERDICT_REFUSED = "REFUSED"

#: One filename token. A leading dot or dash is refused too: `-x` reads as a flag downstream.
_BATCH_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]*")


@dataclass(frozen=True)
class GoReceipt:
    """What the reader found. Printed as one JSON line; the exit code follows `verdict`."""
    batch: str
    searched: str            # the exact path looked at ('' when it could not be formed)
    present: bool
    verdict: str             # GO | REFUSED
    reason: str

    @property
    def ok(self) -> bool:
        return self.verdict == VERDICT_GO


def resolve_transport(explicit: Optional[str]) -> Optional[Path]:
    """The transport directory, or None when it cannot be resolved.

    `--transport` wins. Otherwise the dispatcher's own precedence (User-scope value, then the
    process copy) so this organ and the launcher never look at two different drives.

    A REFUSAL FROM THE DISPATCHER STANDS. `prompts_dir` refuses when the authority drive is
    unmounted, and reading the process copy of the variable after that would hand back exactly the
    stale directory the refusal exists to prevent (E-29) -- a false GO from the wrong drive. The
    process copy is read only where the dispatcher cannot be imported at all.
    """
    if explicit:
        return Path(explicit)
    try:
        import dispatch as _dispatch                     # noqa: PLC0415
    except ImportError:
        try:
            from scripts import dispatch as _dispatch    # noqa: PLC0415  # pragma: no cover
        except ImportError:                              # pragma: no cover -- no dispatcher here
            raw = (os.environ.get("CLAUDE_PROMPTS_DIR") or "").strip()
            return Path(raw) if raw else None
    try:
        return _dispatch.prompts_dir()
    except Exception as exc:  # noqa: BLE001 -- an unmounted authority drive is a refusal
        logger.warning("transport not resolvable through dispatch.prompts_dir: %r", exc)
        return None


def read_go(batch: str, transport: Optional[Path]) -> GoReceipt:
    """Answer the one question. Never raises: every failure is a REFUSED receipt."""
    if not _BATCH_RE.fullmatch(batch or "") or ".." in batch:
        return GoReceipt(batch, "", False, VERDICT_REFUSED,
                         f"{batch!r} is not one filename token, so no GO path can be formed "
                         f"from it (no separators, no `..`, no leading dot or dash)")
    if transport is None:
        return GoReceipt(batch, "", False, VERDICT_REFUSED,
                         "the transport directory is unresolved -- pass --transport <dir> or set "
                         "CLAUDE_PROMPTS_DIR. Refused rather than guessed: two live values of it "
                         "exist on the operator's machine")
    path = Path(transport) / INBOX / GO_NAME.format(batch=batch)
    if path.is_file():
        return GoReceipt(batch, str(path), True, VERDICT_GO, f"found {path}")
    return GoReceipt(batch, str(path), False, VERDICT_REFUSED,
                     f"no GO for batch {batch!r}: {path} is absent. The operator writes it; "
                     f"this reader never does")


@click.command(help="Is there a `to-cc/GO-<batch>.md`? Exit 0 with a receipt when yes; "
                    "non-zero with a REFUSED receipt when not. Reads; writes no GO.")
@click.option("--batch", required=True, help="the batch whose GO is read")
@click.option("--transport", default=None, type=click.Path(file_okay=False),
              help="the transport directory holding to-cc/ [default: the dispatcher's "
                   "CLAUDE_PROMPTS_DIR resolution]")
def cli(batch: str, transport: Optional[str]) -> None:
    receipt = read_go(batch, resolve_transport(transport))
    click.echo(json.dumps(asdict(receipt), sort_keys=True))
    logger.info("go_reader batch=%s verdict=%s", batch, receipt.verdict)
    raise SystemExit(0 if receipt.ok else 1)


if __name__ == "__main__":
    cli()
