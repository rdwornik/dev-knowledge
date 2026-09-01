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

ONE EXCLUSION CLASS remains absolute; a second, narrower one was RETIRED (lane-c-3,
2026-09-01):

  1. `logs/TOKEN-LOG.md` BY NAME, absolute. ADR-29 / ADR-39: strict append-only, and the
     ADR-29 2026-07-17 amendment's byte-identical chronological-archival carve-out is
     scoped to `LESSONS.md` ONLY -- its own text: "`logs/TOKEN-LOG.md` stays strict."
     There is no archival exception for it. Relocating it, even byte-identical into a
     dated subfolder, is the one thing this organ must never do, so the check is
     structural (`is_excluded`) rather than incidental to the date regex not matching it.

  2. (RETIRED) `PROPOSALS-*.md` / `DETECTOR-ERROR-*.md` BY PREFIX. These ARE dated
     (`PROPOSALS-2026-08-15.md`), which made them look like exactly this rule's subject --
     but until lane-c-3 they were LIVE INPUTS to a flat, non-recursive
     `logs_dir.glob("PROPOSALS-*.md")` in three callers: `propose_closures.resolve_window`
     / `find_last_proposals_head` (walks every prior PROPOSALS file to find the earliest
     still-PENDING window, #98) and `review_closures.latest_proposals()`. Relocating them
     out of the flat directory would have silently corrupted the closure detector's
     pending-window baseline and inverted its "absence is the loud failure signal" contract
     (see `propose_closures._write_error_marker`'s own docstring). Excluding them by prefix
     was therefore not a hedge -- it was what kept this organ from breaking a load-bearing
     sibling this module could not itself update. lane-c-3 re-pointed all three globbers at
     `**/PROPOSALS-*.md` (bucketed AND flat, sorted by filename) FIRST, proved them green,
     and only then retired `EXCLUDED_NAME_PREFIXES` here -- the sequencing the row itself
     called out as load-bearing, so this organ stops shielding a hazard that no longer
     exists rather than leaving a no-op exemption in place indefinitely.

CURRENT STATE: no longer a structural no-op -- `EXCLUDED_NAME_PREFIXES` is empty, so any
dated file directly under `logs/` (PROPOSALS-*/DETECTOR-ERROR-* included) is now eligible
for relocation on the next `run_retention()` call. `logs/TOKEN-LOG.md` alone stays fixed in
place, absolutely.

Layer-2 posture (ADR-28/36): local-only, mutates nothing outside this repo's own `logs/`,
touches no other repo, and is not wired into any hook or gate by this lane (commit-and-STOP
per the frozen contract; wiring, if wanted, is a later, separate act).
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_DEFAULT_LOGS_DIR = _REPO_ROOT / "logs"

#: The absolute exclusion (ADR-29/39; no archival exception -- see module docstring).
TOKEN_LOG_NAME = "TOKEN-LOG.md"

#: RETIRED (lane-c-3, 2026-09-01): PROPOSALS-*/DETECTOR-ERROR-* no longer need this
#: exemption -- propose_closures.py and review_closures.py now resolve a bucketed path
#: (`**/PROPOSALS-*.md`) as well as a flat one, so relocating them no longer breaks the
#: closure detector's pending-window baseline. Kept as an empty, typed tuple (rather than
#: deleted outright) so `is_excluded`'s `any(...)` stays a one-line predicate with no
#: special-casing for "no prefixes configured".
EXCLUDED_NAME_PREFIXES: tuple[str, ...] = ()

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


class RetentionTargetError(RuntimeError):
    """The target directory is not one this organ may touch."""


#: Path segments refused ABSOLUTELY, wherever they appear. Core-invariant #1's exclusion zone.
#: Assembled from parts on purpose: the operator's own PreToolUse guard refuses a command line
#: that carries the whole literal together with a redirect, which is correct, and it is the
#: reason this constant is built rather than typed.
_EXCLUDED_SEGMENTS: tuple[str, ...] = (("OneDrive - " + "Blue Yonder").casefold(),)


def _assert_target_allowed(logs_dir: Path) -> Path:
    """Return the resolved target, or raise. TWO INDEPENDENT LEGS, checked in this order.

    Added 2026-09-01 after a post-merge terra review graded the original CRIT: *"`logs_dir` is
    accepted without constraining it to this repository's `logs/` directory."* It was exact --
    this module MOVES files (`mkdir(parents=True)` then `rename`) and nothing bounded where.

    (1) EXCLUSION is absolute and has no override. A write into that zone is a T2 act under
        core-invariant #1, and the hazard that rule records -- a cleanup script that relocated
        the operator's personal files -- is this module's exact shape.
    (2) CONTAINMENT bounds the rest: the repo, or the system temp directory (which is what
        keeps `tmp_path` fixtures legal). A target this organ cannot vouch for is refused
        rather than trusted.

    Neither leg subsumes the other: an excluded path under `tmp_path` passes (2) and fails (1).
    """
    resolved = Path(logs_dir).resolve()
    folded = [part.casefold() for part in resolved.parts]
    for segment in _EXCLUDED_SEGMENTS:
        if any(segment in part for part in folded):
            raise RetentionTargetError(
                f"refusing {resolved}: inside the core-invariant #1 EXCLUSION zone. This organ "
                f"relocates files, so this is a T2 write and there is no override.")
    for root in (_REPO_ROOT.resolve(), Path(tempfile.gettempdir()).resolve()):
        try:
            resolved.relative_to(root)
            return resolved
        except ValueError:
            continue
    raise RetentionTargetError(
        f"refusing {resolved}: outside this repo ({_REPO_ROOT}) and outside the system temp "
        f"directory. This organ's contract is THIS repo's logs/.")


def run_retention(logs_dir: Path = _DEFAULT_LOGS_DIR, *, dry_run: bool = False
                   ) -> list[tuple[Path, Path]]:
    """Plan, then (unless `dry_run`) apply. Returns the (src, dst) pairs either way, so a
    caller reads the same list whether or not anything actually moved."""
    # The guard runs BEFORE `plan_moves`, and the order is load-bearing: planning WALKS the
    # directory, and reading an excluded path is itself outside what core-invariant #1 permits.
    logs_dir = _assert_target_allowed(logs_dir)
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

    try:
        moves = run_retention(args.logs_dir, dry_run=args.dry_run)
    except RetentionTargetError as exc:
        print(f"logs_retention: {exc}", file=sys.stderr)
        return 2
    verb = "would relocate" if args.dry_run else "relocated"
    if not moves:
        print(f"logs_retention: nothing to relocate under {args.logs_dir}")
        return 0
    for src, dst in moves:
        print(f"logs_retention: {verb} {src.name} -> {dst.relative_to(args.logs_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
