#!/usr/bin/env python
"""commit-msg hook (ADR-65/66 forward-only index).

A commit that **removes** a `- [#id]` task from `BACKLOG.md` (i.e. closes or relocates
it) must reference that id as `[#<id>]` or `closes [#<id>]` in the commit message —
so the implementing/closing commit is locatable by id later (`git log --grep 'closes \\[#'`).

A reworded task (its `[#id]` appears on both sides of the diff) does NOT trigger.
Read-only: reads the staged diff + the message file; never writes.

Wired via `.pre-commit-config.yaml` `stages: [commit-msg]`; install with
`pre-commit install --hook-type commit-msg`.
"""

from __future__ import annotations

import re
import subprocess
import sys

_REMOVED_RE = re.compile(r"^-- \[#(\d+)\]", re.M)
_ADDED_RE = re.compile(r"^\+- \[#(\d+)\]", re.M)
_REF_RE = re.compile(r"\[#(\d+)\]")


def check(msg, diff):
    """Return the list of removed task ids not referenced in the message (empty = OK)."""
    removed = set(_REMOVED_RE.findall(diff))
    added = set(_ADDED_RE.findall(diff))
    closed = sorted(removed - added, key=int)
    referenced = set(_REF_RE.findall(msg))
    return [i for i in closed if i not in referenced]


def main():
    if len(sys.argv) < 2:
        return 0
    try:
        msg = open(sys.argv[1], encoding="utf-8").read()
    except OSError:
        return 0
    try:
        diff = subprocess.run(
            ["git", "diff", "--cached", "-U0", "--", "BACKLOG.md"],
            capture_output=True, text=True, encoding="utf-8",
        ).stdout
    except OSError as exc:
        # Fail OPEN but LOUD: this is a hygiene gate, not a safety control — bricking every
        # commit on a near-impossible git failure is worse than skipping one id-check. The
        # warning ensures the skip is never silent. (git-missing => pre-commit wouldn't run anyway.)
        print(f"commit-msg: WARNING — could not read staged diff ({exc}); backlog-id check skipped",
              file=sys.stderr)
        return 0
    missing = check(msg, diff or "")
    if missing:
        ids = ", ".join(f"#{i}" for i in missing)
        print(f"commit-msg: BACKLOG task(s) {ids} removed but not referenced in the message.", file=sys.stderr)
        print("  Add [#<id>] or 'closes [#<id>]' for each (ADR-65/66 forward-only index).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
