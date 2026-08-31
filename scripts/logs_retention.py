#!/usr/bin/env python
"""logs_retention.py -- HY-2 (batch-E) the `logs/` RETENTION RULE, as a MECHANISM.

WHAT THIS IS. `logs/` accumulates dated, per-run artifacts over time -- today the only
live producer of that shape is `scripts/propose_closures.py`'s `PROPOSALS-YYYY-MM-DD.md`
/ `DETECTOR-ERROR-YYYY-MM-DD.md` pair. Left flat, a directory like this grows one file per
event forever with no organ ever tidying it -- "a cleanup that leaves no rule behind will
be re-needed next month" (the frozen contract's own words). This module is that rule,
expressed as code that a caller runs (`main()` / `run_retention()`), not a one-time sweep:
a file named `<STEM>-YYYY-MM-DD.<ext>` sitting DIRECTLY under `logs/` is relocated,
byte-identical, into a `logs/YYYY-MM/` month subfolder keyed off its own date. No content
is ever read, rewritten or reformatted -- `apply_moves` is a bare `Path.rename`.

MONTH, NOT DAY. A per-day subfolder would start life holding exactly one file, which is
the shape `docs/audits/2026-08-31-census-single-file-folders.md` (Z-G5, "no single-file
folders, ever") measures and flags across this same tree. A per-month bucket instead
accumulates every dated file from that month, so it fills rather than sitting empty of
siblings by construction. This is a contract default, not a ruling -- recorded here so it
is not silently re-derived differently later.

TWO EXCLUSION CLASSES, and the rule NAMES both (the contract: "names what it EXCLUDES,
`logs/TOKEN-LOG.md` first among them"):

  1. `logs/TOKEN-LOG.md` BY NAME, absolute. ADR-29 / ADR-39: strict append-only, and the
     ADR-29 2026-07-17 amendment's byte-identical chronological-archival carve-out is
     scoped to `LESSONS.md` ONLY -- its own text: "`logs/TOKEN-LOG.md` stays strict."
     There is no archival exception for it. Relocating it, even byte-identical into a
     dated subfolder, is the one thing this organ must never do, so the check is
     structural (`is_excluded`) rather than incidental to the date regex not matching it.

  2. `PROPOSALS-*.md` / `DETECTOR-ERROR-*.md` BY PREFIX. These ARE dated (`PROPOSALS-
     2026-08-15.md`), which makes them look like exactly this rule's subject -- but they
     are LIVE INPUTS to a flat `logs_dir.glob("PROPOSALS-*.md")` two callers already run:
     `propose_closures.resolve_window` / `find_last_proposals_head` (walks every prior
     PROPOSALS file to find the earliest still-PENDING window, #98) and
     `review_closures.latest_proposals()` (`sorted(...)[-1]`). Relocating them out of the
     flat directory would silently corrupt the closure detector's pending-window baseline
     and invert its "absence is the loud failure signal" contract (see
     `propose_closures._write_error_marker`'s own docstring). Excluding them by prefix is
     therefore not a hedge, it is what keeps this organ from breaking a load-bearing
     sibling that this lane's write-scope (`logs/`, `scripts/`, `tests/`) does not include
     `scripts/propose_closures.py` / `scripts/review_closures.py` to also update.

CURRENT STATE: a no-op today. Nothing presently written into `logs/` is both dated AND
outside the two exclusions, so `run_retention()` plans zero moves against the live tree.
The mechanism exists for the NEXT dated producer, per the contract's own framing --
"re-needed next month" is exactly the failure this organ is written ahead of.

Layer-2 posture (ADR-28/36): local-only, mutates nothing outside this repo's own `logs/`,
touches no other repo, and is not wired into any hook or gate by this lane (commit-and-STOP
per the frozen contract; wiring, if wanted, is a later, separate act).
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_DEFAULT_LOGS_DIR = _REPO_ROOT / "logs"

#: The absolute exclusion (ADR-29/39; no archival exception -- see module docstring).
TOKEN_LOG_NAME = "TOKEN-LOG.md"

#: The live-flat-glob-consumer exclusions (propose_closures.py / review_closures.py).
EXCLUDED_NAME_PREFIXES: tuple[str, ...] = ("PROPOSALS-", "DETECTOR-ERROR-")

#: `<STEM>-YYYY-MM-DD.<ext>`, stem and extension both required and non-empty. Greedy
#: `.+` is safe here: the anchored `-\d{4}-\d{2}-\d{2}\.` suffix is what backtracking
#: settles on, so a stem that itself contains hyphens (`SOME-THING-2026-08-15.md`) still
#: resolves to date = the trailing one.
_DATED_RE = re.compile(r"^(?P<stem>.+)-(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})\.(?P<ext>[^./\\]+)$")


class RetentionError(Exception):
    """Raised by `apply_moves` instead of silently overwriting an existing archive
    file -- a destination collision means something is already at that path, and this
    organ never edits or deletes content (the frozen contract's done-contract item 4)."""


def is_excluded(name: str) -> bool:
    """True when `name` (a bare filename, not a path) must never be relocated.

    Absolute (`TOKEN_LOG_NAME`) or live-consumer prefix (`EXCLUDED_NAME_PREFIXES`) --
    see the module docstring for why each exists.
    """
    if name == TOKEN_LOG_NAME:
        return True
    return any(name.startswith(prefix) for prefix in EXCLUDED_NAME_PREFIXES)


def parse_dated_month(name: str) -> str | None:
    """`"YYYY-MM"` if `name` carries a trailing `-YYYY-MM-DD.<ext>`, else `None`.

    Validates the date is a REAL calendar date (`datetime.date` construction) so a
    filename that merely LOOKS dated (`WIDGET-2026-13-40.md`) is left alone rather than
    filed under a month that cannot exist.
    """
    m = _DATED_RE.match(name)
    if not m:
        return None
    y, mo, d = m.group("y"), m.group("m"), m.group("d")
    try:
        date(int(y), int(mo), int(d))
    except ValueError:
        return None
    return f"{y}-{mo}"


def plan_moves(logs_dir: Path) -> list[tuple[Path, Path]]:
    """(src, dst) pairs for every eligible file DIRECTLY under `logs_dir`.

    Pure planning -- no filesystem mutation. Skips: an absent `logs_dir` (empty plan,
    not an error -- a fresh checkout has nothing to archive), subdirectories (so a file
    already relocated into `logs/YYYY-MM/` on a prior run is never re-planned -- this is
    what makes `run_retention` idempotent without a separate marker), excluded names
    (`is_excluded`), and undated names (`parse_dated_month` returns `None`).
    """
    if not logs_dir.is_dir():
        return []
    moves: list[tuple[Path, Path]] = []
    for entry in sorted(logs_dir.iterdir()):
        if not entry.is_file():
            continue
        name = entry.name
        if is_excluded(name):
            continue
        month = parse_dated_month(name)
        if month is None:
            continue
        moves.append((entry, logs_dir / month / name))
    return moves


def apply_moves(moves: list[tuple[Path, Path]]) -> None:
    """Relocate each (src, dst) pair. Byte-identical (`Path.rename`; no read, no rewrite).

    Refuses (`RetentionError`) on a destination collision rather than overwriting --
    leaves both the source and the pre-existing destination untouched so nothing is lost.
    """
    for src, dst in moves:
        if dst.exists():
            raise RetentionError(
                f"refusing to overwrite an existing archived file: {dst} "
                f"(source left in place: {src})"
            )
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)


def run_retention(logs_dir: Path = _DEFAULT_LOGS_DIR, *, dry_run: bool = False
                   ) -> list[tuple[Path, Path]]:
    """Plan, then (unless `dry_run`) apply. Returns the (src, dst) pairs either way, so a
    caller reads the same list whether or not anything actually moved."""
    moves = plan_moves(logs_dir)
    if not dry_run:
        apply_moves(moves)
    return moves


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--logs-dir", type=Path, default=_DEFAULT_LOGS_DIR,
                         help="logs/ directory to operate on (default: this repo's logs/).")
    parser.add_argument("--dry-run", action="store_true",
                         help="Report what would move without moving it.")
    args = parser.parse_args(argv)

    moves = run_retention(args.logs_dir, dry_run=args.dry_run)
    verb = "would relocate" if args.dry_run else "relocated"
    if not moves:
        print(f"logs_retention: nothing to relocate under {args.logs_dir}")
        return 0
    for src, dst in moves:
        print(f"logs_retention: {verb} {src.name} -> {dst.relative_to(args.logs_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
