#!/usr/bin/env python
"""failed_set.py — the base failed-set a lane's delta-A2 acceptance compares against.

WHY THIS EXISTS. Batch G's acceptance rule (delta A2) is *"do not make it worse"*: a lane's own
run may leave tests failing, provided the SET of failing nodeids stays a subset of the set that
was already failing before the batch began. That rule needs a base set, and the base set has to
be a COMMITTED artifact rather than a local file, because `.pytest_cache` is per-checkout and
per-substrate — a lane in a worktree, or in a container, has a different one or none at all.

STDLIB ONLY, DELIBERATELY. `pytest-json-report` would give a richer record and is a NEW
dependency; under ADR-106 the environment is declared by `pyproject.toml` + `uv.lock` and a bump
is its own gated change, which is not a cost this reader is worth. pytest already writes
`.pytest_cache/v/cache/lastfailed` as `{nodeid: true}`, so `json` reads it with no new seam.

SETS, NEVER COUNTS. Under `-n auto` the suite is sharded across workers, and the ORDER and the
COUNT of reported failures move between runs while the SET does not. A comparison on counts
reports drift that did not happen and hides drift that did, so every comparison here is on
nodeids.

ABSENCE IS A REPORTED GAP, NOT AN EMPTY SET (register ruling Z-G4). A missing cache file and a
fully green suite are indistinguishable by content — both read as zero failures — and they are
opposite facts. A missing cache therefore RAISES rather than emitting an empty base set that a
later lane would compare against and thereby "prove" it broke nothing.

HONEST LIMIT, because it bounds every verdict built on this file: `lastfailed` records the last
run in THAT checkout. It says nothing about tests that were never collected — a suite that died
during collection leaves a small, misleadingly clean set. The emitted artifact therefore records
the sha and substrate it was measured on, and a comparison across two of them is a comparison of
two measurements, not of one moving number.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "failed-set/1"
CACHE_RELPATH = Path(".pytest_cache") / "v" / "cache" / "lastfailed"


class FailedSetError(RuntimeError):
    """The cache could not be read. FAIL-LOUD: callers report it, they do not swallow it."""


def read_lastfailed(cache: Path) -> set[str]:
    """The set of nodeids pytest recorded as failing. Absence RAISES — see the module docstring."""
    if not cache.is_file():
        raise FailedSetError(
            f"{cache} is absent, so a failed-set could not be computed. An absent cache and a "
            f"green suite both look like zero failures and are opposite facts — run the suite "
            f"in this checkout first (Z-G4).")
    try:
        raw = json.loads(cache.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise FailedSetError(f"cannot read {cache}: {exc!r}") from exc
    if not isinstance(raw, dict):
        raise FailedSetError(f"{cache} is not the expected mapping of nodeid to true")
    return {str(k) for k in raw}


#: `FAILED tests/x.py::t - AssertionError` / `ERROR tests/x.py::t`, with any ANSI colouring.
_REPORT_RE = re.compile(r"^(?:FAILED|ERROR)\s+(\S+?)(?:\s+-\s.*)?$")
_ANSI_RE = re.compile(chr(27) + r"\[[0-9;]*m")


def read_report(path: Path) -> set[str]:
    """The failing nodeids a pytest RUN reported, read from its own captured output.

    WHY THIS SOURCE EXISTS AND IS THE DEFAULT FOR A FULL RUN. `lastfailed` is the obvious
    source and it is NOT reliable in this repo: `addopts = "-n auto"`, and a full suite run on
    2026-09-02 rewrote `.pytest_cache/v/cache/nodeids` (15:01) while leaving
    `.pytest_cache/v/cache/lastfailed` untouched from the PREVIOUS DAY (21:37). The stale file
    was a strict SUPERSET -- 45 nodeids against the 13 the run actually reported -- so reading it
    would have produced a base set that silently forgives 32 tests that now pass. That is exactly
    the false base this module exists to prevent, and it is worse than an absent one, because it
    looks like a measurement.

    The run's own report is therefore the authority: it is what the suite SAID, at a known sha,
    in one pass. Absence RAISES for the same reason `read_lastfailed` does.
    """
    if not Path(path).is_file():
        raise FailedSetError(f"{path} is absent, so no run report could be read (Z-G4)")
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise FailedSetError(f"cannot read {path}: {exc!r}") from exc

    found = set()
    for line in _ANSI_RE.sub("", text).splitlines():
        m = _REPORT_RE.match(line.strip())
        if m:
            found.add(m.group(1))
    if not found and "passed" not in text:
        raise FailedSetError(
            f"{path} carries neither a FAILED/ERROR line nor a pytest summary — it does not look "
            f"like a pytest run report, and guessing an empty set here would forgive everything")
    return found


def head_sha(repo: Path) -> str:
    """Short HEAD, or `unknown` — a missing sha degrades the record, it does not stop the emit."""
    out = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else "unknown"


def build_record(nodeids: set[str], sha: str, substrate: str) -> dict:
    """The committed artifact. `count` is informational; every comparison reads `nodeids`."""
    return {
        "schema": SCHEMA,
        "sha": sha,
        "substrate": substrate,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(nodeids),
        "nodeids": sorted(nodeids),
    }


def load_record(path: Path) -> set[str]:
    """The nodeid set out of a committed artifact, refusing a shape it does not understand."""
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise FailedSetError(f"cannot read the base set {path}: {exc!r}") from exc
    if not isinstance(raw, dict) or raw.get("schema") != SCHEMA:
        raise FailedSetError(f"{path} does not carry schema {SCHEMA!r}")
    return {str(n) for n in raw.get("nodeids", [])}


def compare(base: set[str], head: set[str]) -> tuple[set[str], set[str]]:
    """`(regressions, fixed)` — failures the base did not carry, and base failures now passing."""
    return (head - base, base - head)


def main(argv: list[str] | None = None) -> int:
    """`--emit` writes the base artifact; `--compare` verdicts a lane's run against one.

    `--compare` exits 1 on a REGRESSION only. A lane that fixed base failures without adding any
    is a pass: delta A2 is "do not make it worse", not "make it better".
    """
    parser = argparse.ArgumentParser(
        prog="failed_set",
        description="Emit or compare the pytest failed-set that delta-A2 acceptance reads.")
    parser.add_argument("--repo", default=".", help="repo root (default: the cwd)")
    parser.add_argument("--cache", default=None,
                        help=f"lastfailed path (default: <repo>/{CACHE_RELPATH.as_posix()})")
    parser.add_argument("--emit", metavar="OUT", help="write the failed-set artifact to OUT")
    parser.add_argument("--substrate", default="local",
                        help="where this was measured (local | codespace | cloud)")
    parser.add_argument("--compare", metavar="BASE",
                        help="verdict this checkout's failed-set against a committed BASE")
    parser.add_argument("--from-report", metavar="RUNLOG", default=None,
                        help="read the failing nodeids from a pytest run's captured output "
                             "instead of the cache (the reliable source under -n auto)")
    args = parser.parse_args(argv)

    repo = Path(args.repo)
    cache = Path(args.cache) if args.cache else repo / CACHE_RELPATH

    try:
        head = (read_report(Path(args.from_report)) if args.from_report
                else read_lastfailed(cache))
        if args.compare:
            regressions, fixed = compare(load_record(Path(args.compare)), head)
            for nodeid in sorted(fixed):
                print(f"fixed:      {nodeid}")
            for nodeid in sorted(regressions):
                print(f"REGRESSION: {nodeid}")
            print(f"{len(regressions)} regression(s), {len(fixed)} fixed, "
                  f"{len(head)} failing here")
            return 1 if regressions else 0

        record = build_record(head, head_sha(repo), args.substrate)
        record["source"] = "run-report" if args.from_report else "pytest-cache"
        if args.emit:
            out = Path(args.emit)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
            print(f"wrote {out} — {record['count']} nodeid(s) at {record['sha']} "
                  f"({record['substrate']})")
        else:
            json.dump(record, sys.stdout, indent=2)
            sys.stdout.write("\n")
        return 0
    except FailedSetError as exc:
        print(f"failed_set: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
