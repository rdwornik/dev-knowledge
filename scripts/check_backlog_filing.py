#!/usr/bin/env python
"""commit-msg hook -- filing backpressure + #279 intake-id advisory (ADR-98 section 3).

Two diff-scoped rules on a commit that ADDS a new `- [#id]` task to BACKLOG.md. A pure
reword (the id appears on BOTH sides of the diff) triggers neither.

  Leg 1 (BLOCK): the commit message MUST carry a `kill-candidates:` line -- either
  naming >=1 existing `#id` proposed for removal, or `kill-candidates: none -- <reason>`.
  Filing backpressure: every new filing proposes a removal candidate. Proposals ONLY --
  this gate never removes or closes anything. PLAYBOOK section 10 doctrine; the add-side
  sibling of `backlog-id-on-close` (which gates the remove side).

  Leg 3 (WARN, #279): a NEW L-sized new-feature epic that lacks an intake-id citation
  (ADR-98 section 3) earns an advisory WARN -- it NEVER blocks. chore/fix residuals and
  bugfixes are EXEMPT (no intake doc by construction); an explicit `intake: n/a -- <reason>`
  also silences it.

Read-only: reads the staged diff + the message file; never writes.
Wired via `.pre-commit-config.yaml` `stages: [commit-msg]`; install with
`pre-commit install --hook-type commit-msg`.
"""

from __future__ import annotations

import re
import subprocess
import sys

# Added / removed task-id LINES in a `git diff -U0` (bullet `- [#id]` => `+- [#id]`).
# Group 1 = the full added bullet line (sans the `+`); group 2 = the id.
_ADDED_LINE_RE = re.compile(r"^\+(- \[#(\d+)\].*)$", re.M)
_REMOVED_ID_RE = re.compile(r"^-- \[#(\d+)\]", re.M)

# Leg 1 -- a `kill-candidates:` line naming >=1 `#id` OR the `none -- <reason>` form.
_KILL_RE = re.compile(r"^kill-candidates:\s*(none\b.*|.*#\d+.*)$", re.M | re.I)

# Leg 3 (#279) -- size-L band `[P{1-3}][L]` (witnessed BACKLOG format, e.g. `[P2][L]`).
# An `intake` mention satisfies the citation (also matches the `intake: n/a -- reason`
# escape); a residual/bugfix keyword exempts the filing entirely.
_LBAND_RE = re.compile(r"\[P[1-3]\]\[L\]")
_INTAKE_RE = re.compile(r"intake", re.I)
_EXEMPT_RE = re.compile(r"\b(bugfix|chore|residual|fix follow-up)\b", re.I)


def check(msg, diff):
    """Return (block_reasons, warnings) for a staged BACKLOG diff + commit message.

    block_reasons non-empty => the commit is rejected (exit 1). warnings are advisory
    (printed, never affect the exit code). A pure reword (id on both diff sides) is
    excluded from `new_ids`, so it triggers neither rule.
    """
    added = {tid: line for (line, tid) in _ADDED_LINE_RE.findall(diff)}
    removed = set(_REMOVED_ID_RE.findall(diff))
    new_ids = set(added) - removed

    block: list[str] = []
    warn: list[str] = []
    if not new_ids:
        return block, warn

    # Leg 1 -- filing backpressure (BLOCK).
    if not _KILL_RE.search(msg):
        ids = ", ".join("#" + i for i in sorted(new_ids, key=int))
        block.append(
            f"new task id(s) {ids} added but the commit message carries no "
            "'kill-candidates:' line (name >=1 existing #id, or 'none -- <reason>')."
        )

    # Leg 3 -- #279 intake-id advisory on new L-epics (WARN, never blocks).
    for tid in sorted(new_ids, key=int):
        line = added[tid]
        if not _LBAND_RE.search(line):
            continue  # not an L-epic -> out of scope
        if _EXEMPT_RE.search(line):
            continue  # chore/fix residual / bugfix -> exempt by construction
        if _INTAKE_RE.search(line):
            continue  # cites an intake-id (or carries the `intake: n/a` escape)
        warn.append(
            f"new L-epic #{tid} lacks an intake-id citation (ADR-98) -- advisory only "
            "(residual/bugfix filings are exempt; add an intake-id or 'intake: n/a -- <reason>')."
        )
    return block, warn


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
        # Fail OPEN but LOUD: a hygiene gate, not a safety control -- bricking every commit
        # on a near-impossible git failure is worse than skipping one filing check.
        print(f"commit-msg: WARNING -- could not read staged diff ({exc}); filing check skipped",
              file=sys.stderr)
        return 0
    block, warn = check(msg, diff or "")
    for w in warn:
        print(f"commit-msg: WARN -- {w}", file=sys.stderr)
    if block:
        for b in block:
            print(f"commit-msg: {b}", file=sys.stderr)
        print("  Filing backpressure (PLAYBOOK section 10): every new BACKLOG task id proposes "
              "a kill-candidate. Proposals only -- nothing is auto-removed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
