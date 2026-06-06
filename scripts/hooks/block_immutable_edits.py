#!/usr/bin/env python
"""block_immutable_edits.py — PreToolUse immutability guard (ADR-77).

Fail-closed PreToolUse hook that blocks in-place modification of EXISTING files
in the immutable zone. Follows the `block-onedrive.ps1` precedent exactly: reads
the hook payload as JSON on stdin, and to DENY prints `{"decision":"block",...}`
on stdout and exits 2; to ALLOW exits 0 silently.

v1 ZONE — transcripts ONLY (`docs/decisions/transcripts/**`). ADRs are
DELIBERATELY out of v1 scope: the repo has a sanctioned in-place ADR-amendment
convention (in-file "Amendment" markers; CLAUDE.md §5 "in-file marker"; ADR-68),
so a hard ADR guard would block a legitimate flow. Per the ADR-77 ruling the ADR
zone is queued behind a script-enforced amend path (Option A, BACKLOG #112);
transcripts have a clean immutability record (37/37 single-commit) so they are
the conflict-free v1 zone shipped now (Option C).

Semantics:
  - DENY  an in-place edit of an EXISTING file in the zone:
      * Edit / MultiEdit / NotebookEdit  -> always (they target existing files);
      * Write                            -> only when the target already exists.
  - ALLOW creation of a NEW file in the zone (new transcripts are the lifecycle).
  - ALLOW everything OUTSIDE the zone, and every non-mutating tool, untouched.

Fail behaviour (asymmetric, by design):
  - OUTSIDE the zone (or when the payload can't be parsed / has no path): a guard
    malfunction must NEVER block normal work -> ALLOW. False lockout of daily
    work is the worse error here.
  - INSIDE the zone, once a zone path is positively identified: any error fails
    CLOSED -> DENY. The whole point of the guard is that the zone is protected
    even when the guard is having a bad day.

Read-only / Layer-2: inspects the tool call and the filesystem (existence only);
mutates nothing. Wired via project `.claude/settings.json` PreToolUse. The pure
decision core (`decide`) is unit-tested directly; `main` is the stdin/stdout/exit
wire adapter.
"""

from __future__ import annotations

import json
import os
import sys

ADR_NN = "ADR-77"

# Mutating file tools. Enumerated explicitly (not a hardcoded "Edit|Write"): a
# guard that misses one mutating tool is decoration. Keep in sync with the
# PreToolUse matcher in .claude/settings.json.
MUTATING_TOOLS = frozenset({"Edit", "MultiEdit", "Write", "NotebookEdit"})

# Tools that may legitimately CREATE a new file — for these, only an edit of an
# ALREADY-EXISTING file is blocked. Edit/MultiEdit always target an existing file.
CREATE_CAPABLE = frozenset({"Write", "NotebookEdit"})

# The v1 immutable zone, as a path fragment matched case-insensitively against a
# forward-slashed path. Matches both `docs/decisions/transcripts/...` (relative)
# and any absolute path that contains the same segment (incl. the `archive/`
# subfolder). Deliberately NOT `docs/decisions/` — ADRs are out of v1 scope.
_ZONE_SEGMENT = "/docs/decisions/transcripts/"

DENY_MSG = (
    f"IMMUTABLE ({ADR_NN}): transcripts are superseded, never edited "
    "- create a new file."
)


def _path_in_zone(path: str) -> bool:
    """True if `path` points inside the transcripts zone (case-insensitive)."""
    norm = "/" + path.replace("\\", "/").lstrip("/")
    return _ZONE_SEGMENT in norm.lower()


def decide(payload: dict, exists=os.path.exists) -> tuple[str, str]:
    """Pure decision core. Returns ("allow"|"block", reason).

    `exists` is injectable so the existing-vs-new distinction is unit-testable
    without touching the filesystem. Never raises for a non-zone path; raises
    only would be caught by the caller and (for a confirmed zone path) failed
    closed.
    """
    tool = (payload.get("tool_name") or "").strip()
    if tool not in MUTATING_TOOLS:
        return "allow", "non-mutating tool"

    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not path:
        return "allow", "no path in tool_input"

    if not _path_in_zone(path):
        return "allow", "outside immutable zone"

    # --- Positively inside the zone from here: any failure fails CLOSED. ---
    if tool in CREATE_CAPABLE and not exists(path):
        return "allow", "new file in zone (creation allowed)"
    return "block", DENY_MSG


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            return 0  # unexpected shape, no identifiable zone path -> don't block
    except Exception:
        # Can't parse the payload -> can't identify a zone path -> never block
        # normal work on a guard malfunction.
        return 0

    # Determine zone membership defensively: an error BEFORE we confirm a zone
    # path allows (don't lock out non-zone work); an error AFTER blocks (the zone
    # stays protected even on guard malfunction).
    try:
        tool = (payload.get("tool_name") or "").strip()
        tool_input = payload.get("tool_input") or {}
        path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        in_zone = bool(path) and tool in MUTATING_TOOLS and _path_in_zone(path)
    except Exception:
        return 0  # cannot establish a zone path -> allow

    if not in_zone:
        return 0

    try:
        decision, reason = decide(payload)
    except Exception as exc:  # confirmed zone path -> fail closed
        decision, reason = "block", f"{DENY_MSG} (guard error, failing closed: {exc!r})"

    if decision == "block":
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
