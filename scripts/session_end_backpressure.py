#!/usr/bin/env python
"""session_end_backpressure.py — #8 Stop-hook session-end backpressure + ADR-85 gate.

A SEPARATE hub-local Stop hook (wired in `.claude/settings.json`, NOT the
fleet-distributed `tier1-lifecycle` plugin). Hub hygiene concepts (JOURNAL,
canonical-freshness cadence) don't belong in the child-repo plugin until the
ADR-78 floor verdict defines child-visible hygiene — Q2 ruling 2026-06-07. It runs
alongside the plugin's Stop->propose_closures hook (both fire; results merge).

At each turn Stop it runs DETERMINISTIC session-end hygiene checks (NO LLM judgment —
ADR-74, ADR-85). Two output modes:

  * HARD GATE (ADR-85) — the JOURNAL commit-SHA anchor. When it trips, the hook emits
    `{"decision": "block", "reason": ...}` so the turn is BLOCKED and cannot stop. It
    blocks-until-compliant (the agent satisfies it by naming a session SHA in JOURNAL.md);
    the only manual exit is `/override [reason]` (logged, HEAD-bound — see `_override_active`).
  * ADVISORY backpressure — BACKLOG marker (interim, ADR-85 R1), dirty tree, canonical
    cadence. Surfaced via `hookSpecificOutput.additionalContext`. Line format:
    `what failed -> expected -> directive`.

Stop-hook contract — CORRECTED (CC 2.1.178; code.claude.com/docs/en/hooks):
  - `{"decision":"block","reason":...}` blocks the stop (counts toward CC's block-cap, which
    force-ends the turn after N consecutive blocks — v2.1.143).
  - `hookSpecificOutput.additionalContext` is NOT a clean allow: per v2.1.163 it "continues
    the conversation so Claude can act on the feedback" — i.e. it KEEPS THE TURN GOING. So an
    "advisory" that re-emits additionalContext on a condition that PERSISTS across stop
    attempts keeps the turn going every retry -> N consecutive keep-goings -> the block-cap
    auto-overrides. That auto-override is the "persistence beats policy" bypass ADR-85
    forbids. (This corrects the original "advisory = exit-0, non-blocking" premise, which was
    wrong: there is no Stop-hook output that surfaces a nudge AND cleanly allows the stop.)
  - `stop_hook_active` is NOT in the CC-2.1.178 Stop-hook stdin schema (verified against the
    docs). So a fire-once-on-retry scheme cannot be the load-bearing guarantee here.

Therefore advisory legs CANNOT loop:
  - STRUCTURAL FLOOR (the active guarantee): advisory-only output never keeps the turn going.
    When no hard leg has tripped, advisory findings are NOT surfaced standalone (the hook
    stays silent and the turn ends); they ride along only when folded into a hard block
    (where the turn is already kept going by the JOURNAL teeth). No standalone keep-going =>
    no advisory loop, with zero dependency on `stop_hook_active`.
  - FIRE-ONCE (defense-in-depth, dormant in CC 2.1.178): IF a runtime ever supplies
    `stop_hook_active`, surface the advisory once on the first attempt (field present+False)
    and suppress on the retry (field True). Currently the field is absent, so this never
    fires and the floor is what runs.
The HARD leg deliberately ignores `stop_hook_active` — honoring it would make the gate
fire-once = the very antipattern ADR-85 forbids. It relies on COMPLIANCE, not the cap.

Both decision-paths reach the model ONLY via VALID JSON on stdout — plain stdout from a Stop
hook goes to the debug log only. So this prints JSON and nothing else.

Fail-soft is preserved as the deadlock-guard: every check is wrapped so ANY error yields
no finding, and the hard block fires ONLY on a positive detection (never on an exception).
So a bug can never wedge a stop un-overridably — the gate is fail-closed on real
non-compliance, fail-open on its own errors.

Checks (all deterministic, all this-session-repairable, all gated to a clean tree = a
plausible wrap, so mid-work turns are not nagged):
  HARD:
    1. journal SHA anchor  — commits landed beyond base but no session commit-SHA appears
                             in the JOURNAL.md entry for the arc (supersedes the older
                             advisory journal-PRESENCE check, which the SHA anchor subsumes).
  ADVISORY:
    2. backlog marker      — commits landed beyond base with no structural-marker change in
                             BACKLOG.md (ADR-85 R1: advisory in v1; promoted to a hard block
                             when the traceability-spine gives it an airtight anchor).
    3. dirty tree          — uncommitted changes at a stop (git-discipline).
    4. canonical cadence   — a canonical living doc edited in the arc without a
                             last_reviewed re-stamp (the freshness cadence).
Deliberately OUT of scope: cross-repo fleet health — surfaced at SessionStart by
fleet_health.py and largely not this-session-repairable, so per-turn nagging on it would be
noise, contrary to the backpressure principle (flag only what should be repaired now).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_JOURNAL = "JOURNAL.md"
_BACKLOG = "BACKLOG.md"
_CANON = ("VISION.md", "ARCHITECTURE.md", "CLAUDE.md", "CONTRIBUTING.md")
# Gitignored, HEAD-bound override signal written by `/override` (ADR-85 §4). The hook only
# READS it (stays a read-only validator per the scripts-are-read-only invariant).
_TOKEN_PATH = _REPO_ROOT / "logs" / ".session-override-token"
# Structural-marker delta the BACKLOG advisory looks for: an issue-id, a status keyword, or
# a checkbox. Matched against ADDED diff lines only.
_BACKLOG_MARKER_RE = re.compile(r"\[#\d+\]|status:|\[[ xX]\]")


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


def _head_sha() -> str | None:
    r = _git("rev-parse", "HEAD")
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def _session_shas() -> list[str]:
    """Full SHAs of the commits this session shipped beyond base (base..HEAD)."""
    base = _base_ref()
    r = _git("rev-list", f"{base}..HEAD")
    if r.returncode != 0:
        return []
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def _added_lines(path: str) -> str:
    """ADDED ('+', not '+++') diff lines for `path` across the arc base..HEAD, joined."""
    base = _base_ref()
    diff = _git("log", f"{base}..HEAD", "-p", "--format=", "--", path)
    if diff.returncode != 0:
        return ""
    return "\n".join(
        ln for ln in diff.stdout.splitlines()
        if ln.startswith("+") and not ln.startswith("+++")
    )


def _override_active() -> bool:
    """True iff a valid `/override` token records the CURRENT HEAD (ADR-85 §4).

    Pure read — never writes or deletes (keeps the hook a read-only validator). The token
    is HEAD-bound: it allows the gate while HEAD is unchanged and re-arms automatically the
    moment a new commit lands (a fresh commit moves HEAD, invalidating the token). Fail-soft:
    a missing/garbled token -> not active.
    """
    try:
        if not _TOKEN_PATH.exists():
            return False
        tok = json.loads(_TOKEN_PATH.read_text(encoding="utf-8"))
        head = _head_sha()
        return bool(head) and tok.get("head") == head
    except Exception:
        return False


def _read_hook_input() -> dict:
    """Parse the Stop-hook JSON payload from stdin; fail-soft to {} (field-absent -> floor).

    CC 2.1.178 does NOT send `stop_hook_active`, so this is normally `{}` or a dict without
    that key — which drives the structural floor. A runtime that DOES send it enables the
    dormant fire-once path. Never raises (no stdin / non-JSON -> {}).
    """
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}
    if not raw or not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _today() -> date:
    """Today's local date — seam for tests (the same-day freshness exemption pivots on it)."""
    return date.today()


