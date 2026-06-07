#!/usr/bin/env python
"""session_end_backpressure.py — #8 Stop-hook session-end backpressure.

A SEPARATE hub-local Stop hook (wired in `.claude/settings.json`, NOT the
fleet-distributed `tier1-lifecycle` plugin). Hub hygiene concepts (JOURNAL,
canonical-freshness cadence) don't belong in the child-repo plugin until the
ADR-78 floor verdict defines child-visible hygiene — Q2 ruling 2026-06-07. It runs
alongside the plugin's Stop->propose_closures hook (both fire; results merge).

At each turn Stop it runs DETERMINISTIC session-end hygiene checks (NO LLM
judgment — ADR-74) and, if any trips, emits `hookSpecificOutput.additionalContext`
so the turn CONTINUES and the agent can repair before truly stopping. Line format
is the backpressure shape: `what failed -> expected -> directive`.

Stop-hook contract (verified at CC 2.1.168): `additionalContext` reaches the model
ONLY via VALID JSON on stdout — plain stdout from a Stop hook goes to the debug log
only (Stop is not among the plain-stdout-as-context events). So this prints JSON
and nothing else. Fail-soft: ANY error -> emit nothing, exit 0 (never wedge a stop).

Checks (all deterministic, all this-session-repairable):
  1. dirty tree         — uncommitted changes at a stop (git-discipline).
  2. journal-for-shipped — commits landed beyond base with no JOURNAL entry.
  3. canonical cadence   — a canonical living doc edited in the arc without a
                           last_reviewed re-stamp (the freshness cadence).
Deliberately OUT of scope: cross-repo fleet health — it is surfaced at SessionStart
by fleet_health.py and is largely not this-session-repairable, so per-turn nagging
on it would be noise, contrary to the backpressure principle (flag only what should
be repaired now).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_JOURNAL = "JOURNAL.md"
_CANON = ("VISION.md", "ARCHITECTURE.md", "CLAUDE.md", "CONTRIBUTING.md")


def _git(*args):
    return subprocess.run(
        ["git", "-C", str(_REPO_ROOT), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
    )


def _is_clean() -> bool:
    r = _git("status", "--porcelain")
    return r.returncode == 0 and not r.stdout.strip()


def _base_ref() -> str:
    r = _git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip()
    return "main"


def check_dirty_tree():
    r = _git("status", "--porcelain")
    if r.returncode != 0:
        return None
    changes = [ln for ln in r.stdout.splitlines() if ln.strip()]
    if not changes:
        return None
    sample = ", ".join(ln[3:].strip() for ln in changes[:3])
    more = f" +{len(changes) - 3} more" if len(changes) > 3 else ""
    return (f"dirty tree: {len(changes)} uncommitted change(s) [{sample}{more}] "
            f"-> expected clean at wrap -> commit or stash (git-discipline).")


def check_journal_for_shipped_session():
    # only meaningful on a clean tree (a plausible wrap); skip while mid-work dirty
    if not _is_clean():
        return None
    base = _base_ref()
    log = _git("log", f"{base}..HEAD", "--name-only", "--format=")
    if log.returncode != 0:
        return None
    touched = {ln.strip() for ln in log.stdout.splitlines() if ln.strip()}
    if not touched:
        return None  # nothing shipped beyond base
    if _JOURNAL in touched:
        return None  # journal already updated in the shipped arc
    cnt = _git("rev-list", "--count", f"{base}..HEAD")
    n = cnt.stdout.strip() if cnt.returncode == 0 else "some"
    return (f"JOURNAL: {n} commit(s) ahead of {base} with no {_JOURNAL} update "
            f"-> expected a session entry -> prepend one (ESSENTIALS 'Ending a Session').")


def check_canonical_freshness():
    # a canonical living doc changed in the arc but its last_reviewed line did not
    if not _is_clean():
        return None
    base = _base_ref()
    stale = []
    for doc in _CANON:
        names = _git("log", f"{base}..HEAD", "--name-only", "--format=", "--", doc)
        if names.returncode != 0 or doc not in names.stdout:
            continue
        diff = _git("log", f"{base}..HEAD", "-p", "--format=", "--", doc)
        if diff.returncode != 0:
            continue
        bumped = any(
            ln[:1] in ("+", "-") and "last_reviewed" in ln
            for ln in diff.stdout.splitlines()
        )
        if not bumped:
            stale.append(doc)
    if not stale:
        return None
    return (f"cadence: {', '.join(stale)} edited in this arc with no last_reviewed bump "
            f"-> expected a freshness re-stamp -> re-read end-to-end + bump last_reviewed "
            f"(CLAUDE 'Freshness cadence').")


_CHECKS = (check_dirty_tree, check_journal_for_shipped_session, check_canonical_freshness)


def gather():
    lines = []
    for chk in _CHECKS:
        try:
            r = chk()
        except Exception:
            r = None
        if r:
            lines.append(r)
    return lines


def main() -> int:
    try:
        lines = gather()
        if not lines:
            return 0  # all clear -> silent (no JSON, nothing surfaced)
        ctx = ("Session-end hygiene (deterministic backpressure — repair before "
               "stopping):\n- " + "\n- ".join(lines))
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": ctx,
            }
        }))
        return 0
    except Exception:
        return 0  # fail-soft: never wedge a stop


if __name__ == "__main__":
    sys.exit(main())
