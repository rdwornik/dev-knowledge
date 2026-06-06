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
      * Edit / MultiEdit              -> always (they target existing files);
      * Write / NotebookEdit          -> only when the target already exists.
  - ALLOW creation of a NEW file in the zone (new transcripts are the lifecycle).
  - ALLOW everything OUTSIDE the zone, and every non-mutating tool, untouched.

Zone matching is on the CANONICALLY-RESOLVED path, not the raw string:
  - normpath collapses `..` so `transcripts/../ADR-77.md` (which resolves OUTSIDE
    the zone) is NOT falsely blocked;
  - realpath resolves symlinks/junctions so an out-of-zone alias pointing AT a
    transcript IS caught.
ALL recognized path fields (`file_path`, `notebook_path`) are evaluated — if ANY
resolves into the zone the call is in-zone, so a benign `file_path` cannot mask
an in-zone `notebook_path`.

Fail behaviour (asymmetric, by design):
  - OUTSIDE the zone (or when the payload can't be parsed / has no path): a guard
    malfunction must NEVER block normal work -> ALLOW. False lockout of daily
    work is the worse error here.
  - INSIDE the zone, once a zone path is positively identified: any error fails
    CLOSED -> DENY. The whole point of the guard is that the zone is protected
    even when the guard is having a bad day.

KNOWN RESIDUAL (honest enforcement limits): this guard matches the file-editing
TOOLS only (Edit/MultiEdit/Write/NotebookEdit). A shell command run via the
Bash/PowerShell tools (`Set-Content`, `>>`, `git checkout`, etc.) can still
mutate a transcript and is NOT caught here. A naive shell-substring guard was
deliberately NOT added: unlike the OneDrive P0 zone (where reads are forbidden
too, so block-onedrive can substring-match), transcripts are freely READABLE, so
blocking every shell command containing the zone path would over-block
legitimate `cat`/`grep`/`git` reads. A precise shell-write guard is future work
(tracked alongside the ADR-zone extension, BACKLOG #112). The primary vector — an
agent editing a record via the Edit/Write tools — is covered.

Read-only / Layer-2: inspects the tool call and the filesystem (existence +
canonical resolution only); mutates nothing. Wired via project
`.claude/settings.json` PreToolUse. The pure decision core (`decide`) is
unit-tested directly; `main` is the stdin/stdout/exit wire adapter.
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

# Path fields a mutating tool may carry, in no particular priority — ALL are
# evaluated so a benign field cannot mask an in-zone one.
PATH_FIELDS = ("file_path", "notebook_path")

# The v1 immutable zone, as a path fragment matched case-insensitively against a
# forward-slashed CANONICAL path. Matches both relative and absolute paths and
# the `archive/` subfolder. Deliberately NOT `docs/decisions/` — ADRs are out of
# v1 scope.
_ZONE_SEGMENT = "/docs/decisions/transcripts/"

DENY_MSG = (
    f"IMMUTABLE ({ADR_NN}): transcripts are superseded, never edited "
    "- create a new file."
)


def _canonical_forms(path: str) -> list[str]:
    """Best-effort canonical forms of `path` (normpath + realpath). Never raises.

    normpath collapses `..` lexically (no filesystem needed); realpath resolves
    symlinks/junctions. Both are checked so neither a `..` escape nor a symlink
    alias slips past the lexical substring test.
    """
    forms: list[str] = []
    for fn in (os.path.normpath, os.path.realpath):
        try:
            forms.append(fn(path))
        except Exception:
            continue
    return forms or [path]


def _path_in_zone(path: str) -> bool:
    """True if any canonical form of `path` resolves inside the transcripts zone."""
    if not path:
        return False
    for form in _canonical_forms(path):
        norm = "/" + form.replace("\\", "/").lstrip("/")
        if _ZONE_SEGMENT in norm.lower():
            return True
    return False


def _candidate_paths(tool_input: dict) -> list[str]:
    """Every non-empty recognized path value in the tool input."""
    out = []
    for field in PATH_FIELDS:
        val = tool_input.get(field)
        if val:
            out.append(val)
    return out


def _zone_paths(payload: dict) -> tuple[str, list[str]]:
    """Return (tool_name, in-zone candidate paths) for a mutating tool, else ("", [])."""
    tool = (payload.get("tool_name") or "").strip()
    if tool not in MUTATING_TOOLS:
        return "", []
    tool_input = payload.get("tool_input") or {}
    zone = [p for p in _candidate_paths(tool_input) if _path_in_zone(p)]
    return tool, zone


def decide(payload: dict, exists=os.path.exists) -> tuple[str, str]:
    """Pure decision core. Returns ("allow"|"block", reason).

    `exists` is injectable so the existing-vs-new distinction is unit-testable
    without touching the filesystem.
    """
    tool, zone = _zone_paths(payload)
    if not tool or not zone:
        return "allow", "outside immutable zone or non-mutating tool"

    # --- Positively inside the zone from here. ---
    if tool not in CREATE_CAPABLE:
        return "block", DENY_MSG  # Edit/MultiEdit are in-place by definition
    # Write/NotebookEdit: block if ANY in-zone target already exists (overwrite);
    # allow only when every in-zone target is a brand-new file (the lifecycle).
    if any(exists(p) for p in zone):
        return "block", DENY_MSG
    return "allow", "new file(s) in zone (creation allowed)"


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
        _tool, zone = _zone_paths(payload)
    except Exception:
        return 0  # cannot establish a zone path -> allow

    if not zone:
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