_FM_LAST_REVIEWED_RE = re.compile(r"^last_reviewed:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def _current_last_reviewed(doc: str) -> date | None:
    """The `last_reviewed` ISO date from `doc`'s YAML frontmatter, or None. Pure read, fail-soft.

    Bounds the search to the frontmatter block (the leading `---`…`---`) so a `last_reviewed`
    mention in body prose can't match. Returns None on missing file / no frontmatter / no key
    / unparseable date.
    """
    try:
        text = (_REPO_ROOT / doc).read_text(encoding="utf-8")
    except Exception:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    front = text[:end] if end != -1 else text
    m = _FM_LAST_REVIEWED_RE.search(front)
    if not m:
        return None
    try:
        return date.fromisoformat(m.group(1))
    except ValueError:
        return None


# --- HARD leg (ADR-85) ------------------------------------------------------

def check_journal_sha_anchor():
    """HARD: commits shipped beyond base but no session commit-SHA in the JOURNAL.md arc.

    The SHA anchor is what makes this un-gameable — a generic "did work" line does not pass;
    the entry must name a real commit from this arc. Supersedes the older advisory
    journal-PRESENCE check (presence without a SHA no longer passes). Matches on the 7-char
    short prefix so any-length reference in the journal (7..40 chars) is caught.
    """
    if not _is_clean():  # only at a plausible wrap; skip mid-work
        return None
    shas = _session_shas()
    if not shas:  # nothing shipped beyond base -> nothing to anchor
        return None
    added = _added_lines(_JOURNAL)
    if any(sha[:7] in added for sha in shas):
        return None
    shorts = ", ".join(sha[:7] for sha in shas[:3])
    more = f" +{len(shas) - 3} more" if len(shas) > 3 else ""
    base = _base_ref()
    return (f"JOURNAL (hard): {len(shas)} commit(s) ahead of {base} but no session "
            f"commit-SHA in the {_JOURNAL} entry -> add/extend a JOURNAL entry naming >=1 "
            f"SHA from this arc [{shorts}{more}] (DEFINITION_OF_DONE 'JOURNAL').")


# --- ADVISORY legs ----------------------------------------------------------

def check_backlog_marker():
    """ADVISORY (ADR-85 R1): commits shipped but no structural-marker change in BACKLOG.md.

    A nudge, not a block, in v1: the marker check is gameable and not always-warranted (per
    'done tasks leave the file', a session that advances but finishes no task warrants no
    backlog edit), so hard-gating it would manufacture false-positives. Promoted to a hard
    block when the traceability-spine ADR gives it an airtight issue-id<->commit anchor.
    """
    if not _is_clean():
        return None
    shas = _session_shas()
    if not shas:
        return None
    if _BACKLOG_MARKER_RE.search(_added_lines(_BACKLOG)):
        return None
    return (f"BACKLOG (advisory): {len(shas)} commit(s) ahead of {_base_ref()} with no "
            f"structural-marker change in {_BACKLOG} -> if this session advanced or closed a "
            f"tracked task, reflect it ([#id]/status/checkbox); a pure advance that finishes "
            f"nothing needs none (DEFINITION_OF_DONE 'BACKLOG').")


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


def check_canonical_freshness():
    # a canonical living doc changed in the arc but its last_reviewed line did not
    if not _is_clean():
        return None
    base = _base_ref()
    today = _today()
    stale = []
    for doc in _CANON:
        names = _git("log", f"{base}..HEAD", "--name-only", "--format=", "--", doc)
        if names.returncode != 0 or doc not in names.stdout:
            continue
        # Same-day exemption (#142): if last_reviewed already == today, the doc is fresh by
        # definition today and re-stamping is a no-op diff — so this leg could NEVER be
        # cleared. Firing here is a false-positive that the agent can't repair; with
        # additionalContext keeping the turn going, it would loop. Skip it.
        if _current_last_reviewed(doc) == today:
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


_HARD_CHECKS = (check_journal_sha_anchor,)
_ADVISORY_CHECKS = (check_backlog_marker, check_dirty_tree, check_canonical_freshness)


def gather(checks):
    lines = []
    for chk in checks:
        try:
            r = chk()
        except Exception:
            r = None
        if r:
            lines.append(r)
    return lines


def main() -> int:
    try:
        if _override_active():
            return 0  # explicit, logged, HEAD-bound override -> allow (ADR-85 §4)
        data = _read_hook_input()
        hard = gather(_HARD_CHECKS)
        if hard:  # HARD GATE — block the stop; fold advisory in so nothing is lost.
            # The hard leg IGNORES stop_hook_active (teeth): it blocks until the JOURNAL names
            # a session SHA. Advisory findings ride inside the block reason — the turn is
            # already kept going by the block, so surfacing them here adds no loop.
            advisory = gather(_ADVISORY_CHECKS)
            reason = (
                "Session-end gate BLOCKED (deterministic; ADR-85) — repair before stopping:"
                "\n- " + "\n- ".join(hard + advisory)
                + "\nIf this block is wrong, exit via `/override [reason]` (logged)."
            )
            print(json.dumps({"decision": "block", "reason": reason}))
            return 0
        # No hard block. additionalContext "continues the conversation" (CC v2.1.163), so a
        # standalone advisory on a PERSISTENT condition would keep the turn going every retry
        # -> the block-cap auto-overrides (the bypass ADR-85 forbids). Surface advisory
        # standalone ONLY on a first-attempt signal we can fire-once on (stop_hook_active
        # present AND False). Absent that signal — the CC-2.1.178 reality, where the field is
        # not sent — the STRUCTURAL FLOOR applies: stay silent, let the turn end. No standalone
        # keep-going => advisory can never loop, with zero dependency on stop_hook_active.
        if data.get("stop_hook_active") is False:  # dormant in CC 2.1.178 (field absent)
            advisory = gather(_ADVISORY_CHECKS)
            if advisory:
                ctx = ("Session-end hygiene (deterministic backpressure — repair before "
                       "stopping):\n- " + "\n- ".join(advisory))
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "Stop",
                        "additionalContext": ctx,
                    }
                }))
                return 0
        return 0  # floor / all-clear / retry -> silent, turn ends
    except Exception:
        return 0  # fail-soft: never wedge a stop on the hook's own error


if __name__ == "__main__":
    sys.exit(main())
